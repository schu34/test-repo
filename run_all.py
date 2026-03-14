#!/usr/bin/env python3
"""
run_all.py
----------
Runs all classic dynamic programming problems in one go.

Problems included:
  1. Fibonacci          (fibonacci.py)
  2. Coin Change        (coin_change.py)
  3. 0/1 Knapsack       (knapsack.py)
  4. Longest Common     (longest_common_subsequence.py)
     Subsequence
"""

import time

DIVIDER = "%" * 60


# ------------------------------------------------------------------ #
# 1. Fibonacci                                                         #
# ------------------------------------------------------------------ #
def run_fibonacci():
    from fibonacci import fibonacci_recursive, fibonacci_memoized, fibonacci_tabulation, fibonacci

    print(DIVIDER)
    print("PROBLEM 1: Fibonacci")
    print(DIVIDER)

    N = 30
    COUNT = 10

    start = time.perf_counter()
    r_naive = fibonacci_recursive(N)
    t_naive = time.perf_counter() - start

    start = time.perf_counter()
    r_memo = fibonacci_memoized(N)
    t_memo = time.perf_counter() - start

    start = time.perf_counter()
    r_tab = fibonacci_tabulation(N + 1)[N]
    t_tab = time.perf_counter() - start

    start = time.perf_counter()
    r_opt = fibonacci(N + 1)[N]
    t_opt = time.perf_counter() - start

    print(f"Naive recursion    F({N}) = {r_naive:>8}  ({t_naive:.4f}s)")
    print(f"Memoization        F({N}) = {r_memo:>8}  ({t_memo:.6f}s)")
    print(f"Tabulation         F({N}) = {r_tab:>8}  ({t_tab:.6f}s)")
    print(f"Space-optimized    F({N}) = {r_opt:>8}  ({t_opt:.6f}s)")
    print(f"\nFirst {COUNT} Fibonacci numbers: {fibonacci(COUNT)}")
    assert r_naive == r_memo == r_tab == r_opt, "Fibonacci: mismatch between approaches!"
    print("All approaches agree.\n")


# ------------------------------------------------------------------ #
# 2. Coin Change                                                        #
# ------------------------------------------------------------------ #
def run_coin_change():
    from coin_change import coin_change_recursive, coin_change_memoized, coin_change, coin_change_with_coins

    print(DIVIDER)
    print("PROBLEM 2: Coin Change")
    print(DIVIDER)

    COINS = [1, 5, 10, 25]
    AMOUNT = 36
    SMALL = 15   # used for exponential naive version

    print(f"Coins  = {COINS}")
    print(f"Amount = {AMOUNT}\n")

    start = time.perf_counter()
    r_naive = coin_change_recursive(COINS, SMALL)
    t_naive = time.perf_counter() - start
    print(f"Naive recursion    amount={SMALL:>3}  -> {r_naive} coins  ({t_naive:.6f}s)")
    print("  (smaller amount used -- naive recursion is exponential)")

    start = time.perf_counter()
    r_memo = coin_change_memoized(COINS, AMOUNT)
    t_memo = time.perf_counter() - start
    print(f"Memoization        amount={AMOUNT:>3}  -> {r_memo} coins  ({t_memo:.6f}s)")

    start = time.perf_counter()
    r_tab = coin_change(COINS, AMOUNT)
    t_tab = time.perf_counter() - start
    print(f"Tabulation         amount={AMOUNT:>3}  -> {r_tab} coins  ({t_tab:.6f}s)")

    count, chosen = coin_change_with_coins(COINS, AMOUNT)
    print(f"Coins used: {chosen}  (sum = {sum(chosen)})")

    assert r_memo == r_tab == count, "Coin Change: mismatch between approaches!"
    print("All approaches agree.\n")


