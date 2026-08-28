# GitHub Actions operations

This repository uses separate workflows for unit tests, live integration tests,
package releases, and Firebase Hosting documentation deployments.

The first migration pull request deliberately kept `.circleci/config.yml` and
`tools/trigger_build_system_test.py` so the old and new test paths could be
observed on the same commit. The cutover commit removes both legacy paths and
the local credential-based publishing target before promotion to `staging`;
never restore both publishers on a release branch.

## Workflows

- `Unit tests` runs `make test` on Python 3.8. Its aggregate job always emits
  the stable `Unit tests` check and fails unless the implementation job
  succeeds. Make that exact check required in branch protection for `develop`,
  `staging`, and `master`. Only stale pull-request runs are cancelled. Push and
  reusable invocations never cancel an in-progress unit run. Release callers
  are serialized by the outer release queue; a standalone unit workflow keeps
  GitHub's default single pending slot.
- `Integration tests` runs against a live, dedicated Datalake channel. It is
  serialized across the repository because every test deletes all files in the
  configured channel. Pending runs are queued instead of replacing one another.
  Keep this check non-required until the tests are made isolated and
  deterministic. Forks, Dependabot, manual runs from branches other than
  `develop`, `staging`, and `master`, and reusable callers whose
  `github.repository` is not exactly `abeja-inc/abeja-platform-sdk` are skipped
  before the Environment is accessed.
- `Release` calls both test workflows, builds one wheel, verifies that the
  target system-test workflow is dispatchable, publishes the wheel, and then
  records the verified PyPI file as a public GitHub check run before triggering
  `platform-system-test`. Integration credentials are mandatory in this release
  path. The SDK release identifies the exact target run and waits for a
  successful conclusion; dispatch acceptance alone is not success. A retry
  reconciles both the provenance check and the target run owned by the
  configured dispatch GitHub App, and fails on duplicate or conflicting state.
  On `master`, the successful System Test is followed by the protected Firebase
  production workflow. That workflow verifies that the source is still the
  current `master` head and reconciles the live Hosting release by source SHA,
  documentation digest, and public marker. A final checkout-free job then
  reconciles the immutable tag and GitHub Release through the API. An identical
  existing immutable state is a safe no-op, while a conflicting tag, release,
  dispatch, or provenance identity fails closed. Firebase is intentionally a
  mutable last-write reconciliation boundary, as described below.

Python 3.8 and Poetry 1.8.0 are intentionally fixed for the initial migration.
The current pytest and mypy versions do not support a Python 3.10/3.11 test
matrix. Upgrade the development dependencies before expanding the matrix.

## Event, trust, and side-effect matrix

| Event | Eligible refs / callers | Trust and credentials | Jobs and side effects |
| --- | --- | --- | --- |
| `pull_request` | Targets `develop`, `staging`, or `master` | Unit tests are unprivileged. Integration receives local Environment secrets only for a same-repository, non-Dependabot head. | Stable `Unit tests` gate; optional serialized integration test; no writes. |
| `push` | `develop` for tests and dev documentation; `staging` and `master` for release | Repository branch code. Production assumes that the `master` ruleset admitted only reviewed changes. Integration uses its Environment; OIDC publishing, Checks write, dispatch credentials, and Firebase OIDC remain in separate jobs. | Tests and automatic dev documentation deployment on `develop`; serialized build/publish/provenance/System-Test completion on release branches; on `master` only, Firebase reconciliation followed by tag/release finalization. |
| `workflow_dispatch` | Unit: any ref, no secrets. Integration: only the three named branches. Firebase: dev only on `develop`. | Integration is skipped before Environment access for every other ref. The dev Firebase job receives OIDC only on `develop`; production Firebase has no direct manual entry point. | Manual validation or an explicit dev documentation redeployment; no package publication or production documentation deployment. |
| `workflow_call` | Unit: public reusable workflow. Integration: same repository only, with the original event/ref restrictions still enforced. Production Firebase: only the trusted `Release` caller on `master`. | Integration's repository guard runs before its Environment is evaluated. Release runs Integration directly so that job can select its protected Environment. Firebase's called job rechecks repository, event, ref, and current `master` SHA before using OIDC. | Reusable test jobs, plus production Firebase only after the exact System Test succeeds. |

