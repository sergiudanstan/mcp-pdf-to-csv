# Security Policy

`mcp-pdf-to-csv` is a local MCP server (stdio, a single Python file) that reads PDF files with
`pdfplumber` and writes the tables it finds as CSV files. It has no network listener and makes
no outgoing network calls. Its tools read and write files on the machine it runs on, with the
privileges of the user who started it.

## Supported versions

| Version | Supported |
|---|---|
| 0.1.x | Current |

Single maintainer; only the latest release receives fixes.

## Reporting a vulnerability

**Please do not open a public issue for a security problem.** Report it privately:
**[Report a vulnerability](https://github.com/sergiudanstan/mcp-pdf-to-csv/security/advisories/new)**
(Security -> Advisories -> Report a vulnerability).

| Stage | Target |
|---|---|
| Acknowledgement | within 3 business days |
| Triage | within 10 business days |
| Fix, or a documented decision not to fix | within 90 days |

These are best-effort targets from a single unpaid maintainer, not a contractual SLA.
There is no bug bounty; credit is offered in the advisory and changelog.

## Threat model

Tool arguments are untrusted: they are chosen by an LLM that may itself be steered by
prompt injection in content it reads. The tools do **not** confine file access to the
configured folders, and I verified this rather than assuming it:

- **Arbitrary directories.** `set_folder` and `set_output` accept any path (with `~`
  expanded), create it if it does not exist, and make it the input or output folder.
  Afterwards CSV files are written to wherever `set_output` pointed, named
  `<pdf-stem>__p<page>_t<n>.csv` or `<pdf-stem>__merged.csv`; an existing file with that
  name is overwritten without warning. The cell contents are whatever the PDF contains.
- **Arbitrary PDFs.** `extract_tables(filename=...)` joins `filename` to the input folder
  without checking the result, so an absolute path or `../` reads any PDF the user can read
  (tested: `../elsewhere/x.pdf` and an absolute path both work). Only files that parse as PDF
  produce output; the error message for others includes the exception text.
- **Hostile PDFs.** PDFs are parsed by `pdfplumber` / `pdfminer.six`. A crafted PDF can use a
  lot of CPU or memory, and there is no timeout or size limit. The `pages` argument such as
  `1-999999999` is expanded into a Python set before being clipped to the page count, so a
  large range can exhaust memory.
- **Shared state.** The input and output folders are process-wide and changed by tool calls;
  a prompt-injected call to `set_output` redirects every later extraction.
- **Code execution and network.** There is no subprocess, `eval` or network use in the server.

Run it only with clients and models you trust with the files your account can read and write,
keep per-tool approval on for `set_folder`, `set_output` and the extract tools, and consider a
dedicated low-privilege user or a container if the model sees untrusted documents.

## Scope

In scope:

- Code execution, command injection or network access reachable through any tool.
- Anything in this repository's workflows that could publish a release not built from `main`.
- A crafted PDF that makes the server write a file other than the documented CSV outputs.

Out of scope:

- The unrestricted folders and paths described above. They are how the tools currently work,
  and the README does not claim otherwise; a hardening change (confining paths to configured
  folders) is welcome as a normal feature request or pull request.
- Resource exhaustion by large or malformed PDFs or page ranges (known, see above).
- Vulnerabilities in `pdfplumber`, `pdfminer.six`, `pandas`, `fastmcp` or the client (report upstream).

## Supply chain

CI runs the test suite on Python 3.10 and 3.13 (PDFs generated in the test and parsed by
`pdfplumber`, tools called through an in-memory MCP client), `ruff` (syntax and undefined-name
checks only), `pip-audit` on the dependencies resolved from `requirements.txt` and on the
hash-pinned CI toolchain, CodeQL, and `zizmor` on the workflows. The runtime dependencies in
`requirements.txt` are version ranges, not a lockfile, so installs resolve to the newest
allowed versions. Actions are pinned to full commit SHAs and kept current by Dependabot.
Releases attach a source archive and a CycloneDX SBOM of the dependency set resolved at release
time, both with Sigstore build provenance:

```
gh attestation verify mcp-pdf-to-csv-v0.1.0.tar.gz --repo sergiudanstan/mcp-pdf-to-csv
```
