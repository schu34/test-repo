# Dynamic Programming: Longest Common Subsequence (LCS)
# ======================================================
#
# The Longest Common Subsequence (LCS) problem is a classic application of
# 2-D DP that shows up in diff tools, bioinformatics, spell-checkers, and
# version control systems.
#
# Problem statement
# -----------------
# Given two sequences (strings or lists) X and Y, find the length of the
# longest subsequence that appears in both X and Y.  A *subsequence* is any
# subset of elements taken in order but not necessarily contiguous.
#
# Example:
#   X = "ABCBDAB"
#   Y = "BDCABA"
#   LCS length = 4   (e.g., "BCBA" or "BDAB")
#
# Why DP?
# -------
#   Optimal substructure  - LCS(X, Y) can be built from LCS(X[:-1], Y),
#                           LCS(X, Y[:-1]), or LCS(X[:-1], Y[:-1]) + 1.
#   Overlapping subproblems - the same (i, j) suffix pair is solved many
#                             times in the naive recursion.


# ------------------------------------------------------------
# Step 1: Naive Recursion (brute-force)
# ------------------------------------------------------------
#
# Recurrence:
#   lcs(i, j) = 0                          if i==0 or j==0  (empty sequence)
#   lcs(i, j) = lcs(i-1, j-1) + 1         if X[i-1] == Y[j-1]
#   lcs(i, j) = max(lcs(i-1, j),
#                   lcs(i, j-1))           otherwise
#
# Here i, j are the lengths of the prefixes we're currently considering.

def lcs_recursive(X, Y, i=None, j=None):
    """Length of LCS of X[:i] and Y[:j].  Naive recursion."""
    if i is None: i = len(X)
    if j is None: j = len(Y)

    # Base case: one sequence is empty
    if i == 0 or j == 0:
        return 0

    if X[i - 1] == Y[j - 1]:
        # Last characters match -- they must be in the LCS
        return 1 + lcs_recursive(X, Y, i - 1, j - 1)
    else:
        # Try dropping the last character of X or Y
        return max(lcs_recursive(X, Y, i - 1, j),
                   lcs_recursive(X, Y, i,     j - 1))

# Time complexity: O(2^(m+n)) in the worst case (every pair of characters
# differs).  Completely impractical for long strings.


# ------------------------------------------------------------
# Step 2: Top-Down DP (Memoization)
# ------------------------------------------------------------
#
# Cache the result for every (i, j) prefix pair we've already solved.

def lcs_memoized(X, Y, i=None, j=None, cache=None):
    """Length of LCS -- top-down DP (memoization)."""
    if i is None: i = len(X)
    if j is None: j = len(Y)
    if cache is None: cache = {}

    if i == 0 or j == 0:
        return 0
    if (i, j) in cache:
        return cache[(i, j)]

    if X[i - 1] == Y[j - 1]:
        result = 1 + lcs_memoized(X, Y, i - 1, j - 1, cache)
    else:
        result = max(lcs_memoized(X, Y, i - 1, j,     cache),
                     lcs_memoized(X, Y, i,     j - 1, cache))

    cache[(i, j)] = result
    return result

# Time complexity:  O(m * n)  -- at most m*n unique (i, j) pairs
# Space complexity: O(m * n)  -- cache + call stack


# ------------------------------------------------------------
# Step 3: Bottom-Up DP (Tabulation)
# ------------------------------------------------------------
#
# Build an (m+1) x (n+1) table where dp[i][j] = LCS length for X[:i], Y[:j].
#
#   dp[0][j] = 0  for all j   (X is empty)
#   dp[i][0] = 0  for all i   (Y is empty)
#   dp[i][j] = dp[i-1][j-1] + 1             if X[i-1] == Y[j-1]
#   dp[i][j] = max(dp[i-1][j], dp[i][j-1])  otherwise

def lcs(X, Y):
    """Length of LCS of X and Y -- bottom-up DP (tabulation)."""
    m, n = len(X), len(Y)
    # (m+1) x (n+1) table; row 0 and column 0 are the base cases (all zeros)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if X[i - 1] == Y[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    return dp[m][n]

# Time complexity:  O(m * n)
# Space complexity: O(m * n)
#
# The table is very revealing.  Every cell says: "the best I can do using
# the first i characters of X and the first j characters of Y."


# ------------------------------------------------------------
# Bonus: Reconstructing the actual subsequence
# ------------------------------------------------------------
#
# With the full dp table we can trace back through it to find the characters
# that form one LCS.

