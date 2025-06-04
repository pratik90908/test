from luna.fuzzer import detect_waf


def test_detect_waf():
    assert detect_waf([200, 403, 403]) is True
    assert detect_waf([200, 200]) is False
