"""Test suite for hello module."""

import pytest
from hello import hello, add


class TestHello:
    """Tests for the hello function."""

    def test_hello_default(self):
        """Test hello with default argument."""
        assert hello() == "Hello, World!"

    def test_hello_with_name(self):
        """Test hello with custom name."""
        assert hello("Alice") == "Hello, Alice!"

    def test_hello_empty_string(self):
        """Test hello with empty string."""
        assert hello("") == "Hello, !"


class TestAdd:
    """Tests for the add function."""

    def test_add_positive(self):
        """Test adding two positive numbers."""
        assert add(2, 3) == 5

    def test_add_negative(self):
        """Test adding negative numbers."""
        assert add(-2, -3) == -5

    def test_add_mixed(self):
        """Test adding positive and negative."""
        assert add(5, -3) == 2

    def test_add_zero(self):
        """Test adding zero."""
        assert add(5, 0) == 5
