
from read_write_file import load_file, write_file
from binary_search_tree import BinarySearchTree


def menu():
    # Create menu in loop so user can select function again without start program again
    while True:
        print()
        print("====================================")
        print("WELCOME TO EMPLOYEE DATA MANAGEMENT")
        print("=============== MENU ===============")
        print("1. Load Data from file")
        print("2. Insert new Employee Data")
        print("3. Inorder traverse")
        print("4. Breadth First Traversal")
        print("5. Search Employee Data by ID")
        print("6. Remove Employee Data by ID")
        print("7. Read Tree")
        print("8. Save Data to file")
        print("0. Exit")
        print("====================================")

        # Make sure user enter a number
        try:
            select = int(input("Please enter a number to select function:\n(Press Enter while in the function to go "
                               "back to Menu)\n"))
        except ValueError:
            print("Please select a number display on the MENU.")
            continue

        # Make sure user enter number from 0 -> 8
        if select < 0 or select > 8:
            print("Please select a number display on the MENU.")
            continue

        # ======= Exit function
        if select == 0:
            print("EXIT.")
            print("Thank you. See you again!")
            break

        # ======= Load data from file, if file path is incorrect, ask user to enter file path again or return to menu
        elif select == 1:
            print("1. Load Data from file")
            data = load_file()
            if not data:
                continue
            print("File loaded successfully!")

            # Create tree from loaded data
            tree = BinarySearchTree()
            for i in data:
                tree.add_employee(int(i["ID"]), i["Name"], i["Date of Birth"], i["Place of Birth"])
            # Print Employee Data after loaded
            to_print = tree.inorder_traverse(tree.root)
            tree.show(to_print)

        # ======= Insert new Employee Data
        elif select == 2:
            print("2. Insert new Employee Data")
            # Check if Dataset is valid
            try:
                tree.root
            except UnboundLocalError:
                print("ERROR: Invalid Dataset. Please load Dataset.")
                continue

            id = input("Please enter Employee ID (In number):\n")

            if id == "":
                continue
            # If ID existed, notify and require user to select another ID
            found = tree.search(int(id), tree.root)
            if found:
                while found.id == int(id):
                    id = input("Invalid ID. Please select another ID.\n")
                    if id == "":
                        break
                    found = tree.search(int(id), tree.root)
                    if found:
                        continue
                    else:
                        break

                # Enter to return to Menu
                if id == "":
                    continue

            name = input("Please enter Employee Name:\n")
            if name == "":
                continue
            dob = input("Please enter Employee Date of Birth:\n")
            if dob == "":
                continue
            pob = input("Please enter Employee Place of Birth:\n")
            if pob == "":
                continue

            tree.add_employee(int(id), name, dob, pob)
            print("Employee Data has been added to Dataset")
            print(f"Employee ID: {id}")
            print(f"Employee Name: {name}")
            print(f"Employee Date of Birth: {dob}")
            print(f"Employee Place of Birth: {pob}")

        # ======= Inorder Traverse
        elif select == 3:
            print("3. Inorder traverse")
            # Check if Dataset is valid
            try:
                tree.root
            except UnboundLocalError:
                print("ERROR: Invalid Dataset. Please load Dataset.")
                continue
            # Get a list of node in inorder traverse, then print information
            to_print = tree.inorder_traverse(tree.root)
            tree.show(to_print)
            # Read ID, parent, left child, right child of node
            # tree.read_tree(to_print)

        # ======= Breadth First Traverse
        elif select == 4:
            print("4. Breadth First Traversal")
            # Check if Dataset is valid
            try:
                tree.root
            except UnboundLocalError:
                print("ERROR: Invalid Dataset. Please load Dataset.")
                continue
            # Get a list of node in breadth first traverse, then print information
            to_print = tree.breadth_first_search(tree.root)
            tree.show(to_print)
            # Read ID, parent, left child, right child of node
            # tree.read_tree(to_print)

        # ======= Search Employee Data by input ID
        elif select == 5:
            print("5. Search Employee Data by ID")
            # Check if Dataset is valid
            try:
                tree.root
            except UnboundLocalError:
                print("ERROR: Invalid Dataset. Please load Dataset.")
                continue

            search_id = input("Please enter Employee ID:\n")
            if search_id == "":
                continue

            # If search return False, notify user and back to menu
            found = [tree.search(int(search_id), tree.root)]
            if not found[0]:
                print("Employee ID does not exist!")
            else:
                tree.show(found)

        # ======= Remove Employee Data by ID
        elif select == 6:
            print("6. Remove Employee Data by ID")
            # Check if Dataset is valid
            try:
                tree.root
            except UnboundLocalError:
                print("ERROR: Invalid Dataset. Please load Dataset.")
                continue

            id = input("Please Enter Employee ID:\n")
            if id == "":
                continue

            id = int(id)
            remove = tree.search(id, tree.root)
            if not remove:
                print("Invalid ID.")
                continue
            else:
                tree.remove_employee(id)
                tree.show([remove])
                print("Employee Data has been deleted")

        # ======= Read ID, parent, left child, right child of nodes
        elif select == 7:
            print("7. Read Tree")
            # Check if Dataset is valid
            try:
                tree.root
            except UnboundLocalError:
                print("ERROR: Invalid Dataset. Please load Dataset.")
                continue
            nodes = tree.breadth_first_search(tree.root)
            tree.read_tree(nodes)

        # ======= Save Data to file
        elif select == 8:
            print("8. Save Data to file")
            # Check if Dataset is valid
            try:
                tree.root
            except UnboundLocalError:
                print("ERROR: Invalid Dataset. Please load Dataset.")
                continue

            nodes = tree.inorder_traverse(tree.root)
            data = []
            for node in nodes:
                node_infor = {"ID": node.id, "Name": node.name, "Date of Birth": node.dob, "Place of Birth": node.pob}
                data.append(node_infor)
            write = write_file(data)
            if not write:
                continue


if __name__ == "__main__":
    menu()
