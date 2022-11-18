import sys
import utilities
import CONSTS

if __name__ == '__main__':

    args = sys.argv
    print(args)

    if len(args) == 4:
        oldProjDir = args[1]
        newProjDir = args[2]
        targetFiles = args[3]
        renameMap = {}

    elif len(args) >= 5:
        oldProjDir = args[1]
        newProjDir = args[2]
        targetFiles = args[3]
        tokens = targetFiles.split(",")
        targetFiles = []
        for filepath in tokens:
            filepath = filepath.strip()
            if filepath != "":
                targetFiles.append(filepath)

        renameMap = args[4]
        tokens = renameMap.split(",")
        renameMap = {}
        for filepath in tokens:
            keyValArr = filepath.split(":")
            if len(keyValArr) >= 2:
                key = keyValArr[0].strip()
                val = keyValArr[1].strip()
                renameMap[key] = val
    else:
        print("Running w/ Default Parameters")
        oldProjDir = CONSTS.defaultOldProjDir
        newProjDir = CONSTS.defaultNewProjDir
        renameMap = CONSTS.defaultReplaceStrMappings
        targetFiles = CONSTS.targetFilesList

        # targetFiles = input("Enter the path of the starting target file: ").strip()
        # if targetFiles.lower() == "exit":
        #     print("'exit' has been entered... Now Exiting program")
        #     exit(0)
        # targetFiles = [].append(targetFiles)


    print(f"{oldProjDir=}")
    print(f"{newProjDir=}")
    print(f"{targetFiles=}")
    print(f"{renameMap=}")

    utilities.driverStart(oldProjDir, newProjDir, targetFiles, renameMap)





