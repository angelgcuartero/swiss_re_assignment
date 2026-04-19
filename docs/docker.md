# Docker related tasks

## How to build the Docker image

Make sure you have Docker installed on your machine: Follow the Docker installation instructions for your OS: <https://docs.astral.sh/uv/getting-started/installation/>

Run the builder script:

```shell
build_tools/build_docker.sh
```

A Docker image will be created and tagged with the name and version included in `pyproject.toml`.

## Checking vulneravilities in the Docker image

Trivy can check the vulnerabilies of the Docker image built with the project.

> **Note**: The Docker Unix socket `/var/run/docker.sock` needs to be mounted to run properly, at least in ARM64 architectures. This may not be needed in AMD64. This is a potential dangerous point as it provides root privileges on the host.

```console
$ docker run -v /var/run/docker.sock:/var/run/docker.sock aquasec/trivy image --severity CRITICAL,HIGH,UNKNOWN swiss-re-assignment:0.1.0
2026-04-17T15:33:23Z    INFO    [vulndb] Need to update DB
2026-04-17T15:33:23Z    INFO    [vulndb] Downloading vulnerability DB...
2026-04-17T15:33:23Z    INFO    [vulndb] Downloading artifact...
repo="mirror.gcr.io/aquasec/trivy-db:2" 3.80 MiB / 90.40 MiB
[-->____________________________________________] 4.20% ? p/s ?21.06 MiB / 90.40 MiB
[-------------->________________________________] 23.29% ? p/s ?38.88 MiB / 90.40 MiB
[-------------------------->____________________] 43.00% ? p/s ?56.97 MiB / 90.40 MiB
[------------------------------>________________] 63.02% 88.37 MiB p/s ETA 0s74.95 MiB / 90.40 MiB
[--------------------------------------->_______] 82.91% 88.37 MiB p/s ETA 0s90.40 MiB / 90.40 MiB
[---------------------------------------------->] 100.00% 88.37 MiB p/s ETA 0s90.40 MiB / 90.40 MiB
[---------------------------------------------->] 100.00% 86.24 MiB p/s ETA 0s90.40 MiB / 90.40 MiB
[---------------------------------------------->] 100.00% 86.24 MiB p/s ETA 0s90.40 MiB / 90.40 MiB
[---------------------------------------------->] 100.00% 86.24 MiB p/s ETA 0s90.40 MiB / 90.40 MiB
[---------------------------------------------->] 100.00% 80.68 MiB p/s ETA 0s90.40 MiB / 90.40 MiB
[---------------------------------------------->] 100.00% 80.68 MiB p/s ETA 0s90.40 MiB / 90.40 MiB
[---------------------------------------------->] 100.00% 80.68 MiB p/s ETA 0s90.40 MiB / 90.40 MiB
[---------------------------------------------->] 100.00% 75.47 MiB p/s ETA 0s90.40 MiB / 90.40 MiB 
[---------------------------------------------->] 100.00% 75.47 MiB p/s ETA 0s90.40 MiB / 90.40 MiB 
[---------------------------------------------->] 100.00% 75.47 MiB p/s ETA 0s90.40 MiB / 90.40 MiB 
[---------------------------------------------->] 100.00% 70.60 MiB p/s ETA 0s90.40 MiB / 90.40 MiB 
[-----------------------------------------------] 100.00% 29.71 MiB p/s 3.2s
2026-04-17T15:33:27Z    INFO    [vulndb] Artifact successfully downloaded     repo="mirror.gcr.io/aquasec/trivy-db:2"
2026-04-17T15:33:27Z    INFO    [vuln] Vulnerability scanning is enabled
2026-04-17T15:33:27Z    INFO    [secret] Secret scanning is enabled
2026-04-17T15:33:27Z    INFO    [secret] If your scanning is slow, please try '--scanners vuln' to disable secret scanning
2026-04-17T15:33:27Z    INFO    [secret] Please see https://trivy.dev/docs/v0.70/guide/scanner/secret#recommendation for faster secret detection
2026-04-17T15:33:28Z    INFO    [python] Licenses acquired from one or more METADATA files may be subject to additional terms. Use `--debug` flag to see all affected packages.
2026-04-17T15:33:28Z    INFO    Detected OS     family="alpine" version="3.23.4"
2026-04-17T15:33:28Z    INFO    [alpine] Detecting vulnerabilities...   os_version="3.23" repository="3.23" pkg_num=44
2026-04-17T15:33:28Z    INFO    Number of language-specific files       num=3
2026-04-17T15:33:28Z    INFO    [python-pkg] Detecting vulnerabilities...
2026-04-17T15:33:28Z    INFO    [rustbinary] Detecting vulnerabilities...

Report Summary

┌──────────────────────────────────────────────────────────────────────────────────┬────────────┬─────────────────┬─────────┐
│                                      Target                                      │    Type    │ Vulnerabilities │ Secrets │
├──────────────────────────────────────────────────────────────────────────────────┼────────────┼─────────────────┼─────────┤
│ swiss-re-assignment:0.1.0 (alpine 3.23.4)                                        │   alpine   │        0        │    -    │
├──────────────────────────────────────────────────────────────────────────────────┼────────────┼─────────────────┼─────────┤
│ app/.venv/lib/python3.12/site-packages/annotated_doc-0.0.4.dist-info/METADATA    │ python-pkg │        0        │    -    │
├──────────────────────────────────────────────────────────────────────────────────┼────────────┼─────────────────┼─────────┤
│ app/.venv/lib/python3.12/site-packages/click-8.3.2.dist-info/METADATA            │ python-pkg │        0        │    -    │
├──────────────────────────────────────────────────────────────────────────────────┼────────────┼─────────────────┼─────────┤
│ app/.venv/lib/python3.12/site-packages/logging-0.4.9.6.dist-info/METADATA        │ python-pkg │        0        │    -    │
├──────────────────────────────────────────────────────────────────────────────────┼────────────┼─────────────────┼─────────┤
│ app/.venv/lib/python3.12/site-packages/markdown_it_py-4.0.0.dist-info/METADATA   │ python-pkg │        0        │    -    │
├──────────────────────────────────────────────────────────────────────────────────┼────────────┼─────────────────┼─────────┤
│ app/.venv/lib/python3.12/site-packages/mdurl-0.1.2.dist-info/METADATA            │ python-pkg │        0        │    -    │
├──────────────────────────────────────────────────────────────────────────────────┼────────────┼─────────────────┼─────────┤
│ app/.venv/lib/python3.12/site-packages/pygments-2.20.0.dist-info/METADATA        │ python-pkg │        0        │    -    │
├──────────────────────────────────────────────────────────────────────────────────┼────────────┼─────────────────┼─────────┤
│ app/.venv/lib/python3.12/site-packages/rich-15.0.0.dist-info/METADATA            │ python-pkg │        0        │    -    │
├──────────────────────────────────────────────────────────────────────────────────┼────────────┼─────────────────┼─────────┤
│ app/.venv/lib/python3.12/site-packages/shellingham-1.5.4.dist-info/METADATA      │ python-pkg │        0        │    -    │
├──────────────────────────────────────────────────────────────────────────────────┼────────────┼─────────────────┼─────────┤
│ app/.venv/lib/python3.12/site-packages/swiss_re_assignment-0.1.0.dist-info/META- │ python-pkg │        0        │    -    │
│ DATA                                                                             │            │                 │         │
├──────────────────────────────────────────────────────────────────────────────────┼────────────┼─────────────────┼─────────┤
│ app/.venv/lib/python3.12/site-packages/typer-0.24.1.dist-info/METADATA           │ python-pkg │        0        │    -    │
├──────────────────────────────────────────────────────────────────────────────────┼────────────┼─────────────────┼─────────┤
│ app/swiss_re_assignment.egg-info/PKG-INFO                                        │ python-pkg │        0        │    -    │
├──────────────────────────────────────────────────────────────────────────────────┼────────────┼─────────────────┼─────────┤
│ root/.cache/uv/archive-v0/CWwiKooE6Y8FyTRv4aoiI/setuptools-82.0.1.dist-info/MET- │ python-pkg │        0        │    -    │
│ ADATA                                                                            │            │                 │         │
├──────────────────────────────────────────────────────────────────────────────────┼────────────┼─────────────────┼─────────┤
│ root/.cache/uv/archive-v0/CWwiKooE6Y8FyTRv4aoiI/setuptools/_vendor/autocommand-- │ python-pkg │        0        │    -    │
│ 2.2.2.dist-info/METADATA                                                         │            │                 │         │
├──────────────────────────────────────────────────────────────────────────────────┼────────────┼─────────────────┼─────────┤
│ root/.cache/uv/archive-v0/CWwiKooE6Y8FyTRv4aoiI/setuptools/_vendor/backports.ta- │ python-pkg │        0        │    -    │
│ rfile-1.2.0.dist-info/METADATA                                                   │            │                 │         │
├──────────────────────────────────────────────────────────────────────────────────┼────────────┼─────────────────┼─────────┤
│ root/.cache/uv/archive-v0/CWwiKooE6Y8FyTRv4aoiI/setuptools/_vendor/importlib_me- │ python-pkg │        0        │    -    │
│ tadata-8.7.1.dist-info/METADATA                                                  │            │                 │         │
├──────────────────────────────────────────────────────────────────────────────────┼────────────┼─────────────────┼─────────┤
│ root/.cache/uv/archive-v0/CWwiKooE6Y8FyTRv4aoiI/setuptools/_vendor/jaraco.text-- │ python-pkg │        0        │    -    │
│ 4.0.0.dist-info/METADATA                                                         │            │                 │         │
├──────────────────────────────────────────────────────────────────────────────────┼────────────┼─────────────────┼─────────┤
│ root/.cache/uv/archive-v0/CWwiKooE6Y8FyTRv4aoiI/setuptools/_vendor/jaraco_conte- │ python-pkg │        0        │    -    │
│ xt-6.1.0.dist-info/METADATA                                                      │            │                 │         │
├──────────────────────────────────────────────────────────────────────────────────┼────────────┼─────────────────┼─────────┤
│ root/.cache/uv/archive-v0/CWwiKooE6Y8FyTRv4aoiI/setuptools/_vendor/jaraco_funct- │ python-pkg │        0        │    -    │
│ ools-4.4.0.dist-info/METADATA                                                    │            │                 │         │
├──────────────────────────────────────────────────────────────────────────────────┼────────────┼─────────────────┼─────────┤
│ root/.cache/uv/archive-v0/CWwiKooE6Y8FyTRv4aoiI/setuptools/_vendor/more_itertoo- │ python-pkg │        0        │    -    │
│ ls-10.8.0.dist-info/METADATA                                                     │            │                 │         │
├──────────────────────────────────────────────────────────────────────────────────┼────────────┼─────────────────┼─────────┤
│ root/.cache/uv/archive-v0/CWwiKooE6Y8FyTRv4aoiI/setuptools/_vendor/packaging-26- │ python-pkg │        0        │    -    │
│ .0.dist-info/METADATA                                                            │            │                 │         │
├──────────────────────────────────────────────────────────────────────────────────┼────────────┼─────────────────┼─────────┤
│ root/.cache/uv/archive-v0/CWwiKooE6Y8FyTRv4aoiI/setuptools/_vendor/platformdirs- │ python-pkg │        0        │    -    │
│ -4.4.0.dist-info/METADATA                                                        │            │                 │         │
├──────────────────────────────────────────────────────────────────────────────────┼────────────┼─────────────────┼─────────┤
│ root/.cache/uv/archive-v0/CWwiKooE6Y8FyTRv4aoiI/setuptools/_vendor/tomli-2.4.0.- │ python-pkg │        0        │    -    │
│ dist-info/METADATA                                                               │            │                 │         │
├──────────────────────────────────────────────────────────────────────────────────┼────────────┼─────────────────┼─────────┤
│ root/.cache/uv/archive-v0/CWwiKooE6Y8FyTRv4aoiI/setuptools/_vendor/wheel-0.46.3- │ python-pkg │        0        │    -    │
│ .dist-info/METADATA                                                              │            │                 │         │
├──────────────────────────────────────────────────────────────────────────────────┼────────────┼─────────────────┼─────────┤
│ root/.cache/uv/archive-v0/CWwiKooE6Y8FyTRv4aoiI/setuptools/_vendor/zipp-3.23.0.- │ python-pkg │        0        │    -    │
│ dist-info/METADATA                                                               │            │                 │         │
├──────────────────────────────────────────────────────────────────────────────────┼────────────┼─────────────────┼─────────┤
│ root/.cache/uv/sdists-v9/pypi/logging/0.4.9.6/nx2IG2qreAvZdfLpz62RZ/src/logging- │ python-pkg │        0        │    -    │
│ .egg-info/PKG-INFO                                                               │            │                 │         │
├──────────────────────────────────────────────────────────────────────────────────┼────────────┼─────────────────┼─────────┤
│ usr/local/lib/python3.12/site-packages/pip-25.0.1.dist-info/METADATA             │ python-pkg │        0        │    -    │
├──────────────────────────────────────────────────────────────────────────────────┼────────────┼─────────────────┼─────────┤
│ bin/uv                                                                           │ rustbinary │        0        │    -    │
├──────────────────────────────────────────────────────────────────────────────────┼────────────┼─────────────────┼─────────┤
│ bin/uvx                                                                          │ rustbinary │        0        │    -    │
└──────────────────────────────────────────────────────────────────────────────────┴────────────┴─────────────────┴─────────┘
Legend:
- '-': Not scanned
- '0': Clean (no security findings detected)
```

## How to run with Docker

This is an example of a typical Docker execution with parameters and options:

```shell
docker run -it -v $(pwd):/app -e swiss-re-assignment:0.1.0 tests/resources tests/output --lfip --mfip --bytes --eps
```

It is important to mount the current working directory over the `/app` folder in the container or it will not be able to read the parameter paths.
