# Writing and data guide

This guide defines the archive contract. Keep prose readable, metadata small, and factual claims linked to original material. Do not invent findings to fill a report. Agents should also read the short `AGENTS.md` workflow before starting.

For onboarding, scheduler setup, and recurring execution, follow [the agent workflow](agent-workflow.md).

## Research workflow

The registry is a **minimum coverage checklist, not an exhaustive source list or search boundary**. A full scan checks each applicable primary source, uses secondary sources when relevant, and deliberately searches outside the registry. Search broader scholarly and general web indexes; follow citations, new terms, lab and institutional pages, project sites, and official code releases. Apply the topic's inclusion rules regardless of where an item was found. Follow discovery hits to original material before assessing a claim.

A targeted follow-up can inspect a smaller set of sources; state its exact question and scope. In either kind of session, record every checked source, including unregistered URLs. A newly discovered source can remain in the session record; add it to `web/_data/sources.yml` only when recurring monitoring would add value. The registry should remain useful without pretending to enumerate the whole research landscape.

### Inclusion threshold and empty periods

Include an item as a finding only when original evidence shows a meaningful connection to the topic and the item could change understanding, a method choice, an evaluation plan, or a research decision. A paper matching a search term is only a candidate. Exclude weakly related, redundant, unsupported, or routine items; record the decision and reason in the search session when the item was screened. Do not lower the threshold to populate a quiet period or manufacture a trend from sparse evidence.

Always keep a session record for a search that found no qualifying work. If a weekly, monthly, or yearly report is due, publish a brief report with accurate zero counts, the searched scope, links to sessions, and any coverage gaps. Remove unused finding cards, ranked lists, and theme sections instead of filling them with generic prose. State “No qualifying findings identified” only for a period actually searched; if it was not searched or coverage was incomplete, describe that limitation rather than treating silence as evidence that nothing happened.

## Files and names

| File | Path and name | Purpose |
| --- | --- | --- |
| Source registry | `web/_data/sources.yml` | Shared minimum coverage checklist; research may go beyond it. |
| Website implementation | `web/` | Jekyll pages, layout, data, and assets; keep root-level site files out of the repository. |
| Topic | `topics/<topic-id>/topic.md` | Scope, vocabulary, relevance rules. |
| Monitoring settings | `topics/<topic-id>/monitoring.yml` | Agreed schedule, persistence mode, and ongoing coverage checkpoint; excluded from the website. |
| Search session | `topics/<topic-id>/sessions/YYYY-MM-DDTHHMMSSZ.md` | One record for every distinct search session. Timestamp is the session start in UTC; seconds prevent collisions. |
| Weekly | `topics/<topic-id>/reports/weekly/YYYY-Www.md` | ISO 8601 week, Monday through Sunday. |
| Monthly | `topics/<topic-id>/reports/monthly/YYYY-MM.md` | Calendar month in UTC. |
| Yearly | `topics/<topic-id>/reports/yearly/YYYY.md` | Calendar year in UTC. |

Use lowercase kebab-case topic IDs and source IDs. Create the topic directory and its `sessions/` and `reports/weekly`, `monthly`, and `yearly` directories when adding a topic. Copy the templates, then replace all examples and placeholders. Empty directories have `.gitkeep` files only so Git retains the layout.

## Time and report inclusion

Use UTC for session times and `generated_at`. Use ISO dates (`YYYY-MM-DD`) for period bounds. `period_start` is inclusive and `period_end` is **exclusive**. For example, `2026-W41.md` covers `2026-10-05` through the end of `2026-10-11`, so its `period_end` is `2026-10-12`. Weekly frontmatter titles and Markdown H1 headings use `Weekly Research Review — 2026-W41 (Oct 5 – Oct 11)`: append the full Monday–Sunday dates with abbreviated month names and no year in the suffix. Use `period_start` through `period_end` minus one day, even for partial coverage. Include this suffix when displaying week labels in links; keep filenames and URLs unchanged. ISO weeks begin Monday; ISO week-year can differ from calendar year near New Year. Derive the filename from the ISO week-year, not just the year in `period_start`.

