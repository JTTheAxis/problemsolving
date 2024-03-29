class BinaryTree:
    def __init__(self,rootObj):
        self.key = rootObj
        self.leftChild = None
        self.rightChild = None
    
    #If leftchild already exists, push the existing one down and insert the newNode as the leftchild of the root.    
    def insertLeft(self,newNode):
        if self.leftChild == None:
            self.leftChild = BinaryTree(newNode)
        else:
            t = BinaryTree(newNode)
            t.leftChild = self.leftChild
            self.leftChild = t
            
    #same with rightchild
    def insertRight(self,newNode):
        if self.rightChild == None:
            self.rightChild = BinaryTree(newNode)
        else:
            t = BinaryTree(newNode)
            t.rightChild = self.rightChild
            self.rightChild = t    
        
    def getRightChild(self):
        return self.rightChild
    
    def getLeftChild(self):
        return self.leftChild
    
    def setRootVal(self,obj):
        self.key = obj
    
    def getRootVal(self):
        return self.key    

class Stack:
    def __init__(self):
        self.items = []
    
    def isEmpty(self):
        return self.items == []
    
    def push(self, item):
        self.items.append(item)
    
    def pop(self):
        return self.items.pop()
    
    def peek(self):
        return self.items[len(self.items)-1]
    
    def size(self):
        return len(self.items)
    
def buildParseTree(fpexp):
    fplist = fpexp.split()
    pStack = Stack()
    eTree = BinaryTree('')
    pStack.push(eTree)
    currentTree = eTree
    for i in fplist:
        if i == '(':
            currentTree.insertLeft('')
            pStack.push(currentTree)
            currentTree = currentTree.getLeftChild()
        elif i not in ['+', '-', '*', '/', ')']:
            currentTree.setRootVal(int(i))
            parent = pStack.pop()
            currentTree = parent
        elif i in ['+', '-', '*', '/']:
            currentTree.setRootVal(i)
            currentTree.insertRight('')
            pStack.push(currentTree)
            currentTree = currentTree.getRightChild()
        elif i == ')':
            currentTree = pStack.pop()
        else:
            raise ValueError("Invalid input for a mathematical expression.")
    return eTree

#evaluating a mathematical tree by using the operator functions and node-checking
def evaluate(parseTree):
    opers = {'+':operator.add, '-':operator.sub, '*':operator.mul, '/':operator.truediv}

    leftC = parseTree.getLeftChild()
    rightC = parseTree.getRightChild()

    if leftC and rightC:
        fn = opers[parseTree.getRootVal()]
        return fn(evaluate(leftC),evaluate(rightC))
    else:
        return parseTree.getRootVal()
    
#Binary trees are similar to binary heaps, with one major exception:
#The BST (Binary Search Tree) Property: 
#In every node x with children l (left) and r (right), l < x and r >=x (note that this means that any values equal to x will be placed to the right node if possible). 

class BinarySearchTree:

    def __init__(self):
        self.root = None
        self.size = 0

    def length(self):
        return self.size

    def __len__(self):
        return self.size

    def __iter__(self):
        return self.root.__iter__()
    
    def __setitem__(self,k,v):
        self.put(k,v)
        
    def put(self,key,val):
        if self.root:
            self._put(key,val,self.root)
        else:
            self.root = TreeNode(key,val)
        self.size = self.size + 1
        tree=self.root.findMin()
        while True:
            tree.succ=tree.findSuccessor()
            if tree.succ is None:
                break
            tree=tree.succ
    
    def _put(self,key,val,currentNode):
        if key < currentNode.key:
            if currentNode.hasLeftChild():
                self._put(key,val,currentNode.leftChild)
            else:
                currentNode.leftChild = TreeNode(key,val,parent=currentNode)
        #If equal key, simply replace the current node with the new one. Make sure not to simply assign currentNode a new TreeNode value, as that would mean that currentNode no longer references the node which must be altered. Simply change the key and value of currentNode accordingly.
        elif key==currentNode.key:
            currentNode.key=key
            currentNode.payload=val
        else:
            if currentNode.hasRightChild():
                self._put(key,val,currentNode.rightChild)
            else:
                currentNode.rightChild = TreeNode(key,val, parent=currentNode)

    def get(self,key):
        if self.root:
            res = self._get(key,self.root)
            if res:
                return res.payload
            else:
                return None
        else:
            return None
    
    def _get(self,key,currentNode):
        if not currentNode:
            return None
        elif currentNode.key == key:
            return currentNode
        elif key < currentNode.key:
            return self._get(key,currentNode.leftChild)
        else:
            return self._get(key,currentNode.rightChild)
    
    def __getitem__(self,key):
        return self.get(key)    

    def __contains__(self,key):
        if self._get(key,self.root):
            return True
        else:
            return False
        
    def delete(self,key):
        if self.size > 1:
            nodeToRemove = self._get(key,self.root)
            if nodeToRemove:
                self.remove(nodeToRemove)
                self.size = self.size-1
            else:
                raise KeyError('Error, key not in tree')
        elif self.size == 1 and self.root.key == key:
            self.root = None
            self.size = self.size - 1
        else:
            raise KeyError('Error, key not in tree')
    
    def __delitem__(self,key):
        self.delete(key)   

    #non-recursive inorder traversal for BSTs
    def inorderTraversal(self):
        tree=self.root
        if not tree.hasAnyChildren():
            print(tree.key)
        tree=tree.findMin()
        while True:
            print(tree.key)
            succ=tree.findSuccessor()
            if succ is None:
                break
            tree=succ