def lcs_with_sequence(X, Y):
    """Return (length, subsequence_string).  Builds and backtracks the table."""
    m, n = len(X), len(Y)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if X[i - 1] == Y[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    # Backtrack to reconstruct the LCS
    result = []
    i, j = m, n
    while i > 0 and j > 0:
        if X[i - 1] == Y[j - 1]:
            result.append(X[i - 1])  # this character is in the LCS
            i -= 1
            j -= 1
        elif dp[i - 1][j] >= dp[i][j - 1]:
            i -= 1  # came from above
        else:
            j -= 1  # came from the left

    result.reverse()
    return dp[m][n], "".join(result)


# ------------------------------------------------------------
# Bonus 2: Space-Optimized LCS (length only)
# ------------------------------------------------------------
#
# dp[i][j] depends only on the current row and the previous row, so we can
# reduce space to O(n) by keeping just two rows.

def lcs_space_optimized(X, Y):
    """Length of LCS -- space-optimized (two 1-D rows)."""
    m, n = len(X), len(Y)
    prev = [0] * (n + 1)

    for i in range(1, m + 1):
        curr = [0] * (n + 1)
        for j in range(1, n + 1):
            if X[i - 1] == Y[j - 1]:
                curr[j] = prev[j - 1] + 1
            else:
                curr[j] = max(prev[j], curr[j - 1])
        prev = curr

    return prev[n]

# Time complexity:  O(m * n)
# Space complexity: O(n)


# ------------------------------------------------------------
# Putting It All Together
# ------------------------------------------------------------

if __name__ == "__main__":
    import time

    X = "ABCBDAB"
    Y = "BDCABA"

    print("=== LCS Tutorial: Comparing DP Approaches ===\n")
    print(f"X = {X!r}")
    print(f"Y = {Y!r}\n")

    # --- Naive recursion ---
    start = time.perf_counter()
    r_naive = lcs_recursive(X, Y)
    elapsed_naive = time.perf_counter() - start
    print(f"Naive recursion    -> LCS length = {r_naive}  (took {elapsed_naive:.6f}s)")

    # --- Memoization ---
    start = time.perf_counter()
    r_memo = lcs_memoized(X, Y)
    elapsed_memo = time.perf_counter() - start
    print(f"Memoization        -> LCS length = {r_memo}  (took {elapsed_memo:.6f}s)")

    # --- Tabulation ---
    start = time.perf_counter()
    r_tab = lcs(X, Y)
    elapsed_tab = time.perf_counter() - start
    print(f"Tabulation         -> LCS length = {r_tab}  (took {elapsed_tab:.6f}s)")

    # --- Space-optimized ---
    start = time.perf_counter()
    r_opt = lcs_space_optimized(X, Y)
    elapsed_opt = time.perf_counter() - start
    print(f"Space-optimized    -> LCS length = {r_opt}  (took {elapsed_opt:.6f}s)")

    # --- With reconstruction ---
    length, subseq = lcs_with_sequence(X, Y)
    print(f"\nOne LCS: {subseq!r}  (length {length})\n")

    assert r_naive == r_memo == r_tab == r_opt == length, \
        "Mismatch between approaches!"
    print("All approaches agree. DP works!\n")

    # A longer example to show the speed difference
    import random, string
    random.seed(42)
    long_X = "".join(random.choices(string.ascii_uppercase[:6], k=500))
    long_Y = "".join(random.choices(string.ascii_uppercase[:6], k=500))

    start = time.perf_counter()
    lcs(long_X, long_Y)
    print(f"Tabulation on 500-char strings: {time.perf_counter() - start:.4f}s")

    start = time.perf_counter()
    lcs_space_optimized(long_X, long_Y)
    print(f"Space-optimized on 500-char strings: {time.perf_counter() - start:.4f}s")

    # ------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------
    #
    # Approach          | Time     | Space    | Notes
    # ------------------|----------|----------|---------------------------
    # Naive recursion   | O(2^m+n) | O(m+n)   | Exponential; impractical
    # Memoization       | O(m*n)   | O(m*n)   | Top-down; natural to write
    # Tabulation        | O(m*n)   | O(m*n)   | Bottom-up; no stack risk
    # Space-optimized   | O(m*n)   | O(n)     | Length only; can't backtrack
    #
    # Key takeaways:
    #   - The 2-D DP table is natural when the state depends on two sequences.
    #   - Backtracking through the table reconstructs the actual subsequence.
    #   - LCS is closely related to edit distance (Levenshtein), diff output,
    #     and sequence alignment in bioinformatics.
    #   - The same pattern extends to Longest Common Substring (require
    #     contiguous match), Longest Increasing Subsequence, and more.
