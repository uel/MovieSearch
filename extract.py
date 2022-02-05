import zipfile
import os
from bs4 import BeautifulSoup

with zipfile.ZipFile('en.zip') as zf:
    i = 0
    for file in zf.namelist():
        if ".xml" in file:
            target = file.replace("OpenSubtitles/raw/en", "data").replace(".xml", ".txt")
            os.makedirs(os.path.dirname(target), exist_ok=True)

            i+=1
            print(i, file)

            soup = BeautifulSoup(zf.read(file), 'xml')
            with open(target, "w") as o:
                for l in soup.find_all("s"):
                    o.write(l.text.strip()+"\n")
                