import os
import shutil
from typing import List

globalDebug = True


def getFilesAndFolders(currPath):
    if os.path.exists(currPath):
        files = []
        folders = []
        allContent = os.listdir(currPath)
        for token in allContent:
            if os.path.isfile(os.path.join(currPath, token)):
                files.append(token)
            elif os.path.isdir(os.path.join(currPath, token)):
                folders.append(token)
        return files, folders
    else:
        print("ERROR:")


import re

fileTypePattern = re.compile("(\\.\\w*)+")


def parseFilesDict(filesList):
    parsedFilesDict = {}
    for file in filesList:
        parsedFile = fileTypePattern.sub("", file)
        parsedFilesDict[parsedFile] = file
    return parsedFilesDict


def navigateAndFindPath(pathTokens: List[str], baseDir: str, debug=globalDebug):
    currDir = os.path.join(baseDir)
    localDir = ""
    i = 0
    hasNavigated = False
    for token in pathTokens:
        if os.path.exists(currDir):
            files, folders = getFilesAndFolders(currDir)
            parsedFiles = parseFilesDict(files)
            # Scenarios:
            #   1) If a folder is available, always navigate down it
            #   2) if a file is the only option-> return the current directory + filename
            #   3) If neither are avaiable that should mean that the current dir is available -> return currDirr
            #   4) If scenario 3, but no folder has been navigated yet, that means we have an invalid path -> return empty string
            if token in folders:
                hasNavigated = True
                localDir = os.path.join(localDir, token)
            elif token in parsedFiles.keys():
                hasNavigated = True
                return baseDir, os.path.join(localDir, parsedFiles.get(token))
            # Block for when you have navia
            elif hasNavigated:
                return baseDir, localDir
            else:
                if debug:
                    print(f"The current import path is not found in the source folder: {currDir}")
                return "", ""
            if debug:
                print(f"{folders=}, {files=}, {parsedFiles=}")
            currDir = os.path.join(currDir, token)
        i += 1
    return "", ""


def runCopyFunction(oldImpStr: str, newImpStr: str, oldProjDir: str, newProjDir: str, debug=globalDebug):
    oldImpTokens = parseImportStr(oldImpStr)
    newImpTokens = parseImportStr(newImpStr)
    if globalDebug:
        print(f"{oldImpStr=} -> {oldImpTokens=}, \n{newImpStr=} -> {newImpTokens=}")
    oldBasePath, oldLocalPath = navigateAndFindPath(oldImpTokens, oldProjDir)
    copyFile(os.path.join(oldBasePath, oldLocalPath), os.path.join(newProjDir, oldLocalPath))
    if debug:
        print(f"{oldBasePath=}")


def parseImportStr(impStr: str, delimiter: str = ".", skipNum: int = 0):
    if impStr.lstrip().startswith("import "):
        impStr = impStr.removeprefix("import ")
    tokens = impStr.split(delimiter)
    tempList = []
    i = 0
    for elem in tokens:
        elem = elem.strip()
        if elem != "":
            if i < skipNum:
                i += 1
                continue
            tempList.append(elem)
            i += 1
    return tempList


def copyFile(oldSrcFileDir: str, newSrcFolderDir: str):
    """
    Assumes the parameters are valid full directories
    :param oldSrcFileDir:
    :param newSrcFolderDir:
    :return:
    """

    if os.path.exists(oldSrcFileDir):
        if not os.path.exists(newSrcFolderDir):
            os.makedirs(newSrcFolderDir)
        # TODO Need to fix the copy so that if you have a directory it will copy the whole directory including the files.
        shutil.copy2(oldSrcFileDir, newSrcFolderDir)
    else:
        print(f"Error occurred, path not valid: {oldSrcFileDir}")


if __name__ == '__main__':
    # oldProjDir = "/home/deck/PycharmProjects/JavaImportReferenceCopier/testFolder/Project1"
    # oldImpStr = "import com.ge.capital.cfs.lease.json.model.userprofilejson"
    #
    # newProjDir = "/home/deck/PycharmProjects/JavaImportReferenceCopier/testFolder/Project2"
    # newImpStr = "import com.myaccounts.user.userservice.model.userprofilejson"
    #
    # targetFile = "targeDoc.java"

    oldProjDir = 'C:\\Users\\Stark Laptop\\PycharmProjects\\JavaImportReferenceCopier\\testFolder\\Project1'
    oldImpStr = "import com.ge.capital.cfs.lease.json.model.userprofilejson"

    newProjDir = 'C:\\Users\\Stark Laptop\\PycharmProjects\\JavaImportReferenceCopier\\testFolder\\Project2'
    newImpStr = "import com.myaccounts.user.userservice.model.userprofilejson"

    targetFile = "targeDoc.java"

    runCopyFunction(oldImpStr, newImpStr, oldProjDir, newProjDir)