class TreeNode:
    def __init__(self,key,val,left=None,right=None,
                                        parent=None):
        self.key = key
        self.payload = val
        self.leftChild = left
        self.rightChild = right
        self.parent = parent
        self.succ=None

    def hasLeftChild(self):
        return self.leftChild

    def hasRightChild(self):
        return self.rightChild

    def isLeftChild(self):
        return self.parent and self.parent.leftChild == self

    def isRightChild(self):
        return self.parent and self.parent.rightChild == self

    def isRoot(self):
        return not self.parent

    def isLeaf(self):
        return not (self.rightChild or self.leftChild)

    def hasAnyChildren(self):
        return self.rightChild or self.leftChild

    def hasBothChildren(self):
        return self.rightChild and self.leftChild

    def replaceNodeData(self,key,value,lc,rc):
        self.key = key
        self.payload = value
        self.leftChild = lc
        self.rightChild = rc
        if self.hasLeftChild():
            self.leftChild.parent = self
        if self.hasRightChild():
            self.rightChild.parent = self
            
    def findSuccessor(self):
        succ = None
        if self.hasRightChild():
            succ = self.rightChild.findMin()
        else:
            if self.parent:
                if self.isLeftChild():
                    succ = self.parent
                else:
                    self.parent.rightChild = None
                    succ = self.parent.findSuccessor()
                    self.parent.rightChild = self
        return succ
    
    def findMin(self):
        current = self
        while current.hasLeftChild():
            current = current.leftChild
        return current
    
    def spliceOut(self):
        if self.isLeaf():
            if self.isLeftChild():
                self.parent.leftChild = None
            else:
                self.parent.rightChild = None
        elif self.hasAnyChildren():
            if self.hasLeftChild():
                if self.isLeftChild():
                    self.parent.leftChild = self.leftChild
                else:
                    self.parent.rightChild = self.leftChild
                self.leftChild.parent = self.parent
            else:
                if self.isLeftChild():
                    self.parent.leftChild = self.rightChild
                else:
                    self.parent.rightChild = self.rightChild
                self.rightChild.parent = self.parent   
                
    def __iter__(self):
        if self:
            if self.hasLeftChild():
                for elem in self.leftChiLd:
                    yield elem
        yield self.key
        if self.hasRightChild():
            for elem in self.rightChild:
                yield elem    
    
"THREE"
#non-recursive inorder traversal for BSTs
def inorderTraversal(self):
    tree=self.root
    if not tree.hasAnyChildren():
        print(tree.key)
    tree=tree.findMin()
    while True:
        print(tree.key)
        succ=tree.findSuccessor()
        if succ is None:
            break
        tree=succ

mytree = BinarySearchTree()
mytree[3]="red"
mytree[4]="blue"
mytree[6]="yellow"
mytree[2]="at"
mytree[5]="green"
mytree[91]="alibaster"  

#mytree.inorderTraversal()

