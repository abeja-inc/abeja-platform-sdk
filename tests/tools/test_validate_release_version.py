import pytest

from tools.validate_release_version import main, validate_release_version


@pytest.mark.parametrize(
    "version,release_stage",
    [
        ("0.0.0rc0", "staging"),
        ("2.3.6rc1", "staging"),
        ("0.0.0", "production"),
        ("2.3.6", "production"),
    ],
)
def test_accepts_canonical_version_for_release_stage(version, release_stage):
    validate_release_version(version, release_stage)


@pytest.mark.parametrize(
    "version,release_stage",
    [
        ("2.3.6", "staging"),
        ("2.3.6rc1", "production"),
        ("02.3.6rc1", "staging"),
        ("2.3.6rc01", "staging"),
        ("2.3", "production"),
        ("2.3.6", "preview"),
    ],
)
def test_rejects_wrong_or_noncanonical_version(version, release_stage):
    with pytest.raises(ValueError):
        validate_release_version(version, release_stage)


def test_cli_fails_closed(capsys):
    assert main(["2.3.6rc1", "production"]) == 1
    assert "production release version" in capsys.readouterr().err
