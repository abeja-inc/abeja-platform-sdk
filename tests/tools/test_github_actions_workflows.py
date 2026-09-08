import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
WORKFLOWS = ROOT / ".github" / "workflows"


def get_step_run(workflow, step_name):
    lines = workflow.splitlines()
    step_index = lines.index(f"      - name: {step_name}")
    run_index = next(
        index
        for index in range(step_index + 1, len(lines))
        if lines[index].startswith("        run: |")
    )
    run_indent = len(lines[run_index]) - len(lines[run_index].lstrip())
    block_indent = run_indent + 2
    block = []
    for line in lines[run_index + 1:]:
        indentation = len(line) - len(line.lstrip()) if line else block_indent
        if line and indentation <= run_indent:
            break
        block.append(line[block_indent:] if line else "")
    return "\n".join(block).rstrip()


def test_release_and_live_integration_runs_are_queued():
    release = (WORKFLOWS / "release.yml").read_text()
    integration = (WORKFLOWS / "integration-test.yml").read_text()

    assert "group: abeja-sdk-pypi-release\n  queue: max" in release
    assert (
        "group: abeja-platform-sdk-datalake-integration\n"
        "      queue: max"
    ) in integration
    assert "cancel-in-progress: false" not in release
    assert "cancel-in-progress: false" not in integration


def test_circleci_and_long_lived_pypi_credentials_stay_removed():
    makefile = (ROOT / "Makefile").read_text()

    assert not (ROOT / ".circleci" / "config.yml").exists()
    assert not (ROOT / "tools" / "trigger_build_system_test.py").exists()
    assert "TWINE_USERNAME" not in makefile
    assert "TWINE_PASSWORD" not in makefile
    assert "poetry publish" not in makefile


def test_migrated_external_actions_are_commit_pinned():
    migrated_workflows = (
        "integration-test.yml",
        "release.yml",
        "test.yml",
    )
    workflows = "\n".join(
        (WORKFLOWS / name).read_text() for name in migrated_workflows
    )
    external_actions = {
        (match.group(1), match.group(2))
        for match in re.finditer(
            r"^\s*uses:\s*([^.\s]\S*?)\s+#\s+(\S+)\s*$",
            workflows,
            flags=re.MULTILINE,
        )
    }
    expected_checkout = (
        "actions/checkout@"
        "d23441a48e516b6c34aea4fa41551a30e30af803"
    )

    assert external_actions == {
        (expected_checkout, "v6.1.0"),
        (
            (
                "actions/setup-python@"
                "ece7cb06caefa5fff74198d8649806c4678c61a1"
            ),
            "v6.3.0",
        ),
        (
            (
                "actions/upload-artifact@"
                "043fb46d1a93c77aae656e7c1c64a875d1fc6a0a"
            ),
            "v7.0.1",
        ),
        (
            (
                "actions/create-github-app-token@"
                "bcd2ba49218906704ab6c1aa796996da409d3eb1"
            ),
            "v3.2.0",
        ),
        (
            (
                "actions/download-artifact@"
                "3e5f45b2cfb9172054b4087a40e8e0b5a5461e7c"
            ),
            "v8.0.1",
        ),
        (
            (
                "astral-sh/setup-uv@"
                "08807647e7069bb48b6ef5acd8ec9567f424441b"
            ),
            "v8.1.0",
        ),
    }
    # Release runs Integration as an Environment-bound job, so it has its own
    # checkout in addition to the reusable integration workflow's checkout.
    assert workflows.count(expected_checkout) == len(migrated_workflows) + 1
    assert workflows.count("persist-credentials: false") == len(
        migrated_workflows
    ) + 1


def test_unit_workflow_has_noncolliding_stale_cancellation_and_stable_gate():
    unit = (WORKFLOWS / "test.yml").read_text()
    required = unit.split("  required:", 1)[1]

    assert (
        "group: abeja-platform-sdk-unit-tests-"
        "${{ github.event.pull_request.number || github.ref }}"
    ) in unit
    assert (
        "cancel-in-progress: "
        "${{ github.event_name == 'pull_request' }}"
    ) in unit
    assert "name: Unit tests" in required
    assert "if: ${{ always() }}" in required
    assert "needs: unit-tests" in required
    assert 'run: test "$UNIT_TESTS_RESULT" = "success"' in required
    assert "permissions: {}" in required


