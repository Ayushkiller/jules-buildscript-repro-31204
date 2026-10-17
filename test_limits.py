from src.config import BURST_CAPACITY, MAX_EVENTS_PER_SEC


def test_burst_exceeds_rate():
    assert BURST_CAPACITY > MAX_EVENTS_PER_SEC
