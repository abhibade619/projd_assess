Read the access log at `/app/access.log` and write a report to `/app/report.json`.

Success criteria:

1. `/app/report.json` must contain a valid JSON object with exactly these keys: `total_requests`, `unique_ips`, and `top_path`.
2. `total_requests` must be an integer equal to the number of non-empty entries in `/app/access.log`.
3. `unique_ips` must be an integer equal to the number of distinct client IP addresses in the first whitespace-delimited field of the non-empty entries.
4. `top_path` must be a string equal to the request target that appears most frequently in the quoted HTTP requests. If multiple request targets have the same highest count, use the lexicographically smallest target.

Do not modify `/app/access.log`.

You have 120 seconds to complete this task. Do not cheat by using online solutions or hints specific to this task.
