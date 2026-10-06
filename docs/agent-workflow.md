# Set up and run a research topic

Read this document before onboarding a topic or running scheduled research.
Use the [writing guide](writing-guide.md) for evidence standards, dates, metadata, and report formats.
The scheduler runs outside this repository.

## First conversation

Inspect existing topics and their `monitoring.yml` files before asking questions.
Reuse answers already supplied by the human; ask only for missing decisions, grouped into a short conversation:

1. **Topic and purpose:** continue an existing topic or create a new one; what question should the archive answer, and what research decision should it support?
2. **Scope:** what belongs in or outside the topic, which source/release types matter, and what would make a finding meaningful? Propose vocabulary and inclusion rules for the human to refine.
3. **Starting point:** monitor from now, start on a particular UTC date, or first backfill a specified historical interval? Keep historical backfill separate from ongoing coverage.
4. **Cadence:** which weekday, local time, and IANA timezone should the weekly run use? Explain that report periods use UTC even when the scheduler uses local time.
5. **Execution and destination:** which agent/scheduler will run, which writable checkout or fork should receive results, and should it save locally, commit, push, or open a pull request? Confirm the branch/remote only for the chosen publishing mode. Ask about website publication only if wanted.
6. **Reading preferences:** propose English, concise assessments, and the repository's relevance/importance rules unless the human has specified another language or emphasis.

Do not create a duplicate topic or scheduler merely because this is a new conversation.
Do not infer authorization to push or publish from possession of a repository link.

## Save and verify setup

1. Create or update `topic.md` using [the topic template](../templates/topic.md), preserving established IDs and scope.
2. Copy [monitoring.yml](../templates/monitoring.yml) into the topic directory and record the agreed settings. Keep credentials out of the repository. This operational file is excluded from the website, but anyone with repository access can read it.
3. Add the topic to relevant registry entries and create its session and weekly/monthly/yearly directories. Existing retrospective examples do not establish ongoing monitoring coverage.
4. Verify that the selected agent can read this repository, browse original sources, write to the agreed destination, and use an external scheduler. If scheduling is unavailable, set `status: manual`, provide the reusable prompt below, and explain how the human can run it weekly. Never claim that a schedule exists without a successful scheduler result.
5. Configure one weekly task with the agreed local weekday/time/timezone and the resolved prompt below. Record the returned scheduler task ID. Check the scheduler's displayed next run and timezone; update an existing task when its ID is already recorded.
6. Set `status: active` only after setup succeeds. Summarize the topic, first search interval, cadence, destination, and actual scheduler status to the human. Do the agreed initial search; do not fabricate an initial report merely to demonstrate setup.

`status` is `needs_setup`, `active`, `manual`, or `paused`.
`monitor_from` is the inclusive UTC start date for ongoing monitoring.
`last_completed_end` is the exclusive UTC cutoff of the latest consecutively covered full scan; leave it null until such a scan is saved successfully.
`backfill_start` and `backfill_end` are optional historical bounds and must not advance this ongoing checkpoint.

## Reusable scheduler prompt

Replace angle-bracket placeholders before saving this prompt in the external scheduler:

> Open <writable repository location> and track topic <topic-id>.
> Read AGENTS.md, docs/agent-workflow.md, docs/writing-guide.md, the topic's topic.md and monitoring.yml, and web/_data/sources.yml.
> Follow the recurring-run procedure, including previous findings and follow-ups, full source coverage, honest partial-session handling, stable finding IDs, weekly updates, and any due monthly/yearly syntheses.
> Validate the archive and built site before saving through the configured persistence mode.
> Report meaningful findings, coverage failures, and any action needed; do not claim complete coverage or a successful publication when it failed.
> Do not create another scheduled task during this run.

## Every recurring run

1. **Read state.** Respect `paused` and `needs_setup`; report what needs attention without starting an unattended scan. Read the topic, monitoring settings, previous sessions, weekly findings, latest syntheses, and unresolved follow-ups. Inspect repository status and preserve unrelated changes. Ensure no other run for this topic is in progress before writing.
2. **Choose the interval.** Use the run's actual UTC start as the exclusive cutoff. Begin at `last_completed_end`, or `monitor_from` on the first run. Requery the preceding `overlap_days` as well, bounded by `monitor_from`, to catch indexing delays. Deduplicate overlap results against existing canonical URLs, alternate versions, and IDs. Check material updates to older work separately.
3. **Catch up honestly.** After missed runs, search the entire uncovered interval. If it cannot be completed in this run, record the outstanding interval and source gaps, mark the session partial, and retain the old checkpoint. Never invent sessions on missed dates. In ongoing mode, newly observed findings belong to the actual observation week, even when their release was earlier; historical backfill uses the separate date rules in the writing guide.
4. **Search and record.** Create a session at its actual UTC start. Save exact executed queries or page URLs, filters, sort order, and pagination limits. Check applicable primary sources, search beyond the registry, assess original material, and record decisions and inaccessible sources. Mark interrupted or incomplete scans partial. A skipped source is not a checked source.
5. **Reconcile identity.** Reuse existing IDs for revisions, acceptances, replications, or code releases. Preserve earlier assessments and add a dated explanation when evidence changes. Resume the same session file when recovering the same interrupted search; a genuinely new search receives a new timestamp. A retry must merge report content by finding ID, never erase other sessions' findings or append duplicate cards.
6. **Update reports.** Merge findings into the appropriate weekly files, union their `session_files`, recompute counts, and rank within relevance groups. Produce or refresh elapsed-week coverage reports, distinguishing searched zero-result intervals from gaps. On each run, check all closed months and years since the configured monitoring/backfill start; create missing syntheses and revise affected existing ones when late evidence changes them. Generate a month after its UTC end and a year after 1 January UTC, normally on the next weekly run. Do not manufacture reports for periods before monitoring began.
7. **Validate and persist.** Follow [development and validation](development.md). Save only task-related changes using the agreed mode. For push/PR modes, check remote state and resolve conflicts without discarding others' work. If validation or persistence fails, keep recoverable work, record the failure, and do not advance the checkpoint. Advance `last_completed_end` to the cutoff only when full source coverage and the relevant outputs are successfully saved. A successful retry may repair an earlier partial run; cite both sessions rather than rewriting history.
8. **Summarize.** State the searched interval, meaningful changes, reports written, remaining gaps, and persistence outcome. For a zero-result run, keep the summary short. Never treat a targeted search as a completed full scan or advance the checkpoint from it.

## Date examples

- A September paper found during an October backfill belongs in its September release week and September synthesis; the session keeps its actual October search date.
- The same old paper first found during ordinary October monitoring belongs in the October observation week. Include it in October's explicitly labelled late-discovery discussion; it is not an October release. Update an existing September review only if the addition materially changes that review.
- A failed run followed by a retry preserves the failed session and any saved cards. The retry searches the still-uncovered interval and reuses finding IDs.
- A run on 4 January checks for the previous December and previous year's syntheses, even when its ISO week-year differs from its calendar year.
