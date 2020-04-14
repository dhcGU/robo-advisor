from app.robo_advisor import compile_url

def test_compile_url():
    expected_result = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=AAPL&apikey=KEY123"
    assert compile_url("DAILY", "AAPL", "KEY123") == expected_result