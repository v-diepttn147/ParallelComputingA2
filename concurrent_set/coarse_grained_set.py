import threading

class CoarseGrainedSet:
    def __init__(self):
        self.head = None
        self.lock = threading.Lock()

    def add(self, value):
        with self.lock:
            prev, curr = None, self.head
            while curr and curr.value < value:
                prev, curr = curr, curr.next
            if curr and curr.value == value:
                return False  # already present
            new_node = Node(value)
            new_node.next = curr
            if prev:
                prev.next = new_node
            else:
                self.head = new_node
            return True


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