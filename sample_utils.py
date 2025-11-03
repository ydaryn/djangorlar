"""
sample_utils.py

A utilities module with multiple functions, classes and a demo.
This file intentionally contains 50+ lines to satisfy the task requirement.
"""

from typing import List, Dict, Any
import math
import random
import datetime

def generate_random_numbers(n: int, low: int = 0, high: int = 100) -> List[int]:
    if n <= 0:
        return []
    return [random.randint(low, high) for _ in range(n)]

def stats(numbers: List[int]) -> Dict[str, Any]:
    if not numbers:
        return {'count': 0, 'mean': None, 'min': None, 'max': None}
    count = len(numbers)
    total = sum(numbers)
    mean = total / count
    minimum = min(numbers)
    maximum = max(numbers)
    variance = sum((x - mean) ** 2 for x in numbers) / count
    stddev = math.sqrt(variance)
    return {
        'count': count,
        'mean': mean,
        'min': minimum,
        'max': maximum,
        'variance': variance,
        'stddev': stddev,
    }

class SimpleDB:
    """A tiny in-memory key-value store for demo/testing purposes."""
    def __init__(self):
        self._store = {}
        self._history = []

    def set(self, key: str, value: Any):
        old = self._store.get(key)
        self._store[key] = value
        self._history.append(('set', key, old, value, datetime.datetime.now()))

    def get(self, key: str, default=None):
        return self._store.get(key, default)

    def delete(self, key: str):
        if key in self._store:
            old = self._store.pop(key)
            self._history.append(('delete', key, old, None, datetime.datetime.now()))
            return True
        return False

    def history(self):
        return list(self._history)

def merge_dicts(a: Dict[str, Any], b: Dict[str, Any]) -> Dict[str, Any]:
    """Merge two dicts in a stable way: keys from b overwrite a; nested dicts merge recursively."""
    result = dict(a)
    for k, v in b.items():
        if isinstance(v, dict) and isinstance(result.get(k), dict):
            result[k] = merge_dicts(result[k], v)
        else:
            result[k] = v
    return result

def demo_usage():
    print('--- demo usage of sample_utils ---')
    nums = generate_random_numbers(10, 1, 50)
    print('nums:', nums)
    s = stats(nums)
    print('stats:', s)
    db = SimpleDB()
    db.set('numbers', nums)
    db.set('stats', s)
    db.set('config', {'a': 1, 'b': {'x': 1}})
    db.set('config', merge_dicts(db.get('config'), {'b': {'y': 2}, 'c': 3}))
    print('db.get config:', db.get('config'))
    db.delete('unused_key')
    print('history length:', len(db.history()))

if __name__ == '__main__':
    demo_usage()