def test_poetry_runtime_stays_compatible_with_python_38():
    for name in ("integration-test.yml", "test.yml"):
        workflow = (WORKFLOWS / name).read_text()
        install_poetry = get_step_run(workflow, "Install Poetry")

        assert 'POETRY_PACKAGING_VERSION: "26.2"' in workflow
        assert (
            'pipx runpip poetry install '
            '"packaging==${POETRY_PACKAGING_VERSION}"'
        ) in install_poetry


def test_integration_secrets_fail_closed_for_manual_external_and_release_callers():
    integration = (WORKFLOWS / "integration-test.yml").read_text()
    release = (WORKFLOWS / "release.yml").read_text()
    integration_job = integration.split("  integration-tests:", 1)[1]
    release_integration_job = release.split("  integration-tests:", 1)[1].split(
        "  build:", 1
    )[0]

    assert "workflow_call:" in integration
    assert (
        "github.repository == 'abeja-inc/abeja-platform-sdk'"
        in integration_job
    )
    assert "github.event_name == 'workflow_dispatch'" in integration_job
    for branch in ("develop", "staging", "master"):
        assert f"github.ref == 'refs/heads/{branch}'" in integration_job
    assert (
        "github.event.pull_request.head.repo.full_name == github.repository"
        in integration_job
    )
    assert "github.actor != 'dependabot[bot]'" in integration_job
    assert "environment: sdk-integration-test" in integration_job
    assert "secrets: inherit" not in integration
    assert not any(
        line.strip() == "secrets: inherit" for line in release.splitlines()
    )
    assert "uses: ./.github/workflows/integration-test.yml" not in release_integration_job
    assert "github.event_name == 'push'" in release_integration_job
    assert "github.ref == 'refs/heads/staging'" in release_integration_job
    assert "github.ref == 'refs/heads/master'" in release_integration_job
    assert "environment: sdk-integration-test" in release_integration_job
    assert 'POETRY_VERSION: "1.8.0"' in release_integration_job
    assert 'POETRY_PACKAGING_VERSION: "26.2"' in release_integration_job
    for secret in (
        "CHANNEL_ID",
        "ORGANIZATION_ID",
        "USER_ID",
        "PERSONAL_ACCESS_TOKEN",
    ):
        assert f"{secret}: ${{{{ secrets.{secret} }}}}" in release_integration_job


def test_release_validates_version_and_exact_target_contract_before_publish():
    release = (WORKFLOWS / "release.yml").read_text()
    readiness = release.split("  system-test-readiness:", 1)[1].split(
        "  publish:", 1
    )[0]

    assert "tools/validate_release_version.py" in release
    assert "inputs.keys.map(&:to_s) - required_inputs" in readiness
    assert "set -Eeuo pipefail" in readiness
    assert 'document["run-name"] == expected_run_name' in readiness
    assert (
        r"^[A-Za-z0-9][A-Za-z0-9._-]*\.ya?ml$"
        in readiness
    )
    for contract_value in (
        "prepare-stg-sdk-deploy",
        "codetest-stg",
        "deploy-stg-sdk-release",
        "deploy staging SDK release",
        '"environment" => "stg"',
        "DEPLOYMENT_OWNER_STG",
        "prepare-prod-sdk-deploy",
        "codetest-prod",
        "deploy-prod-sdk-release",
        "deploy production SDK release",
        '"environment" => "prod"',
        "DEPLOYMENT_OWNER_PROD",
        'permissions["contents"] == "read"',
        'permissions["id-token"] == "write"',
        'concurrency["queue"] == "max"',
        'step["uses"] == "./.github/actions/deploy-serverless"',
        "checkout_index < deploy_index",
        "stage-specific terminal deployment job",
    ):
        assert contract_value in readiness
    assert release.index("system-test-readiness:") < release.index("publish:")


