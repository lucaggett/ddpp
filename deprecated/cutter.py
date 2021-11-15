with open('input.txt', 'r') as f:
    for line in f.readlines():
        # remove the number followed by the dot at the start of each line and write the result to a new file
        with open('output.txt', 'a') as f2:
            f2.write("\"" + line.split('.')[1].strip() + "\"," + "\n")