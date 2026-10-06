#!/usr/bin/env python3
"""Validate the archive and an already-built Jekyll site (no network requests)."""
import argparse
import datetime as dt
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import subprocess
import sys
from urllib.parse import unquote, urljoin, urlsplit
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--site', type=Path, default=ROOT / '_site')
args = parser.parse_args()
site = args.site.resolve()
errors = []
checks = 0

def check(ok, message):
    global checks
    checks += 1
    if not ok:
        errors.append(message)


def date(value):
    return dt.date.fromisoformat(str(value)[:10])


def read_yaml(paths):
    # Ruby/Psych comes with the site's Ruby runtime; Python needs no YAML package.
    ruby = '''require 'yaml'; require 'json'; require 'date'; require 'time'
result = {}
ARGV.each do |path|
  text = File.read(path)
  text = text.split(/^---\\s*$\\n?/, 3)[1] if text.start_with?("---\\n")
  result[path] = YAML.safe_load(text, permitted_classes: [Date, Time], aliases: false)
end
puts JSON.generate(result)
'''
    result = subprocess.run(['ruby', '-e', ruby, *map(str, paths)], text=True, capture_output=True)
    if result.returncode:
        sys.exit('YAML parsing failed:\n' + result.stderr)
    return json.loads(result.stdout)


archive_paths = sorted((ROOT / 'topics').rglob('*.md'))
yaml_paths = archive_paths + list((ROOT / 'topics').glob('*/monitoring.yml'))
yaml_paths += [ROOT / '_config.yml', ROOT / 'web/_data/sources.yml']
metadata = read_yaml(yaml_paths)
archive = {p: metadata[str(p)] for p in archive_paths}
config = metadata[str(ROOT / '_config.yml')]
base = config.get('baseurl', '').rstrip('/')
sources = metadata[str(ROOT / 'web/_data/sources.yml')]['sources']
topics = {m['id'] for m in archive.values() if m['type'] == 'topic'}
source_ids = [s['id'] for s in sources]
for topic in topics:
    check((ROOT / 'topics' / topic / 'monitoring.yml').is_file(), f'{topic}: missing monitoring settings')
check(len(source_ids) == len(set(source_ids)), 'Duplicate source IDs')
for source in sources:
    for field in ['id', 'name', 'url', 'priority', 'type', 'canonical', 'useful_for', 'evidence_note', 'topics', 'notes']:
        check(field in source, f"Source {source.get('id')} lacks {field}")
    check(source['priority'] in ['primary', 'secondary', 'discovery'], f"Invalid priority: {source['id']}")
    check(set(source['topics']) <= topics, f"Unknown topic: {source['id']}")

