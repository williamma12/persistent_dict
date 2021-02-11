import pytest

from RoomDict.LRUCache import LRUCache, CacheRecord

from RoomDict.test.utils import assert_equal

TEST_SIZE = 5
TEST_RECORDS = [(f"test{i}", i) for i in range(10)]

@pytest.fixture
def filled_cache():
    cache = LRUCache(TEST_SIZE)

    for i in range(5):
        key, value = TEST_RECORDS[i]

        evicted_record = cache.put(key, value)
        expected_eviction = None
        
        assert_equal(expected_eviction, evicted_record)

    return cache

def test_put(filled_cache):
    for i in range(5):
        key, value = TEST_RECORDS[i+5]
        evicted_record = filled_cache.put(key, value)

        evicted_key, evicted_value = TEST_RECORDS[i]
        expected_eviction = CacheRecord(evicted_key, evicted_value)

        assert_equal(expected_eviction, evicted_record)

def test_get(filled_cache):
    for i in range(TEST_SIZE):
        key, value = TEST_RECORDS[i]

        actual_record = filled_cache.get(key)
        expected_record = CacheRecord(key, value)

        assert_equal(expected_record, actual_record)

def test_bad_get(filled_cache):
    actual_record = filled_cache.get("BAD_KEY")
    expected_record = None

    assert_equal(expected_record, actual_record)

def test_put_and_get(filled_cache):
    # Get first item to move it to most used.
    first_key, first_value = TEST_RECORDS[0]
    assert_equal(CacheRecord(first_key, first_value), filled_cache.get(first_key))

    # Check that the second to last record is evicted.
    evicted_key, evicted_value = TEST_RECORDS[1]
    new_key, new_value = TEST_RECORDS[TEST_SIZE]

    expected_eviction = CacheRecord(evicted_key, evicted_value)
    actual_eviction = filled_cache.put(new_key, new_value)
    assert_equal(expected_eviction, actual_eviction)

def test_hot_key(filled_cache):
    hot_key, hot_value = TEST_RECORDS[0]
    hot_record = CacheRecord(hot_key, hot_value)

    for i in range(5):
        evicted_key, evicted_value = TEST_RECORDS[i+1]
        new_key, new_value = TEST_RECORDS[i+5]

        actual_hot_record = filled_cache.get(hot_key)
        assert_equal(hot_record, actual_hot_record)

        expected_eviction = CacheRecord(evicted_key, evicted_value)
        actual_eviction = filled_cache.put(new_key, new_value)
        assert_equal(expected_eviction, actual_eviction)