In ongoing monitoring, weekly reports cover findings first observed or materially updated in sessions during that week. A newly discovered older paper may be included; its original publication date must still be stated. For a **retrospective backfill**, create the session on the actual search date, then assign a finding to the week of its verified public release or substantive update. Mark the reports `retrospective: true`, state the limited search scope, and never imply the search happened during the historical week. A boundary week may cover only the days inside the backfilled month; set `coverage_start` (inclusive) and `coverage_end` (exclusive) while retaining the full ISO `period_start` and `period_end`.

Monthly and yearly reviews use release/event dates to select what happened in the calendar period, then reconsider older work when new evidence changes its interpretation. Avoid counting the same work twice merely because it appears in multiple source indexes. An acceptance, major revision, replication, or code release may merit a new assessment of an existing finding ID. A retrospective monthly review includes only releases/events inside that calendar month, even when its boundary-week reports also cover adjacent dates. In ongoing reviews, discuss newly discovered older work in a labelled late-discovery section for the observation period, without presenting it as a new release. Count each discussed finding once and revise a previous synthesis only when the new assessment materially changes its conclusions. Session dates establish when discovery occurred; they do not change release/event dates.

If a scan spans midnight, name the session for its UTC start and state its actual coverage in the record. If two independent scans occur, create two files. If a session is interrupted, keep the file and mark `status: partial`, describing the gap.

## Source registry

`web/_data/sources.yml` is the single canonical registry. Each entry has:

| Field | Meaning |
| --- | --- |
| `id` | Stable lowercase kebab-case identifier. Never silently reuse it for a different source. |
| `name`, `url` | Human label and entry URL. Item citations should use the original item URL, not this home page. |
| `priority` | `primary`, `secondary`, or `discovery`. Primary means explicitly check in every full scan of a listed topic; conditional sources may be skipped with a reason. Secondary means check when relevant. Discovery marks a starting mechanism for finding original material, not a complete list of discovery routes. |
| `type` | Descriptive source class, such as preprint repository or proceedings. |
| `canonical` | Whether an item hosted there can be cited as the original item record. This does **not** mean all claims are reliable. A code host is canonical for its own release, not for a paper’s publication metadata. |
| `useful_for`, `evidence_note`, `notes` | Why to check it, how to treat evidence, and practical instructions. |
| `topics` | Topic IDs for which the source is monitored. Add a topic ID to relevant sources when creating a topic. |

The primary list includes arXiv, OpenReview, NeurIPS proceedings, ICML/PMLR, ICLR, JMLR, ACL Anthology, and Q Labs Research. In a full ZO scan, check the relevant view of each or explicitly record why a conditional source (such as ACL Anthology for non-NLP work) was not applicable. Continue searching beyond these entries. A source may be both a discovery route and a first-party record in different contexts; use the individual item’s actual provenance in the finding assessment.

## Search session: the audit trail

Create one Markdown file from `templates/session.md` for every search session, including a zero-result session. The frontmatter fields are `schema_version`, `topic`, `type: session`, `searched_at` (UTC timestamp), `search_scope` (`full` or `targeted`), `status` (`complete` or `partial`), `source_ids_checked` (registered IDs actually checked), `additional_sources_checked` (URLs of unregistered sources actually checked), and `candidate_count` (number of non-placeholder candidate rows). A targeted follow-up is a session too; describe its narrower scope. The sources table records the query or page, date range, result, and coverage gaps for both registered and unregistered sources. Do not claim a source was checked merely because it appears in the registry.

Capture candidate titles and original URLs even when the item is later excluded. Use `candidate`, `included`, `excluded`, or `follow_up` as decisions and explain exclusions or follow-ups. Record updates to known work separately. Link each included candidate to the stable finding ID used in reports. A session records discovery and decisions; a report contains the complete considered assessment. Do not omit an otherwise relevant item because its source is absent from the registry.

