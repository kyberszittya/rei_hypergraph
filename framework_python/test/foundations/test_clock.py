from rei.foundations.clock import DummyClock, LocalClock


def test_dummy_time():
    clock = DummyClock()
    assert clock.get_time_sec() == 0.0
    assert clock.get_time_ns() == 0


def test_local_time():
    clock = LocalClock()
    # Assert typical values
    import time
    assert clock.get_time_ns() > 0
    assert clock.get_time_sec() > 0.0
    assert clock.get_time_sec() == time.time()
    assert time.time_ns() == clock.get_time_ns()