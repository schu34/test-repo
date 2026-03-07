# Dynamic Programming: 0/1 Knapsack
# ===================================
#
# The 0/1 knapsack problem is a cornerstone of DP.  It introduces the idea
# of a two-dimensional DP table -- one dimension for items, one for capacity.
#
# Problem statement
# -----------------
# You have a knapsack with a weight capacity W and a list of n items.
# Each item i has:
#   - weight[i]  -- how much it contributes to your weight limit
#   - value[i]   -- how much profit/utility it provides
#
# You may take each item at most once ("0/1" = skip or take).
# Maximize the total value without exceeding W.
#
# Example:
#   capacity = 7
#   weights  = [1, 3, 4, 5]
#   values   = [1, 4, 5, 7]
#   answer   = 9  (take items with weight 3 and 4, value 4+5)
#
# Why DP?
# -------
#   Optimal substructure  - the best packing of capacity c using items 0..i
#                           can be built from best packing of c using 0..i-1.
#   Overlapping subproblems - the same (item, remaining-capacity) pair is
#                             reached by many different item orderings.


# ------------------------------------------------------------
# Step 1: Naive Recursion (brute-force)
# ------------------------------------------------------------
#
# For each item we make a binary choice: take it or leave it.
# We recurse over all 2^n subsets.

def knapsack_recursive(weights, values, capacity, i=None):
    """Max value we can carry -- naive recursion.  i = current item index."""
    if i is None:
        i = len(weights) - 1   # start from the last item

    # Base case: no items left or no capacity remaining
    if i < 0 or capacity == 0:
        return 0

    # If the item is too heavy, we must leave it
    if weights[i] > capacity:
        return knapsack_recursive(weights, values, capacity, i - 1)

    # Otherwise try both choices and take the better one
    skip = knapsack_recursive(weights, values, capacity,          i - 1)
    take = knapsack_recursive(weights, values, capacity - weights[i], i - 1) + values[i]
    return max(skip, take)

# Time complexity: O(2^n) -- one branch per item.
# Unusable for n > ~20.


# ------------------------------------------------------------
# Step 2: Top-Down DP (Memoization)
# ------------------------------------------------------------
#
# The recursive solution has *overlapping subproblems*: the same (i, capacity)
# pair is solved many times.  We cache results in a dictionary.

def knapsack_memoized(weights, values, capacity, i=None, cache=None):
    """Max value -- top-down DP (memoization)."""
    if i is None:
        i = len(weights) - 1
    if cache is None:
        cache = {}

    if i < 0 or capacity == 0:
        return 0

    if (i, capacity) in cache:
        return cache[(i, capacity)]

    if weights[i] > capacity:
        result = knapsack_memoized(weights, values, capacity, i - 1, cache)
    else:
        skip = knapsack_memoized(weights, values, capacity,          i - 1, cache)
        take = knapsack_memoized(weights, values, capacity - weights[i], i - 1, cache) + values[i]
        result = max(skip, take)

    cache[(i, capacity)] = result
    return result

# Time complexity:  O(n * W)  -- at most n*W unique (i, capacity) pairs
# Space complexity: O(n * W)  -- cache + call stack


# ------------------------------------------------------------
# Step 3: Bottom-Up DP (Tabulation)
# ------------------------------------------------------------
#
# Build a 2-D table:
#
#   dp[i][c] = maximum value using items 0..i with capacity c
#
# Recurrence:
#   dp[i][c] = dp[i-1][c]                              if weights[i] > c
#   dp[i][c] = max(dp[i-1][c],
#                  dp[i-1][c - weights[i]] + values[i]) otherwise
#
# Base case: dp[-1][c] = 0 for all c  (no items => zero value).
# We represent "no items" as row 0 filled with zeros, and items as rows 1..n.

def knapsack(weights, values, capacity):
    """Max value -- bottom-up DP (tabulation).  Returns the value."""
    n = len(weights)
    # dp[i][c]: best value using first i items with capacity c
    # Row 0 is the base case (0 items): all zeros.
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        w = weights[i - 1]
        v = values[i - 1]
        for c in range(capacity + 1):
            # Option A: leave item i out
            dp[i][c] = dp[i - 1][c]
            # Option B: take item i (only if it fits)
            if w <= c:
                dp[i][c] = max(dp[i][c], dp[i - 1][c - w] + v)

    return dp[n][capacity]

# Time complexity:  O(n * W)
# Space complexity: O(n * W)  -- the full table


# ------------------------------------------------------------
# Step 4: Space-Optimized Bottom-Up DP
# ------------------------------------------------------------
#
# Notice that dp[i][c] only ever looks at row i-1.  We can keep just one
# row and update it in place, as long as we iterate capacity from right
# to left (so we don't accidentally use the "new" value of a smaller
# capacity in the same row).

