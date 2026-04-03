class HeapModel:
    def __init__(self, is_min=True):
        self.heap = []
        self.is_min = is_min

    def compare(self, i, j):
        if self.is_min:
            return self.heap[i] < self.heap[j]
        else:
            return self.heap[i] > self.heap[j]

    def insert(self, value):
        self.heap.append(value)
        return self._heapify_up(len(self.heap) - 1)

    def _heapify_up(self, idx):
        swaps = []
        while idx > 0:
            parent = (idx - 1) // 2
            if self.compare(idx, parent):
                self.heap[idx], self.heap[parent] = self.heap[parent], self.heap[idx]
                swaps.append((idx, parent))
                idx = parent
            else:
                break
        return swaps

    def extract(self):
        if len(self.heap) == 0: return None, []
        if len(self.heap) == 1:
            val = self.heap.pop()
            return val, []
            
        val = self.heap[0]
        self.heap[0] = self.heap.pop()
        swaps = self._heapify_down(0)
        return val, swaps
        
    def _heapify_down(self, idx):
        swaps = []
        n = len(self.heap)
        while True:
            left = 2 * idx + 1
            right = 2 * idx + 2
            extreme = idx
            
            if left < n and self.compare(left, extreme):
                extreme = left
            if right < n and self.compare(right, extreme):
                extreme = right
                
            if extreme != idx:
                self.heap[idx], self.heap[extreme] = self.heap[extreme], self.heap[idx]
                swaps.append((idx, extreme))
                idx = extreme
            else:
                break
        return swaps

    def get_in_order(self):
        res = []
        self._in_order(0, res)
        return res
    def _in_order(self, idx, res):
        if idx < len(self.heap):
            self._in_order(2*idx+1, res)
            res.append(idx)
            self._in_order(2*idx+2, res)
            
    def get_pre_order(self):
        res = []
        self._pre(0, res)
        return res
    def _pre(self, idx, res):
        if idx < len(self.heap):
            res.append(idx)
            self._pre(2*idx+1, res)
            self._pre(2*idx+2, res)
            
    def get_post_order(self):
        res = []
        self._post(0, res)
        return res
    def _post(self, idx, res):
        if idx < len(self.heap):
            self._post(2*idx+1, res)
            self._post(2*idx+2, res)
            res.append(idx)