def test_release_ref_must_still_be_the_current_branch_head():
    release = (WORKFLOWS / "release.yml").read_text()
    build = release.split("  build:", 1)[1].split(
        "  system-test-readiness:", 1
    )[0]
    publish = release.split("  publish:", 1)[1].split(
        "  record-release-provenance:", 1
    )[0]

    assert "Verify release source is the current branch head" in build
    assert "git/ref/heads/$SOURCE_REF_NAME" in build
    assert 'current_sha" != "$SOURCE_SHA' in build
    assert "Recheck release source before first publication" in publish
    assert "if: steps.pypi-state.outputs.state == 'missing'" in publish
    assert "Refusing stale publication" in publish
    assert publish.index("Recheck release source before first publication") < (
        publish.index("Publish distribution")
    )


def test_readiness_inspection_is_read_only_and_write_is_probed_before_publish():
    release = (WORKFLOWS / "release.yml").read_text()
    readiness = release.split("  system-test-readiness:", 1)[1].split(
        "  publish:", 1
    )[0]
    trigger = release.split("  trigger-system-tests:", 1)[1]

    assert "permission-actions: read" in readiness
    assert "Verify cross-repository dispatch permission" in readiness
    assert "permission-actions: write" in readiness
    assert "steps.read-token.outputs.token" in readiness
    assert "permission-actions: write" in trigger
    assert "permission-contents: read" in trigger
    assert (
        "workflow: ${{ steps.target-workflow.outputs.workflow }}"
        in readiness
    )
    assert (
        "target-ref-sha: ${{ steps.target-workflow.outputs.target-ref-sha }}"
        in readiness
    )
    assert '"repos/$TARGET_REPOSITORY/commits/$ref"' in readiness
    assert '-f "ref=$ref_sha"' in readiness
    assert (
        "SYSTEM_TEST_WORKFLOW: "
        "${{ needs.system-test-readiness.outputs.workflow }}"
        in trigger
    )
    assert "vars.SYSTEM_TEST_WORKFLOW" not in trigger


def test_system_test_dispatch_waits_for_publish_and_forwards_the_contract():
    release = (WORKFLOWS / "release.yml").read_text()
    trigger = release.split("  trigger-system-tests:", 1)[1]

    assert (
        "      - build\n"
        "      - publish\n"
        "      - record-release-provenance\n"
        "      - system-test-readiness"
    ) in trigger
    expected_arguments = {
        '--arg sdk_version "$SDK_VERSION"',
        '--arg release_stage "$RELEASE_STAGE"',
        '--arg sdk_sha "$GITHUB_SHA"',
        '--arg source_repository "$GITHUB_REPOSITORY"',
        '--arg source_run_id "$GITHUB_RUN_ID"',
        '--arg source_run_url "$GITHUB_SERVER_URL/$GITHUB_REPOSITORY/actions/runs/$GITHUB_RUN_ID"',
    }
    for argument in expected_arguments:
        assert argument in trigger
    for field in (
        "sdk_version",
        "release_stage",
        "sdk_sha",
        "source_repository",
        "source_run_id",
        "source_run_url",
    ):
        assert f"{field}: ${field}" in trigger
    assert "return_run_details" not in trigger


