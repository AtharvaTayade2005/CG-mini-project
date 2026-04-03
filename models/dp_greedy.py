class DPGreedyModel:
    def __init__(self):
        pass

    def fractional_knapsack(self, capacity, weights, values):
        n = len(weights)
        items = [(values[i]/weights[i], weights[i], values[i], i) for i in range(n)]
        yield {'type': 'init', 'items': items, 'capacity': capacity, 'msg': "Fractional Knapsack: We calculate the Value-to-Weight ratio for all items."}
        
        items.sort(reverse=True)
        yield {'type': 'sorted', 'items': items, 'capacity': capacity, 'msg': "Greedy choice: We sorted all items based on their ratio, highest first!"}
        
        total_value = 0
        rem_capacity = capacity
        taken = []
        
        for ratio, w, v, orig_idx in items:
            yield {'type': 'checking', 'items': items, 'capacity': capacity, 'rem': rem_capacity, 'current': orig_idx, 'taken': taken, 'msg': f"Checking item (Weight: {w}, Value: {v}). Remaining bag capacity is {rem_capacity}."}
            if w <= rem_capacity:
                rem_capacity -= w
                total_value += v
                taken.append((orig_idx, 1.0)) # 100% taken
                yield {'type': 'taken', 'items': items, 'capacity': capacity, 'rem': rem_capacity, 'current': orig_idx, 'taken': taken, 'total_v': total_value, 'msg': f"Item fully fits! Taking 100%. Total value rises to {total_value:.2f}."}
            else:
                fraction = rem_capacity / w
                total_value += v * fraction
                taken.append((orig_idx, fraction))
                yield {'type': 'taken', 'items': items, 'capacity': capacity, 'rem': 0, 'current': orig_idx, 'taken': taken, 'total_v': total_value, 'msg': f"Item is too big to fit! Greedily taking {fraction*100:.1f}% to perfectly fill the bag."}
                rem_capacity = 0
                break
            
        yield {'type': 'done', 'taken': taken, 'total_v': total_value, 'msg': f"Bag is full! Algorithm complete. Maximum Value achieved: {total_value:.2f}"}

    def zero_one_knapsack(self, capacity, weights, values):
        n = len(weights)
        dp = [[0 for _ in range(capacity + 1)] for _ in range(n + 1)]
        
        yield {'type': 'grid', 'dp': [row[:] for row in dp], 'weights': weights, 'values': values, 'capacity': capacity, 'msg': "0/1 Knapsack: Initializing a DP table of dimensions (Items + 1) x (Capacity + 1) with zeros."}
        
        for i in range(1, n + 1):
            for w in range(1, capacity + 1):
                yield {'type': 'calc', 'dp': [row[:] for row in dp], 'i': i, 'w': w, 'weights': weights, 'values': values, 'capacity': capacity, 'msg': f"Item {i-1} (Weight {weights[i-1]}, Val {values[i-1]}) at capacity {w}. Checking if we can pick it."}
                if weights[i-1] <= w:
                    v_include = values[i-1] + dp[i-1][w-weights[i-1]]
                    v_exclude = dp[i-1][w]
                    if v_include > v_exclude:
                        dp[i][w] = v_include
                        yield {'type': 'updated', 'dp': [row[:] for row in dp], 'i': i, 'w': w, 'weights': weights, 'values': values, 'capacity': capacity, 'msg': f"Yes! It fits. Including it yields (Val {values[i-1]} + DP {dp[i-1][w-weights[i-1]]} = {v_include}) which is > omitting {v_exclude}."}
                    else:
                        dp[i][w] = v_exclude
                        yield {'type': 'updated', 'dp': [row[:] for row in dp], 'i': i, 'w': w, 'weights': weights, 'values': values, 'capacity': capacity, 'msg': f"Yes it fits, but skipping it keeps a HIGHER previous value: {v_exclude}."}
                else:
                    dp[i][w] = dp[i-1][w]
                    yield {'type': 'updated', 'dp': [row[:] for row in dp], 'i': i, 'w': w, 'weights': weights, 'values': values, 'capacity': capacity, 'msg': f"Too heavy! Inheriting previous max value {dp[i][w]} directly."}
                
        yield {'type': 'done', 'dp': [row[:] for row in dp], 'max_val': dp[n][capacity], 'msg': f"Finished populating grid! The final answer is strictly in the bottom right corner: {dp[n][capacity]}."}

    def lcs(self, s1, s2):
        n = len(s1)
        m = len(s2)
        dp = [[0 for _ in range(m + 1)] for _ in range(n + 1)]
        
        yield {'type': 'grid', 'dp': [row[:] for row in dp], 's1': s1, 's2': s2, 'msg': f"LCS: Processing strings '{s1}' and '{s2}'. Base row and column are zeros."}
        
        for i in range(1, n + 1):
            for j in range(1, m + 1):
                yield {'type': 'calc', 'dp': [row[:] for row in dp], 'i': i, 'j': j, 's1': s1, 's2': s2, 'msg': f"Comparing '{s1[i-1]}' against '{s2[j-1]}'..."}
                if s1[i-1] == s2[j-1]:
                    dp[i][j] = dp[i-1][j-1] + 1
                    yield {'type': 'updated', 'dp': [row[:] for row in dp], 'i': i, 'j': j, 's1': s1, 's2': s2, 'msg': f"Match Found! Adding 1 to previous diagonal. Value -> {dp[i][j]}."}
                else:
                    dp[i][j] = max(dp[i-1][j], dp[i][j-1])
                    yield {'type': 'updated', 'dp': [row[:] for row in dp], 'i': i, 'j': j, 's1': s1, 's2': s2, 'msg': f"No match. Inheriting MAX from Above ({dp[i-1][j]}) or Left ({dp[i][j-1]}). Result: {dp[i][j]}."}
                
        # Backtracking
        i, j = n, m
        path = []
        yield {'type': 'done_fwd', 'dp': [row[:] for row in dp], 'msg': f"Forward computation complete. Length of LCS is {dp[n][m]}. Now mathematically backtracking the path!"}
        
        while i > 0 and j > 0:
            yield {'type': 'backtrack', 'dp': [row[:] for row in dp], 'i': i, 'j': j, 's1': s1, 's2': s2, 'path': path, 'msg': f"Backtracking from ({i},{j})..."}
            if s1[i-1] == s2[j-1]:
                path.append((i, j))
                i -= 1
                j -= 1
                yield {'type': 'backtrack', 'dp': [row[:] for row in dp], 'i': i, 'j': j, 's1': s1, 's2': s2, 'path': path, 'msg': f"Matched previously! Moving diagonal up-left to sequence index."}
            elif dp[i-1][j] > dp[i][j-1]:
                i -= 1
                yield {'type': 'backtrack', 'dp': [row[:] for row in dp], 'i': i, 'j': j, 's1': s1, 's2': s2, 'path': path, 'msg': f"Above value is higher. Tracing up..."}
            else:
                j -= 1
                yield {'type': 'backtrack', 'dp': [row[:] for row in dp], 'i': i, 'j': j, 's1': s1, 's2': s2, 'path': path, 'msg': f"Left value is greater or equal. Tracing left..."}
                
        yield {'type': 'done', 'dp': [row[:] for row in dp], 'path': path, 'lcs_len': dp[n][m], 'msg': f"Finished Backtracking. Highlighted cells represent the sequence path characters."}
