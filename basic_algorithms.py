
# CS121: Analyzing Election Tweets

# Omar Elmasry and Mufitcan Atalay 

# Algorithms for efficiently counting and sorting distinct
# `entities`, or unique values, are widely used in data
# analysis. Functions to implement: count_items, find_top_k,
# find_min_count, find_frequent

# DO NOT REMOVE THESE LINES OF CODE
# pylint: disable-msg=missing-docstring

from util import sort_count_pairs


def count_items(items):
    '''
    Counts each distinct item (entity) in a list of items

    Inputs:
        items: list of items (must be hashable/comparable)

    Returns: list (item, number of occurrences).
    '''

    # YOUR CODE GOES HERE
    entities = {}
    for item in items:
            entities[item] = entities.get(item,0) + 1
    return entities.items()




def find_top_k(items, k):
    '''
    Find the K most frequently occurring items

    Inputs:
        items: list of items (must be hashable/comparable)
        k: a non-negative integer

    Returns: sorted list of the top K tuples

    '''

    # Error checking (DO NOT MODIFY)
    if k < 0:
        raise ValueError("In find_top_k, k must be a non-negative integer")

    # Runs the helper function for you (DO NOT MODIFY)
    item_counts = count_items(items)

    # YOUR CODE GOES HERE
    tiptop = sort_count_pairs(item_counts)
    topk = tiptop[0:k]

    # REPLACE RETURN VALUE WITH AN APPROPRIATE VALUE
    return topk

def find_min_count(items, min_count):
    '''
    Find the items that occur at least min_count times

    Inputs:
        items: a list of items  (must be hashable/comparable)
        min_count: integer

    Returns: sorted list of tuples
    '''

    # Runs the helper function for you (DO NOT MODIFY)
    item_counts = count_items(items)

    # YOUR CODE HERE
    
    minc = []
    tiptop = sort_count_pairs(item_counts)
    for i in range(0, len(tiptop)):
        if tiptop[i][1] >= min_count:
            minc.append(tiptop[i])

    # REPLACE RETURN VALUE WITH AN APPROPRIATE VALUE
    return minc


def find_frequent(items, k):
    '''
    Find items where the number of times the item occurs is at least
    1/k * len(items).

    Input:
        items: a list of items  (must be hashable/comparable)
        k: integer

    Returns: sorted list of tuples
    '''

    counter = {}

    for item in items:
        if item in counter:
            counter[item] += 1
        else:
            if len(counter) > k - 1:
                raise ValueError(
                    "The number of elements stored in counter" +
                    " should not exceed (k-1)=" + str(k-1))
            elif len(counter) < k-1:
                counter[item] = counter.get(1,0) +1
            elif len(counter) == k-1:
                for key in counter.copy():
                    counter[key] -= 1
                    if counter[key] <= 0:
                        del counter[key]

    return sort_count_pairs(counter.items())