def test_verified_release_provenance_check_binds_the_published_wheel():
    release = (WORKFLOWS / "release.yml").read_text()
    publish = release.split("  publish:", 1)[1].split(
        "  record-release-provenance:", 1
    )[0]
    provenance = release.split("  record-release-provenance:", 1)[1].split(
        "  trigger-system-tests:", 1
    )[0]

    assert release.count("checks: write") == 1
    assert "checks: write" not in publish
    assert "checks: write" in provenance
    assert "contents:" not in provenance
    assert "id-token:" not in provenance
    assert "actions/checkout@" not in publish
    assert "actions/checkout@" not in provenance
    publish_step_positions = [
        publish.index("Check existing PyPI distribution"),
        publish.index("Publish distribution"),
        publish.index("Verify published distribution"),
        publish.index("Record successful publish attempt"),
    ]
    assert publish_step_positions == sorted(publish_step_positions)
    assert (
        "run-attempt: ${{ steps.publish-attempt.outputs.run-attempt }}"
        in publish
    )
    assert (
        "run: printf 'run-attempt=%s\\n' \"$GITHUB_RUN_ATTEMPT\" "
        '>> "$GITHUB_OUTPUT"'
    ) in publish
    assert release.index("  publish:") < release.index(
        "  record-release-provenance:"
    )
    assert release.index("  record-release-provenance:") < release.index(
        "  trigger-system-tests:"
    )
    assert "Verify exact PyPI wheel" in provenance
    assert 'metadata.get("Name") != "abeja-sdk"' in provenance
    assert 'metadata.get("Version") != package_version' in provenance
    assert "len(urls) == 1" in provenance
    assert 'urls[0].get("filename") == wheel.name' in provenance
    assert 'remote.get("yanked") is True' in provenance
    assert "remote_digest != local_digest" in provenance
    assert "filename={wheel.name}" in provenance
    assert "sha256={local_digest}" in provenance
    assert "retention-days: 31" in release
    assert 'check_name="ABEJA SDK release provenance"' in provenance
    assert 'output_title="ABEJA SDK release provenance v1"' in provenance
    assert 'schema="abeja-sdk-release-provenance/v1"' in provenance
    assert 'external_id_prefix="abeja-sdk-release-provenance:v1"' in provenance
    assert "jq -cSn" in provenance
    assert (
        "SOURCE_RUN_ATTEMPT: ${{ needs.publish.outputs.run-attempt }}"
        in provenance
    )
    assert (
        'if [ "$SOURCE_RUN_ATTEMPT" -gt "$GITHUB_RUN_ATTEMPT" ]'
        in provenance
    )
    assert 'case "$RELEASE_STAGE" in' in provenance
    assert "version_pattern=" in provenance
    assert (
        'external_id="$external_id_prefix:$GITHUB_RUN_ID:$SOURCE_RUN_ATTEMPT:'
        '$PACKAGE_VERSION:$WHEEL_SHA256"'
    ) in provenance
    assert '--arg details_url' not in provenance
    assert 'details_url: $details_url' not in provenance
    assert "presentation-only value" in provenance
    assert '--arg source_run_id "$GITHUB_RUN_ID"' in provenance
    assert (
        '--arg source_run_attempt "$SOURCE_RUN_ATTEMPT"'
        in provenance
    )
    for field in (
        "package_version",
        "release_stage",
        "wheel_filename",
        "wheel_sha256",
        "source_repository",
        "source_workflow",
        "source_run_id",
        "source_run_attempt",
        "source_head_sha",
    ):
        assert f"{field}: ${field}" in provenance
    assert 'app_slug: "github-actions"' in provenance
    assert 'status: "completed"' in provenance
    assert 'conclusion: "success"' in provenance


def test_release_provenance_check_is_retry_safe_and_fails_on_conflicts():
    release = (WORKFLOWS / "release.yml").read_text()
    provenance = release.split("  record-release-provenance:", 1)[1].split(
        "  trigger-system-tests:", 1
    )[0]

    assert "commits/$GITHUB_SHA/check-runs" in provenance
    assert '-f "check_name=$check_name"' in provenance
    assert '-f "filter=all"' in provenance
    assert (
        'logical_external_id_prefix="$external_id_prefix:$GITHUB_RUN_ID:'
        '$SOURCE_RUN_ATTEMPT:$PACKAGE_VERSION:"'
    ) in provenance
    assert 'jq -c --arg prefix "$logical_external_id_prefix"' in provenance
    assert "startswith($prefix)" in provenance
    assert "select(.external_id == $external_id)" not in provenance
    assert 'if [ "$match_count" -gt 1 ]' in provenance
    assert 'if [ "$match_count" -eq 1 ]' in provenance
    assert 'operation="Reusing"' in provenance
    assert 'operation="Created"' in provenance
    assert "repos/$GITHUB_REPOSITORY/check-runs" in provenance
    assert 'actual_contract" != "$expected_contract' in provenance
    assert "differs from the contract" in provenance


