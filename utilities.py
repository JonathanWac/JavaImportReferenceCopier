import os
import shutil
import sys
from typing import List, Dict
import re
from pathlib import Path

import CONSTS
import CommonUtilities

globalDebug = CONSTS.debug


def copytree(src, dst, symlinks=False, ignore=None):
    if not os.path.exists(dst):
        os.makedirs(dst)
    for item in os.listdir(src):
        oldSrcItem = os.path.join(src, item)
        newSrcItem = os.path.join(dst, item)
        if os.path.isdir(oldSrcItem):
            copytree(oldSrcItem, newSrcItem, symlinks, ignore)
        else:
            # If the destination is a file, and does not already exists, then copy
            # If the src file has been modified after the destination file has been,
            #   then copy over and update the destination file
            if not os.path.exists(newSrcItem) or os.stat(oldSrcItem).st_mtime - os.stat(newSrcItem).st_mtime > 1:
                addFilesToRecursionList(oldSrcItem, newSrcItem)
                if newSrcItem not in CONSTS.allCopiedFiles:
                    CONSTS.allCopiedFiles.append(newSrcItem)
                shutil.copy2(oldSrcItem, newSrcItem)


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

def __navigateAndFindPath_recursiveCall(pathTokens: List[str], baseDir: str, debug=globalDebug):
    currDir = os.path.join(baseDir)
    localDir = ""
    i = 0
    tokenNum = 0
    hasNavigated = False
    foundDirsList= []
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
                # Recursive solution: From here, call the base recursive function to start.
                #  The recursive function will create a global list so that it can crawl down the current directory
                #  and search every possible subdirectory

                if debug:
                    print(f"The current import path is not found in the source folder: {currDir}")
                return "", ""
            currDir = os.path.join(currDir, token)
        i += 1
    return "", ""

def navigateAndFindPath_recursiveStart(pathTokens: List[str], baseDir: str, debug=globalDebug):
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
                # Recursive solution: From here, call the base recursive function to start.
                #  The recursive function will create a global list so that it can crawl down the current directory
                #  and search every possible subdirectory

                if debug:
                    print(f"The current import path is not found in the source folder: {currDir}")
                return "", ""
            currDir = os.path.join(currDir, token)
        i += 1
    return "", ""


def navigateAndFindPath_old(pathTokens: List[str], baseDir: str, debug=globalDebug):
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
                # Recursive solution: From here, call the base recursive function to start.
                #  The recursive function will create a global list so that it can crawl down the current directory
                #  and search every possible subdirectory

                if debug:
                    print(f"The current import path is not found in the source folder: {currDir}")
                return "", ""
            currDir = os.path.join(currDir, token)
        i += 1
    return "", ""


def convertPathToPackage(path: str, packageSep: str = "."):
    impStatement = path.replace(os.sep, packageSep)
    return impStatement


def replaceFileText(filePath: str, replacementStrs: Dict[str, str], lineByLine: bool = False):
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


def getNewLocalPath(oldBasePath: str, oldLocalPath: str, defLocalWriteLoc: str, replacementStrTuples: List):

    if defLocalWriteLoc == "":
        newLocalPath = oldLocalPath
    else:
        newLocalPath = defLocalWriteLoc

    for key, val in replacementStrTuples:
        if key.lower() in oldLocalPath.lower():
            path = ""
            for token in val.split("."):
                path = os.path.join(path, token)
            newLocalPath = path
            break

    if os.path.isfile(os.path.join(oldBasePath, oldLocalPath)):
        fullPath = Path(os.path.join(oldBasePath, oldLocalPath))
        print(f"Filename: {fullPath.name}")
        newLocalPath = os.path.join(newLocalPath, fullPath.name)

    return newLocalPath