def knapsack_space_optimized(weights, values, capacity):
    """Max value -- space-optimized bottom-up DP (1-D table)."""
    n = len(weights)
    dp = [0] * (capacity + 1)  # dp[c] = best value with capacity c so far

    for i in range(n):
        w = weights[i]
        v = values[i]
        # Iterate from right to left to avoid using item i more than once
        for c in range(capacity, w - 1, -1):
            dp[c] = max(dp[c], dp[c - w] + v)

    return dp[capacity]

# Time complexity:  O(n * W)
# Space complexity: O(W)  -- single 1-D array instead of full table


# ------------------------------------------------------------
# Bonus: Reconstructing which items were chosen
# ------------------------------------------------------------
#
# We need the full 2-D table to trace back the solution.

def knapsack_with_items(weights, values, capacity):
    """Return (max_value, [item_indices]).  Items are 0-indexed."""
    n = len(weights)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        w = weights[i - 1]
        v = values[i - 1]
        for c in range(capacity + 1):
            dp[i][c] = dp[i - 1][c]
            if w <= c:
                dp[i][c] = max(dp[i][c], dp[i - 1][c - w] + v)

    # Backtrack to find chosen items
    chosen = []
    c = capacity
    for i in range(n, 0, -1):
        if dp[i][c] != dp[i - 1][c]:
            # Item i was taken (convert to 0-indexed)
            chosen.append(i - 1)
            c -= weights[i - 1]

    chosen.reverse()
    return dp[n][capacity], chosen


# ------------------------------------------------------------
# Putting It All Together
# ------------------------------------------------------------

if __name__ == "__main__":
    import time

    weights  = [1, 3, 4, 5]
    values   = [1, 4, 5, 7]
    capacity = 7

    print("=== Knapsack Tutorial: Comparing DP Approaches ===\n")
    print(f"Items (weight, value): {list(zip(weights, values))}")
    print(f"Capacity: {capacity}\n")

    # --- Naive recursion ---
    start = time.perf_counter()
    r_naive = knapsack_recursive(weights, values, capacity)
    elapsed_naive = time.perf_counter() - start
    print(f"Naive recursion    -> max value = {r_naive}  (took {elapsed_naive:.6f}s)")

    # --- Memoization ---
    start = time.perf_counter()
    r_memo = knapsack_memoized(weights, values, capacity)
    elapsed_memo = time.perf_counter() - start
    print(f"Memoization        -> max value = {r_memo}  (took {elapsed_memo:.6f}s)")

    # --- Tabulation ---
    start = time.perf_counter()
    r_tab = knapsack(weights, values, capacity)
    elapsed_tab = time.perf_counter() - start
    print(f"Tabulation         -> max value = {r_tab}  (took {elapsed_tab:.6f}s)")

    # --- Space-optimized ---
    start = time.perf_counter()
    r_opt = knapsack_space_optimized(weights, values, capacity)
    elapsed_opt = time.perf_counter() - start
    print(f"Space-optimized    -> max value = {r_opt}  (took {elapsed_opt:.6f}s)")

    # --- With reconstruction ---
    max_val, chosen_items = knapsack_with_items(weights, values, capacity)
    print(f"\nChosen items (0-indexed): {chosen_items}")
    for idx in chosen_items:
        print(f"  item {idx}: weight={weights[idx]}, value={values[idx]}")
    total_w = sum(weights[i] for i in chosen_items)
    total_v = sum(values[i]  for i in chosen_items)
    print(f"  Total weight: {total_w} / {capacity}")
    print(f"  Total value:  {total_v}\n")

    assert r_naive == r_memo == r_tab == r_opt == max_val, \
        "Mismatch between approaches!"
    print("All approaches agree. DP works!")

    # ------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------
    #
    # Approach          | Time     | Space    | Notes
    # ------------------|----------|----------|------------------------
    # Naive recursion   | O(2^n)   | O(n)     | Exponential; impractical
    # Memoization       | O(n*W)   | O(n*W)   | Top-down; natural to write
    # Tabulation        | O(n*W)   | O(n*W)   | Bottom-up; no stack risk
    # Space-optimized   | O(n*W)   | O(W)     | Best for value-only answer
    #
    # Key takeaways:
    #   - The DP state is a pair (item index, remaining capacity).
    #   - Iterating capacity right-to-left in the 1-D version enforces the
    #     "each item used at most once" constraint.
    #   - To reconstruct the solution you need the full 2-D table.
    #   - Many real-world problems (resource allocation, budgeting) reduce
    #     to knapsack; the same template applies.