fields = ['Authors', 'Publication/release date', 'Source / venue', 'Publication type', 'Canonical URL', 'Importance', 'Relevance', 'Evidential maturity', 'Contribution', 'Why it matters', 'Evidence and source quality', 'Major limitations', 'Code / project URL', 'Status / update']
findings = set()
known_finding_ids = {f['id'] for meta in archive.values() if meta['type'] == 'weekly' for f in meta.get('findings', [])}
for path, m in archive.items():
    label = str(path.relative_to(ROOT))
    body = path.read_text().split('---', 2)[2]
    try:
        check(m['schema_version'] == 1, f'{label}: schema version')
        check(m.get('topic', m.get('id')) in topics, f'{label}: unknown topic')
        if m['type'] == 'topic':
            check(m['permalink'] == f"/projects/{m['id']}/", f'{label}: topic permalink')
            continue
        if m['type'] == 'session':
            stamp = dt.datetime.fromisoformat(m['searched_at'].replace(' UTC', '+00:00').replace('Z', '+00:00'))
            check(stamp.utcoffset() == dt.timedelta(0), f'{label}: session timestamp must be UTC')
            check(path.stem == stamp.strftime('%Y-%m-%dT%H%M%SZ'), f'{label}: session filename')
            check(m['search_scope'] in ['full', 'targeted'], f'{label}: search scope')
            check(m['status'] in ['complete', 'partial'], f'{label}: session status')
            check(set(m['source_ids_checked']) <= set(source_ids), f'{label}: unknown checked source')
            candidates = body.split('## Candidates', 1)[1].split('\n## ', 1)[0]
            count = len(re.findall(r'\| (?:included|excluded|follow_up|candidate) \|', candidates))
            check(count == m['candidate_count'], f'{label}: candidate count')
            continue
        start, end = date(m['period_start']), date(m['period_end'])
        check(start < end, f'{label}: period bounds')
        cs, ce = date(m.get('coverage_start', m['period_start'])), date(m.get('coverage_end', m['period_end']))
        check(start <= cs < ce <= end, f'{label}: coverage bounds')
        check('session_files' in m, f'{label}: missing session_files')
        for session in m.get('session_files', []):
            target = (path.parent / session).resolve()
            check(target in archive and archive[target]['type'] == 'session' and archive[target]['topic'] == m['topic'], f'{label}: invalid session {session}')
        if not m.get('session_files'):
            check(bool(re.search(r'coverage (?:was |is )?absent|not searched|unsearched', body, re.I)), f'{label}: empty session list without coverage explanation')
        if m['type'] == 'weekly':
            check(start.weekday() == 0 and (end-start).days == 7, f'{label}: ISO week bounds')
            check(path.stem == start.strftime('%G-W%V'), f'{label}: ISO week filename')
            sunday = end - dt.timedelta(days=1)
            expected_title = f'Weekly Research Review — {start:%G-W%V} ({start:%b} {start.day} – {sunday:%b} {sunday.day})'
            check(m['title'] == expected_title and '# '+expected_title in body, f'{label}: weekly title needs Monday–Sunday date suffix')
            cards = m['findings']
            ids = [f['id'] for f in cards]
            findings.update(ids)
            anchors = re.findall(r'<span id="([^"]+)"></span>', body)
            check(len(ids) == m['findings_count'] and len(ids) == len(set(ids)), f'{label}: finding count/duplicate ID')
            check(sorted(ids) == sorted(anchors), f'{label}: finding anchors')
            for finding in cards:
                check(finding['id'].startswith(m['topic']+'-'), f'{label}: finding topic ID')
                canonical = finding.get('canonical_url', '')
                check(isinstance(canonical, str) and canonical.startswith('https://'), f'{label}: missing canonical URL')
                heading = re.search(r'(?m)^### .*<span id="'+re.escape(finding['id'])+r'"></span>([^\n]+)', body)
                check(bool(heading) and canonical in heading[1], f'{label}: heading should link to canonical URL')
                released = finding.get('released_on')
                check(released is not None or bool(finding.get('date_uncertainty')), f'{label}: unknown release date needs explanation')
                if released is not None:
                    date(released)
                    check(f'**Publication/release date:** {date(released).isoformat()}' in body, f'{label}: release date missing from card')
                else:
                    check('**Publication/release date:** Unknown' in body, f'{label}: unknown date missing from card')
                if m.get('retrospective'):
                    event = finding.get('event_on') or released
                    check(event is not None and cs <= date(event) < ce, f'{label}: undated/out-of-period retrospective finding')
            for level in ['high', 'medium', 'low']:
                n = len(re.findall(r'\*\*Relevance:\*\* '+level+r'\b', body))
                check(n == m[f'{level}_priority_count'], f'{label}: {level} count')
            for section in re.split(r'(?m)(?=^## )', body):
                heading = re.match(r'## (High|Medium|Low) Priority', section)
                if not heading:
                    continue
                sections = re.split(r'(?m)^### ', section)[1:]
                check(bool(sections), f'{label}: empty priority section')
                previous = 6
                for card in sections:
                    for field in fields:
                        check('**'+field+':**' in card, f'{label}: missing card field {field}')
                    score = re.search(r'\*\*Importance:\*\* (\d)/5', card)
                    maturity = re.search(r'\*\*Evidential maturity:\*\* (\d)/5', card)
                    check(bool(score) and 1 <= int(score[1]) <= previous, f'{label}: importance order/range')
                    if score:
                        previous = int(score[1])
                    check(bool(maturity) and 1 <= int(maturity[1]) <= 5, f'{label}: maturity range')
                    check('**Relevance:** '+heading[1].lower() in card, f'{label}: wrong relevance group')
        elif m['type'] == 'monthly':
            next_month = (start.replace(day=28) + dt.timedelta(days=4)).replace(day=1)
            check(start.day == 1 and end == next_month and path.stem == start.strftime('%Y-%m'), f'{label}: calendar month')
            index = body.split('## Full Included Findings', 1)[-1].split('\n## ', 1)[0]
            ids = set(re.findall(r'\[`([^`]+)`\]', index))
            check(len(ids) == m['findings_count'] and ids <= known_finding_ids, f'{label}: monthly count/reference')
        elif m['type'] == 'yearly':
            check(start == dt.date(start.year, 1, 1) and end == dt.date(start.year+1, 1, 1) and path.stem == str(start.year), f'{label}: calendar year')
            ids = set(re.findall(r'(?:#|`)([a-z0-9-]+-\d{4}-\d{2}-\d{2}-[a-z0-9-]+)', body))
            check(len(ids) == m['findings_count'] and ids <= known_finding_ids, f'{label}: yearly count/reference')
        else:
            check(False, f'{label}: unknown report type')
    except (KeyError, ValueError, TypeError, IndexError) as error:
        check(False, f'{label}: invalid metadata/content ({error})')

