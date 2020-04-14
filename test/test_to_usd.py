from app.robo_advisor import to_usd

def test_usd():
    result = to_usd(4)
    assert result == "$4.00"