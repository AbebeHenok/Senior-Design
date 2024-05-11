class deque:
    runningSum = 0
    def __init__(self, iterable=None):        
        if iterable is None:
            self.q = []
        else:
            self.q = list(iterable)

    def popleft(self):
        
        popped = self.q.pop(0)
        self.runningSum -= popped
        return popped

    def popright(self):        
        popped = self.q.pop()
        self.runningSum -= popped
        return popped

    def pop(self):
        popped = self.q.pop()
        self.runningSum -= popped
        return popped

    def append(self, a):
        self.q.append(a)
        self.runningSum += a
    
    def appendleft(self, a):
        self.q.insert(0, a)
        self.runningSum += a
        
    def peek(self):
        right = self.q.pop()
        self.q.append(right)
        return right
        
    def peekleft(self):
        left = self.q.pop(0)
        self.q.insert(0, left)
        return left
    
    def extend(self, a):
        self.q.extend(a)
        
    def runSum(self):    
        return self.runningSum
    
    def runAvg(self):
        return self.runningSum / len(self.q)
    
    def __len__(self):
        return len(self.q)

    def __bool__(self):
        return bool(self.q)

    def __iter__(self):
        yield from self.q

    def __str__(self):
        return "deque({})".format(self.q)