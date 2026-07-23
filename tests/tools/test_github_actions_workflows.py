from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
WORKFLOWS = ROOT / ".github" / "workflows"


def test_release_and_live_integration_runs_are_queued():
    release = (WORKFLOWS / "release.yml").read_text()
    integration = (WORKFLOWS / "integration-test.yml").read_text()

    assert "group: release\n  queue: max" in release
    assert (
        "group: abeja-platform-sdk-datalake-integration\n"
        "      queue: max"
    ) in integration
    assert "cancel-in-progress: false" not in release
    assert "cancel-in-progress: false" not in integration


def test_migrated_workflows_use_current_checkout_major():
    migrated_workflows = (
        "auto-tag-on-release.yml",
        "integration-test.yml",
        "release.yml",
        "test.yml",
    )
    workflows = "\n".join(
        (WORKFLOWS / name).read_text() for name in migrated_workflows
    )

    assert "actions/checkout@v6" not in workflows
    assert workflows.count("actions/checkout@v7") == len(migrated_workflows)


def test_release_validates_version_and_exact_target_contract_before_publish():
    release = (WORKFLOWS / "release.yml").read_text()

    assert "tools/validate_release_version.py" in release
    assert "inputs.keys.map(&:to_s) - required_inputs" in release
    assert release.index("system-test-readiness:") < release.index("publish:")


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


def test_system_test_dispatch_waits_for_publish_and_forwards_the_contract():
    release = (WORKFLOWS / "release.yml").read_text()
    trigger = release.split("  trigger-system-tests:", 1)[1]

    assert "needs:\n      - build\n      - publish" in trigger
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


def test_credentialed_release_jobs_do_not_receive_the_repository_token():
    release = (WORKFLOWS / "release.yml").read_text()

    for start, end in (
        ("  system-test-readiness:", "  publish:"),
        ("  publish:", "  trigger-system-tests:"),
        ("  trigger-system-tests:", None),
    ):
        job = release.split(start, 1)[1]
        if end is not None:
            job = job.split(end, 1)[0]
        assert "    permissions: {}" in job