Release runs share the `abeja-sdk-pypi-release` queue. The queue retains at
most 100 pending runs and does not guarantee dispatch order, so every release
re-reads PyPI and GitHub state after entering the queue. A run also fails if
its source commit is no longer the current head of the release branch, and
staging refuses to create another RC after the matching final version exists
on PyPI. If release volume could exceed that bound, replace it with a durable
external queue.

## Environments and secrets

Create these GitHub Environments before enabling the workflows.

### `firebase-hosting-dev` and `firebase-hosting-production`

The Firebase workflows build the Sphinx documentation under `doc/source` and
deploy `doc/build/html` to two Hosting sites in the shared
`apf-mlops-docs` Firebase project:

| Environment | Eligible branch | Firebase target | Hosting site | Approval |
| --- | --- | --- | --- | --- |
| `firebase-hosting-dev` | `develop` | `sdk-spec-dev` | `apf-mlops-docs-sdk-dev` | Automatic after a push |
| `firebase-hosting-production` | `master` | `sdk-spec-prod` | `apf-mlops-docs-sdk` | Automatic after a reviewed pull request is merged |

Restrict each Environment to its exact branch. Do not add a required
Environment reviewer: review and approval of the pull request into `master` is
the production approval gate, and the documentation deploy starts
automatically from `Release` after merge and after the exact production System
Test succeeds. The production workflow is callable only; it has no independent
`push` or `workflow_dispatch` entry point. Protect `master` with a ruleset that
requires a pull request, at least one approval, resolution of review
conversations, and the stable `Unit tests` check; direct pushes must not bypass
that gate.

Both sites intentionally share the Workload Identity Provider and
`github-deploy@apf-mlops-docs.iam.gserviceaccount.com`. The Google Cloud trust
policy admits this repository as a whole and deliberately does not distinguish
Git refs. Firebase Hosting IAM is also intentionally shared between the dev and
production sites in this one-project, multi-site design. The workflow ref
guards and Environment deployment rules protect the normal deployment paths,
but they are not a separate Google Cloud IAM boundary. Repository write access
is therefore part of the accepted Firebase trust boundary. Splitting service
accounts, refs, sites, or Firebase projects is a separate architecture change,
not a prerequisite for this CI migration.

The jobs request only `contents: read` and `id-token: write`; no Google Cloud
service-account key is stored in GitHub. GitHub's OIDC assertion is exchanged
through Workload Identity Federation for short-lived Google Cloud credentials.
Keep the provider, service account, Firebase project, and deploy targets fixed
unless the repository owner and the Firebase infrastructure owner review the
trust-boundary change together.

The production workflow checks the current `master` head before the protected
job and again immediately before mutation. Together with the documented
production-release `master` freeze, these fences prevent an old Actions run
from moving the mutable site backward. Its Sphinx build uses the commit time as
`SOURCE_DATE_EPOCH`,
hashes the generated file tree, and publishes
`abeja-platform-sdk-release.json` with the source SHA and digest. The same
identity is stored as the Firebase release message. Before and after deployment,
the workflow reads the live channel. A different current release identity is
the normal predecessor and is replaced by the reviewed current-`master`
artifact; it is not treated as an immutable-state conflict. If the release
identity is already the expected one, the workflow skips only when the public
marker also matches and otherwise fails closed. After a deployment it requires
both the live release identity and public marker to match, and it accepts an
ambiguous nonzero CLI exit only when those two external records prove that the
intended release became current. The pre-deployment Firebase Version name is
written to the run summary as the emergency rollback reference. An out-of-band
console or CLI deployment can therefore be overwritten by the next reviewed
SDK production release and must be coordinated with the Hosting owner.

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

