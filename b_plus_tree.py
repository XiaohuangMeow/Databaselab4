class Node(object):
    """
    右节点大于等于索引值
    """
    # order 阶数
    def __init__(self, order):
        self.order = order
        self.keys = []
        self.values = []
        self.leaf = True
        self.parent=None

    def add(self, key, value):
        """
        Adds a key-value pair to the node.
        """

        # keys is [],as first insert
        if not self.keys:
            self.keys.append(key)
            self.values.append([value])
            return None

        for i, item in enumerate(self.keys):
            # same key:add value list
            if key == item:
                self.values[i].append(value)
                break
            # insert middle
            elif key < item:
                self.keys = self.keys[:i] + [key] + self.keys[i:]
                self.values = self.values[:i] + [[value]] + self.values[i:]
                break
            # add to the rightest
            elif i + 1 == len(self.keys):
                self.keys.append(key)
                self.values.append([value])
                break

    def split(self):
        # spilt into two nodes
        left = Node(self.order)
        right = Node(self.order)
        mid = self.order // 2

        left.keys = self.keys[:mid]
        left.values = self.values[:mid]
        left.parent=self

        right.keys = self.keys[mid:]
        right.values = self.values[mid:]
        right.parent=self

        self.keys = [right.keys[0]]
        self.values = [left, right]
        self.leaf = False

    def is_full(self):
        return len(self.keys) == self.order

    def show(self, counter=0):
        print(counter, str(self.keys))

        if not self.leaf:
            for item in self.values:
                item.show(counter + 1)


class BPlusTree(object):
    def __init__(self, order=4):
        self.root = Node(order)

    def _find(self, node, key):
        """
        根据key，找到应该插入的位置和对应的value_list
        """
        x=0
        for i, item in enumerate(node.keys):
            x=i
            if key < item:
                return node.values[i], i

        return node.values[x + 1], x + 1

    def _merge(self, parent, child, index):
        """
        给定父节点和子节点，以及索引index，将子节点的pivot插入父节点
        """
        parent.values.pop(index)
        pivot = child.keys[0]

        for i, item in enumerate(parent.keys):
            # 将pivot插入parent的中间
            if pivot < item:
                parent.keys = parent.keys[:i] + [pivot] + parent.keys[i:]
                parent.values = parent.values[:i] + child.values + parent.values[i:]
                break
            # 将pivot插入parent右边
            elif i + 1 == len(parent.keys):
                parent.keys += [pivot]
                parent.values += child.values
                break

    def insert(self, key, value):
        """
        插入节点，包括key和value
        """
        parent = None
        child = self.root

        while not child.leaf:
            parent = child
            child, index = self._find(child, key)

        child.add(key, value)
        if child.is_full():
            child.split()
            # parent非None且parent未满
            # if parent and not parent.is_full():
            #     self._merge(parent, child, index)
            if parent:
                self._merge(parent, child, index)
                if parent.is_full():
                    self.parent_spilt(parent)

    def parent_spilt(self,node):
        # 父节点为None
        parent = Node(node.order)
        left = Node(node.order)
        right = Node(node.order)
        left.parent = parent
        right.parent = parent
        mid = node.order // 2
        left.keys = node.keys[:mid]
        left.values = node.values[:mid + 1]
        right.keys = node.keys[mid + 1:]
        right.values = node.values[mid + 1:]
        parent.values=[left,right]
        parent.leaf = False
        left.leaf = False
        right.leaf = False
        if not node.parent:
            parent.parent=None
            parent.keys=[node.keys[mid]]
            self.root = parent
        else:
            pivot = node.keys[mid]
            _,index=self._find(node.parent,pivot)
            node.parent.values.pop(index)
            for i, item in enumerate(node.parent.keys):
                # 将pivot插入parent的中间
                if pivot < item:
                    node.parent.keys = node.parent.keys[:i] + [pivot] + node.parent.keys[i:]
                    node.parent.values = node.parent.values[:i] + parent.values + node.parent.values[i:]
                    break
                # 将pivot插入parent右边
                elif i + 1 == len(node.parent.keys):
                    node.parent.keys += [pivot]
                    node.parent.values += parent.values
                    break
            if node.parent.is_full():
                self.parent_spilt(node.parent)

    def retrieve(self, key):
        """
        Returns a value for a given key, and None if the key does not exist.
        """
        child = self.root
        while not child.leaf:
            child, index = self._find(child, key)
        for i, item in enumerate(child.keys):
            if key == item:
                return child.values[i]
        return None

    def show(self):
        self.root.show()