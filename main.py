



import os
import shutil


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
    pass

