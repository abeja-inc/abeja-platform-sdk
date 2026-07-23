# GitHub Actions operations

This repository uses separate workflows for unit tests, live integration tests,
and package releases.

## Workflows

- `Unit tests` runs `make test` on Python 3.8. Make the stable `Unit tests`
  check required in branch protection for `develop`, `staging`, and `master`.
- `Integration tests` runs against a live, dedicated Datalake channel. It is
  serialized across the repository because every test deletes all files in the
  configured channel. Pending runs are queued instead of replacing one another.
  Keep this check non-required until the tests are made isolated and
  deterministic.
- `Release` calls both test workflows, builds one wheel, verifies that the
  target system-test workflow is dispatchable, publishes the wheel, and then
  triggers `platform-system-test`. Integration credentials are
  mandatory in this release path. A successful release means that the target
  accepted the dispatch; it does not wait for the target run to finish.
- `Auto Tag on Release` creates the production tag and GitHub Release only
  after the complete `Release` workflow succeeds on `master`.

Python 3.8 and Poetry 1.8.0 are intentionally fixed for the initial migration.
The current pytest and mypy versions do not support a Python 3.10/3.11 test
matrix. Upgrade the development dependencies before expanding the matrix.

## Environments and secrets

Create these GitHub Environments before enabling the workflows.

### `sdk-integration-test`

Use a Datalake channel dedicated to this repository. Do not share the channel
with another test runner. Use a dedicated, least-privilege test account and
token because trusted pull-request code receives these credentials. Direct
workflow runs fail if any credential is missing; fork and Dependabot pull
requests skip the integration job before the Environment is accessed.

| Secret | Purpose |
| --- | --- |
| `CHANNEL_ID` | Dedicated Datalake channel |
| `ORGANIZATION_ID` | ABEJA Platform organization |
| `USER_ID` | ABEJA Platform user |
| `PERSONAL_ACCESS_TOKEN` | ABEJA Platform personal access token |

### `pypi-staging` and `pypi-production`

| Secret | Purpose |
| --- | --- |
| `PYPI_API_TOKEN` | Project-scoped token for `abeja-sdk` |

Restrict `pypi-staging` to `staging` and `pypi-production` to `master`. Add a
required reviewer to `pypi-production` if the repository's release policy
requires approval. Release runs share one FIFO concurrency queue so that RC
numbering and PyPI publication cannot overlap or silently replace a pending
release.

### `system-test-dispatch`

Install a GitHub App only on `abeja-inc/platform-system-test` and grant it
`Actions: Read and write` and `Contents: Read-only`. The SDK workflow creates a
short-lived installation token scoped to that repository. Its preflight job
blocks PyPI publication if the App cannot read or dispatch the target workflow.
Restrict this Environment's deployment branches to selected branches
`staging` and `master`, and protect both branches. No pull request or arbitrary
branch may obtain the App private key. The readiness token is downscoped to
`Actions: Read` and `Contents: Read`. A second token creation checks
`Actions: Write` before publication without passing that token to a shell step.
The post-publication trigger token also requests `Actions: Write`.

| Type | Name | Purpose |
| --- | --- | --- |
| Variable | `SYSTEM_TEST_DISPATCH_APP_CLIENT_ID` | GitHub App client ID |
| Secret | `SYSTEM_TEST_DISPATCH_APP_PRIVATE_KEY` | GitHub App private key |
| Variable (optional) | `SYSTEM_TEST_WORKFLOW` | Target workflow filename; defaults to `system-test.yml` |

The same target workflow filename must exist on the target repository's default
branch (`master`) so GitHub registers the `workflow_dispatch` event, and on
`deployment/staging` and `deployment/production` so each release can run the
workflow at its deployment ref. It must declare exactly the six inputs below,
each as `type: string` and `required: true`:

- `sdk_version`
- `release_stage`
- `sdk_sha`
- `source_repository`
- `source_run_id`
- `source_run_url`

The target must reject a mismatch between `release_stage=staging` and
`deployment/staging`, or `release_stage=production` and
`deployment/production`. Staging accepts only a canonical RC such as
`2.3.6rc1`, while production accepts only a canonical final version such as
`2.3.6`. It must install the exact
`abeja-sdk==<sdk_version>` version, run the existing tests, and perform the
Serverless deployment currently covered by the CircleCI pipeline. PyPI
propagation may take a short time, so installation should use a bounded retry
rather than silently falling back to another SDK version.

The SDK build also validates this version shape before publication: a
`staging` release must be canonical `X.Y.ZrcN`, while a `master` release must
be canonical `X.Y.Z`. The target readiness check verifies the exact six-input
contract on both the default branch and selected deployment ref before the
PyPI job can start.

Use stage-specific GitHub Environments, OIDC permissions (`contents: read` and
`id-token: write`), AWS role trust and variables/secrets, and stage-specific
concurrency in the target repository. Include `source_run_url` in the target
run summary so a failed system test can be traced back to the SDK release.

Do not enable SDK release branches until the target workflow and GitHub App
have been manually verified for both stages. If dispatch fails after PyPI has
accepted a package, fix the target configuration and use **Re-run failed jobs**
for the dispatch job only; never rerun the successful publish job. Before
retrying, search target runs for the `source_run_id` to avoid a duplicate
dispatch.

For any failure after a package may have reached PyPI, use **Re-run failed
jobs**, not **Re-run all jobs**. A full staging rerun recalculates the next RC
from PyPI and can intentionally produce a new version. On a failed publish-job
retry, the workflow compares the downloaded artifact's filename and SHA-256
with PyPI. It skips the upload only when they match exactly and fails closed on
any mismatch or yanked wheel. The build artifact is retained for seven days;
after that window, compare the PyPI digest with the version, filename, source
SHA, and wheel SHA-256 recorded in the build job summary.

For an exact staging match, manually dispatch the target with the recorded RC
version and source identifiers; do not create a tag or GitHub Release. For an
exact production match, manually dispatch the target, then create the missing
tag at the recorded source SHA and the matching GitHub Release. Never move an
existing tag. If the PyPI version is missing, yanked, or has a different digest,
stop recovery and investigate; use a new package version rather than dispatching
or tagging an unverified artifact.

## Migration and decommission checklist

1. Add the four Environments and their secrets/variables.
2. Add the complete target receiver (`system-test.yml`, its reusable workflows,
   helpers, packaging Dockerfile and constraints, `serverless.yml` changes,
   and tests) to `master` and both deployment branches, then manually verify
   both deployment refs.
3. Run `Unit tests` and `Integration tests` on a pull request.
4. As soon as the migration pull request has produced the new `Unit tests`
   status, replace every CircleCI required check with that stable check before
   merging the CircleCI-config deletion. Do not make `Integration tests`
   required yet.
5. Merge the migration to `develop` and verify its push workflows. The release
   workflow has no dry-run mode: the first subsequent merge to `staging` is the
   live RC cutover, so do not perform it until the Environments, App, target
   receiver, and recovery procedure above have all been verified.
6. Merge to `staging`; verify the RC on PyPI and the dispatched system-test run.
7. Merge to `master`; verify the final PyPI version, system-test run, tag, and
   GitHub Release.
8. Remove the old CircleCI project variables and stop the CircleCI project.
