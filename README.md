# rtd-scorecards

Weekly [OSSF Scorecard](https://github.com/ossf/scorecard) scans of the
Read the Docs and EthicalAds open-source repos.

A GitHub Actions workflow ([`scorecard.yml`](.github/workflows/scorecard.yml))
runs every Monday, scans each repo listed in [`repos.txt`](repos.txt) with the
Scorecard CLI, and commits the scoreboard below. Raw JSON results are attached
to each workflow run as artifacts.

## Scoreboard

<!-- scoreboard:start -->
Last scan: 2026-09-01 · Scorecard v5.5.0

| Repo | Score | Lowest checks |
|------|-------|---------------|
| [readthedocs/sphinx-build-compatibility](https://github.com/readthedocs/sphinx-build-compatibility) | 2.9 | Branch-Protection (0), CI-Tests (0), CII-Best-Practices (0) |
| [readthedocs/readthedocs-docker-images](https://github.com/readthedocs/readthedocs-docker-images) | 3.2 | Branch-Protection (0), CII-Best-Practices (0), Dependency-Update-Tool (0) |
| [readthedocs/addons](https://github.com/readthedocs/addons) | 4.8 | Branch-Protection (0), CII-Best-Practices (0), Dependency-Update-Tool (0) |
| [readthedocs/sphinx-autoapi](https://github.com/readthedocs/sphinx-autoapi) | 5.3 | Branch-Protection (0), CII-Best-Practices (0), Fuzzing (0) |
<!-- scoreboard:end -->

Scores are 0–10 (higher is better), sorted worst-first. "Lowest checks" lists
each repo's three lowest-scoring checks that score below 5.

## Notes

- Repos are scanned from the outside, without admin access, so checks that
  need it (parts of Branch-Protection, for example) can score low or show as
  inconclusive. Treat scores as a relative signal, not an absolute grade.
- The workflow's `GITHUB_TOKEN` cannot read classic branch protection rules,
  so repos using classic branch protection are scored without the
  Branch-Protection check (the scan retries with it excluded). Adding a
  classic PAT from an org admin as a `SCORECARD_TOKEN` repository secret
  restores that check — it takes precedence over the workflow token, and also
  helps if runs hit API rate limits.
- To add or remove a repo, edit `repos.txt`.
