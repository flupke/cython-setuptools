import atexit
from pathlib import Path
import shutil
import uuid

import pytest


@pytest.fixture()
def tmp_dir(request):
    """
    Return a :class:`pathlib.Path` object pointing to the "tmp" directory
    relative to the test file.
    """
    tmp_dir = Path(request.fspath.dirpath(f"tmp-{uuid.uuid4()}"))
    tmp_dir.mkdir()
    yield tmp_dir

    # remove temporary directory
    if tmp_dir.exists():
        # Windows compatible solution to clean-up the tmp_dir
        atexit.register(shutil.rmtree, tmp_dir, ignore_errors=True)