The reusable Integration workflow declares no named caller-provided secrets.
Release does not invoke it as a reusable workflow: Release's direct,
same-repository `push` job selects `sdk-integration-test` itself, so the
Environment secrets remain scoped to that job and `secrets: inherit` is not
used. The Integration job-level repository identity guard must remain in place
because this is a public repository: an external repository may call the
workflow, but that job is skipped before `sdk-integration-test` is evaluated.
Manual runs have the same fail-closed branch allowlist. Use required reviewers
and compatible branch/tag deployment rules as a second Environment boundary;
verify the pull-request merge-ref behavior before enabling the workflow.

### `pypi-staging` and `pypi-production`

Do not add a `PYPI_API_TOKEN`. Configure two PyPI Trusted Publishers for the
`abeja-sdk` project, both scoped to this repository and `release.yml`, with
Environment names `pypi-staging` and `pypi-production` respectively. The
publish job grants job-level `contents: read` only to recheck the release ref
and `id-token: write` for Trusted Publishing; it does not check out or execute
repository code. It downloads the already-built wheel, rechecks the filename
and SHA-256 against PyPI on every publish-job attempt, verifies that a new
publication still comes from the current branch head, and invokes a
checksum-verified fixed `uv` version only when the package version is absent.
`uv publish --trusted-publishing always` fails closed unless the PyPI OIDC
exchange succeeds. PEP 740 attestations are intentionally disabled for this
initial migration; add a separately reviewed attestation step before enabling
them.

After either verifying an identical existing wheel or publishing and verifying
a new wheel, a dedicated checkout-free job downloads the build artifact and
re-verifies its embedded package name/version, exact filename, SHA-256, and
non-yanked state against public PyPI. That job has only `checks: write`; the
OIDC-enabled publish job does not receive Checks permission. It then creates a
completed GitHub check run before dispatch. `platform-system-test` reads this
check through the public Checks REST API and compares its wheel digest with
PyPI before accepting the dispatch. Because this SDK repository and its
release evidence are public, the target performs that read without a GitHub
credential. No CI read GitHub App, `CI_APP_CLIENT_ID`, or
`CI_APP_PRIVATE_KEY` is required. The target fails closed if the anonymous API
is unavailable, rate-limited, or returns incomplete evidence. The shared-IP
anonymous rate limit is an accepted operational risk; retry the failed target
run after the rate-limit reset rather than weakening provenance validation.
This public evidence read is separate from the SDK-owned App that dispatches
`platform-system-test`.

The release-provenance contract is exact:

- `name`: `ABEJA SDK release provenance`
- `app.slug`: `github-actions`
- `head_sha`: the 40-character release source SHA
- `external_id`:
  `abeja-sdk-release-provenance:v1:<run-id>:<run-attempt>:<package-version>:<wheel-sha256>`
- `status` / `conclusion`: `completed` / `success`
- `output.title`: `ABEJA SDK release provenance v1`
- `output.summary`: one compact JSON object with lexicographically sorted keys.
  Every value, including the positive run identifiers, is a JSON string:

```json
{"package":"abeja-sdk","package_version":"<package-version>","release_stage":"<staging-or-production>","schema":"abeja-sdk-release-provenance/v1","source_head_sha":"<40-lowercase-hex>","source_repository":"abeja-inc/abeja-platform-sdk","source_run_attempt":"<run-attempt>","source_run_id":"<run-id>","source_workflow":".github/workflows/release.yml","wheel_filename":"<wheel-filename>","wheel_sha256":"<64-lowercase-hex>"}
```

Consumers list all checks with that name for the source SHA using
`GET /repos/abeja-inc/abeja-platform-sdk/commits/<sha>/check-runs`, select the
exact `external_id`, and reject missing, duplicate, or conflicting records.
They must also compare `wheel_filename` and `wheel_sha256` with the PyPI JSON
response and verify the `Publish to PyPI` job in the recorded workflow-run
attempt. `source_run_attempt` is the successful publish job's attempt, preserved
as a job output: rerunning only a failed provenance or dispatch job therefore
reuses the same identical check. Rerunning the publish job records its new
attempt and produces a distinct external ID.