## Finding identity and report-only storage

For this version, findings live in weekly report cards. Assign an ID when first assessed: `<topic-id>-<first-seen-YYYY-MM-DD>-<short-slug>`, for example `zero-order-training-2026-10-06-mpsub`. If a collision occurs, add a short distinguishing suffix. Keep the ID through revisions, acceptances, and later synthesis. Use the original item’s stable landing page as `Canonical URL`; add a code/project URL separately. When the same work is on arXiv and a proceedings site, cite the most authoritative current publication page and note alternate versions when they matter. Do not create a new ID for a version change.

Cross-report references should use the finding ID and a relative Markdown link to the first weekly assessment's `#<finding-id>` anchor. This makes later extraction into `findings/<id>.md` possible without changing IDs or rewriting links conceptually. Separate finding files should be introduced only if per-finding history, cross-topic reuse, or dedicated pages become a real need. At that point, migrate the existing IDs and keep redirects or links from reports; do not maintain two competing full descriptions.

## Weekly reports

Use `templates/weekly.md`. Frontmatter includes `title`, `topic`, `type`, inclusive `period_start`, exclusive `period_end`, `generated_at`, `session_files` (relative paths from the report), `findings_count`, high/medium/low counts, and a `findings` list containing each card's stable `id`, `released_on` date (or null with `date_uncertainty`), `canonical_url`, and short display `title`. Put `<span id="<finding-id>"></span>` inside the matching card heading, immediately before its text. The validator checks this index against the cards; IDs, counts, dates, and anchors must agree. Direct finding links target the matching heading anchors. Use a linked paper title in each heading. An otherwise qualifying ongoing finding with an unverified release date may use `released_on: null` and a nonempty `date_uncertainty` explanation; its card says `Unknown`, and it belongs to the observation week. For retrospective placement, require either a verified release date or a verified substantive `event_on` date with the event described in the card; otherwise retain it as `follow_up` in the session until dated. Never invent a date. Optional `retrospective`, `coverage_start`, and `coverage_end` describe a historical backfill. `session_files` can be empty only if the report explicitly says coverage was absent. A week without qualifying findings says so briefly and identifies the searched scope and coverage limits; remove unused cards and priority sections and set `findings: []`.

Keep the executive summary to about three to five bullets. Put cards under High, Medium, or Low according to **relevance**; rank within each section by importance. For every card include all template fields. `Authors` should reflect the original record. Use `Unknown` when a date or author cannot be verified, and explain consequential uncertainty. Contribution is one or two sentences; `Why it matters` is separate. Cite the original source for the result and describe the actual experimental or theoretical support. Do not treat an abstract, acceptance label, code link, or press summary as proof of a performance claim.

### Three distinct judgments

| Dimension | Values | Question |
| --- | --- | --- |
| Relevance | high / medium / low | How directly does it answer the topic question? |
| Importance | 1–5 | If the claim is true, how much could it change methods, understanding, or research priorities? |
| Evidential maturity | 1–5 | How strongly is the claim supported and independently scrutinized now? |

**Importance:** 1 = minor context; 2 = modest incremental value; 3 = useful result or method; 4 = major advance or consequential negative result; 5 = potentially field-shaping. This is a judgment of potential consequence, not popularity.

**Evidential maturity:** 1 = announcement or thin evidence; 2 = detailed first-party claim with important missing controls; 3 = substantive methods and experiments or theory, still largely first-party; 4 = strong, well-documented evidence with meaningful external scrutiny or reproducibility; 5 = convergent independent evidence, robust replication, or comparably mature support. Peer review may improve scrutiny but never automatically sets a score. A new lab report can be importance 5 and maturity 3; a well-established accepted paper can be importance 3 and maturity 5.

