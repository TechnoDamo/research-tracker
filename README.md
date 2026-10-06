# Research Tracker

A small, Git-friendly archive and static portal for following research publications and releases over time. The first topic is zero-order training; the structure supports other topics without changing the report formats.

This repository is a human-readable research record. A search session records what was checked and what it found. Weekly reports assess meaningful findings. Monthly and yearly reports synthesize developments and changes in evidence. Quiet periods get a brief, honest zero-finding record when searched; reports are never padded with weak items or generic analysis.

## Structure

```text
_data/sources.yml                    Shared source registry and site data
topics/<topic-id>/topic.md           Topic scope and relevance rules
topics/<topic-id>/sessions/          One Markdown record per search session
topics/<topic-id>/reports/weekly/    YYYY-Www.md
topics/<topic-id>/reports/monthly/   YYYY-MM.md
topics/<topic-id>/reports/yearly/    YYYY.md
templates/                           Copyable session and report formats
docs/writing-guide.md                Field definitions and writing process
index.html, archive.html, sources.html  Static portal pages
_layouts/, assets/, _config.yml       GitHub Pages layout and styling
```

Start with [the agent workflow](AGENTS.md), [the ZO topic](topics/zero-order-training/topic.md), [the source registry](_data/sources.yml), and [the writing guide](docs/writing-guide.md).

For a worked example, read the [September 2026 monthly review](topics/zero-order-training/reports/monthly/2026-09.md), its five linked weekly reports, and the [retrospective search session](topics/zero-order-training/sessions/2026-10-06T141730Z.md). The example is explicitly marked as a targeted, partial backfill.

## Working sequence

1. Read the topic scope and source registry. The registry is a minimum coverage checklist, **not a boundary on search**. Check relevant listed sources and actively discover work elsewhere using broader search, citations, lab pages, and new terminology.
2. Create a session record from `templates/session.md` for **each** search session, including sessions with no useful results. Record every checked source, including unregistered ones, plus queries, candidate links, and gaps.
3. Write a weekly report from `templates/weekly.md` after reviewing the session records and original material. Include only meaningful findings; assess importance and evidence separately.
4. Write monthly and yearly reviews from their templates. Recheck important claims and synthesize developments instead of concatenating earlier reports.

Sessions are an audit trail, while reports contain the considered assessments. Finding IDs connect session candidates and reports. No individual finding files are required in this version; [the guide](docs/writing-guide.md) explains how to add them later if needed.

## Static site

The minimal interface has an overview, report and session archive, topic pages, and a source list. GitHub Pages can build it from the `main` branch root with Jekyll. It reads topic and report frontmatter and the canonical `_data/sources.yml` file; no generated content, database, or JavaScript is required. New reports with frontmatter appear in the archive automatically.

The configured `baseurl` is `/research-tracker`, matching a GitHub Pages project site with that repository name. Change it in `_config.yml` if the repository name or hosting path changes. The site is local only until a GitHub remote is created and Pages is enabled.

For a local preview with Jekyll installed, run `jekyll serve` from the repository root and open `/research-tracker/` on the local server. GitHub Pages should be configured to publish from `main` at the repository root when the repository is eventually hosted.

## Scope

This version contains no scheduled scans, crawler, database, backend, or LLM integration. The website displays the manually maintained archive; it does not perform research.
