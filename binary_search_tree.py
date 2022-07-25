import queue

class Node:
    """Node represents an employee which contains employee's information"""
    def __init__(self, id, name, dob, pob, parent=None):
        self.id = id
        self.name = name
        # Date of Birth
        self.dob = dob
        # Place of Birth
        self.pob = pob
        # Parent of a node, default is None
        self.parent = parent
        # Initialize left child and right child of node
        self.left = None
        self.right = None
        # Height of a node, default is 1
        self.height = 1


class BinarySearchTree:
    """Binary Search Tree that store all employees' information"""
    def __init__(self):
        # Initialize tree root is None
        self.root = None

    def add_employee(self, id, name, dob, pob):
        """Add new employee to tree"""

        id = int(id)

        # Create tree root if there is not one (First input employee to the tree)
        if self.root is None:
            self.root = Node(id, name, dob, pob)
        # Find position and add employee to Tree
        else:
            self.insert(self.root, id, name, dob, pob)

    def breadth_first_search(self, node):
        """Return a list of nodes follow BFS theory"""
        result = []
        q = queue.Queue()
        q.put(node)
        while not q.empty():
            root = q.get()
            result.append(root)
            if root.left:
                q.put(root.left)
            if root.right:
                q.put(root.right)

        return result

    def delete_node(self, node):
        """Delete a node from tree"""
        # Check if there is no node with input ID in tree
        if not node or not self.search(node.id, self.root):
            return False

        # If node is valid, there are 3 cases to check
        parent = node.parent
        # number of children is condition for each case
        num_children = self.number_of_children(node)

        # Case 1: node has no children => node is leave => point node's parent to None in replace of node
        if num_children == 0:
            # If node's parent is None => node is root
            if parent is None:
                self.root = None
            else:
                # parent of deleting node points to None
                if parent.left == node:
                    parent.left = None
                elif parent.right == node:
                    parent.right = None

        # Case 2: node has 1 child
        elif num_children == 1:
            # Get node's child
            if node.left is not None:
                child = node.left
            else:
                child = node.right

            # If node's parent is None => node is root
            if parent is None:
                self.root = child
            else:
                # Remove node by pointing node parent to child and pointing node's child to node's parent
                if parent.left == node:
                    parent.left = child
                else:
                    parent.right = child
            child.parent = parent

        # Case 3: node has 2 children => replace node with its successor/predecessor,
        # delete successor/predecessor, recalculate heights of nodes, execute re-balance
        elif num_children == 2:
            # Get successor (the smallest of right branch) or predecessor (the largest of left branch)
            successor = self.min_node(node.right)

            # replace employee information in node with successor/predecessor
            # (or replace pointers of node's parent to suc/pred and pointers of suc/pred with node's pointers)
            node.id = successor.id
            node.name = successor.name
            node.dob = successor.dob
            node.pob = successor.pob

            # delete successor/predecessor, in the recursive call of deleter successor node,
            # since successor is leave or has 1 right child, case 1 or 2 is executed,
            # then program going to next step: re-balancing tree/subtree
            self.delete_node(successor)

            return

        # Update height and re-balance after deletion
        # Do not have to check for parent is None because
        # Case 1 + 2 covered parent is None
        # Case 3 will recursive call on deletion of suc/pred which then back to case 1 or 2
        if parent is not None:
            # Update node's parent's height
            parent.height = max(self.get_height(parent.left), self.get_height(parent.right)) + 1

            # Function to traverse back to root, check balance, and re-balance
            self.rebalance_deletion(parent)

    def get_height(self, node):
        """Get height of a node"""
        # If node is None, return node's height is 0
        if not node:
            return 0
        else:
            return node.height

    def get_balance(self, node):
        """Get the balance factor of a node"""
        # If node is None, return balance factor of node is 0
        if not node:
            return 0
        # Apply AVL theory to find balance factor
        else:
            return self.get_height(node.left) - self.get_height(node.right)

    def inorder_traverse(self, node):
        """Traversal from left to root to right of subtree/tree"""
        result = []
        # If input node is not None, start traversing
        if node:
            result += self.inorder_traverse(node.left)
            result.append(node)
            result += self.inorder_traverse(node.right)
        # Return list of nodes
        return result

    def insert(self, root, id, name, dob, pob):
        """
        If tree root created, find position and insert employee to tree,
        update height of ancestors, rotate if tree is unbalance (Apply AVL tree)
        """

        # If new ID < than current ID, move node to the left of current node
        if id < root.id:
            # If current node already had left node, recursive call insert on current left node
            # (current left node become root)
            if root.left:
                self.insert(root.left, id, name, dob, pob)
            # when the left of current node is None, create new node to its left, whose parent is current node
            else:
                root.left = Node(id, name, dob, pob, root)

        # If new ID > than current ID, perform to the right similar on the left of current node
        elif id > root.id:
            if root.right:
                self.insert(root.right, id, name, dob, pob)
            else:
                root.right = Node(id, name, dob, pob, root)

        # If ID existed, notify and return False
        else:
            print("Invalid ID.")
            return False

        # Update height of ancestors
        root.height = max(self.get_height(root.left), self.get_height(root.right)) + 1

        # If new node makes tree unbalance, rotate
        self.rebalance(root)

    def min_node(self, root):
        """Return node that is the smallest ID start from a selected node
        (i.e. start from root: root = BinarySearchTree.root)"""
        if root is None or root.left is None:
            return root
        return self.min_node(root.left)

    def number_of_children(self, node):
        """Check how many children a node has (0, 1, 2)"""
        children = 0
        if node.left:
            children += 1
        if node.right:
            children += 1
        return children

    def rebalance(self, node):
        """
        Check Balance factor of Node to find out if tree/subtree is unbalance
        (-1 > balance factor: right heavy
        1 < balance factor: left heavy
        -1 <= balance factor <= 1: balance tree/subtree)
        if tree/subtree is unbalance, check what case it is to perform rotating
        """
        # Get balance factor of current node
        balance = self.get_balance(node)

        # If tree/subtree is unbalance, there are 4 cases
        # Case 1: left heavy and node -> left -> left ===>> rotate right
        if balance > 1 and node.left.left:
            self.rotate_right(node)

        # Case 2: right heavy and node -> right -> left ===>> rotate right at right node ===>> rotate left at node
        elif balance < -1 and node.right.left:
            # rotate the right node of current node to back to case 2
            self.rotate_right(node.right)
            # then perform case 2 rotation on current node
            self.rotate_left(node)

        # Case 3: node -> right -> right ===>> rotate left
        elif balance < -1 and node.right.right:
            self.rotate_left(node)

        # Case 4: right heavy and node -> left -> right ===>> rotate left at left node ===>> rotate right at node
        elif balance > 1 and node.left.right:
            # rotate the left node of current node to back to case 1
            self.rotate_left(node.left)
            # then perform case 1 rotation on current node
            self.rotate_right(node)

    def rebalance_deletion(self, node):
        """Traverse up to root, balance tree/subtree if a node is found unbalance"""
        # Stop at the root of the tree
        if node is None:
            return

        # Execute re-balance method if a node is found unbalance while traverse back to root
        if abs(self.get_balance(node)) > 1:
            self.rebalance(node)

        # Recursive call to traverse back to root and execute re-balance
        self.rebalance_deletion(node.parent)

    def remove_employee(self, id):
        """Take input ID then remove node contains the ID from tree"""
        return self.delete_node(self.search(id, self.root))

    def read_tree(self, traversal_result):
        """Print ID, parent, left child, right child of nodes"""
        for node in traversal_result:
            # If node.parent is None => node is root
            if node.parent is None:
                parent = "Root"
            else:
                parent = node.parent.id
            if node.left is None:
                left = "None"
            else:
                left = node.left.id
            if node.right is None:
                right = "None"
            else:
                right = node.right.id
            print(f"ID: {node.id:<5} | Parent: {parent:<5} | Left: {left:<5} | Right: {right:<5}")

    def rotate_left(self, x):
        """Rotate tree/subtree to left"""
        # If tree/subtree is right heavy (balance factor > -1)
        #       parent                       parent
        #          |                            |
        #          x                            y
        #           \       rotate left        / \
        #            y          =>>           x   node
        #           / \                        \
        #          z  node                      z

        # Set up nodes
        parent = x.parent
        y = x.right
        z = y.left

        # Rotate
        y.left, x.right = x, z
        # If z is not None
        if z:
            z.parent = x

        x.parent = y
        y.parent = parent
        # If node's parent is None => node is tree's root
        if y.parent is None:
            self.root = y
        else:
            # Check y is on the left or right of y's parent if parent is not None
            if y.parent.left == x:
                y.parent.left = y
            elif y.parent.right == x:
                y.parent.right = y

        # Update x and y heights
        x.height = max(self.get_height(x.left), self.get_height(x.right)) + 1
        y.height = max(self.get_height(y.left), self.get_height(y.right)) + 1

    def rotate_right(self, x):
        """Rotate tree/subtree to right"""
        # If tree/subtree is left heavy (balance factor > 1)
        #      parent                           parent
        #         |                               |
        #         x         rotate right          y
        #        /          =>>                  / \
        #       y                              node x
        #      / \                                 /
        #    node z                               z

        # Set up nodes
        parent = x.parent
        y = x.left
        z = y.right

        # Rotate
        y.right, x.left = x, z
        # If z is not None
        if z:
            z.parent = x

        x.parent = y
        y.parent = parent
        # If node's parent is None => node is tree's root
        if y.parent is None:
            self.root = y
        else:
            # Check y is on the left or right of y's parent if parent is not None
            if y.parent.left == x:
                y.parent.left = y
            elif y.parent.right == x:
                y.parent.right = y

        # Update x and y heights
        x.height = max(self.get_height(x.left), self.get_height(x.right)) + 1
        y.height = max(self.get_height(y.left), self.get_height(y.right)) + 1

    def search(self, id, root):
        """Search for a node by input ID start from a node
        (i.e. start from root: self.root)"""

        if self.root is None:
            return False
        else:
            if id == root.id:
                return root
            elif id > root.id and root.right:
                return self.search(id, root.right)
            elif id < root.id and root.left:
                return self.search(id, root.left)
            else:
                return False

    def show(self, traversal_result):
        """Print employee data in the order of traversal type"""
        # Title
        print(f"{'ID':^4} | {'Name':^20} | {'Date of Birth':^14} | {'Place of Birth':<10}")
        # Each employee data
        for node in traversal_result:
            print(f"{node.id:<4} | {node.name:<20} | {node.dob:^14} | {node.pob:^10}")


