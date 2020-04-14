from app.robo_advisor import hasNumber

def test_hasNumber():
    to_test = "abcdef7jeje"
    assert hasNumber(to_test) == True