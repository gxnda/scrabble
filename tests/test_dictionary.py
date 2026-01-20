"""Tests for Dictionary class"""
import pytest
from pathlib import Path
from src.dictionary import Dictionary


class TestDictionary:
    """Test Dictionary functionality"""

    def test_dictionary_creation(self, test_dictionary):
        """Test creating a dictionary from file"""
        assert test_dictionary is not None
        assert len(test_dictionary) > 0

    def test_dictionary_contains_word(self, test_dictionary):
        """Test checking if word exists in dictionary"""
        assert "cat" in test_dictionary
        assert "dog" in test_dictionary
        assert "hello" in test_dictionary

    def test_dictionary_case_insensitive(self, test_dictionary):
        """Test that dictionary lookups are case-insensitive"""
        assert "cat" in test_dictionary
        assert "CAT" in test_dictionary
        assert "Cat" in test_dictionary
        assert "cAt" in test_dictionary

    def test_dictionary_word_not_found(self, test_dictionary):
        """Test that non-existent words return False"""
        assert "notaword" not in test_dictionary
        assert "xyz123" not in test_dictionary
        assert "zzzzz" not in test_dictionary

    def test_dictionary_len(self, test_dictionary):
        """Test dictionary length"""
        # Count words in our test dictionary file
        dict_path = Path(__file__).parent / "fixtures" / "test_dict.txt"
        with dict_path.open() as f:
            expected_count = len(f.read().splitlines())
        assert len(test_dictionary) == expected_count

    def test_dictionary_repr(self, test_dictionary):
        """Test dictionary string representation"""
        repr_str = repr(test_dictionary)
        assert "Dictionary" in repr_str
        assert "test_dict.txt" in repr_str

    def test_real_dictionary_has_common_words(self, real_dictionary):
        """Test that real dictionary has common Scrabble words"""
        assert "scrabble" in real_dictionary
        assert "quiz" in real_dictionary
        assert "jazz" in real_dictionary
        assert "fizz" in real_dictionary
        assert "the" in real_dictionary
        assert "and" in real_dictionary

    def test_real_dictionary_size(self, real_dictionary):
        """Test that real dictionary has reasonable size (SOWPODS has ~267k words)"""
        assert len(real_dictionary) > 200000
        assert len(real_dictionary) < 300000