if __name__ == "__main__":
    data = [{'ID': '1', 'Name': 'Nguyen Ba Ngoc Dung', 'Date of Birth': '03/09/1990', 'Place of Birth': 'VT'},
            {'ID': '4', 'Name': 'Python Awesome', 'Date of Birth': '02/07/1980', 'Place of Birth': 'USA'},
            {'ID': '6', 'Name': 'Johny Bravo', 'Date of Birth': '05/01/2000', 'Place of Birth': 'UK'},
            {'ID': '9', 'Name': 'Nguyen Aisha', 'Date of Birth': '09/11/2010', 'Place of Birth': 'HCM'},
            {'ID': '15', 'Name': 'Monkey D. Luffy', 'Date of Birth': '03/09/1990', 'Place of Birth': 'VT'},
            {'ID': '20', 'Name': 'Roronoa Zoro', 'Date of Birth': '02/07/1980', 'Place of Birth': 'USA'},
            {'ID': '170', 'Name': 'Gold D. Ace', 'Date of Birth': '05/01/2000', 'Place of Birth': 'UK'},
            ]
    tree = BinarySearchTree()
    for i in data:
        tree.add_employee(i["ID"], i["Name"], i["Date of Birth"], i["Place of Birth"])
    # inorder_nodes = tree.traversal_inorder(tree.root)
    # tree.show(inorder_nodes)
    # bfs = tree.breadth_first_search(tree.root)
    # tree.show(bfs)
    # tree.read_tree(bfs)

    # search_emp = [tree.search(170, tree.root)]
    # tree.show(search_emp)

    tree.add_employee("50", "sth", "sth", "sth")
    tree.add_employee("10", "sth", "sth", "sth")
    tree.add_employee("40", "sth", "sth", "sth")
    tree.add_employee("30", "sth", "sth", "sth")
    tree.add_employee("25", "sth", "sth", "sth")
    tree.add_employee("17", "sth", "sth", "sth")

    # tree.remove_employee(1)
    # tree.remove_employee(4)
    # tree.remove_employee(6)
    # tree.remove_employee(7)
    # tree.remove_employee(8)
    # tree.remove_employee(9)
    # tree.remove_employee(10)
    # tree.remove_employee(15)
    # tree.remove_employee(17)
    # tree.remove_employee(20)
    # tree.remove_employee(25)
    # tree.remove_employee(30)
    # tree.remove_employee(40)
    # tree.remove_employee(50)

    # tree.remove_employee(10)
    #
    # bfs = tree.breadth_first_search(tree.root)
    # tree.show(bfs)
    # tree.read_tree(bfs)

    # inorder_nodes = tree.inorder_traverse(tree.root)
    # tree.show(inorder_nodes)
