# Dynamic Programming: A Hands-On Tutorial with Fibonacci
# =========================================================
#
# Dynamic programming (DP) is one of those topics that sounds intimidating
# but becomes intuitive once you see it in action. In this tutorial, we'll
# use the Fibonacci sequence as our running example to build up from a naive
# recursive solution all the way to an optimal DP approach.
#
# What is dynamic programming?
# -----------------------------
# DP is an algorithmic technique for solving problems by breaking them into
# overlapping subproblems and storing the results so we never compute the
# same thing twice. Two key properties signal that DP might help:
#
#   1. Optimal substructure  - the solution can be built from solutions to
#                              smaller subproblems.
#   2. Overlapping subproblems - the same subproblems recur many times.
#
# Fibonacci is the classic teaching example because both properties are
# immediately visible.


# ------------------------------------------------------------
# Step 1: The Naive Recursive Solution
# ------------------------------------------------------------
#
# The mathematical definition of Fibonacci is recursive:
#
#   F(0) = 0
#   F(1) = 1
#   F(n) = F(n-1) + F(n-2)  for n >= 2
#
# Translating that directly into code gives us:

def fibonacci_recursive(n):
    """Return the nth Fibonacci number (0-indexed). Naive recursive version."""
    # Base cases: F(0) = 0, F(1) = 1
    if n <= 1:
        return n
    # Recursive case: add the two preceding values
    return fibonacci_recursive(n - 1) + fibonacci_recursive(n - 2)

# This is beautifully simple, but it has a serious problem.
# Try calling fibonacci_recursive(40) and watch how long it takes.
#
# Why is it slow? Because we recompute the same values over and over.
# For example, computing F(5) requires F(4) and F(3). Computing F(4)
# *also* requires F(3). So F(3) is computed at least twice -- and the
# redundancy grows exponentially as n increases.
#
# The time complexity of the naive recursion is O(2^n). For n=50 that is
# over a quadrillion calls. Not great.


# ------------------------------------------------------------
# Step 2: Top-Down DP (Memoization)
# ------------------------------------------------------------
#
# The fix is simple: remember every result the first time we compute it,
# and look it up instead of recomputing it on subsequent calls. This
# technique is called *memoization* (from "memo", not "memory").
#
# We keep a cache (dictionary) that maps n -> F(n). Before doing any
# work we check the cache; if the answer is already there, we return it
# immediately.

def fibonacci_memoized(n, cache=None):
    """Return the nth Fibonacci number using top-down DP (memoization)."""
    # Initialize the cache on the first call
    if cache is None:
        cache = {}

    # If we've already solved this subproblem, return the cached result
    if n in cache:
        return cache[n]

    # Base cases
    if n <= 1:
        return n

    # Solve the subproblems, store the result, then return it
    cache[n] = fibonacci_memoized(n - 1, cache) + fibonacci_memoized(n - 2, cache)
    return cache[n]

# Now each unique value of n is computed exactly once, so the time
# complexity drops to O(n) -- a massive improvement.
#
# Python's standard library even ships a decorator for this pattern:
#
#   from functools import lru_cache
#
#   @lru_cache(maxsize=None)
#   def fibonacci_lru(n):
#       if n <= 1:
#           return n
#       return fibonacci_lru(n - 1) + fibonacci_lru(n - 2)
#
# Under the hood, lru_cache does exactly what our cache dictionary does.
#
# Top-down DP is a great starting point because the structure mirrors the
# mathematical recurrence closely. The downside is call-stack overhead: for
# very large n Python will hit its recursion limit.


# ------------------------------------------------------------
# Step 3: Bottom-Up DP (Tabulation)
# ------------------------------------------------------------
#
# Instead of starting at F(n) and recursing downward, we can flip the
# direction: start at F(0) and F(1), then iteratively build up to F(n).
# This is called *tabulation* because we fill in a table of results.
#
# The table (a list here) plays the same role as the cache above -- it
# stores previously computed answers -- but we populate it in a deliberate
# order so every subproblem is ready before it is needed.

def fibonacci_tabulation(n):
    """Return the first n Fibonacci numbers using bottom-up DP (tabulation)."""
    if n == 0:
        return []
    if n == 1:
        return [0]

    # Initialize the DP table with the two base cases
    dp = [0] * n
    dp[0] = 0  # F(0)
    dp[1] = 1  # F(1)

    # Fill the table from left to right.
    # At each step, dp[i] = dp[i-1] + dp[i-2], which are already computed.
    for i in range(2, n):
        dp[i] = dp[i - 1] + dp[i - 2]

    return dp

