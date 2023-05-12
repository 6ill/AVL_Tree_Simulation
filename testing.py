import graphviz
import streamlit as st
# import os
# os.environ["PATH"] += os.pathsep + "C:/Program Files/Graphviz/bin"
PICTURE_NAME = "avl_tree"

class AVLTreeNode:
    def __init__(self, val):
        self.val = val
        self.height = 1
        self.left = None
        self.right = None

def getHeight(root: AVLTreeNode):
    if root:
        return root.height
    
    return 0

def getBalance(root: AVLTreeNode):
    if root:
        return getHeight(root.left) - getHeight(root.right)
    
    return 0

def getHeightTree(root:AVLTreeNode):
    if not root:
        return 0
    
    return 1 + max(getHeightTree(root.left), getHeightTree(root.right))

def leftRotate(root: AVLTreeNode):
    new_root = root.right
    child_of_new = new_root.left

    new_root.left = root
    root.right = child_of_new

    new_root.height = getHeightTree(new_root)
    root.height = getHeightTree(root)
    
    return new_root

def rightRotate(root: AVLTreeNode):
    new_root = root.left
    child_of_new = new_root.right

    new_root.right = root
    root.left = child_of_new

    new_root.height = getHeightTree(new_root)
    root.height = getHeightTree(root)
    
    return new_root


def insert(root: AVLTreeNode, value):
    if not root:
        return AVLTreeNode(value)
    
    if value <= root.val:
        root.left = insert(root.left, value)
    elif value > root.val:
        root.right = insert(root.right, value)

    root.height = 1 + max(getHeight(root.left), getHeight(root.right))

    balance = getBalance(root)

    if balance > 1 and value < root.left.val: # left-left
        return rightRotate(root)
    if balance < -1 and value > root.right.val: # right-right
        return leftRotate(root)
    if balance > 1 and value > root.left.val: # left-right
        root.left = leftRotate(root.left)
        return rightRotate(root)
    if balance < -1 and value < root.right.val: # right-left
        root.right = rightRotate(root.right)
        return leftRotate(root)

    return root
    
def search(root:AVLTreeNode, value, counter):
    if not root or root.val == value:
        return root, counter

    if root.val < value:
        counter += 1
        return search(root.right, value, counter)

    counter += 1
    return search(root.left, value, counter)


def print_preorder(root: AVLTreeNode):
    if root:
        print(root.val, end=" ")
        print_preorder(root.left)
        print_preorder(root.right)

def tree_to_array(root: AVLTreeNode, arr: list):
    if root:
        arr.append(root.val)
        tree_to_array(root.left, arr)
        tree_to_array(root.right, arr)

def breadth_first_traversal(root: AVLTreeNode):
    if not root:
        return

    q = []
    q.append(root)

    while(len(q)):
        current = q.pop(0)
        print(current.val, end=" ")

        if current.left is not None:
            q.append(current.left)
        if current.right is not None:
            q.append(current.right)

def add_nodes_edges(node, dot:graphviz.Digraph):
    if node.left:
        dot.node(str(node.left.val))
        dot.edge(str(node.val), str(node.left.val))
        add_nodes_edges(node.left, dot)
    if node.right:
        dot.node(str(node.right.val))
        dot.edge(str(node.val), str(node.right.val))
        add_nodes_edges(node.right, dot)

def visualize_binary_tree(root: AVLTreeNode):
    dot = graphviz.Digraph()
    dot.node(str(root.val))
    add_nodes_edges(root, dot)
    dot.render(PICTURE_NAME, format='png')

def button_search():
    # Button to search node 
    input_search = st.sidebar.number_input("Search Value", value=20, step=1)
    if st.sidebar.button("Search node"):
        counter = 0
        search_node, counter = search(st.session_state['root'], input_search, counter)
        if not search_node: 
            st.write(f"No node with value {input_search}")
        else:
            st.write(f"Hoop Nodes: {counter}")
            st.write(search_node.val)

def button_reset():
    if st.sidebar.button("Reset", help="Click twice to reset") and st.session_state.root:
        st.session_state['root'] = None

def display_tree():
    c = st.container()
    if st.session_state['root']:
        c.image(f"{PICTURE_NAME}.png")
    else:
        c.caption("### Tree is empty")

def insert_node():
    input_value = st.sidebar.number_input("Value", value=1, step=1)

    # Button to input new value
    if st.sidebar.button("Enter New Value"):
        st.session_state['root'] = insert(st.session_state['root'], input_value)
        visualize_binary_tree(st.session_state['root'])

if __name__ == "__main__":
    if 'root' not in st.session_state:
        st.session_state['root'] = None

    st.title("AVL Tree Simulation")
    st.sidebar.header('User Input Features')

    insert_node()
    display_tree()
    button_search()
    button_reset()
    
    # all_tests()