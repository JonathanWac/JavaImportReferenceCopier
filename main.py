import os
import shutil
from typing import List, Dict
import re
from pathlib import Path

globalDebug = True


def copytree(src, dst, symlinks=False, ignore=None):
    if not os.path.exists(dst):
        os.makedirs(dst)
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            copytree(s, d, symlinks, ignore)
        else:
            if not os.path.exists(d) or os.stat(s).st_mtime - os.stat(d).st_mtime > 1:
                shutil.copy2(s, d)


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


fileTypePattern = re.compile("(\\.\\w*)+")


def parseFilesDict(filesList):
    parsedFilesDict = {}
    for file in filesList:
        parsedFile = fileTypePattern.sub("", file)
        parsedFilesDict[parsedFile] = file
    return parsedFilesDict


def navigateAndFindPath2(pathTokens: List[str], baseDir: str, debug=globalDebug):
    currDir = os.path.join(baseDir)
    localDir = ""
    i = 0
    hasNavigated = False
    for token in pathTokens:
        if os.path.exists(currDir):
            # TODO Fix code so that it accesses the last token
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


def navigateAndFindPath(pathTokens: List[str], baseDir: str, debug=globalDebug):
    currDir = os.path.join(baseDir)
    localDir = ""
    i = 0
    tokenNum = 0
    hasNavigated = False
    for token in pathTokens:
        if os.path.exists(currDir):
            tokenNum += 1
            files, folders = getFilesAndFolders(currDir)
            parsedFiles = parseFilesDict(files)
            if debug:
                print(f"{folders=}, {files=}, {parsedFiles=}")
            # Scenarios:
            #   1) If a folder is available, always navigate down it
            #   2) if a file is the only option-> return the current directory + filename
            #   3) If neither are avaiable that should mean that the current dir is available -> return currDirr
            #   4) If scenario 3, but no folder has been navigated yet, that means we have an invalid path -> return empty string

            if token in folders:
                hasNavigated = True
                localDir = os.path.join(localDir, token)
                if tokenNum >= len(pathTokens):
                    return baseDir, localDir
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
            currDir = os.path.join(currDir, token)
        i += 1
    return "", ""


def convertPathToPackage(path: str, packageSep: str = "."):
    impStatement = path.replace(os.sep, packageSep)
    return impStatement


def replaceFileText(filePath: str, replacementStrs: Dict[str,str], lineByLine: bool = False):

    if lineByLine:
        lines = []
        with open(filePath) as infile:
            for line in infile:
                for origStr, replacement in replacementStrs.items():
                    line = line.replace(origStr, replacement)
                lines.append(line)
        with open(filePath, 'w') as outfile:
            for line in lines:
                outfile.write(line)
    else:
        content = None
        with open(filePath) as infile:
            content = infile.read()

        if content is not None:


            for origStr, replacement in replacementStrs.items():
                content = content.replace(origStr, replacement)

            with open(filePath, 'w') as outfile:
                outfile.write(content)




def runCopyFunction(oldImpStr: str, oldProjDir: str, newProjDir: str, map: Dict, debug=globalDebug,
                    defLocalWriteLoc: str = ""):
    replacementStrs = {}
    oldImpTokens = parseImportStr(oldImpStr)
    if globalDebug:
        print(f"{oldImpStr=} -> {oldImpTokens=}")
    oldBasePath, oldLocalPath = navigateAndFindPath(oldImpTokens, oldProjDir)
    oldFullPath = os.path.join(oldBasePath, oldLocalPath)
    if defLocalWriteLoc != "":
        newLocalPath = defLocalWriteLoc
    else:
        newLocalPath = oldLocalPath

    if os.path.isdir(oldFullPath):
        oldPath = Path(oldFullPath)
        lastDir = oldPath.name
        if lastDir in map.keys():
            newLocalPath = map.get(lastDir)
    elif os.path.isfile(oldFullPath):
        oldPath = Path(oldFullPath)
        lastDir = oldPath.parent.name
        if lastDir in map.keys():
            newLocalPath = os.path.join(map.get(lastDir), oldPath.name)

    copyFile(oldFullPath, os.path.join(newProjDir, newLocalPath))
    newImpStr = convertPathToPackage(newLocalPath)
    oldImpStr = ""
    first = True
    for token in oldImpTokens:
        if first:
            oldImpStr += token
            first = False
        else:
            oldImpStr += f".{token}"
    if oldImpStr != "":
        replacementStrs[oldImpStr] = newImpStr
    if debug:
        print(f"{oldBasePath=}")
    return replacementStrs


fromPattern = re.compile("(from\\s+\\w+(\\.\\w+)*)")
importPattern = re.compile("(import\\s+\\w+(\\.\\w+)*)")


def parseImportStr(impStr: str, delimiter: str = ".", skipNum: int = 0):
    if impStr.lstrip().startswith("from "):
        fromMatch = fromPattern.search(impStr)
        if fromMatch:
            impStr = fromMatch.group(0).removeprefix("from ")
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
        # if not os.path.exists(newSrcFolderDir):
        #     os.makedirs(newSrcFolderDir)
        if os.path.isdir(oldSrcFileDir):
            copytree(oldSrcFileDir, newSrcFolderDir)
        elif os.path.isfile(oldSrcFileDir):
            # newSrcFolderDir = 'C:\\Users\\Stark Laptop\\PycharmProjects\\JavaImportReferenceCopier\\testFolder\\Project2\\com\\ge\\capital\\cfs\\lease\\json\\model\\testFile2.txt'

            newSrcFolderPath = Path(newSrcFolderDir)
            # print(newSrcFolderPath.parent.absolute())
            if not os.path.exists(newSrcFolderPath.parent.absolute()):
                os.makedirs(newSrcFolderPath.parent.absolute())
            shutil.copy2(oldSrcFileDir, newSrcFolderDir)
        else:
            newSrcFolderPath = Path(newSrcFolderDir)
            if not os.path.exists(newSrcFolderPath.parent.absolute()):
                os.makedirs(newSrcFolderPath.parent.absolute())
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

    # targetFile = "targetDoc.java"

    # Tested for 1 file to 1 file
    # Tested for 1 folder w/ multiple files ->
    #
    oldProjDir = 'C:\\Users\\Stark Laptop\\PycharmProjects\\JavaImportReferenceCopier\\testFolder\\Project1'
    oldImpStr = "import com.ge.capital.cfs.lease.json.model"

    newProjDir = 'C:\\Users\\Stark Laptop\\PycharmProjects\\JavaImportReferenceCopier\\testFolder\\Project2'
    newImpStr = "import com.myaccounts.user.userservice.model"

    targetFilePath = "C:\\Users\\Stark Laptop\\PycharmProjects\\JavaImportReferenceCopier\\testFolder\\Project2\\com" \
                     "\\myaccounts\\user\\userservice\\model\\testFile.java"

    renameMap = {
        "model": "com\\myaccounts\\user\\userservice\\model",
        "service": "com\\myaccounts\\user\\userservice\\service"
    }
    replacementTexts = runCopyFunction(oldImpStr, oldProjDir, newProjDir, renameMap, defLocalWriteLoc="default\\assets")

    replaceFileText(targetFilePath, replacementTexts)
