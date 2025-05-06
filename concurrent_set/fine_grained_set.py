import threading

class Node:
    def __init__(self, value):
        self.value = value
        self.next = None
        self.lock = threading.Lock()

class FineGrainedSet:
    def __init__(self):
        self.head = Node(float('-inf'))
        self.tail = Node(float('inf'))
        self.head.next = self.tail

    def add(self, value):
        pred, curr = self.head, self.head.next
        pred.lock.acquire()
        curr.lock.acquire()
        try:
            while curr.value < value:
                pred.lock.release()
                pred, curr = curr, curr.next
                curr.lock.acquire()
            if curr.value == value:
                return False
            node = Node(value)
            node.next = curr
            pred.next = node
            return True
        finally:
            pred.lock.release()
            curr.lock.release()

    def remove(self, value):
        pred, curr = self.head, self.head.next
        pred.lock.acquire()
        curr.lock.acquire()
        try:
            while curr.value < value:
                pred.lock.release()
                pred, curr = curr, curr.next
                curr.lock.acquire()
            if curr.value != value:
                return False
            pred.next = curr.next
            return True
        finally:
            pred.lock.release()
            curr.lock.release()

    def contains(self, value):
        curr = self.head
        curr.lock.acquire()
        while curr.value < value:
            pred = curr
            curr = curr.next
            curr.lock.acquire()
            pred.lock.release()
        result = curr.value == value
        curr.lock.release()
        return result