"FOUR"
#The goal here is to thread the binary search tree. Threading it means to maintain a link between each node and its successor.
#The first step of this will be to put the successor reference in the constructor for the TreeNode class.
def __init__(self,key,val,left=None,right=None,
                                    parent=None):
    self.key = key
    self.payload = val
    self.leftChild = left
    self.rightChild = right
    self.parent = parent
    self.succ=None
    
#Next, the put method must be modified so that every time a new node is put in, successors are recalculated.
def put(self,key,val):
    if self.root:
        self._put(key,val,self.root)
    else:
        self.root = TreeNode(key,val)
    self.size = self.size + 1
    tree=self.root.findMin()
    while True:
        tree.succ=tree.findSuccessor()
        if tree.succ is None:
            break
        tree=tree.succ
        
#Now, we can modify the inorder traversal method as we no longer need to repeatedly call findSuccessor(). 
def inorderTraversal(self):
    tree=self.root
    if not tree.hasAnyChildren():
        print(tree.key)
    while tree.leftChild:
        tree=tree.leftChild
    while True:
        print(tree.key)
        tree=tree.succ
        if tree is None:
            break
    
mytree = BinarySearchTree()
mytree[3]="red"
mytree[4]="blue"
mytree[6]="yellow"
mytree[2]="at"
mytree[5]="green"
mytree[91]="alibaster" 

#mytree.inorderTraversal()

"FIVE"
#Modifying the BST _put method so that instead of adding another duplicate node with the same key, it replaces the old key instead.
def _put(self,key,val,currentNode):
    if key < currentNode.key:
        if currentNode.hasLeftChild():
            self._put(key,val,currentNode.leftChild)
        else:
            currentNode.leftChild = TreeNode(key,val,parent=currentNode)
    #If equal key, simply replace the current node with the new one. Make sure not to simply assign currentNode a new TreeNode value, as that would mean that currentNode no longer references the node which must be altered. Simply change the key and value of currentNode accordingly.
    elif key==currentNode.key:
        currentNode.key=key
        currentNode.payload=val
    else:
        if currentNode.hasRightChild():
            self._put(key,val,currentNode.rightChild)
        else:
            currentNode.rightChild = TreeNode(key,val, parent=currentNode)
            
mytree = BinarySearchTree()
mytree[3]="red"
mytree[4]="blue"
mytree[6]="yellow"
mytree[2]="at"
mytree[5]="green"
mytree[91]="alibaster"
mytree[1]="prime"
mytree[1]="one"
mytree[3]="orange"
mytree[4]="purple"
print(mytree[1])
print(mytree[3])
print(mytree[4])

"ELEVEN"
#class PriorityQueue evolved from BinHeap.
class BinHeap:
    def __init__(self):
        self.heapList = [0]
        self.currentSize = 0
    
    def percUp(self,i):
        while i // 2 > 0:
            if self.heapList[i] < self.heapList[i // 2]:
                tmp = self.heapList[i // 2]
                self.heapList[i // 2] = self.heapList[i]
                self.heapList[i] = tmp
            i = i // 2    
            
    def insert(self,k):
        self.heapList.append(k)
        self.currentSize = self.currentSize + 1
        self.percUp(self.currentSize)
        
    def percDown(self,i):
        while (i * 2) <= self.currentSize:
            mc = self.minChild(i)
            if self.heapList[i] > self.heapList[mc]:
                tmp = self.heapList[i]
                self.heapList[i] = self.heapList[mc]
                self.heapList[mc] = tmp
            i = mc
    
    def minChild(self,i):
        if i * 2 + 1 > self.currentSize:
            return i * 2
        else:
            if self.heapList[i*2] < self.heapList[i*2+1]:
                return i * 2
            else:
                return i * 2 + 1    
            
    def delMin(self):
        retval = self.heapList[1]
        self.heapList[1] = self.heapList[self.currentSize]
        self.currentSize = self.currentSize - 1
        self.heapList.pop()
        self.percDown(1)
        return retval    
    
    def buildHeap(self,alist):
        i = len(alist) // 2
        self.currentSize = len(alist)
        self.heapList = [0] + alist[:]
        while (i > 0):
            self.percDown(i)
            i = i - 1    

class PriorityQueue(BinHeap):
        
    def enqueue(self, key):
        self.insert(key)
    
    def dequeue(self):
        self.delMin()

p=PriorityQueue()
p.enqueue(1)
p.dequeue()
print(p.heapList)
