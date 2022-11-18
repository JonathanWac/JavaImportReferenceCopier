import os


def writeOutToFile(outfileLocation: os.path, outString: str, append = True):

    if append:
        with open(outfileLocation, "a") as outFile:
            outFile.write(outString)
    else:
        with open(outfileLocation, "w") as outFile:
            outFile.write(outString)