from bs4 import BeautifulSoup
import random
import glob
import json

result = {}

for pathname in glob.iglob('Levels\*.oel'):
    filename = pathname.split('\\')[1]
    with open(pathname) as file:
        soup = BeautifulSoup(file.read(), 'xml')
        cores = soup.reference.find_all('col_core1')
        for core in cores:
            core['id'] = 99
        if len(cores):
            result[filename] = [str(c) for c in cores]

with open('potential_core_spots.json', 'w') as writefile:
    writefile.write(json.dumps(result))
