import pytest

from podcast import MemoryRepository, populate
from pathlib import Path


@pytest.fixture
def in_memory_repo():
    repo = MemoryRepository()
    data_path = Path('podcast') / 'adapters' / 'data'
    populate(data_path, repo)
    return repo
