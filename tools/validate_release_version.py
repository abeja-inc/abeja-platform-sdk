"""Validate that an SDK version belongs to its release stage."""

import argparse
import re
import sys


VERSION_BASE = (
    r"(?:0|[1-9][0-9]*)"
    r"\.(?:0|[1-9][0-9]*)"
    r"\.(?:0|[1-9][0-9]*)"
)
STAGE_PATTERNS = {
    "staging": re.compile(VERSION_BASE + r"rc(?:0|[1-9][0-9]*)\Z"),
    "production": re.compile(VERSION_BASE + r"\Z"),
}


def validate_release_version(version, release_stage):
    """Raise ValueError unless version is canonical for release_stage."""
    try:
        pattern = STAGE_PATTERNS[release_stage]
    except KeyError as error:
        raise ValueError(
            "release stage must be staging or production: {!r}".format(
                release_stage
            )
        ) from error

    if pattern.fullmatch(version) is None:
        expected = "X.Y.ZrcN" if release_stage == "staging" else "X.Y.Z"
        raise ValueError(
            "{} release version must be canonical {}: {!r}".format(
                release_stage,
                expected,
                version,
            )
        )


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("version")
    parser.add_argument("release_stage")
    args = parser.parse_args(argv)

    try:
        validate_release_version(args.version, args.release_stage)
    except ValueError as error:
        print("error: {}".format(error), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
