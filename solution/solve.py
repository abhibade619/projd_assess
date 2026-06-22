import json
import re
from collections import Counter
from pathlib import Path

INPUT_PATH = Path("/app/access.log")
OUTPUT_PATH = Path("/app/report.json")
REQUEST_PATTERN = re.compile(
    r'"[^"\s]+\s+(\S+)\s+HTTP/\d(?:\.\d)?"'
)


def main():
    total_requests = 0
    unique_ips = set()
    path_counts = Counter()

    for raw_line in INPUT_PATH.read_text(
        encoding="utf-8"
    ).splitlines():
        line = raw_line.strip()

        if not line:
            continue

        total_requests += 1
        unique_ips.add(line.split(maxsplit=1)[0])

        match = REQUEST_PATTERN.search(line)
        if match is None:
            raise ValueError(
                f"Unable to parse request from log entry: {line}"
            )

        path_counts[match.group(1)] += 1

    top_path = min(
        path_counts,
        key=lambda path: (-path_counts[path], path),
    )

    report = {
        "total_requests": total_requests,
        "unique_ips": len(unique_ips),
        "top_path": top_path,
    }

    OUTPUT_PATH.write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()