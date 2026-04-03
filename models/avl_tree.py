class Node:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None
        self.height = 1

class AVLTreeModel:
    def __init__(self):
        self.root = None

    def height(self, node):
        if not node: return 0
        return node.height

    def get_balance(self, node):
        if not node: return 0
        return self.height(node.left) - self.height(node.right)

    def insert(self, root, key):
        if not root: return Node(key)
        elif key < root.val: root.left = self.insert(root.left, key)
        elif key > root.val: root.right = self.insert(root.right, key)
        else: return root # No duplicates

        root.height = 1 + max(self.height(root.left), self.height(root.right))
        balance = self.get_balance(root)

        if balance > 1 and key < root.left.val: return self.right_rotate(root)
        if balance < -1 and key > root.right.val: return self.left_rotate(root)
        if balance > 1 and key > root.left.val:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)
        if balance < -1 and key < root.right.val:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)
        return root

    def left_rotate(self, z):
        y = z.right
        T2 = y.left
        y.left = z
        z.right = T2
        z.height = 1 + max(self.height(z.left), self.height(z.right))
        y.height = 1 + max(self.height(y.left), self.height(y.right))
        return y

    def right_rotate(self, z):
        y = z.left
        T3 = y.right
        y.right = z
        z.left = T3
        z.height = 1 + max(self.height(z.left), self.height(z.right))
        y.height = 1 + max(self.height(y.left), self.height(y.right))
        return y

    def min_value_node(self, root):
        if root is None or root.left is None: return root
        return self.min_value_node(root.left)

    def delete(self, root, key):
        if not root: return root
        elif key < root.val: root.left = self.delete(root.left, key)
        elif key > root.val: root.right = self.delete(root.right, key)
        else:
            if root.left is None:
                tmp = root.right; root = None; return tmp
            elif root.right is None:
                tmp = root.left; root = None; return tmp
            tmp = self.min_value_node(root.right)
            root.val = tmp.val
            root.right = self.delete(root.right, tmp.val)
        if root is None: return root

        root.height = 1 + max(self.height(root.left), self.height(root.right))
        balance = self.get_balance(root)

        if balance > 1 and self.get_balance(root.left) >= 0: return self.right_rotate(root)
        if balance < -1 and self.get_balance(root.right) <= 0: return self.left_rotate(root)
        if balance > 1 and self.get_balance(root.left) < 0:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)
        if balance < -1 and self.get_balance(root.right) > 0:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)
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
