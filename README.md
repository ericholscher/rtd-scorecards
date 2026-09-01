# rtd-scorecards

Weekly [OSSF Scorecard](https://github.com/ossf/scorecard) scans of the
Read the Docs and EthicalAds open-source repos.

A GitHub Actions workflow ([`scorecard.yml`](.github/workflows/scorecard.yml))
runs every Monday, scans each repo listed in [`repos.txt`](repos.txt) with the
Scorecard CLI, and commits the scoreboard below. Raw JSON results are attached
to each workflow run as artifacts.

## Scoreboard

<!-- scoreboard:start -->
_No scans yet — the scoreboard appears after the first workflow run._
<!-- scoreboard:end -->

Scores are 0–10 (higher is better), sorted worst-first. "Lowest checks" lists
each repo's three lowest-scoring checks that score below 5.

## Notes

- Repos are scanned from the outside, without admin access, so checks that
  need it (parts of Branch-Protection, for example) can score low or show as
  inconclusive. Treat scores as a relative signal, not an absolute grade.
- The scan authenticates with the workflow's `GITHUB_TOKEN`. If runs start
  hitting API rate limits, add a classic PAT with `public_repo` scope as a
  `SCORECARD_TOKEN` repository secret — it takes precedence.
- To add or remove a repo, edit `repos.txt`.
