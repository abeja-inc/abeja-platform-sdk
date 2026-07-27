import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
WORKFLOWS = ROOT / ".github" / "workflows"


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
    assert workflows.count(expected_checkout) == len(migrated_workflows)
    assert workflows.count("persist-credentials: false") == len(
        migrated_workflows
    )


def test_unit_workflow_has_noncolliding_stale_cancellation_and_stable_gate():
    unit = (WORKFLOWS / "test.yml").read_text()
    required = unit.split("  required:", 1)[1]

    assert (
        "group: abeja-platform-sdk-unit-tests-"
        "${{ github.event.pull_request.number || github.ref }}"
    ) in unit
    assert "cancel-in-progress: true" in unit
    assert "name: Unit tests" in required
    assert "if: ${{ always() }}" in required
    assert "needs: unit-tests" in required
    assert 'run: test "$UNIT_TESTS_RESULT" = "success"' in required
    assert "permissions: {}" in required


def test_integration_secrets_fail_closed_for_manual_and_external_callers():
    integration = (WORKFLOWS / "integration-test.yml").read_text()
    release = (WORKFLOWS / "release.yml").read_text()
    integration_job = integration.split("  integration-tests:", 1)[1]

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
    assert "secrets: inherit" not in release


def test_release_validates_version_and_exact_target_contract_before_publish():
    release = (WORKFLOWS / "release.yml").read_text()

    assert "tools/validate_release_version.py" in release
    assert "inputs.keys.map(&:to_s) - required_inputs" in release
    assert 'document["run-name"] == expected_run_name' in release
    assert (
        r"^[A-Za-z0-9][A-Za-z0-9._-]*\.ya?ml$"
        in release
    )
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
    assert (
        "workflow: ${{ steps.target-workflow.outputs.workflow }}"
        in readiness
    )
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
    expected_fields = {
        'sdk_version=$SDK_VERSION',
        'release_stage=$RELEASE_STAGE',
        'sdk_sha=$GITHUB_SHA',
        'source_repository=$GITHUB_REPOSITORY',
        'source_run_id=$GITHUB_RUN_ID',
        (
            'source_run_url=$GITHUB_SERVER_URL/$GITHUB_REPOSITORY/'
            'actions/runs/$GITHUB_RUN_ID'
        ),
    }
    for field in expected_fields:
        assert f'--field "{field}"' in trigger


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
    assert (
        'details_url="$GITHUB_SERVER_URL/$GITHUB_REPOSITORY/actions/runs/'
        '$GITHUB_RUN_ID/attempts/$SOURCE_RUN_ATTEMPT"'
    ) in provenance
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
        "  finalize-production-release:", 1
    )[0]

    assert "find_existing_dispatch()" in trigger
    assert (
        'expected_title="SDK $SDK_VERSION -> $RELEASE_STAGE '
        '(source $GITHUB_RUN_ID)"'
    ) in trigger
    assert "display_title" in trigger
    assert "Found multiple matching system-test runs" in trigger
    assert "Matching system-test dispatch already exists" in trigger
    assert "System-test dispatch accepted" in trigger


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
        "  finalize-production-release:", 1
    )[0]
    finalize = release.split("  finalize-production-release:", 1)[1]

    assert "permissions: {}\n" in release.split("jobs:", 1)[0]
    assert "    permissions: {}" in readiness
    assert "    permissions: {}" in trigger
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


def test_privileged_workflow_run_is_removed_and_release_is_reconciled_inline():
    release = (WORKFLOWS / "release.yml").read_text()
    finalize = release.split("  finalize-production-release:", 1)[1]

    assert not (WORKFLOWS / "auto-tag-on-release.yml").exists()
    assert "workflow_run:" not in release
    assert "needs.build.outputs.release-stage == 'production'" in finalize
    assert "contents: write" in finalize
    assert "actions/checkout@" not in finalize
    assert 'SOURCE_EVENT" != "push' in finalize
    assert "SOURCE_REF\" != \"refs/heads/master" in finalize
    assert "repos/$REPOSITORY/git/ref/tags/$PACKAGE_VERSION" in finalize
    assert "commit $SOURCE_SHA" in finalize
    assert "repos/$REPOSITORY/releases/tags/$PACKAGE_VERSION" in finalize
    assert "expected_release_state" in finalize


def test_shell_scripts_do_not_interpolate_actions_expressions_directly():
    for name in ("integration-test.yml", "release.yml", "test.yml"):
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
