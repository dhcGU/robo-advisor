from app.robo_advisor import write_to_csv
import os

def test_write_to_csv():
    f_name = "test.csv"
    cols = ["this", 'is', 'a', 'test']
    t_series = {}
    write_to_csv(f_name, cols, t_series)
    assert os.path.exists("test.csv")