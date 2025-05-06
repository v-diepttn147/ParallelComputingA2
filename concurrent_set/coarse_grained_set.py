import threading

class CoarseGrainedSet:
    def __init__(self):
        self.head = None
        self.lock = threading.Lock()

    def add(self, value):
        with self.lock:
            if not self.contains(value):
                node = Node(value)
                node.next = self.head
                self.head = node
                return True
            return False

    def remove(self, value):
        with self.lock:
            prev, curr = None, self.head
            while curr:
                if curr.value == value:
                    if prev:
                        prev.next = curr.next
                    else:
                        self.head = curr.next
                    return True
                prev, curr = curr, curr.next
            return False

    def contains(self, value):
        curr = self.head
        while curr:
            if curr.value == value:
                return True
            curr = curr.next
        return False

class Node:
    def __init__(self, value):
        self.value = value
        self.next = None
