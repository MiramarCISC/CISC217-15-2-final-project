from pathlib import Path
import pytest
@pytest.mark.cleanup_guard
def test_instructor_example_has_been_removed():
    assert not Path("PROVIDED_EXAMPLE_CODE_PRESENT.txt").exists(), "Run: python scripts/cleanup_example.py"
