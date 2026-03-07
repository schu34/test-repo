# Dynamic Programming: Coin Change
# =================================
#
# The coin change problem is one of the most instructive DP examples after
# Fibonacci because it shows exactly the same two properties --
#
#   1. Optimal substructure  - the minimum number of coins for amount A can be
#                              built from the minimum for A - coin[i].
#   2. Overlapping subproblems - many different coin combinations reduce to
#                               the same smaller amount.
#
# Problem statement
# -----------------
# Given a list of coin denominations and a target amount, find the minimum
# number of coins needed to make that amount.  If the amount cannot be made,
# return -1.
#
# Example:
#   coins  = [1, 5, 10, 25]   (penny, nickel, dime, quarter)
#   amount = 36
#   answer = 3  (25 + 10 + 1)


# ------------------------------------------------------------
# Step 1: Naive Recursion (brute-force)
# ------------------------------------------------------------
#
# At each step we try every coin.  For coin c we need
#   1 + solve(amount - c)
# coins.  We take the minimum over all valid choices.

def coin_change_recursive(coins, amount):
    """Return the minimum number of coins to make 'amount'.  Naive recursion."""
    # Base cases
    if amount == 0:
        return 0          # no coins needed for amount zero
    if amount < 0:
        return float('inf')  # impossible

    # Try every coin and return the best result
    best = float('inf')
    for coin in coins:
        sub = coin_change_recursive(coins, amount - coin)
        if sub != float('inf'):
            best = min(best, 1 + sub)

    return best if best != float('inf') else -1

# Time complexity: O(S^n) where S = amount and n = len(coins).
# Exponential -- unusable for large inputs.


# ------------------------------------------------------------
# Step 2: Top-Down DP (Memoization)
# ------------------------------------------------------------
#
# We cache the answer for every amount we've already solved.
# The rest of the logic is identical to the recursive version.

def coin_change_memoized(coins, amount, cache=None):
    """Minimum coins to make 'amount' -- top-down DP (memoization)."""
    if cache is None:
        cache = {}

    if amount in cache:
        return cache[amount]
    if amount == 0:
        return 0
    if amount < 0:
        return float('inf')

    best = float('inf')
    for coin in coins:
        sub = coin_change_memoized(coins, amount - coin, cache)
        if sub != float('inf'):
            best = min(best, 1 + sub)

    cache[amount] = best if best != float('inf') else -1
    return cache[amount]

# Each unique amount is computed exactly once.
# Time complexity:  O(S * n)  -- S amounts, n coins each
# Space complexity: O(S)       -- cache + call stack


# ------------------------------------------------------------
# Step 3: Bottom-Up DP (Tabulation)
# ------------------------------------------------------------
#
# Build a table dp where dp[a] = minimum coins needed to make amount a.
#
# Recurrence:
#   dp[0] = 0
#   dp[a] = 1 + min(dp[a - c] for c in coins if a - c >= 0)
#
# We fill the table from a=1 up to a=amount so every sub-answer is ready
# when it is needed.

def coin_change(coins, amount):
    """Minimum coins to make 'amount' -- bottom-up DP (tabulation)."""
    # Use amount+1 as a sentinel for "impossible" (more coins than we'd ever
    # need), so we can work with plain integers instead of float('inf').
    INF = amount + 1
    dp = [INF] * (amount + 1)
    dp[0] = 0  # base case: 0 coins for amount 0

    for a in range(1, amount + 1):
        for coin in coins:
            if coin <= a:
                dp[a] = min(dp[a], 1 + dp[a - coin])

    return dp[amount] if dp[amount] != INF else -1

# Time complexity:  O(S * n)
# Space complexity: O(S)
#
# This is the version you'll see in most textbooks and interviews.
# The table makes it very concrete: we're building the answer for each
# amount from the ground up, never revisiting completed work.


# ------------------------------------------------------------
# Bonus: Reconstructing the coins chosen
# ------------------------------------------------------------
#
# Knowing the count is useful, but sometimes we need to know *which* coins
# were chosen.  We do this by recording, for each amount, which coin
# produced the optimal result.

def coin_change_with_coins(coins, amount):
    """Return (min_count, [coins_used]).  Returns (-1, []) if impossible."""
    INF = amount + 1
    dp = [INF] * (amount + 1)
    dp[0] = 0
    # For each amount, remember which coin step got us there optimally
    last_coin = [-1] * (amount + 1)

    for a in range(1, amount + 1):
        for coin in coins:
            if coin <= a and 1 + dp[a - coin] < dp[a]:
                dp[a] = 1 + dp[a - coin]
                last_coin[a] = coin

    if dp[amount] == INF:
        return -1, []

    # Backtrack through last_coin to reconstruct the solution
    chosen = []
    remaining = amount
    while remaining > 0:
        chosen.append(last_coin[remaining])
        remaining -= last_coin[remaining]

    return dp[amount], chosen


# ------------------------------------------------------------
# Putting It All Together
# ------------------------------------------------------------

if __name__ == "__main__":
    import time

    COINS  = [1, 5, 10, 25]  # U.S. coin denominations
    AMOUNT = 36

    print("=== Coin Change Tutorial: Comparing DP Approaches ===\n")
    print(f"Coins  = {COINS}")
    print(f"Amount = {AMOUNT}\n")

    # --- Naive recursion (small amount only -- it's exponential!) ---
    small = 15
    start = time.perf_counter()
    r_naive = coin_change_recursive(COINS, small)
    elapsed_naive = time.perf_counter() - start
    print(f"Naive recursion    amount={small:>3}  -> {r_naive} coins  (took {elapsed_naive:.6f}s)")
    print("  (using a smaller amount because naive recursion is exponential)\n")

    # --- Memoization ---
    start = time.perf_counter()
    r_memo = coin_change_memoized(COINS, AMOUNT)
    elapsed_memo = time.perf_counter() - start
    print(f"Memoization        amount={AMOUNT:>3}  -> {r_memo} coins  (took {elapsed_memo:.6f}s)")

    # --- Tabulation ---
    start = time.perf_counter()
    r_tab = coin_change(COINS, AMOUNT)
    elapsed_tab = time.perf_counter() - start
    print(f"Tabulation         amount={AMOUNT:>3}  -> {r_tab} coins  (took {elapsed_tab:.6f}s)")

    # --- With reconstruction ---
    count, chosen = coin_change_with_coins(COINS, AMOUNT)
    print(f"Coins used: {chosen}  (sum = {sum(chosen)})\n")

    assert r_memo == r_tab == count, "Mismatch between approaches!"
    print("All approaches agree. DP works!\n")

    # Edge cases
    print("Edge cases:")
    print(f"  amount=0  -> {coin_change(COINS, 0)} coins  (expected 0)")
    print(f"  amount=3 with coins=[2] -> {coin_change([2], 3)} coins  (expected -1, impossible)")

    # ------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------
    #
    # Approach        | Time      | Space | Notes
    # ----------------|-----------|-------|-----------------------------
    # Naive recursion | O(S^n)    | O(S)  | Exponential; educational only
    # Memoization     | O(S * n)  | O(S)  | Top-down; easy to write
    # Tabulation      | O(S * n)  | O(S)  | Bottom-up; no recursion risk
    #
    # Key takeaways:
    #   - Define the subproblem clearly: dp[a] = min coins for amount a.
    #   - Write the recurrence: dp[a] = 1 + min(dp[a-c] for valid coins c).
    #   - Fill the table in order so dependencies are already computed.
    #   - Reconstruct the solution by recording choices during tabulation.