def test_system_test_dispatch_reconciles_retries_by_run_and_version():
    release = (WORKFLOWS / "release.yml").read_text()
    trigger = release.split("  trigger-system-tests:", 1)[1].split(
        "  verify-system-tests:", 1
    )[0]

    assert "find_existing_dispatch()" in trigger
    assert (
        'expected_title="SDK $SDK_VERSION -> $RELEASE_STAGE '
        '(source $GITHUB_RUN_ID)"'
    ) in trigger
    assert "display_title" in trigger
    assert "steps.app-token.outputs.app-slug" in trigger
    assert 'expected_actor="${APP_SLUG}[bot]"' in trigger
    assert ".actor.login" in trigger
    assert '$2 == expected && $3 == actor { print $1 }' in trigger
    assert "Found multiple matching system-test runs" in trigger
    assert "Matching system-test dispatch already exists" in trigger
    assert "System-test dispatch accepted" in trigger
    assert "record_dispatch_response()" in trigger
    assert "X-GitHub-Api-Version: 2026-03-10" in trigger
    assert ".workflow_run_id" in trigger
    assert ".run_url" in trigger
    assert ".html_url" in trigger
    assert "gh workflow run" not in trigger
    assert (
        "EXPECTED_TARGET_SHA: "
        "${{ needs.system-test-readiness.outputs.target-ref-sha }}"
        in trigger
    )
    assert 'current_target_sha" != "$EXPECTED_TARGET_SHA' in trigger
    assert 'target_sha" != "$EXPECTED_TARGET_SHA' in trigger
    assert "cancel_unverified_run()" in trigger
    assert "actions/runs/$run_id/cancel" in trigger
    assert 'run_status" = "completed"' in trigger
    assert "completed before it could be cancelled" in trigger
    assert "System-test run did not use the inspected target SHA" in trigger
    assert 'allow_contract_settle="${2:-false}"' in trigger
    assert 'record_dispatch_response "$dispatched_response" true' in trigger
    assert "return 3" in trigger
    assert 'case "$record_status" in' in trigger
    assert "run record is eventually consistent" in trigger
    assert "identity did not settle by its returned ID" in trigger
    for output in ("run-id", "run-url", "target-sha"):
        assert f"{output}: ${{{{ steps.dispatch.outputs.{output} }}}}" in trigger
        assert f"printf '{output}=%s\\n'" in trigger


def test_release_waits_for_the_exact_successful_system_test_run():
    release = (WORKFLOWS / "release.yml").read_text()
    verify = release.split("  verify-system-tests:", 1)[1].split(
        "  deploy-production-firebase:", 1
    )[0]
    finalize = release.split("  finalize-production-release:", 1)[1]

    assert release.index("  trigger-system-tests:") < release.index(
        "  verify-system-tests:"
    )
    assert release.index("  verify-system-tests:") < release.index(
        "  deploy-production-firebase:"
    )
    assert "      - trigger-system-tests" in verify
    assert "    permissions: {}" in verify
    assert "permission-actions: read" in verify
    assert "permission-actions: write" not in verify
    assert "actions/checkout@" not in verify
    assert "actions/runs/$RUN_ID" in verify
    for identity_field in (
        "id: .id",
        "display_title: .display_title",
        "event: .event",
        "head_branch: .head_branch",
        "head_sha: .head_sha",
        "path: .path",
        "actor_login: .actor.login",
        "actor_type: .actor.type",
        "html_url: .html_url",
    ):
        assert identity_field in verify
    assert 'if [ "$actual_identity" != "$expected_identity" ]' in verify
    assert 'if [ "$status" = "completed" ]' in verify
    assert 'if [ "$conclusion" != "success" ]' in verify
    assert "actions/runs/$RUN_ID/jobs" in verify
    assert 'expected_terminal_job="deploy staging SDK release"' in verify
    assert 'expected_terminal_job="deploy production SDK release"' in verify
    assert 'terminal_count" -ne 1' in verify
    assert 'terminal_status" != "completed"' in verify
    assert 'terminal_conclusion" != "success"' in verify
    assert 'terminal_sha" != "$TARGET_SHA' in verify
    assert "Verified terminal deployment job" in verify
    assert "seq 1 200" in verify
    assert "sleep 15" in verify
    assert "timeout-minutes: 55" in verify
    assert "      - verify-system-tests" in finalize


