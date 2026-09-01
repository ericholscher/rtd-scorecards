#!/usr/bin/env python3
"""Generate the scoreboard from OSSF Scorecard JSON results.

Reads every ``*.json`` file in the results directory. With ``--readme``,
splices the scoreboard into that file between the scoreboard markers;
without it, prints the scoreboard to stdout (used for the job summary).
"""

import argparse
import json
import pathlib
import sys

START_MARKER = "<!-- scoreboard:start -->"
END_MARKER = "<!-- scoreboard:end -->"

# Checks scoring below this are listed in the "Lowest checks" column.
FAILING_THRESHOLD = 5

# List at most this many failing checks per repo.
MAX_LISTED_CHECKS = 3


def load_results(results_dir):
    results = []
    for path in sorted(results_dir.glob("*.json")):
        with open(path) as fd:
            data = json.load(fd)
        results.append(data)
    return results


def lowest_checks(result):
    """Return a short label for the repo's worst-scoring checks."""
    failing = []
    for check in result.get("checks", []):
        score = check.get("score")
        if score is None or score < 0:
            # A score of -1 means the check was inconclusive; skip it.
            continue
        if score < FAILING_THRESHOLD:
            failing.append((score, check["name"]))
    failing.sort()

    labels = []
    for score, name in failing[:MAX_LISTED_CHECKS]:
        labels.append(f"{name} ({score})")
    if not labels:
        return "—"
    return ", ".join(labels)


def build_scoreboard(results):
    rows = []
    for result in results:
        # Scorecard reports the repo as e.g. "github.com/readthedocs/addons".
        full_name = result["repo"]["name"]
        short_name = full_name.removeprefix("github.com/")
        rows.append(
            {
                "name": short_name,
                "url": f"https://{full_name}",
                "score": result["score"],
                "lowest": lowest_checks(result),
            }
        )
    # Worst score first, so the most critical repos are at the top.
    rows.sort(key=lambda row: row["score"])

    first = results[0]
    # Scorecard reports a full timestamp; the date alone reads better.
    scan_date = first.get("date", "unknown")[:10]
    version = first.get("scorecard", {}).get("version", "unknown")

    lines = []
    lines.append(f"Last scan: {scan_date} · Scorecard {version}")
    lines.append("")
    lines.append("| Repo | Score | Lowest checks |")
    lines.append("|------|-------|---------------|")
    for row in rows:
        lines.append(
            f"| [{row['name']}]({row['url']}) "
            f"| {row['score']:.1f} "
            f"| {row['lowest']} |"
        )
    return "\n".join(lines)


def splice_readme(readme_path, scoreboard):
    content = readme_path.read_text()
    if START_MARKER not in content or END_MARKER not in content:
        sys.exit(f"error: scoreboard markers not found in {readme_path}")
    before, _, rest = content.partition(START_MARKER)
    _, _, after = rest.partition(END_MARKER)
    updated = before + START_MARKER + "\n" + scoreboard + "\n" + END_MARKER + after
    readme_path.write_text(updated)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--results",
        type=pathlib.Path,
        required=True,
        help="Directory containing Scorecard JSON output files",
    )
    parser.add_argument(
        "--readme",
        type=pathlib.Path,
        help="README to update in place; omit to print to stdout",
    )
    args = parser.parse_args()

    results = load_results(args.results)
    if not results:
        sys.exit(f"error: no results found in {args.results}")

    scoreboard = build_scoreboard(results)
    if args.readme:
        splice_readme(args.readme, scoreboard)
    else:
        print(scoreboard)


if __name__ == "__main__":
    main()
