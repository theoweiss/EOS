import json
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

DIR_PROJECT_ROOT = Path(__file__).parent.parent
DIR_TESTDATA = Path(__file__).parent / "testdata"


def test_openapi_spec_current(config_eos):
    """Verify the openapi spec hasn´t changed."""
    expected_spec_path = DIR_PROJECT_ROOT / "openapi.json"
    new_spec_path = DIR_TESTDATA / "openapi-new.json"

    with open(expected_spec_path) as f_expected:
        expected_spec = json.load(f_expected)

    # Patch get_config and import within guard to patch global variables within the eos module.
    with patch("akkudoktoreos.config.config.get_config", return_value=config_eos):
        # Ensure the script works correctly as part of a package
        root_dir = Path(__file__).resolve().parent.parent
        sys.path.insert(0, str(root_dir))
        from scripts import generate_openapi

        spec = generate_openapi.generate_openapi()

    with open(new_spec_path, "w") as f_new:
        json.dump(spec, f_new, indent=4, sort_keys=True)

    # Serialize to ensure comparison is consistent
    spec_str = json.dumps(spec, indent=4, sort_keys=True)
    expected_spec_str = json.dumps(expected_spec, indent=4, sort_keys=True)

    try:
        assert spec_str == expected_spec_str
    except AssertionError as e:
        pytest.fail(
            f"Expected {new_spec_path} to equal {expected_spec_path}.\n"
            + f"If ok: `make gen-docs` or `cp {new_spec_path} {expected_spec_path}`\n"
        )


def test_openapi_md_current(config_eos):
    """Verify the generated openapi markdown hasn´t changed."""
    expected_spec_md_path = DIR_PROJECT_ROOT / "docs" / "_generated" / "openapi.md"
    new_spec_md_path = DIR_TESTDATA / "openapi-new.md"

    with open(expected_spec_md_path, encoding="utf8") as f_expected:
        expected_spec_md = f_expected.read()

    # Patch get_config and import within guard to patch global variables within the eos module.
    with patch("akkudoktoreos.config.config.get_config", return_value=config_eos):
        # Ensure the script works correctly as part of a package
        root_dir = Path(__file__).resolve().parent.parent
        sys.path.insert(0, str(root_dir))
        from scripts import generate_openapi_md

        spec_md = generate_openapi_md.generate_openapi_md()

    with open(new_spec_md_path, "w", encoding="utf8") as f_new:
        f_new.write(spec_md)

    try:
        assert spec_md == expected_spec_md
    except AssertionError as e:
        pytest.fail(
            f"Expected {new_spec_md_path} to equal {expected_spec_md_path}.\n"
            + f"If ok: `make gen-docs` or `cp {new_spec_md_path} {expected_spec_md_path}`\n"
        )


def test_config_md_current(config_eos):
    """Verify the generated configuration markdown hasn´t changed."""
    expected_config_md_path = DIR_PROJECT_ROOT / "docs" / "_generated" / "config.md"
    new_config_md_path = DIR_TESTDATA / "config-new.md"

    with open(expected_config_md_path, encoding="utf8") as f_expected:
        expected_config_md = f_expected.read()

    # Patch get_config and import within guard to patch global variables within the eos module.
    with patch("akkudoktoreos.config.config.get_config", return_value=config_eos):
        # Ensure the script works correctly as part of a package
        root_dir = Path(__file__).resolve().parent.parent
        sys.path.insert(0, str(root_dir))
        from scripts import generate_config_md

        config_md = generate_config_md.generate_config_md()

    with open(new_config_md_path, "w", encoding="utf8") as f_new:
        f_new.write(config_md)

    try:
        assert config_md == expected_config_md
    except AssertionError as e:
        pytest.fail(
            f"Expected {new_config_md_path} to equal {expected_config_md_path}.\n"
            + f"If ok: `make gen-docs` or `cp {new_config_md_path} {expected_config_md_path}`\n"
        )
