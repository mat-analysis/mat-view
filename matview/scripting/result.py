import os
import glob2 as glob

# Under DEV

def getResultFiles(res_path, patterns = []):
    def findFiles(x):
        search = os.path.join(res_path, '**', x)
        return list(glob.glob(search, recursive=True))
       
    filesList = sum(list(map(lambda p: findFiles(p), patterns)), [])
    filesList = list(set(filesList))
    filesList.sort()
    
    return filesList