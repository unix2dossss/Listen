import pytest

from podcast import MemoryRepository


@pytest.fixture
def in_memory_repo():
    repo = MemoryRepository()
    return repo