`details_url` is intentionally not an evidence field: GitHub Actions owns and
normalizes it to the Check Run page. Consumers validate the immutable source
run, Check Run identity, canonical summary, publish attempt, and PyPI digest
instead.

Restrict `pypi-staging` to `staging` and `pypi-production` to `master`. Add a
required reviewer to `pypi-production` if the repository's release policy
requires approval. Verify the real OIDC claims and PyPI publisher configuration
before enabling either branch. With GitHub's default subject format the
Environment, rather than the ref, appears in `sub`; the Environment deployment
rules therefore enforce the eligible branch.

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
The post-publication trigger token requests `Actions: Write`. A separate wait
job creates a fresh token downscoped to `Actions: Read` and does not check out
repository code.

| Type | Name | Purpose |
| --- | --- | --- |
| Variable | `SYSTEM_TEST_DISPATCH_APP_CLIENT_ID` | GitHub App client ID |
| Secret | `SYSTEM_TEST_DISPATCH_APP_PRIVATE_KEY` | GitHub App private key |
| Variable (optional) | `SYSTEM_TEST_WORKFLOW` | Target workflow filename; defaults to `system-test.yml` |

`SYSTEM_TEST_WORKFLOW` must be a single safe `.yml` or `.yaml` filename (ASCII
letters, digits, dots, underscores, and hyphens; no path separators). The
readiness job validates it once, verifies the target contract, and exposes the
validated filename as a job output. The dispatch job consumes only that output
and never evaluates the Environment variable again.

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

It must also keep this exact `run-name`, which is the retry-reconciliation key
that the SDK workflow verifies before publishing:

```yaml
run-name: SDK ${{ inputs.sdk_version }} -> ${{ inputs.release_stage }} (source ${{ inputs.source_run_id }})
```

The target must reject a mismatch between `release_stage=staging` and
`deployment/staging`, or `release_stage=production` and
`deployment/production`. Staging accepts only a canonical RC such as
`2.3.6rc1`, while production accepts only a canonical final version such as
`2.3.6`. It must install the exact
`abeja-sdk==<sdk_version>` version, run the existing tests, and perform the
Serverless deployment currently covered by the CircleCI pipeline. PyPI
propagation may take a short time, so installation should use a bounded retry
rather than silently falling back to another SDK version.

For an SDK-triggered staging system test, the final Serverless deployment must
be an ordinary job bound directly to the target repository's `stg` Environment.
Do not put that Environment behind a reusable-workflow call or use
`secrets: inherit`: Environment-scoped credentials must remain available only
to the final, protected deployment job. That job must still keep the validated
bot/ref/provenance inputs, OIDC account binding, freshness verification, and
the same deployment-concurrency group as the ordinary staging deployment.

When that final job invokes a repository-local composite action, it must check
out the verified `deployment/staging` revision first with
`persist-credentials: false`; keep that checkout outside the composite action.

The SDK build also validates this version shape before publication: a
`staging` release must be canonical `X.Y.ZrcN`, while a `master` release must
be canonical `X.Y.Z`. The target readiness check verifies the exact six-input
contract on both the default branch and selected deployment ref before the
PyPI job can start. On the selected ref it also verifies the stage-specific
prepare, codetest, and terminal deployment jobs, including their Environment,
dependencies, permissions, ownership guard, concurrency, and checkout boundary.
The selected ref is resolved to a commit SHA. The dispatch is rejected if the
ref advances before the API call. If it moves in the remaining API race and the
created run does not use the exact inspected SHA, the SDK release fails closed,
requests cancellation of that run, and requires target-repository investigation.

Use stage-specific GitHub Environments, OIDC permissions (`contents: read` and
`id-token: write`), AWS role trust and variables/secrets, and stage-specific
concurrency in the target repository. Include `source_run_url` in the target
run summary so a failed system test can be traced back to the SDK release.

Do not enable SDK release branches until the target workflow and GitHub App
have been manually verified for both stages. If dispatch fails after PyPI has
accepted a package, fix the target configuration and use **Re-run failed jobs**
for the dispatch job only; never rerun the successful publish job. The dispatch
job automatically searches the target by `source_run_id`, `sdk_version`, and
`release_stage`, skips one exact prior dispatch, and fails if duplicate matches
already exist.