def test_release_credentials_are_scoped_to_the_jobs_that_need_them():
    release = (WORKFLOWS / "release.yml").read_text()
    readiness = release.split("  system-test-readiness:", 1)[1].split(
        "  publish:", 1
    )[0]
    publish = release.split("  publish:", 1)[1].split(
        "  record-release-provenance:", 1
    )[0]
    provenance = release.split("  record-release-provenance:", 1)[1].split(
        "  trigger-system-tests:", 1
    )[0]
    trigger = release.split("  trigger-system-tests:", 1)[1].split(
        "  verify-system-tests:", 1
    )[0]
    verify = release.split("  verify-system-tests:", 1)[1].split(
        "  deploy-production-firebase:", 1
    )[0]
    firebase = release.split("  deploy-production-firebase:", 1)[1].split(
        "  finalize-production-release:", 1
    )[0]
    finalize = release.split("  finalize-production-release:", 1)[1]

    assert "permissions: {}\n" in release.split("jobs:", 1)[0]
    assert "    permissions: {}" in readiness
    assert "    permissions: {}" in trigger
    assert "    permissions: {}" in verify
    assert "permission-actions: read" in verify
    assert "permission-actions: write" not in verify
    assert (
        "    permissions:\n"
        "      contents: read"
    ) in publish
    assert "id-token: write" in publish
    assert "checks: write" not in publish
    assert (
        "    permissions:\n"
        "      checks: write # Create/reconcile the exact public provenance check only.\n"
        "    steps:"
    ) in provenance
    assert "contents:" not in provenance
    assert "id-token:" not in provenance
    assert "      contents: read" in firebase
    assert "      id-token: write" in firebase
    assert "    permissions:\n      contents: write" in finalize


def test_pypi_uses_protected_environment_and_trusted_publishing():
    release = (WORKFLOWS / "release.yml").read_text()
    publish = release.split("  publish:", 1)[1].split(
        "  record-release-provenance:", 1
    )[0]

    assert "name: pypi-${{ needs.build.outputs.release-stage }}" in publish
    assert "id-token: write" in publish
    assert "PYPI_API_TOKEN" not in publish
    assert "password:" not in publish
    assert "actions/checkout@" not in publish
    assert "actions/setup-python@" not in publish
    assert "Check existing PyPI distribution" in publish
    assert "remote_digest != local_digest" in publish
    assert "astral-sh/setup-uv@" in publish
    assert 'version: "0.11.16"' in publish
    assert (
        "checksum: "
        "74947fe2c03315cf07e82ab3acc703eddef01aba4d5232a98e4c6825ec116131"
    ) in publish
    assert "uv publish --trusted-publishing always --no-attestations" in publish
    assert "gh-action-pypi-publish@" not in publish
    assert "Verify published distribution" in publish
    assert "Published PyPI wheel digest differs" in publish
    assert "PyPI publication was not verified" in publish


def test_pypi_preflight_runs_the_exact_unit_tested_script():
    release = (WORKFLOWS / "release.yml").read_text()
    tested_script = (ROOT / "tools" / "check_pypi_distribution.py").read_text()

    assert get_step_run(
        release,
        "Check existing PyPI distribution",
    ) == tested_script.rstrip()


def test_privileged_workflow_run_is_removed_and_release_is_reconciled_inline():
    release = (WORKFLOWS / "release.yml").read_text()
    finalize = release.split("  finalize-production-release:", 1)[1]

    assert not (WORKFLOWS / "auto-tag-on-release.yml").exists()
    assert "workflow_run:" not in release
    assert "      - verify-system-tests" in finalize
    assert "      - deploy-production-firebase" in finalize
    assert "needs.build.outputs.release-stage == 'production'" in finalize
    assert "contents: write" in finalize
    assert "actions/checkout@" not in finalize
    assert 'SOURCE_EVENT" != "push' in finalize
    assert "SOURCE_REF\" != \"refs/heads/master" in finalize
    assert "Refusing stale production finalization" in finalize
    assert 'current_master_sha" != "$SOURCE_SHA' in finalize
    assert finalize.index('if [ -z "$tag_state" ]') < finalize.index(
        'current_master_sha="$(gh api'
    )
    assert finalize.index('current_master_sha="$(gh api') < finalize.index(
        'if ! gh api --method POST "repos/$REPOSITORY/git/refs"'
    )
    assert "repos/$REPOSITORY/git/ref/tags/$PACKAGE_VERSION" in finalize
    assert "commit $SOURCE_SHA" in finalize
    assert "repos/$REPOSITORY/releases/tags/$PACKAGE_VERSION" in finalize
    assert "expected_release_state" in finalize


