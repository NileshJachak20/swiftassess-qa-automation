"""
Demo unit tests to demonstrate CI/CD pipeline without browser automation
"""

import pytest


class TestMathOperations:
    """Demo tests for basic math operations"""

    @pytest.mark.smoke
    @pytest.mark.unit
    def test_addition(self):
        """Test addition operation"""
        assert 2 + 2 == 4
        assert 10 + 5 == 15
        assert -1 + 1 == 0

    @pytest.mark.regression
    @pytest.mark.unit
    def test_subtraction(self):
        """Test subtraction operation"""
        assert 5 - 3 == 2
        assert 10 - 5 == 5
        assert 0 - 1 == -1

    @pytest.mark.unit
    def test_multiplication(self):
        """Test multiplication operation"""
        assert 3 * 4 == 12
        assert 5 * 5 == 25
        assert 0 * 100 == 0

    @pytest.mark.unit
    def test_division(self):
        """Test division operation"""
        assert 10 / 2 == 5
        assert 15 / 3 == 5
        assert 100 / 4 == 25


class TestStringOperations:
    """Demo tests for string operations"""

    @pytest.mark.smoke
    @pytest.mark.unit
    def test_string_concatenation(self):
        """Test string concatenation"""
        assert "Hello" + " " + "World" == "Hello World"
        assert "Test" + "123" == "Test123"

    @pytest.mark.regression
    @pytest.mark.unit
    def test_string_upper_lower(self):
        """Test string case conversion"""
        assert "hello".upper() == "HELLO"
        assert "WORLD".lower() == "world"

    @pytest.mark.unit
    def test_string_length(self):
        """Test string length"""
        assert len("Hello") == 5
        assert len("") == 0
        assert len("Testing 123") == 11


class TestListOperations:
    """Demo tests for list operations"""

    @pytest.mark.unit
    def test_list_append(self):
        """Test list append operation"""
        my_list = [1, 2, 3]
        my_list.append(4)
        assert my_list == [1, 2, 3, 4]

    @pytest.mark.unit
    def test_list_length(self):
        """Test list length"""
        assert len([1, 2, 3, 4, 5]) == 5
        assert len([]) == 0

    @pytest.mark.unit
    def test_list_contains(self):
        """Test list contains operation"""
        my_list = ["apple", "banana", "cherry"]
        assert "banana" in my_list
        assert "orange" not in my_list


class TestDictOperations:
    """Demo tests for dictionary operations"""

    @pytest.mark.unit
    def test_dict_access(self):
        """Test dictionary key access"""
        my_dict = {"name": "SwiftAssess", "type": "Testing", "year": 2025}
        assert my_dict["name"] == "SwiftAssess"
        assert my_dict["year"] == 2025

    @pytest.mark.unit
    def test_dict_keys(self):
        """Test dictionary keys"""
        my_dict = {"a": 1, "b": 2, "c": 3}
        assert "a" in my_dict
        assert "d" not in my_dict

    @pytest.mark.unit
    def test_dict_values(self):
        """Test dictionary values"""
        my_dict = {"name": "Test", "count": 10}
        assert my_dict.get("name") == "Test"
        assert my_dict.get("count") == 10
        assert my_dict.get("missing", "default") == "default"