def runCopyFunction(oldImpStrTuple: str, oldProjDir: str, newProjDir: str, replacementStrMap: Dict, debug=globalDebug,
                    defLocalWriteLoc: str = "", replacementStrs: Dict[str, str] = None ):
    if replacementStrs is None:
        replacementStrs = {}

    oldImpTokens = parseImportStr(oldImpStrTuple[0])

    for impStrs in CONSTS.defaultNonFoundImpStatements:
        if oldImpStrTuple[0] in impStrs:
            if debug:
                print(f"Skipping Non Found Import Statements: \n\t{impStrs} from {oldImpStrTuple[0]}")
            return replacementStrs

    #Checking if the import tokens are any default Java library imports
    # TODO test
    if len(oldImpTokens) > 0:
        prefixToken = oldImpTokens[0]
        for impStatementTokens in CONSTS.defaultJavaImportPrefixBlacklist:
            if prefixToken == impStatementTokens:
                if debug:
                    print(f"Skipping Default Import: \n\t{impStatementTokens} from {oldImpStrTuple[0]}")
                CONSTS.defaultJavaImportBlacklist.append(oldImpStrTuple[0])
                return replacementStrs


    recursiveFlag = True
    #Checking if any keywords, like Service or Dao, are inside the import statement.
    # If so, copy it but do not add it to the list of recursive files to clean
    for nonRecursiveFlagToken in CONSTS.defaultJavaImportNonRecursiveTokens:
        for impStatementTokens in oldImpTokens:
            if nonRecursiveFlagToken in impStatementTokens:
                recursiveFlag = False
                break
        # if nonRecursiveFlagToken in oldImpStrTuple[0]:
        #     print("NonRecursiveFlagToken")

    if globalDebug:
        print(f"{oldImpStrTuple=} -> {oldImpTokens=}")
    oldBasePath, oldLocalPath = navigateAndFindPath_old(oldImpTokens, oldProjDir)

    # TODO test
    # No file could be found from the imp str, so we will save the string so it will note be run later
    if oldBasePath == "" and oldLocalPath == "":
        CONSTS.defaultNonFoundImpStatements.append(oldImpStrTuple[0])
        return replacementStrs

    # for elem in CONSTS.defaultJavaImportNonRecursiveTokens:
    #     if elem in oldLocalPath:
    #         recursiveFlag = False
    #         break

    oldFullPath = os.path.join(oldBasePath, oldLocalPath)
    newLocalPath = getNewLocalPath(oldBasePath, oldLocalPath, defLocalWriteLoc, replacementStrMap)
    newFullPath = os.path.join(newProjDir, newLocalPath)
    # True means that the file is allowed to be used for recursion, meaning it should be added to the global target files
    # # TODO TEST
    # if os.path.isfile(newFullPath):
    #     if recursiveFlag:
    #         CONSTS.targetFilesList.append(newFullPath)
    #     else:
    #         CONSTS.manualEditFiles.append(newFullPath)

    copyFile(oldFullPath, newFullPath)
    newImpStr = convertPathToPackage(newLocalPath)
    oldImpStrTuple = ""
    first = True
    for impStatementTokens in oldImpTokens:
        if first:
            oldImpStrTuple += impStatementTokens
            first = False
        else:
            oldImpStrTuple += f".{impStatementTokens}"
    if oldImpStrTuple != "":
        replacementStrs[oldImpStrTuple] = newImpStr
    if debug:
        print(f"{oldBasePath=}")
    return replacementStrs


fromPattern = re.compile("(from\\s+\\w+(\\.\\w+)*)")
importPattern = re.compile("(import\\s+\\w+(\\.\\w+)*)")


#TODO handle Static import strings
def parseImportStr(impStr: str, delimiter: str = ".", skipNum: int = 0)-> List[str]:
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

def addFilesToRecursionList(oldSrcFileLoc: str, newSrcFileLoc):
    recursiveFlag = True
    for elem in CONSTS.defaultJavaImportNonRecursiveTokens:
        if elem.lower() in oldSrcFileLoc.lower():
            recursiveFlag = False
            break

    if recursiveFlag and CONSTS.allowRecursion:
        if newSrcFileLoc not in CONSTS.targetFilesList:
            CONSTS.targetFilesList.append(newSrcFileLoc)
    else:
        if newSrcFileLoc not in CONSTS.manualEditFiles:
            CONSTS.manualEditFiles.append(newSrcFileLoc)

