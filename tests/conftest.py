import pytest


@pytest.fixture
def tmp_dir(request):
    """
    Return a :class:`py.path.local` object pointing to the "tmp" directory
    relative to the test file.
    """
    tmp_dir = request.fspath.dirpath('tmp')
    if tmp_dir.isdir():
        tmp_dir.remove()
    tmp_dir.mkdir()
    return tmp_dir
