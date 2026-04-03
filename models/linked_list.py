class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

class LinkedListModel:
    def __init__(self):
        self.head = None

    def insert_head(self, value):
        new_node = Node(value)
        new_node.next = self.head
        self.head = new_node
        return new_node

    def insert_tail(self, value):
        new_node = Node(value)
        if not self.head:
            self.head = new_node
            return new_node
        
        curr = self.head
        while curr.next:
            curr = curr.next
        curr.next = new_node
        return new_node

    def delete_head(self):
        if not self.head:
            return None
        node = self.head
        self.head = self.head.next
        return node
        
    def delete_tail(self):
        if not self.head:
            return None
        if not self.head.next:
            node = self.head
            self.head = None
            return node
            
        curr = self.head
        while curr.next.next:
            curr = curr.next
        node = curr.next
        curr.next = None
        return node

    def get_items(self):
        items = []
        curr = self.head
        while curr:
            items.append(curr)
            curr = curr.next
        return items
