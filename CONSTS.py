import datetime
import os

version_num = "0.1"
debug = True
allowRecursion = True

defaultOldProjDir = "C:\\Users\\Stark Laptop\\PycharmProjects\\JavaImportReferenceCopier\\testFolder\\Project1"
defaultNewProjDir = "C:\\Users\\Stark Laptop\\PycharmProjects\\JavaImportReferenceCopier\\testFolder\\Project2"
targetFilesList = ["C:\\Users\\Stark Laptop\\PycharmProjects\\JavaImportReferenceCopier\\testFolder\\Project2\\src\\testEditFile.java"]
defaultReplaceStrMappings = [
    ("controller", "com.myaccounts.homeservice.home_service.controller"),
    ("dao", "com.myaccounts.homeservice.home_service.dao"),
    ("dto", "com.myaccounts.homeservice.home_service.dto"),
    ("service", "com.myaccounts.homeservice.home_service.service"),
    ("model", "com.myaccounts.homeservice.home_service.model"),
    ("util", "com.myaccounts.homeservice.home_service.util"),
    ("exception", "com.myaccounts.homeservice.home_service.exception"),
    ("const", "com.myaccounts.homeservice.home_service.constants")
]
defaultUnmappedFilesDir = os.path.join("com", "myaccounts", "other")

outFileName = "JavaImportRefLogs.txt"



allCopiedFiles = []
manualEditFiles = []
defaultNonFoundImpStatements = []
defaultNonRecursiveCopyFiles = []
defaultJavaImportPrefixBlacklist = [
    "java"
]
defaultJavaImportNonRecursiveTokens = [
    "service",
    "dao"
]
defaultJavaImportBlacklist = [
    ""
]
outPutFileHeader = f"\n{datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')} "