def test_shell_scripts_do_not_interpolate_actions_expressions_directly():
    for name in (
        "firebase-deploy-prod.yml",
        "integration-test.yml",
        "release.yml",
        "test.yml",
    ):
        lines = (WORKFLOWS / name).read_text().splitlines()
        index = 0
        while index < len(lines):
            match = re.match(r"^(\s*)run:\s*(.*)$", lines[index])
            if match is None:
                index += 1
                continue

            indent = len(match.group(1))
            assert "${{" not in match.group(2)
            if match.group(2) in ("|", ">"):
                index += 1
                while index < len(lines):
                    line = lines[index]
                    if line and len(line) - len(line.lstrip()) <= indent:
                        break
                    assert "${{" not in line
                    index += 1
                continue
            index += 1


def test_dependabot_alert_lookup_uses_the_matching_token_permission():
    workflow = (WORKFLOWS / "dependabot-auto-merge.yml").read_text()

    assert "vulnerability-alerts: read" in workflow
    assert "security-events: read" not in workflow
    assert "alert-lookup: true" in workflow
    assert "updated-dependencies-json" in workflow
    assert "dependency.alertState" in workflow
    assert "dependency.ghsaId" in workflow
    assert "dependency.cvss" in workflow
    assert "allDependenciesHaveOpenAlerts" in workflow
    assert "listAlertsForRepo" not in workflow
    assert "pr.title" not in workflow
    assert "pr.labels" not in workflow


def test_migrated_workflows_use_supported_runner_image():
    workflows = "\n".join(
        (WORKFLOWS / name).read_text()
        for name in (
            "integration-test.yml",
            "release.yml",
            "test.yml",
        )
    )

    assert "ubuntu-22.04" not in workflows
    assert workflows.count("runs-on: ubuntu-24.04") == 11


def test_firebase_deployments_use_branch_scoped_environments():
    dev = (WORKFLOWS / "firebase-deploy-dev.yml").read_text()
    production = (WORKFLOWS / "firebase-deploy-prod.yml").read_text()

    assert "if: github.ref == 'refs/heads/develop'" in dev
    assert "environment: firebase-hosting-dev" in dev
    assert "SOURCE_REF: ${{ github.ref }}" in production
    assert 'SOURCE_REF" != "refs/heads/master' in production
    assert "environment: firebase-hosting-production" in production
    for workflow in (dev, production):
        assert "permissions: {}" in workflow.split("jobs:", 1)[0]
        assert "contents: read" in workflow
        assert "id-token: write" in workflow
        assert "service_account: github-deploy@apf-mlops-docs.iam.gserviceaccount.com" in workflow