After registration, the dispatch API returns the exact target run ID and URLs;
the SDK does not guess which run was created from list timing. Because a newly
created run record can be temporarily incomplete, the trigger re-reads that
exact ID for a bounded period before accepting it or treating a persistent
identity mismatch as a conflict. The SDK wait job then repeatedly reads that
exact run ID. It verifies the workflow path, deployment ref
and inspected SHA, App bot identity, display title, event type, and URL on every
read. A successful overall run is still insufficient by itself: the waiter also
requires the exact stage-specific terminal deployment job to be
`completed` / `success`. A failed, cancelled, timed-out, stale, skipped-terminal,
or conflicting run fails the SDK workflow; queued or in-progress runs are
bounded to 50 minutes so the short-lived App token cannot expire silently.

For any failure after a package may have reached PyPI, use **Re-run failed
jobs**, not **Re-run all jobs**. A full staging rerun recalculates the next RC
from PyPI and can intentionally produce a new version. On a failed publish-job
retry, the workflow compares the downloaded artifact's filename and SHA-256
with PyPI. It skips the upload only when they match exactly and fails closed on
any mismatch or yanked wheel. The build artifact is retained for 31 days,
covering GitHub's 30-day workflow rerun window.

The target rejects new human dispatches and accepts only the configured SDK
GitHub App bot. If the target dispatch was never accepted, rerun the failed SDK
workflow jobs so that the App-authenticated dispatch and provenance checks are
reused. If the linked target run exists but fails, first rerun that target run's
failed jobs and then rerun the SDK workflow's failed jobs. The SDK trigger and
waiter both reuse the same run ID. Do not manually create a new target dispatch,
production tag, or GitHub Release. If the rerun window has closed, or if the
PyPI version is missing, yanked, or has a different digest, stop and escalate
to the release owners for a separately reviewed recovery; use a new package
version rather than dispatching or tagging unverified evidence.

If the failure is caused by the workflow definition itself, a GitHub rerun
still uses that original definition. Merge and validate the repair through the
normal release path; do not mutate historical provenance evidence to force a
retry.

## Production failure and rollback boundary

PyPI files, release evidence, tags, and published GitHub Releases are immutable
history in this process. "Rollback" therefore means preserving that history,
restoring mutable service state when necessary, and shipping a corrected new
version. It never means deleting and reusing a package version.

| Failure point | State and permitted recovery |
| --- | --- |
| Before PyPI publication | No public package exists. Repair the cause and rerun through the normal reviewed branch path. |
| PyPI published; System Test not successful | Do not create a tag or GitHub Release. First determine whether the stage-specific terminal deployment job started. If it never started and the failure is transient, rerun the exact target run's failed jobs and then the SDK failed jobs. If deployment started or its state is uncertain, freeze promotion and, in a `platform-system-test` change window, inspect and stabilize CloudFormation before deciding whether a rerun is safe: `serverless deploy` can partially mutate service state before a later ledger check fails. For an artifact defect, record the reason, request a PyPI yank, and use a new staging RC or a new production patch version. |
| System Test successful; Firebase not reconciled | The package and platform test evidence remain valid, **and the production platform stack has already been deployed** by the terminal System Test job, but production finalization is blocked. Rerun only the failed Firebase/caller job while `master` still identifies the same SHA. If service state needs recovery, freeze promotion and use the owning service's reviewed incident/change procedure to inspect and stabilize it; never dispatch an older SDK as rollback. Use the Version name recorded in the job summary only for an explicitly approved emergency Hosting rollback. |
| Tag and GitHub Release created | Do not move/delete the tag or rewrite release metadata to hide a defect. Request a reasoned PyPI yank if appropriate, restore mutable service state under the owning system's incident runbook, and release a new patch version. |

