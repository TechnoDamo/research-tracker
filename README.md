# Research Tracker

A small, Git-friendly archive for following research publications and releases over time. The first topic is zero-order training; the structure supports other topics without changing the report formats.

This repository is a human-readable research record. A search session records what was checked and what it found. Weekly reports assess meaningful findings. Monthly and yearly reports synthesize developments and changes in evidence. Absence of a finding is recorded explicitly; reports are never padded.

## Structure

```text
sources.yaml                         Shared source registry
topics/<topic-id>/topic.md           Topic scope and relevance rules
topics/<topic-id>/sessions/          One Markdown record per search session
topics/<topic-id>/reports/weekly/    YYYY-Www.md
topics/<topic-id>/reports/monthly/   YYYY-MM.md
topics/<topic-id>/reports/yearly/    YYYY.md
templates/                           Copyable session and report formats
docs/writing-guide.md                Field definitions and writing process
```

Start with [the ZO topic](topics/zero-order-training/topic.md), [the source registry](sources.yaml), and [the writing guide](docs/writing-guide.md).

## Working sequence

1. Read the topic scope and the sources assigned to it.
2. Create a session record from `templates/session.md` for **each** search session, including sessions with no useful results. Record checked sources, queries, candidate links, and gaps.
3. Write a weekly report from `templates/weekly.md` after reviewing the session records and original material. Include only meaningful findings; assess importance and evidence separately.
4. Write monthly and yearly reviews from their templates. Recheck important claims and synthesize developments instead of concatenating earlier reports.

Sessions are an audit trail, while reports contain the considered assessments. Finding IDs connect session candidates and reports. No individual finding files are required in this version; [the guide](docs/writing-guide.md) explains how to add them later if needed.

## Scope

This version contains no scheduled scans, crawler, database, backend, LLM integration, or website. The Markdown and YAML files can be read directly by a later static GitHub Pages build.
