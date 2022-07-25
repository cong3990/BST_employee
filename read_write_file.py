import json


def load_file():
    """Read file and return an ID sorted list of dictionary of data"""

    while True:
        file_path = input("Please enter file path:\n")
        if file_path == "":
            return False

        # Check if input file path is valid
        try:
            f = open(file_path, "r")
        except FileNotFoundError:
            print("File not found. Please enter file path again\n")
            continue
        else:
            read_data = f.read()
            data = json.loads(read_data)
            f.close()

            return data


def write_file(data):
    """Write json data to file"""

    while True:
        file_path = input("Please enter file path:\n")
        if file_path == "":
            return False
        # Check if file path is valid
        try:
            f = open(file_path, "w")
        except FileNotFoundError:
            print("File or directory not found. Please enter file path again")
            continue

        else:
            data = json.dumps(data, indent=4)
            f.write(data)
            f.close()

            return


if __name__ == "__main__":
    data = [{'ID': '1', 'Name': 'Nguyen Ba Ngoc Dung', 'Date of Birth': '03/09/1990', 'Place of Birth': 'VT'},
            {'ID': '4', 'Name': 'Python Awesome', 'Date of Birth': '02/07/1980', 'Place of Birth': 'USA'},
            {'ID': '6', 'Name': 'Johny Bravo', 'Date of Birth': '05/01/2000', 'Place of Birth': 'UK'},
            {'ID': '9', 'Name': 'Aisha Nguyen', 'Date of Birth': '09/11/2010', 'Place of Birth': 'HCM'},
            {'ID': '15', 'Name': 'Monkey D. Luffy', 'Date of Birth': '03/09/1990', 'Place of Birth': 'VT'},
            {'ID': '20', 'Name': 'Roronoa Zoro', 'Date of Birth': '02/07/1980', 'Place of Birth': 'USA'},
            {'ID': '170', 'Name': 'Gold D. Ace', 'Date of Birth': '05/01/2000', 'Place of Birth': 'UK'},
            ]
    # == Write data ==
    write_file(data)

    # == Load data ==
    # load_data = load_file()
    # print(type(load_data))
    # for i in load_data:
    #     print(i)
