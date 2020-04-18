# a rote stack implementation
# print("Stack imported")
class Stack:
    def __init__(self):
        self.st = []
    def push(self, item):
        self.st.append(item)
    def pop(self):
        self.st.pop()
    def top(self):
        return self.st[(len(self.st) -1 )]
    def empty(self):
        if len(self.st) == 0:
            return True
        else: 
            return False
    def size(self):
        return len(self.st)
  