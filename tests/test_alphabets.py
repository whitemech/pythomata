"""This module contains tests for alphabets."""
from pythomata.alphabets import ArrayAlphabet, VectorizedAlphabet


class TestVectorizedAlphabet:
    """Test vectorized alphabet."""

    def test_character_vectorized_alphabet(self):
        """Test character vectorized alphabet."""
        a = ArrayAlphabet(["a", "b", "c"])
        va = VectorizedAlphabet(a, 2)

        assert va.size == 3 ** 2

        assert va.get_symbol(0) == ("a", "a")
        assert va.get_symbol(1) == ("a", "b")
        assert va.get_symbol(2) == ("a", "c")
        assert va.get_symbol(3) == ("b", "a")
        assert va.get_symbol(4) == ("b", "b")
        assert va.get_symbol(5) == ("b", "c")
        assert va.get_symbol(6) == ("c", "a")
        assert va.get_symbol(7) == ("c", "b")
        assert va.get_symbol(8) == ("c", "c")
