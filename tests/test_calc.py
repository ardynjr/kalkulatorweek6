import pytest
from app import eval_expr

@pytest.mark.parametrize("expr,expected", [
    ("320*100/120+56", 322.66667),
    ("(2+3)*4", 20.0),
    ("10%3", 1.0),
])
def test_eval_ok(expr, expected):
    assert round(eval_expr(expr),5) == expected

def test_invalid_expr():
    with pytest.raises(Exception):
        eval_expr("__import__('os').system('echo bad')")
