import json
import re
from collections import Counter
from pathlib import Path

REPORT_PATH = Path("/app/report.json")
REFERENCE_LOG_PATH = Path("/tests/access.log")
REQUEST_PATTERN = re.compile(
    r'"[^"\s]+\s+(\S+)\s+HTTP/\d(?:\.\d)?"'
)


def load_report():
    return json.loads(
        REPORT_PATH.read_text(encoding="utf-8")
    )


def calculate_expected_values():
    total_requests = 0
    unique_ips = set()
    path_counts = Counter()

    for raw_line in REFERENCE_LOG_PATH.read_text(
        encoding="utf-8"
    ).splitlines():
        line = raw_line.strip()

        if not line:
            continue

        total_requests += 1
        unique_ips.add(line.split(maxsplit=1)[0])

        match = REQUEST_PATTERN.search(line)
        if match is None:
            raise AssertionError(
                f"Unable to parse verifier log entry: {line}"
            )

        path_counts[match.group(1)] += 1

    top_path = min(
        path_counts,
        key=lambda path: (-path_counts[path], path),
    )

    return {
        "total_requests": total_requests,
        "unique_ips": len(unique_ips),
        "top_path": top_path,
    }


EXPECTED = calculate_expected_values()


def test_report_format():
    # Verifies instruction.md success criterion 1.
    assert REPORT_PATH.is_file(), (
        "/app/report.json was not created"
    )

    try:
        report = load_report()
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise AssertionError(
            "/app/report.json must contain valid UTF-8 JSON"
        ) from error

    assert isinstance(report, dict), (
        "/app/report.json must contain a JSON object"
    )

    assert set(report) == {
        "total_requests",
        "unique_ips",
        "top_path",
    }, (
        "The report must contain exactly total_requests, "
        "unique_ips, and top_path"
    )


def test_total_requests():
    # Verifies instruction.md success criterion 2.
    report = load_report()

    assert type(report["total_requests"]) is int, (
        "total_requests must be an integer"
    )

    assert (
        report["total_requests"]
        == EXPECTED["total_requests"]
    )


def test_unique_ips():
    # Verifies instruction.md success criterion 3.
    report = load_report()

    assert type(report["unique_ips"]) is int, (
        "unique_ips must be an integer"
    )

    assert report["unique_ips"] == EXPECTED["unique_ips"]


def test_top_path():
    # Verifies instruction.md success criterion 4.
    report = load_report()

    assert type(report["top_path"]) is str, (
        "top_path must be a string"
    )

    assert report["top_path"] == EXPECTED["top_path"]