A PyPI yank is non-destructive and exact `==` pins can still select a yanked
file, so it is a warning and resolver control rather than erasure. Package files
and filenames cannot be reused after deletion. Never delete a release in order
to republish the same version, never dispatch an older SDK as an automatic
rollback, and never bypass the target freshness guard. Infrastructure rollback
and stabilization belong to the owning service's reviewed incident procedure;
Firebase rollback belongs to the Hosting owner and must use the recorded prior
Version. The rollback section of the `platform-system-test` migration runbook
only transfers **CI deployment ownership** back to CircleCI in the order
"disable GitHub Actions ownership, drain its runs, stabilize CloudFormation,
then restore CircleCI." It is not an application rollback or an older-SDK
rollback procedure.
See PyPI's [yanking guidance](https://docs.pypi.org/project-management/yanking/)
and [file-name reuse policy](https://pypi.org/help/#file-name-reuse) before an
incident operator changes public package state.

Production System Test ownership is an external precondition, not something the
SDK workflow can switch safely. Before merging a `staging` to `master` release,
follow the target runbook's exact order: prepare and review the CircleCI change;
remove only the production deployment filter; freeze the deployment ref and
legacy SDK trigger; block new CircleCI production work; drain every active
production deployment; read the CircleCI config from the actual triggering ref
and prove that no new production `build` can start; only then set
`DEPLOYMENT_OWNER_PROD=github-actions`. If any check fails, keep the SDK
production PR draft and use the target repository's rollback sequence to
restore CircleCI ownership.

After merging the production release PR, keep SDK `master` frozen until the
same workflow has verified System Test and Firebase and has created the tag and
GitHub Release. Firebase re-reads the current `master` head before mutation, and
the finalizer does so before creating a previously absent tag. If the ref
advances before either boundary, the stale release deliberately stops; do not
force-rerun it, and stop for a separately reviewed recovery and version
decision. If the exact tag was already created before a transient GitHub
Release failure, **Re-run failed jobs** may finish reconciling that same tag;
never delete or move the tag to manufacture a retry.

## Migration and decommission checklist

1. Add the four Environments, their required secrets/variables and deployment
   rules, and the two PyPI Trusted Publisher records. Do not retain a PyPI API
   token.
2. Add the complete target receiver (`system-test.yml`, its reusable workflows,
   helpers, packaging Dockerfile and constraints, `serverless.yml` changes,
   and tests) to `master` and both deployment branches, then manually verify
   both deployment refs.
3. Keep the CircleCI configuration in the first `develop` pull request. Run
   both the old `ci/circleci: codetest` and new `Unit tests` on the same head
   commit, configure `sdk-integration-test`, and observe `Integration tests`.
4. After the exact new `Unit tests` status succeeds, replace the CircleCI
   required check with that stable check. Do not make `Integration tests`
   required yet.
5. Merge the parallel migration to `develop`, verify both push paths, and
   observe the agreed stability period.
6. In the cutover commit on `develop`, remove the CircleCI config, the
   system-test trigger helper, and the `TWINE_USERNAME`/`TWINE_PASSWORD`
   publishing target. Confirm those legacy paths remain absent before opening
   the `develop` to `staging` pull request. Do not promote a commit containing
   both publishers to `staging`.
7. Immediately before the first `staging` promotion, use CircleCI's reversible
   block on new work if the project can still start pipelines, then drain
   running jobs. Keep the ability to unblock for rollback.
8. Merge the cutover to `staging`; verify the RC digest on PyPI and successful
   completion of the uniquely identified system-test run.
9. Before the production merge, prepare and review the CircleCI change; remove
   only its production deployment filter; freeze the deployment ref and legacy
   SDK trigger; block new CircleCI production work; drain active deployments;
   read the config from the actual triggering ref and prove no new production
   `build` can start; then set `DEPLOYMENT_OWNER_PROD=github-actions` under the
   reviewed change window.
10. Merge to `master`; verify the final PyPI digest, exact successful System Test,
   reconciled Firebase source/digest marker, and the release workflow's tag and
   GitHub Release. Do not merge another SDK change to `master` until this
   finalization completes.
11. Only after production succeeds, permanently stop the CircleCI project and
    remove its old variables, contexts, and credentials.
