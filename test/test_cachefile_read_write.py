import pytest
from pathlib import Path

from kernel_tuner.cache.file import read_cache_file, write_cache_file


TEST_PATH = Path(__file__).parent
TEST_CACHE_PATH = TEST_PATH / "test_cache_files"
CLOSED_CACHE_PATH = TEST_CACHE_PATH / "small_cache.json"
OPEN_CACHE_NO_COMMA_PATH = TEST_CACHE_PATH / "open_cache_no_comma.json"
OPEN_CACHE_COMMA_PATH = TEST_CACHE_PATH / "open_cache_with_comma.json"


@pytest.fixture
def output_path(tmp_path):
    return tmp_path / "output.json"


@pytest.mark.parametrize(
    "filename",
    [CLOSED_CACHE_PATH, OPEN_CACHE_NO_COMMA_PATH, OPEN_CACHE_COMMA_PATH],
    ids=["closed cache", "open cache without comma", "open cache with comma"],
)
def test_read_cache_file(filename):
    # Read device name of the given file
    file_content = read_cache_file(filename)
    device_name = file_content.get("device_name")

    # Check if the expected value of device name is in the file
    assert device_name == "Testing"


def test_write_cache_file(output_path):
    sample_cache = read_cache_file(CLOSED_CACHE_PATH)

    write_cache_file(sample_cache, output_path)

    with open(output_path, 'r') as output, open(CLOSED_CACHE_PATH, 'r') as input:
        assert output.read() == input.read()


@pytest.mark.skip
def test_write_open_cache_file(output_path):
    sample_cache = read_cache_file(OPEN_CACHE_COMMA_PATH)

    write_cache_file(sample_cache, output_path, keep_open=True)

    with open(output_path, 'r') as output, open(OPEN_CACHE_COMMA_PATH, 'r') as input:
        assert output.read() == input.read()