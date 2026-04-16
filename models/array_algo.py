class ArrayModel:
    def __init__(self, size=15):
        import random
        self.arr = [random.randint(10, 100) for _ in range(size)]

    def generate_new(self, size=15):
        import random
        self.arr = [random.randint(10, 100) for _ in range(size)]
        return self.arr.copy()

    def set_arr(self, str_val):
        try:
            self.arr = [int(x.strip()) for x in str_val.replace(',', ' ').split() if x.strip()]
        except:
            pass

    # --- SORTING GENERATORS ---
    def bubble_sort(self):
        code = [
            "def bubble_sort(arr):",               # 0
            "    n = len(arr)",                    # 1
            "    for i in range(n):",              # 2
            "        for j in range(0, n-i-1):",   # 3
            "            if arr[j] > arr[j + 1]:", # 4
            "                swap(arr[j], arr[j + 1])" # 5
        ]
        time_c = "O(N^2)"
        space_c = "O(1)"
        base = {'code': code, 'time_c': time_c, 'space_c': space_c}
        
        arr = self.arr.copy()
        n = len(arr)
        yield {**base, 'arr': arr.copy(), 'sorted': [], 'msg': "Starting Bubble Sort.", 'line': 0}
        yield {**base, 'arr': arr.copy(), 'sorted': [], 'msg': f"n = {n}", 'line': 1}
        for i in range(n):
            yield {**base, 'arr': arr.copy(), 'sorted': list(range(n - i, n)), 'msg': f"i = {i}, starting pass.", 'line': 2}
            for j in range(0, n - i - 1):
                yield {**base, 'arr': arr.copy(), 'compare': [j, j+1], 'sorted': list(range(n - i, n)), 'msg': f"Comparing {arr[j]} and {arr[j+1]}.", 'line': 4}
                if arr[j] > arr[j + 1]:
                    yield {**base, 'arr': arr.copy(), 'swap': [j, j+1], 'sorted': list(range(n - i, n)), 'msg': f"{arr[j]} > {arr[j+1]}, swapping them!", 'line': 5}
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
            yield {**base, 'arr': arr.copy(), 'sorted': list(range(n - i - 1, n)), 'msg': f"Pass complete.", 'line': 3}
        self.arr = arr
        yield {**base, 'arr': arr.copy(), 'sorted': list(range(n)), 'msg': "Array is completely sorted!", 'line': 0}

    def insertion_sort(self):
        code = [
            "def insertion_sort(arr):",                 # 0
            "    for i in range(1, len(arr)):",         # 1
            "        key = arr[i]",                     # 2
            "        j = i - 1",                        # 3
            "        while j >= 0 and key < arr[j]:",   # 4
            "            arr[j + 1] = arr[j]",          # 5
            "            j -= 1",                       # 6
            "        arr[j + 1] = key"                  # 7
        ]
        base = {'code': code, 'time_c': "O(N^2)", 'space_c': "O(1)"}
        arr = self.arr.copy()
        n = len(arr)
        sorted_range = [0]
        yield {**base, 'arr': arr.copy(), 'sorted': sorted_range, 'msg': "Starting Insertion Sort.", 'line': 0}
        for i in range(1, n):
            yield {**base, 'arr': arr.copy(), 'sorted': sorted_range, 'msg': f"Outer loop i={i}.", 'line': 1}
            key = arr[i]
            j = i - 1
            yield {**base, 'arr': arr.copy(), 'compare': [i], 'sorted': sorted_range, 'msg': f"key = {key}", 'line': 2}
            
            while j >= 0 and key < arr[j]:
                yield {**base, 'arr': arr.copy(), 'compare': [j+1, j], 'sorted': sorted_range, 'msg': f"{arr[j]} > {key}, need to shift.", 'line': 4}
                yield {**base, 'arr': arr.copy(), 'swap': [j+1, j+2], 'sorted': sorted_range, 'msg': f"Shifting {arr[j]} to right.", 'line': 5}
                arr[j + 1] = arr[j]
                j -= 1
            arr[j + 1] = key
            sorted_range.append(i)
            yield {**base, 'arr': arr.copy(), 'sorted': sorted_range, 'msg': f"Placed {key} at its correct position.", 'line': 7}
        self.arr = arr
        yield {**base, 'arr': arr.copy(), 'sorted': list(range(n)), 'msg': "Array is completely sorted!", 'line': 0}

    def quick_sort(self):
        code = [
            "def quick_sort(arr, low, high):",
            "    if low < high:",
            "        pi = partition(arr, low, high)",
            "        quick_sort(arr, low, pi - 1)",
            "        quick_sort(arr, pi + 1, high)",
            "",
            "def partition(arr, low, high):",
            "    pivot = arr[high]",
            "    i = low - 1",
            "    for j in range(low, high):",
            "        if arr[j] < pivot:",
            "            i += 1",
            "            swap(arr[i], arr[j])",
            "    swap(arr[i + 1], arr[high])",
            "    return i + 1"
        ]
        base = {'code': code, 'time_c': "O(N log N)", 'space_c': "O(log N)"}
        arr = self.arr.copy()
        yield {**base, 'arr': arr.copy(), 'msg': "Starting Quick Sort. We will recursively pick a pivot and partition elements around it.", 'line': 0}
        def qs(low, high):
            if low < high:
                pi = yield from partition(low, high)
                yield from qs(low, pi - 1)
                yield from qs(pi + 1, high)

        def partition(low, high):
            pivot = arr[high]
            i = low - 1
            yield {**base, 'arr': arr.copy(), 'pivot': high, 'msg': f"Selected pivot {pivot} at index {high}. Scanning from {low} to {high-1}.", 'line': 7}
            for j in range(low, high):
                yield {**base, 'arr': arr.copy(), 'compare': [j, high], 'pivot': high, 'msg': f"Checking if {arr[j]} < pivot ({pivot}).", 'line': 10}
                if arr[j] < pivot:
                    i = i + 1
                    arr[i], arr[j] = arr[j], arr[i]
                    yield {**base, 'arr': arr.copy(), 'swap': [i, j], 'pivot': high, 'msg': f"Yes. Swapping smaller element {arr[i]} into the low-tracking region.", 'line': 12}
            arr[i + 1], arr[high] = arr[high], arr[i + 1]
            yield {**base, 'arr': arr.copy(), 'swap': [i+1, high], 'sorted': [i+1], 'msg': f"Partition done. Placed pivot {pivot} firmly at index {i+1}.", 'line': 13}
            return i + 1

        yield from qs(0, len(arr) - 1)
        self.arr = arr
        yield {**base, 'arr': arr.copy(), 'sorted': list(range(len(arr))), 'msg': "Array is completely sorted!", 'line': 0}

    def merge_sort(self):
        code = [
            "def merge_sort(arr, left, right):",
            "    if left < right:",
            "        mid = (left + right) // 2",
            "        merge_sort(arr, left, mid)",
            "        merge_sort(arr, mid + 1, right)",
            "        merge(arr, left, mid, right)",
            "",
            "def merge(arr, left, mid, right):",
            "    L = arr[left:mid + 1]",
            "    R = arr[mid + 1:right + 1]",
            "    i = j = 0",
            "    k = left",
            "    while i < len(L) and j < len(R):",
            "        if L[i] <= R[j]:",
            "            arr[k] = L[i]",
            "            i += 1",
            "        else:",
            "            arr[k] = R[j]",
            "            j += 1",
            "        k += 1",
            "    # copy remaining items"
        ]
        base = {'code': code, 'time_c': "O(N log N)", 'space_c': "O(N)"}
        arr = self.arr.copy()
        yield {**base, 'arr': arr.copy(), 'msg': "Starting Merge Sort. We will recursively split the array into halves until size 1, then merge back.", 'line': 0}
        def ms(left, right):
            if left < right:
                mid = (left + right) // 2
                yield {**base, 'arr': arr.copy(), 'msg': f"Splitting left bound [{left} to {right}] at center {mid}.", 'line': 2}
                yield from ms(left, mid)
                yield from ms(mid + 1, right)
                yield from merge(left, mid, right)

        def merge(left, mid, right):
            yield {**base, 'arr': arr.copy(), 'msg': f"Merging subarrays [{left}-{mid}] and [{mid+1}-{right}].", 'line': 7}
            L = arr[left:mid + 1]
            R = arr[mid + 1:right + 1]
            i = 0
            j = 0
            k = left
            while i < len(L) and j < len(R):
                yield {**base, 'arr': arr.copy(), 'compare': [left+i, mid+1+j], 'msg': f"Comparing {L[i]} (left block) and {R[j]} (right block).", 'line': 13}
                if L[i] <= R[j]:
                    yield {**base, 'arr': arr.copy(), 'msg': f"{L[i]} <= {R[j]}. Placing {L[i]} into array.", 'line': 14}
                    arr[k] = L[i]
                    i += 1
                else:
                    yield {**base, 'arr': arr.copy(), 'msg': f"{R[j]} < {L[i]}. Placing {R[j]} into array.", 'line': 16}
                    arr[k] = R[j]
                    j += 1
                k += 1
                yield {**base, 'arr': arr.copy(), 'merged': list(range(left, k)), 'line': 19}
            
            while i < len(L):
                arr[k] = L[i]
                yield {**base, 'arr': arr.copy(), 'merged': list(range(left, k+1)), 'msg': f"Flushing remaining element {L[i]} from left block.", 'line': 20}
                i += 1
                k += 1
            while j < len(R):
                arr[k] = R[j]
                yield {**base, 'arr': arr.copy(), 'merged': list(range(left, k+1)), 'msg': f"Flushing remaining element {R[j]} from right block.", 'line': 20}
                j += 1
                k += 1

        yield from ms(0, len(arr) - 1)
        self.arr = arr
        yield {**base, 'arr': arr.copy(), 'sorted': list(range(len(arr))), 'msg': "Array is completely sorted!", 'line': 0}

    # --- SEARCHING GENERATORS ---
    def linear_search(self, target):
        code = [
            "def linear_search(arr, target):",
            "    for i in range(len(arr)):",
            "        if arr[i] == target:",
            "            return i",
            "    return -1"
        ]
        base = {'code': code, 'time_c': "O(N)", 'space_c': "O(1)"}
        arr = self.arr.copy()
        for i in range(len(arr)):
            yield {**base, 'arr': arr, 'compare': [i], 'msg': f"Checking index {i}. Is {arr[i]} == {target}?", 'line': 1}
            if arr[i] == target:
                yield {**base, 'arr': arr, 'found': i, 'msg': f"Match found! {arr[i]} == {target} at index {i}.", 'line': 3}
                return
        yield {**base, 'arr': arr, 'not_found': True, 'msg': f"Target {target} not found in the array.", 'line': 4}

    def binary_search(self, target):
        code = [
            "def binary_search(arr, target):",
            "    left, right = 0, len(arr) - 1",
            "    while left <= right:",
            "        mid = (left + right) // 2",
            "        if arr[mid] == target:",
            "            return mid",
            "        elif arr[mid] < target:",
            "            left = mid + 1",
            "        else:",
            "            right = mid - 1",
            "    return -1"
        ]
        base = {'code': code, 'time_c': "O(log N)", 'space_c': "O(1)"}
        arr = self.arr.copy()
        arr.sort()
        self.arr = arr
        yield {**base, 'arr': arr, 'msg': "Binary Search requires a sorted array. We instantly sorted the elements to begin.", 'line': 0}
        
        left = 0
        right = len(arr) - 1
        while left <= right:
            mid = (left + right) // 2
            yield {**base, 'arr': arr, 'left': left, 'right': right, 'mid': mid, 'msg': f"Search Space: [{left} to {right}]. Checking middle index {mid}.", 'line': 3}
            if arr[mid] == target:
                yield {**base, 'arr': arr, 'left': left, 'right': right, 'mid': mid, 'found': mid, 'msg': f"Target found! {arr[mid]} == {target} at index {mid}.", 'line': 5}
                return
            elif arr[mid] < target:
                yield {**base, 'arr': arr, 'left': left, 'right': right, 'msg': f"{arr[mid]} < {target}. Eliminating left half. Updating 'Left' pointer to {mid+1}.", 'line': 7}
                left = mid + 1
            else:
                yield {**base, 'arr': arr, 'left': left, 'right': right, 'msg': f"{arr[mid]} > {target}. Eliminating right half. Updating 'Right' pointer to {mid-1}.", 'line': 9}
                right = mid - 1
        yield {**base, 'arr': arr, 'not_found': True, 'msg': f"Left bound bypassed Right bound. Validating {target} does not exist in array.", 'line': 10}