def test_production_firebase_is_gated_and_retry_safe():
    release = (WORKFLOWS / "release.yml").read_text()
    production = (WORKFLOWS / "firebase-deploy-prod.yml").read_text()
    build_docs = production.split("  build-docs:", 1)[1].split(
        "  deploy-prod:", 1
    )[0]
    deploy = production.split("  deploy-prod:", 1)[1]
    caller = release.split("  deploy-production-firebase:", 1)[1].split(
        "  finalize-production-release:", 1
    )[0]

    assert "workflow_call:" in production
    assert "  push:" not in production.split("permissions:", 1)[0]
    assert "workflow_dispatch:" not in production
    assert "      - verify-system-tests" in caller
    assert "uses: ./.github/workflows/firebase-deploy-prod.yml" in caller
    assert "  validate-call:" in production
    assert "  build-docs:" in production
    assert "      - validate-call" in deploy
    assert "      - build-docs" in deploy
    assert "SOURCE_WORKFLOW_REF: ${{ github.workflow_ref }}" in production
    assert "Verify trusted Release caller and current master head" in production
    assert "git/ref/heads/master" in production
    assert "Refusing stale Firebase deployment" in production
    assert "Recheck production source before Firebase mutation" in production
    assert 'configured_site" != "apf-mlops-docs-sdk' in production
    assert 'configured_public" != "doc/build/html' in production
    assert "SOURCE_DATE_EPOCH" in production
    assert "abeja-platform-sdk-release.json" in production
    assert "docs_sha256" in production
    assert "firebase hosting:channel:list" in production
    assert "/channels/live" in production
    assert ".release.message" in production
    assert ".release.version.name" in production
    assert "--message \"$RELEASE_IDENTITY\"" in production
    assert "steps.live-state.outputs.identical != 'true'" in production
    assert "deploy_status=0" in production
    assert "|| deploy_status=$?" in production
    assert 'last_message" = "$RELEASE_IDENTITY' in production
    assert 'last_marker" = "$EXPECTED_MARKER' in production
    assert "Firebase Hosting did not reconcile" in production
    assert "firebase-tools@15.22.4" in deploy
    assert "--ignore-scripts" in deploy

    # Repository code is built without the Environment or OIDC permission.
    # The credential-bearing job receives one exact same-run artifact and
    # verifies its complete Firebase config, content digest, and marker.
    assert "environment:" not in build_docs
    assert "id-token:" not in build_docs
    assert "actions/checkout@" in build_docs
    assert "sphinx-build" in build_docs
    assert "actions/upload-artifact@" in build_docs
    assert "retention-days: 31" in build_docs
    assert "overwrite: true" in build_docs
    assert "environment: firebase-hosting-production" in deploy
    assert "id-token: write" in deploy
    assert "actions/checkout@" not in deploy
    assert "actions/setup-python@" not in deploy
    assert "poetry install" not in deploy
    assert "sphinx-build" not in deploy
    assert "actions/download-artifact@" in deploy
    assert "artifact-ids: ${{ needs.build-docs.outputs.artifact-id }}" in deploy
    assert "merge-multiple: true" in deploy
    assert "complete reviewed contract" in deploy
    assert "deploy hooks and unknown keys are forbidden" in deploy
    assert "actual_firebaserc" in deploy
    assert "actual_firebase_json" in deploy
    assert "Firebase documentation marker differs from its artifact" in deploy
    assert production.count("git/ref/heads/master") == 3
    assert deploy.count("Refusing stale Firebase deployment") == 2
    for match in re.finditer(r"^\s*uses:\s*([^\s]+)", production, re.MULTILINE):
        reference = match.group(1)
        assert re.search(r"@[0-9a-f]{40}$", reference), reference


def test_firebase_shared_trust_boundary_is_documented():
    operations = (ROOT / ".github" / "CICD.md").read_text()
    normalized = " ".join(operations.split())

    assert "one-project, multi-site design" in normalized
    assert "deliberately does not distinguish Git refs" in normalized
    assert "review and approval of the pull request into `master`" in normalized
    assert "Do not add a required Environment reviewer" in normalized
    assert "different current release identity is the normal predecessor" in normalized
    assert "out-of-band console or CLI deployment can therefore be overwritten" in normalized


def test_production_rollback_boundary_and_ownership_cutover_are_documented():
    operations = (ROOT / ".github" / "CICD.md").read_text()
    normalized = " ".join(operations.split())

    assert "## Production failure and rollback boundary" in operations
    assert "It never means deleting and reusing a package version" in normalized
    assert "A PyPI yank is non-destructive" in normalized
    assert "exact `==` pins can still select a yanked" in normalized
    assert "release a new patch version" in normalized
    assert "production platform stack has already been deployed" in normalized
    assert "never dispatch an older SDK" in normalized
    assert "terminal deployment job started" in normalized
    assert "inspect and stabilize CloudFormation" in normalized
    assert "new staging RC or a new production patch version" in normalized
    assert "CI deployment ownership" in normalized
    assert "not an application rollback or an older-SDK rollback" in normalized
    assert "DEPLOYMENT_OWNER_PROD" in normalized
    assert "keep SDK `master` frozen" in normalized
    assert "Do not merge another SDK change to `master`" in normalized
    cutover_steps = (
        "prepare and review the CircleCI change",
        "remove only the production deployment filter",
        "freeze the deployment ref and legacy SDK trigger",
        "block new CircleCI production work",
        "drain every active production deployment",
        "prove that no new production `build` can start",
        "DEPLOYMENT_OWNER_PROD=github-actions",
    )
    positions = [normalized.index(step) for step in cutover_steps]
    assert positions == sorted(positions)
    assert "keep the SDK production PR draft" in normalized
