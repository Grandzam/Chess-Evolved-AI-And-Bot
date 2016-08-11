with open("piece-names.txt", "r") as f:
    newFile = ""
    currentNum = 1
    for line in f:
        newFile = newFile + str(currentNum) + ' ' + line.split()[1] + '\n'
        currentNum = currentNum+1
        newFile = newFile + str(currentNum) + ' '  + line.split()[1] + '+\n'
        currentNum = currentNum+1
        newFile = newFile + str(currentNum) + ' ' + line.split()[1] + '++\n'
        currentNum = currentNum+1
        newFile = newFile + str(currentNum) + ' ' + line.split()[1] + '+++\n'
        currentNum = currentNum+1

    with open("piece_abilities.txt", "w") as writeFile:
        writeFile.write(newFile)
