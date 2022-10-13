
import os
import shutil




def runCopyFunction(oldImpStr: str, newImpStr: str):
    oldImpTokens = parseImportStr(oldImpStr)
    newImpTokens = parseImportStr(newImpStr)


def parseImportStr(impStr: str, delimiter: str = "."):
    tokens = impStr.split(delimiter)
    tempList = []
    for elem in tokens:
        elem = elem.strip()
        if elem is not "":
            tempList.append(elem)
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
        shutil.copy2(oldSrcFileDir, newSrcFolderDir)
    else:
        print(f"Error occurred, path not valid: {oldSrcFileDir}")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    args = ["import com.ge.capital.cfs.lease.json.model.userprofilejson",
            "import com.myaccounts.user.userservice.model.userprofilejson",
            "targeDoc.java"]
