while True:
    x = 0
    string1 = ""
    while x != 4:
        string2 = "4:"
        value = input()
        string3 = int(value) * 8 + 6
        string1 += string2 + str(string3) + " "
        x += 1
    print(string1)