# Time complexity: O(n)  -- same as memoization, no recursion overhead.
# Space complexity: O(n) -- we store all n values in the table.
#
# Notice how explicit the "overlapping subproblems" property is here:
# dp[i] depends on dp[i-1] and dp[i-2], both of which sit right next to
# it in the table, already filled in.


# ------------------------------------------------------------
# Step 4: Space-Optimized DP
# ------------------------------------------------------------
#
# Look at the recurrence again: F(n) = F(n-1) + F(n-2).
# To compute the next value we only ever need the *two most recent* values.
# We don't actually need the whole table -- just two variables.
#
# This is a common DP optimization: once you have the tabulation solution,
# ask yourself "how many previous rows/values do I actually need?" If the
# answer is a small constant, you can reduce memory usage accordingly.

def fibonacci(n):
    """Return the first n Fibonacci numbers using space-optimized DP."""
    fibs = []
    # prev = F(i-2), curr = F(i-1)
    prev, curr = 0, 1

    for _ in range(n):
        fibs.append(prev)
        # Advance both pointers in a single step (no temporary variable needed
        # thanks to Python's tuple unpacking)
        prev, curr = curr, prev + curr

    return fibs

# Time complexity:  O(n)
# Space complexity: O(1) extra space (beyond the output list itself)
#
# This is the version you'd use in production for Fibonacci specifically.
# For more complex DP problems (grids, knapsack, etc.) you often need the
# full table -- but the principle of "do I need the whole table?" always
# applies.


# ------------------------------------------------------------
# Putting It All Together
# ------------------------------------------------------------
#
# Let's run all four approaches and compare their outputs to confirm they
# all agree, then time them so the performance difference is concrete.

if __name__ == "__main__":
    import time

    N = 30  # index for single-value comparisons
    COUNT = 10  # how many terms to display in the sequence

    print("=== Fibonacci Tutorial: Comparing DP Approaches ===\n")

    # --- Naive recursion ---
    start = time.perf_counter()
    result_naive = fibonacci_recursive(N)
    elapsed_naive = time.perf_counter() - start
    print(f"Naive recursion    F({N}) = {result_naive:>8}  (took {elapsed_naive:.4f}s)")

    # --- Memoization ---
    start = time.perf_counter()
    result_memo = fibonacci_memoized(N)
    elapsed_memo = time.perf_counter() - start
    print(f"Memoization        F({N}) = {result_memo:>8}  (took {elapsed_memo:.6f}s)")

    # --- Tabulation ---
    start = time.perf_counter()
    result_tab = fibonacci_tabulation(N + 1)  # +1 to include index N
    elapsed_tab = time.perf_counter() - start
    print(f"Tabulation         F({N}) = {result_tab[N]:>8}  (took {elapsed_tab:.6f}s)")

    # --- Space-optimized ---
    start = time.perf_counter()
    result_opt = fibonacci(N + 1)
    elapsed_opt = time.perf_counter() - start
    print(f"Space-optimized    F({N}) = {result_opt[N]:>8}  (took {elapsed_opt:.6f}s)")

    print()
    print(f"First {COUNT} Fibonacci numbers: {fibonacci(COUNT)}")

    # Sanity check: all approaches produce the same answer
    assert result_naive == result_memo == result_tab[N] == result_opt[N], \
        "Mismatch between approaches -- something is wrong!"
    print("\nAll approaches agree. DP works!")

    # ------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------
    #
    # Approach            | Time      | Space  | Notes
    # --------------------|-----------|--------|---------------------------
    # Naive recursion     | O(2^n)    | O(n)   | Stack frames; exponential
    # Memoization (TD-DP) | O(n)      | O(n)   | Cache + call stack
    # Tabulation  (BU-DP) | O(n)      | O(n)   | Iterative; no stack risk
    # Space-optimized     | O(n)      | O(1)*  | Best for Fibonacci
    #                     |           |        | (* beyond output storage)
    #
    # Key takeaways:
    #   - Identify overlapping subproblems and optimal substructure.
    #   - Cache results (memoization) or build bottom-up (tabulation).
    #   - Once it works, look for space optimizations.
    #   - The same pattern applies to harder problems: longest common
    #     subsequence, knapsack, shortest paths, coin change, and more.
