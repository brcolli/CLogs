from synthetic_log_generator import SyntheticLogGenerator


def test_generate_log_entry():
    slg = SyntheticLogGenerator()
    log_entry = slg.generate_log_entry()
    assert isinstance(log_entry, str)


def test_generate_log_entries():
    slg = SyntheticLogGenerator()
    num_logs = 10
    log_entries = slg.generate_log_entries(num_logs)
    assert len(log_entries) == num_logs
    for log_entry in log_entries:
        assert isinstance(log_entry, str)