for path in (ROOT / 'topics').glob('*/monitoring.yml'):
    m = metadata[str(path)]
    try:
        check(m['schema_version'] == 1 and m['topic'] == path.parent.name, f'{path}: monitoring identity')
        check(m['status'] in ['needs_setup', 'active', 'manual', 'paused'], f'{path}: monitoring status')
        check(isinstance(m['overlap_days'], int) and m['overlap_days'] >= 0, f'{path}: overlap_days')
        if m['status'] in ['active', 'manual']:
            date(m['monitor_from'])
            check(m['persistence']['mode'] in ['local', 'commit', 'push', 'pull_request'], f'{path}: persistence mode')
        if m['status'] == 'active':
            ZoneInfo(m['timezone'])
            check(m['weekday'] in ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'], f'{path}: weekday')
            dt.time.fromisoformat(m['local_time'])
            check(bool(m['scheduler']['provider']) and bool(m['scheduler']['task_id']), f'{path}: scheduler not verified')
        if m.get('backfill_start') is not None or m.get('backfill_end') is not None:
            check(bool(m.get('backfill_start')) and bool(m.get('backfill_end')) and date(m['backfill_start']) < date(m['backfill_end']), f'{path}: invalid backfill interval')
        if m.get('last_completed_end') is not None:
            end = dt.datetime.fromisoformat(m['last_completed_end'].replace(' UTC', '+00:00').replace('Z', '+00:00'))
            check(end.utcoffset() == dt.timedelta(0) and date(m['monitor_from']) <= end.date(), f'{path}: invalid completed cutoff')
        if m.get('persistence', {}).get('mode') in ['push', 'pull_request']:
            check(bool(m['persistence'].get('remote')) and bool(m['persistence'].get('branch')), f'{path}: remote and branch are required')
        check(not (site / path.relative_to(ROOT)).exists(), f'{path}: operational settings leaked into website')
    except (KeyError, ValueError, TypeError) as error:
        check(False, f'{path}: invalid monitoring settings ({error})')

# Local Markdown references, including onboarding links and explicit finding anchors.
md_paths = archive_paths + list((ROOT / 'docs').glob('*.md')) + [ROOT/'README.md', ROOT/'AGENTS.md']
markdown_links = 0
for path in md_paths:
    for raw in re.findall(r'\]\(([^\s)]+)\)', path.read_text()):
        link = urlsplit(raw)
        if link.scheme or raw.startswith('#'):
            continue
        markdown_links += 1
        target = (path.parent / unquote(link.path)).resolve()
        check(target.is_file(), f'{path.name}: missing Markdown target {raw}')
        if link.fragment and target.is_file():
            check(f'id="{unquote(link.fragment)}"' in target.read_text(), f'{path.name}: missing explicit anchor {raw}')

class Page(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.ids, self.refs, self.tags = [], [], []
        self.feed(text)

    def handle_starttag(self, tag, attributes):
        self.tags.append(tag)
        attrs = dict(attributes)
        if 'id' in attrs:
            self.ids.append(attrs['id'])
        for attr in ['src', 'href', 'data-report-url']:
            if attrs.get(attr):
                self.refs.append(attrs[attr])

pages = {p: Page(p.read_text()) for p in site.rglob('*.html')}
check(bool(pages), 'No built HTML found; run Jekyll first')
html_refs = 0
for path, page in pages.items():
    check('html' in page.tags and 'body' in page.tags, f'{path.relative_to(site)}: missing document layout')
    check(len(page.ids) == len(set(page.ids)), f'{path.relative_to(site)}: duplicate HTML IDs')
    page_url = 'http://archive.test' + base + '/' + str(path.relative_to(site)).removesuffix('index.html')
    for raw in page.refs:
        parsed = urlsplit(urljoin(page_url, raw))
        if parsed.scheme not in ['http', 'https'] or parsed.netloc != 'archive.test':
            continue
        html_refs += 1
        urlpath = unquote(parsed.path)
        check(not base or urlpath.startswith(base+'/'), f'{path.name}: link escapes baseurl: {raw}')
        relative = urlpath[len(base):].lstrip('/') if base else urlpath.lstrip('/')
        target = (site / relative).resolve()
        if target.is_dir():
            target /= 'index.html'
        check(target.is_file() and site in target.parents, f'{path.relative_to(site)}: missing local target {raw}')
        if parsed.fragment and target in pages:
            check(unquote(parsed.fragment) in pages[target].ids, f'{path.relative_to(site)}: missing anchor {raw}')

# README prose must render one sentence per line; preserve decimals such as CC BY 4.0.
for number, line in enumerate((ROOT/'README.md').read_text().splitlines(), 1):
    if not line.strip() or line.startswith(('#', '<img', '[Website')):
        continue
    check(line.rstrip().endswith('<br>'), f'README:{number}: missing rendered line break')
    prose = re.sub(r'\[([^]]+)\]\([^)]+\)', r'\1', line)
    prose = re.sub(r'`[^`]*`', '', prose)
    prose = re.sub(r'^\s*\d+\. ', '', prose)
    check(not re.search(r'[.!?] +[A-Z]', prose), f'README:{number}: multiple sentences on one line')

print(json.dumps({'checks': checks, 'topics': len(topics), 'archive_documents': len(archive), 'findings': len(findings), 'sources': len(sources), 'markdown_links': markdown_links, 'html_references': html_refs, 'errors': errors}, indent=2))
sys.exit(bool(errors))
