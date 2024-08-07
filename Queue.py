import QueueObject

class Queue():
    def __init__(self):
         self.items:queue_object = []

    def enqueue(self, item):
        self.items.append(item)

    def dequeue(self):
        return self.items.pop(self.size()-1)

    def size(self):
        return len(self.items)

    def find(self, id):
        for item in self.items:
            if item.id == id:
                return item
        return None

    def clear(self):
        return self.items.clear()

    def delete(self, item:QueueObject):
        self.items.remove(item)
        return None