# ------------------------------------------------------------------ #
# 3. 0/1 Knapsack                                                       #
# ------------------------------------------------------------------ #
def run_knapsack():
    from knapsack import (knapsack_recursive, knapsack_memoized,
                          knapsack, knapsack_space_optimized, knapsack_with_items)

    print(DIVIDER)
    print("PROBLEM 3: 0/1 Knapsack")
    print(DIVIDER)

    weights  = [1, 3, 4, 5]
    values   = [1, 4, 5, 7]
    capacity = 7

    print(f"Items (weight, value): {list(zip(weights, values))}")
    print(f"Capacity: {capacity}\n")

    start = time.perf_counter()
    r_naive = knapsack_recursive(weights, values, capacity)
    t_naive = time.perf_counter() - start
    print(f"Naive recursion    -> max value = {r_naive}  ({t_naive:.6f}s)")

    start = time.perf_counter()
    r_memo = knapsack_memoized(weights, values, capacity)
    t_memo = time.perf_counter() - start
    print(f"Memoization        -> max value = {r_memo}  ({t_memo:.6f}s)")

    start = time.perf_counter()
    r_tab = knapsack(weights, values, capacity)
    t_tab = time.perf_counter() - start
    print(f"Tabulation         -> max value = {r_tab}  ({t_tab:.6f}s)")

    start = time.perf_counter()
    r_opt = knapsack_space_optimized(weights, values, capacity)
    t_opt = time.perf_counter() - start
    print(f"Space-optimized    -> max value = {r_opt}  ({t_opt:.6f}s)")

    max_val, chosen_items = knapsack_with_items(weights, values, capacity)
    print(f"\nChosen items (0-indexed): {chosen_items}")
    for idx in chosen_items:
        print(f"  item {idx}: weight={weights[idx]}, value={values[idx]}")
    print(f"  Total weight: {sum(weights[i] for i in chosen_items)} / {capacity}")
    print(f"  Total value:  {sum(values[i] for i in chosen_items)}")

    assert r_naive == r_memo == r_tab == r_opt == max_val, "Knapsack: mismatch between approaches!"
    print("All approaches agree.\n")


# ------------------------------------------------------------------ #
# 4. Longest Common Subsequence                                         #
# ------------------------------------------------------------------ #
def run_lcs():
    from longest_common_subsequence import (lcs_recursive, lcs_memoized,
                                            lcs, lcs_space_optimized,
                                            lcs_with_sequence)

    print(DIVIDER)
    print("PROBLEM 4: Longest Common Subsequence (LCS)")
    print(DIVIDER)

    X = "ABCBDAB"
    Y = "BDCABA"

    print(f"X = {X!r}")
    print(f"Y = {Y!r}\n")

    start = time.perf_counter()
    r_naive = lcs_recursive(X, Y)
    t_naive = time.perf_counter() - start
    print(f"Naive recursion    -> LCS length = {r_naive}  ({t_naive:.6f}s)")

    start = time.perf_counter()
    r_memo = lcs_memoized(X, Y)
    t_memo = time.perf_counter() - start
    print(f"Memoization        -> LCS length = {r_memo}  ({t_memo:.6f}s)")

    start = time.perf_counter()
    r_tab = lcs(X, Y)
    t_tab = time.perf_counter() - start
    print(f"Tabulation         -> LCS length = {r_tab}  ({t_tab:.6f}s)")

    start = time.perf_counter()
    r_opt = lcs_space_optimized(X, Y)
    t_opt = time.perf_counter() - start
    print(f"Space-optimized    -> LCS length = {r_opt}  ({t_opt:.6f}s)")

    length, subseq = lcs_with_sequence(X, Y)
    print(f"\nOne LCS: {subseq!r}  (length {length})")

    assert r_naive == r_memo == r_tab == r_opt == length, "LCS: mismatch between approaches!"
    print("All approaches agree.\n")


# ------------------------------------------------------------------ #
# Entry point                                                           #
# ------------------------------------------------------------------ #
if __name__ == "__main__":
    print("\n" + DIVIDER)
    print("  CLASSIC DP PROBLEMS -- ALL IN ONE")
    print(DIVIDER + "\n")

    overall_start = time.perf_counter()

    run_fibonacci()
    run_coin_change()
    run_knapsack()
    run_lcs()

    overall_elapsed = time.perf_counter() - overall_start

    print(DIVIDER)
    print(f"All problems completed successfully in {overall_elapsed:.4f}s")
    print(DIVIDER + "\n")
