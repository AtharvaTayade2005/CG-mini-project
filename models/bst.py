class Node:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None

class BSTModel:
    def __init__(self):
        self.root = None

    def insert(self, root, key):
        if not root: return Node(key)
        if key < root.val: root.left = self.insert(root.left, key)
        elif key > root.val: root.right = self.insert(root.right, key)
        return root

    def min_value_node(self, root):
        if root is None or root.left is None: return root
        return self.min_value_node(root.left)

    def delete(self, root, key):
        if not root: return root
        if key < root.val: root.left = self.delete(root.left, key)
        elif key > root.val: root.right = self.delete(root.right, key)
        else:
            if root.left is None:
                tmp = root.right; root = None; return tmp
            elif root.right is None:
                tmp = root.left; root = None; return tmp
            tmp = self.min_value_node(root.right)
            root.val = tmp.val
            root.right = self.delete(root.right, tmp.val)
        return root

    def do_insert(self, val):
        self.root = self.insert(self.root, val)
        
    def do_delete(self, val):
        self.root = self.delete(self.root, val)
        
    def get_in_order(self):
        res = []
        self._in(self.root, res)
        return res
    def _in(self, n, r):
        if n: self._in(n.left, r); r.append(n.val); self._in(n.right, r)
        
    def get_pre_order(self):
        res = []
        self._pre(self.root, res)
        return res
    def _pre(self, n, r):
        if n: r.append(n.val); self._pre(n.left, r); self._pre(n.right, r)
        
    def get_post_order(self):
        res = []
        self._post(self.root, res)
        return res
    def _post(self, n, r):
        if n: self._post(n.left, r); self._post(n.right, r); r.append(n.val)

    def search(self, val):
        return self._search(self.root, val)
    def _search(self, n, val):
        if not n: return False
        if n.val == val: return True
        elif val < n.val: return self._search(n.left, val)
        else: return self._search(n.right, val)

    def get_search_path(self, val):
        path = []
        self._search_path(self.root, val, path)
        return path
        
    def _search_path(self, n, val, path):
        if not n: return
        path.append(n.val)
        if n.val == val: return
        elif val < n.val: self._search_path(n.left, val, path)
        else: self._search_path(n.right, val, path)
