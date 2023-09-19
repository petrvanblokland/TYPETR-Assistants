# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#       stack.py
#


DEBUG = False

class Stack:

    def __init__(self):
        self.clear()

    def __len__(self):
        return len(self.data)

    def __setitem__(self, index, value):
        self.data[index] = value

    def __getitem__(self, index):
        return self.data[index]

    def __repr__(self):
        if not self.data:
            return 'In Stack: not self.data'
        if len(self.data) == 1:
            s = self.data[0]
        else:
            s = self.data
        if isinstance(s, str):
            return s
        return repr(s)

    def clear(self):
        """
        The @clear@ method clears the stack.
        """
        self.data = []

    def setItem(self, item):
        """
        The @setItem@ method sets the stack content to @[item]@.
        """
        self.data = [item]

    def push(self, item):
        """
        The @push@ method pushes the _item_ on stack.
        """
        self.data.append(item)

    def getAll(self):
        """
        The @getAll@ method answers the whole list with stacked elements.
        """
        return self.data

    def replace(self, item):
        """
        The @replace@ method replaces the top element of the stack by _item_.
        """
        self.data[-1] = item

    def top(self, amount=1):
        """
        The @top@ method peeks the top level of the stack. This is the identical to @self.peek()
        @. If the stack is empty, then answer @None@.
        """
        if not self.data:
            return None
        if amount == 1:
            return self.data[-1]
        return self.data[-amount:]

    def peek(self, index=0):
        """
        The @peek@ method peeks into the stacked list of elements. The optional _index_ (default
        value is @0@) goes backwards, so an _index_ of @0@ is the top of the stack.
        """
        if index >= len(self.data):
            return None
        return self.data[-index - 1]

    def root(self):
        """
        The @root@ method answers the root @self.data[0]@ element of the stack.
        """
        return self.data[0]

    def delete(self, index=0):
        """
        The @delete@ method deletes the element, indicated by _index_and answers the deleted
        element.
        """
        value = self.peek(index)
        del self.data[index]
        return value

    def pop(self):
        """
        The @pop@ method pops the stack and answers the popped element.
        """
        if not self.data:
            if DEBUG: print('[Stack error] Pop from empty list')
            return None
        return self.data.pop()

    def slicePop(self, cnt):
        """
        The @slicePop@ method pops the stack and answers the popped element. If count is not 1, then a
        slice of elements is popup and answered.
        """
        if not self.data:
            if DEBUG: print('[Stack error] Pop from empty list')
            return []
        if cnt == 0:
            return []
        slice = self.data[-cnt:]
        self.data = self.data[:-cnt]
        return slice

    def popAll(self):
        """
        Pops and answers all the current values on the stack.
        """
        data = self.data
        self.data = []
        return data

if __name__ == "__main__":
    stack = Stack()
    stack.push(0)
    stack.push(1)
    stack.push(2)
    print(stack.peek())
    print(stack.pop())
    print(stack.pop())