Use `Evidence and source quality` to state concrete facts: venue status, available methods, baseline fairness, scale, seeds, compute accounting, code, independent checks, and unresolved questions. Use `Major limitations` for the most decision-relevant caveats. Revise scores when evidence changes, and say why.

## Monthly and yearly reports

Monthly reviews select and compare the most consequential developments in the calendar month, including updates to older work. Cover methodological themes, stronger or weaker claims, what deserves deep reading, what became less important, and implications for current research. The `Full Included Findings` table links IDs to weekly assessments; it is an index, not four weeks pasted together. If nothing qualifies, use a short zero-finding synthesis and coverage statement; do not force every template section or recommend reading merely to fill space.

Yearly reviews make a higher-level judgment about methods, empirical and theoretical progress, negative results, shifts in confidence, groups contributing important work, open problems, and canonical reading. Link every major conclusion to source material through finding IDs or original URLs. The timeline selects milestones rather than enumerating every item. If the year yields no supported material change, state that succinctly with coverage and evidence limits; omit empty rankings and timeline rows.

Every monthly and yearly report includes `session_files`, listing the actual supporting sessions relative to that report, so direct session navigation works. Collect these from supporting weekly/monthly reports; deduplicate them. Empty lists are allowed only when coverage was absent and the report says so.

For monthly and yearly metadata, `findings_count` is the number of distinct findings in the included-finding index or, for yearly, the distinct findings explicitly discussed or listed. Keep it honest; it is not a count of all publications in the field.

## Adding another topic

1. Choose a stable kebab-case topic ID and create `topics/<id>/topic.md` from `templates/topic.md`, adapting all frontmatter and scope sections. Set `type: topic`, `layout: project`, a short `summary`, and `permalink: /projects/<id>/` so the Projects page can list it and the project layout can show its report hierarchy.
2. Add the topic ID to applicable entries in `web/_data/sources.yml`; add new sources only when they provide distinct coverage.
3. Create its session and report directories. Copy the session/report templates only when a real search occurred or a report is due; replace every example ID, date, and placeholder.
4. Follow `docs/agent-workflow.md` to agree on and save monitoring settings before activating a schedule.
5. Keep topic-specific search vocabulary and inclusion rules in the topic file. Keep shared source facts in the source registry.

## Static GitHub Pages site

The Jekyll site enumerates `topics/*/topic.md` and report/session pages with frontmatter, and reads the canonical `web/_data/sources.yml`. Keep site-only pages, layouts, data, and assets inside `web/`; `_config.yml` remains at the root and points to the moved layout and data folders. Primary navigation is Overview, Projects, Sources. The [Projects page](../web/projects.html) lists topics, while `web/_layouts/project.html` groups each topic's reports by year, then month, then week. For retrospective boundary weeks, `coverage_start` determines the displayed month. Each report can expand in place or open in a new tab. Keep `/`, `/projects/`, `/sources/`, and report URLs stable through permalinks. Link every displayed paper title, including summary and session-table titles, directly to its canonical original URL; the site opens external links in new tabs. Search sessions are reached from the report that cites them; each session page can link back to that report. There is no separate findings index or archive page. `title` supplies the browser label; keep it aligned with the document heading. Add reports as Markdown files in the documented directories and they will appear without editing HTML. Relative `.md` links between files are converted to site page links by the GitHub Pages-supported `jekyll-relative-links` plugin.

Topic icons are optional image paths in topic frontmatter and live under `web/assets/brand/` or another documented site asset folder. If a topic has no icon, the Projects page uses the standard blank document icon; use the shared folder and document treatments for structural navigation icons rather than inventing a new visual language per topic.

Finding links point into the original weekly assessments; the site has no separate finding copies. A small script loads rendered report content when a report is expanded, while each report remains available as its own page if the script is unavailable. `_config.yml` sets the GitHub Pages origin, project path, and repository URL; update them if the repository is renamed or moved.
