import threading

class Node:
    def __init__(self, value):
        self.value = value
        self.next = None
        self.lock = threading.Lock()

class FineGrainedSet:
    def __init__(self):
        self.head = Node(None)
        self.tail = Node(None)
        self.head.next = self.tail

    def add(self, value):
        pred = self.head
        pred.lock.acquire()
        curr = pred.next
        curr.lock.acquire()
        try:
            while curr.value is not None and value < curr.value:
                pred.lock.release()
                pred, curr = curr, curr.next
                curr.lock.acquire()

            if curr.value == value:
                return False

            new_node = Node(value)
            new_node.next = curr
            pred.next = new_node
            return True
        finally:
            curr.lock.release()
            pred.lock.release()

    def remove(self, value):
        pred = self.head
        pred.lock.acquire()
        curr = pred.next
        curr.lock.acquire()
        try:
            while curr.value is not None and value < curr.value:
                pred.lock.release()
                pred, curr = curr, curr.next
                curr.lock.acquire()

            if curr.value != value:
                return False

            pred.next = curr.next
            return True
        finally:
            curr.lock.release()
            pred.lock.release()

    def contains(self, value):
        curr = self.head
        curr.lock.acquire()
        try:
            next_node = curr.next
            next_node.lock.acquire()
            try:
                while next_node.value is not None and value < next_node.value:
                    curr.lock.release()
                    curr = next_node
                    next_node = curr.next
                    next_node.lock.acquire()

                return next_node.value == value
            finally:
                next_node.lock.release()
        finally:
            curr.lock.release()