def copyFile(oldSrcLoc: str, newSrcLoc: str):
    """
    Assumes the parameters are valid full directories
    :param oldSrcLoc:
    :param newSrcLoc:
    :return:
    """

    if os.path.exists(oldSrcLoc):
        # if not os.path.exists(newSrcFolderDir):
        #     os.makedirs(newSrcFolderDir)
        if os.path.isdir(oldSrcLoc):
            copytree(oldSrcLoc, newSrcLoc)
        else:
            newSrcFolderPath = Path(newSrcLoc)
            if not os.path.exists(newSrcFolderPath.parent.absolute()):
                os.makedirs(newSrcFolderPath.parent.absolute())
            if not os.path.exists(newSrcLoc) or os.stat(oldSrcLoc).st_mtime - os.stat(newSrcLoc).st_mtime > 1:
                addFilesToRecursionList(oldSrcLoc, newSrcLoc)
                if newSrcLoc not in CONSTS.allCopiedFiles:
                    CONSTS.allCopiedFiles.append(newSrcLoc)
                shutil.copy2(oldSrcLoc, newSrcLoc)
    else:
        print(f"Error occurred, path not valid: {oldSrcLoc}")


# TODO may need to change ? to a {1}
fromImportPattern = re.compile("(from\\s+\\w+(\\.\\w+)*){1}(\\s+import\\s+\\w+(\\.\\w+)*)*")


def parseImpStringsFromFile(infileName: str) -> List[str]:
    finalImpStrList = []
    with open(infileName) as inFile:
        inFileData = inFile.read()

        fromImportMatches = fromImportPattern.findall(inFileData)
        for importMatch in fromImportMatches:
            if importMatch not in finalImpStrList:
                finalImpStrList.append(importMatch)
        # TODO check on Java project exacly how from __ import __ statements work
        importMatches = importPattern.findall(inFileData)
        for importMatch in importMatches:
            isPresent = False
            for importFroms in finalImpStrList:
                if importMatch in importFroms:
                    isPresent = True
                    continue
            if not isPresent:
                finalImpStrList.append(importMatch)

    return finalImpStrList


def parseReplacementStrs(replacementStrsDict: Dict[str, str]) -> Dict[str, str]:
    # TODO BEST Sort by length, smallest first. Then go through the list of keys and replace any
    #  substring values with the key if present

    replacementStrsList = [[key, val] for key, val in sorted(replacementStrsDict.items(), key = lambda ele: len(ele[0]))]
    print(f"ReplaceStrsList before: {replacementStrsList}")

    for i in range(len(replacementStrsList)):
        for j in range(len(replacementStrsList)):
            if i == j:
                continue
            keyI = replacementStrsList[i][0]
            keyJ = replacementStrsList[j][0]

            if keyI in keyJ:
                keyJ = keyJ.replace(keyI, replacementStrsList[i][1])
                replacementStrsList[j][0] = keyJ
    print(f"ReplaceStrsList after: {replacementStrsList}")

    return {k: v for k, v in replacementStrsList}


def driverStart(oldProjDir: str, newProjDir: str, targetFiles: List[str], renameMap: Dict[str, str] = CONSTS.defaultReplaceStrMappings,
                defLocalWriteLoc=CONSTS.defaultUnmappedFilesDir):

    allImpStrsRan = []
    for targetFile in targetFiles:
        if targetFile not in CONSTS.targetFilesList:
            CONSTS.targetFilesList.append(targetFile)

    for targetFile in CONSTS.targetFilesList:
        oldImpStrTuples = parseImpStringsFromFile(targetFile)
        for impStrRan in allImpStrsRan:
            if impStrRan in oldImpStrTuples:
                oldImpStrTuples.remove(impStrRan)

        replacementStrs = {}
        for oldImpStatementTuple in oldImpStrTuples:
            replacementStrs = runCopyFunction(oldImpStatementTuple, oldProjDir, newProjDir, renameMap, defLocalWriteLoc=defLocalWriteLoc,replacementStrs=replacementStrs)
        # TODO sort replacementStrs in order of string length
        # TODO Complex sort: Group strings that share common substrings,
        #   sort by length, then resort the entire list by length

        # TODO BEST Sort by length, smallest first. Then go through the list of keys and replace any
        #  substring values with the key if present
        #
        replacementStrs = parseReplacementStrs(replacementStrs)
        replaceFileText(targetFile, replacementStrs)
        allImpStrsRan.extend(oldImpStrTuples)

    print(f"The following files need to be manually editted: \n\t{CONSTS.manualEditFiles}")
    CommonUtilities.writeOutToFile(os.path.join(os.getcwd(), CONSTS.outFileName), f"{CONSTS.outPutFileHeader} {len(CONSTS.manualEditFiles)} files copied, but not cleaned: \n{CONSTS.manualEditFiles}", append=True)

