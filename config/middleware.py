"""
Custom middleware - Python 3.14 compatibility fixes.
"""
from django.template import Context


# Monkey patch for Python 3.14 compatibility
original_copy = Context.__copy__


def patched_copy(self):
    """Fixed __copy__ method for Python 3.14."""
    duplicate = self.__class__()
    # Use dict() instead of direct attribute access
    if hasattr(self, 'dicts'):
        duplicate.dicts = self.dicts[:]
    elif hasattr(self, '_dict'):
        duplicate._dict = self._dict.copy()
    return duplicate


# Apply patch
Context.__copy__ = patched_copy
