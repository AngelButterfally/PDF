import os
def getFaltDictionaryPath():
    baseDir = os.path.dirname(__file__)
    path_1 = os.path.join(baseDir, "TXT", "S120_failure_code_list.txt")
    path_2 = os.path.join(baseDir, "TXT", "G120C_failure_code_list.txt")
    path_3 = os.path.join(baseDir, "TXT", "G120X_failure_code_list.txt")
    faultDictionary = [[path_1,'S120'],[path_2,'G120C'],[path_3,'G120X']]
    return faultDictionary
# baseDir = os.path.dirname(__file__)
# print(os.path.join(baseDir, "TXT22"))