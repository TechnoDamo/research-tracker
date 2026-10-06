# Preview, validate, and publish

## Local setup

Install Ruby, Bundler, and Python 3.9 or later.
The repository's Gemfile and lockfile declare the Jekyll dependencies.
From the repository root:

```sh
bundle config --local path vendor/bundle
bundle install
bundle exec jekyll serve --host 127.0.0.1
```

Open `http://127.0.0.1:4000/research-tracker/` with the current `baseurl`.
The installed gems and local Bundler configuration are ignored by Git.
Never commit credentials or local caches.

## Required validation

Run this after changing research records, templates, or the website:

```sh
bundle exec jekyll build
python3 scripts/validate.py
git diff --check
```

To keep generated files outside the repository:

```sh
bundle exec jekyll build --destination /tmp/research-tracker-site
python3 scripts/validate.py --site /tmp/research-tracker-site
```

The validator checks source/topic metadata, report dates and counts, required finding fields and ordering, anchors, session references, monitoring settings, README line breaks, and built local links/assets.
It exits unsuccessfully when a check fails.
It does not verify external websites, scientific claims, complete source coverage, or whether an external scheduler is actually running.
Agents must verify those facts from the original sources and scheduler results.

After website changes, also check the browser:

1. Open Overview, Projects, Sources, and a project on desktop and a narrow mobile viewport.
2. Expand year, month, and weekly reports; check the full Monday–Sunday suffix in week labels and standalone report headings.
3. Open paper links from both expanded and standalone reports; both must open the original in a new tab.
4. Follow “Inspect search session”, return to the report, and follow a finding anchor.
5. Check for broken images, resource errors, page-width overflow, and duplicate report headings. Wide tables may scroll within their container.

No annual report is fabricated for testing.
For new report types or date-boundary changes, use temporary fixtures outside the archive and check ISO New Year, cross-month weeks, zero findings, and partial coverage.

## Publishing to GitHub Pages

Agree on the destination repository and publishing permission with the human.
Create or select their writable repository/fork, set its remote, and set `_config.yml`:

- `url`: the public origin, for example `https://ACCOUNT.github.io`.
- `baseurl`: `/REPOSITORY` for a project site, or an empty string for an account site or custom domain served at its root.
- `github_url`: the actual repository URL.

Push the reviewed source changes using the agreed persistence mode.
Configure GitHub Pages to build from the source branch's root, where `_config.yml` lives, using its Jekyll support; alternatively configure an explicit build/deployment workflow for the same source.
Check the deployment result and then the live navigation, assets, reports, and anchors at the real URL.
Only after verifying publication, replace the labelled placeholder link in README with that URL and remove its placeholder label.
Keep the placeholder while no public destination exists.

Website deployment and scheduled research are separate setup steps.
Publishing the site does not create or activate an external research scheduler.
