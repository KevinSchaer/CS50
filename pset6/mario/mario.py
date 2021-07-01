# get user input
while True:  # infinite loop
    height = input("Enter the height: ")  # get user input
    if height.isnumeric() == True:  # can also recognize numbers although they are strings
        height = int(height)  # change datatype because input takes numbers as string
        if height >= 1 and height <= 8:
            break
    print("invalid input")


# print pyramid
for i in range(1, height + 1):
    print(" " * (height - i), end="")
    print("#" * i, end="")
    print("  ", end="")
    print("#" * i, end="\n")