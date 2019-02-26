class Student:
    def __init__(self, name, score):
        self.name = name
        self.score = score

    def __str__(self):
        return '{}: {}'.format(self.name, self.score)


def better_score(s1, s2):
    if s1.score > s2.score:
        return True
    return False


def equal_score(s1, s2):
    if s1.score == s2.score:
        return True
    return False


class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


def pre_order_traverse(node):
    global traversal_list

    if node:
        print(node.val, end=' -> ')
        traversal_list.append(node)
        pre_order_traverse(node.left)
        pre_order_traverse(node.right)


def in_order_traverse(node):
    global traversal_list
    if node is None:
        return

    in_order_traverse(node.left)
    print(node.val, end=' -> ')
    traversal_list.append(node)
    in_order_traverse(node.right)


def post_order_traverse(node, result):
    if node is None:
        return

    post_order_traverse(node.left, result)
    post_order_traverse(node.right, result)
    print(node.val, end=' -> ')
    result.append(node)


def post_order_traverse2(node):
    current_node = node
    results = []
    left_stack = []
    right_stack = []

    while True:
        if current_node.left and not (current_node.left in results):
            left_stack.append(current_node)
            current_node = current_node.left
            continue

        if current_node.right and not (current_node.right in results):
            right_stack.append(current_node)
            current_node = current_node.right
            continue

        if current_node is None or current_node in results:
            break

        print(current_node.val, end=' -> ')
        results.append(current_node)

        if left_stack:
            current_node = left_stack.pop()
            continue

        if right_stack:
            current_node = right_stack.pop()
            continue

    return results


def level_order_traverse(node):
    print(node.val, end=' -> ')
    results = [node]

    current_nodes = []
    if node.left:
        current_nodes.append(node.left)

    if node.right:
        current_nodes.append(node.right)

    while True:
        next_nodes = []

        for node in current_nodes:
            if node:
                print(node.val, end=' -> ')
                results.append(node)

            if node.left:
                next_nodes.append(node.left)

            if node.right:
                next_nodes.append(node.right)

        current_nodes = next_nodes

        if not current_nodes:
            break

    return results


def find_most_left(node):
    parent = None
    while node.left:
        parent = node
        node = node.left
    return node, parent


def find_most_right(node):
    parent = None
    while node.right:
        parent = node
        node = node.right
    return node, parent


class BinaryTree:
    def __init__(self, node, comparison):
        self.root = node
        self.comparison = comparison
        self.equal = None

    def set_equal(self, equal):
        self.equal = equal

    def insert(self, node):
        root = self.root

        while root:
            if self.comparison(node.val, root.val):
                if not root.right:
                    root.right = node
                    break
                root = root.right
            else:
                if not root.left:
                    root.left = node
                    break
                root = root.left

    def find_val(self, val):
        root = self.root
        result = None
        while root:
            if self.equal(val, root.val):
                result = root.val
                break

            if self.comparison(val, root.val):
                if root.right:
                    root = root.right
                else:
                    break

            else:
                if root.left:
                    root = root.left
                else:
                    break

        return result

    def find_node(self, val):
        root = self.root
        parent = None
        result = None
        while root:
            if self.equal(val, root.val):
                result = root
                break

            if self.comparison(val, root.val):
                if root.right:
                    parent = root
                    root = root.right
                else:
                    break

            else:
                if root.left:
                    parent = root
                    root = root.left
                else:
                    break

        return result, parent

    def delete(self, val):
        """
        no implement
        :param val:
        :return:
        """
        current, parent = self.find_node(val)

        # no found
        if current is None:
            return False

        # root
        if parent is None:
            "no implement"
            # leaf
            if current.right is None and current.left is None:
                self.root = None
                return True

            # one child
            if current.right is None or current.left is None:
                if current.right:
                    self.root = current.right
                else:
                    self.root = current.left
                return True

            # two children
            c, p = find_most_right(current.left)

            if p is None:
                c.right = current.right
            else:
                if c.left:
                    p.right = c.left
                else:
                    p.right = None
                    c.right = current.right
                    c.left = current.left

            self.root = c
            return True

        if parent.right is current:
            child = 'right'
        else:
            child = 'left'

        # leaf
        if current.right is None and current.left is None:
            setattr(parent, child, None)
            return True

        # one child
        if current.right is None or current.left is None:
            if current.right:
                setattr(parent, child, current.right)
            else:
                setattr(parent, child, current.left)
            return True

        # two children
        c, p = find_most_right(current.left)

        if p is None:
            c.right = current.right
        else:
            if c.left:
                p.right = c.left
            else:
                p.right = None
                c.right = current.right
                c.left = current.left

        setattr(parent, child, c)
        return True


if __name__ == '__main__':
    # data
    s0 = Student('s0', 60)
    s1 = Student('s1', 20)
    s2 = Student('s2', 80)
    s3 = Student('s3', 10)
    s4 = Student('s4', 40)
    s5 = Student('s5', 30)
    s6 = Student('s6', 50)
    s7 = Student('s7', 70)
    s8 = Student('s8', 90)
    s9 = Student('s9', 100)
    s10 = Student('s10', 0)
    s11 = Student('s11', 15)

    # # insert
    # n0 = TreeNode(s0)
    # n0.left = TreeNode(s1)
    # n0.right = TreeNode(s2)
    # n0.left.left = TreeNode(s3)
    # n0.left.right = TreeNode(s4)
    # n0.right.right = TreeNode(s5)
    # n0.left.left.left = TreeNode(s6)
    # n0.left.left.right = TreeNode(s7)
    # n0.right.right.left = TreeNode(s8)
    # n0.right.right.right = TreeNode(s9)
    # print(n0.left.val, n0.right.val)
    #
    # # traverse
    # global traversal_list
    #
    # traversal_list = []
    # pre_order_traverse(n0)
    # print()
    #
    # traversal_list = []
    # in_order_traverse(n0)
    # print()
    #
    # post_traversal_list = []
    # post_order_traverse(n0, post_traversal_list)
    # print()
    #
    # post_order_traverse2(n0)
    #
    # print()
    # level_order_traverse(n0)

    # sort insert
    binary_tree = BinaryTree(TreeNode(Student('s0', 60)), better_score)
    binary_tree.insert(TreeNode(s1))
    binary_tree.insert(TreeNode(s2))
    binary_tree.insert(TreeNode(s3))
    binary_tree.insert(TreeNode(s4))
    binary_tree.insert(TreeNode(s5))
    binary_tree.insert(TreeNode(s6))
    binary_tree.insert(TreeNode(s7))
    binary_tree.insert(TreeNode(s8))
    binary_tree.insert(TreeNode(s9))
    binary_tree.insert(TreeNode(s10))
    binary_tree.insert(TreeNode(s11))

    # print(binary_tree.root.val)

    level_order_traverse(binary_tree.root)

    # print(binary_tree.root.left.val, binary_tree.root.right.val)
    # print(binary_tree.root.right.left, binary_tree.root.right.right)
    binary_tree.set_equal(equal_score)
    print()

    # b = binary_tree.find_val(Student('b', 50))
    # print(b)
    # print()

    c1, p1 = binary_tree.find_node(Student('b', 40))
    # print(c1.val)
    # print(p1)
    print()

    # c2, p2 = find_most_right(c1)
    # print(c2.val)
    # print(p2.val)
    # print()

    # binary_tree.delete(Student('b', 40))
    binary_tree.delete(Student('b', 60))
    level_order_traverse(binary_tree.root)
