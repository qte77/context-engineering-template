# https://hypothesis.readthedocs.io/en/latest/quickstart.html
# contents of example.py
from hypothesis import given
from hypothesis import strategies as st

@given(st.integers())
def test_integers(n):
    print(f"called with {n}")
    assert isinstance(n, int)

test_integers()

@st.composite
def ordered_pairs(draw):
    n1 = draw(st.integers())
    n2 = draw(st.integers(min_value=n1))
    return (n1, n2)

@given(ordered_pairs())
def test_pairs_are_ordered(pair):
    n1, n2 = pair
    assert n1 <= n2

test_pairs_are_ordered()