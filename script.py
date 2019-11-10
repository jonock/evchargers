import requests
import json
from datetime import datetime
import csv

now = datetime.now()
def gatherSBB():
    response = requests.get(
        'https://data.sbb.ch/api/records/1.0/search/?dataset=ist-daten-sbb&facet=betreiber_id&facet=produkt_id&facet=linien_id&facet=linien_text&facet=verkehrsmittel_text&facet=faellt_aus_tf&facet=bpuic&facet=ankunftszeit&facet=an_prognose&facet=an_prognose_status&facet=ab_prognose_status&facet=ankunftsverspatung&facet=abfahrtsverspatung&refine.verkehrsmittel_text=NJ')
    resp = json.loads(response.text)
    print(resp)

def gatherBS(id=100004):
    response = requests.get(
        f'https://data.bs.ch/api/v2/catalog/datasets/{id}/exports/json?rows=-1&pretty=false&timezone=UTC'
    )
    resp = json.loads(response.text)
    return resp

def addData(data,filename,recent):
    with open(f'data/{filename}', 'r') as fileread:
       existingLines = [line for line in csv.reader(fileread)]
    with open (f'data/{recent}', 'r') as recentdata:
        reader2 = csv.reader(recentdata)
        for row in reader2:
            if row not in existingLines:
                print('NEWentry')
                with open(f'data/{filename}', 'a') as dbfile:
                    appender = csv.writer(dbfile)
                    appender.writerow(row)
                    dbfile.close()
    fileread.close()
    recentdata.close()




def writeCSVinit(data, filename):
    file = open(f'data/{filename}', 'w')
    csvwriter = csv.writer(file)
    count = 0
    for i in data:
        if count == 0:
            header = data[1].keys()
            csvwriter.writerow(header)
            count+=1
        csvwriter.writerow(i.values())
    file.close()

def addTimestamp(filename):
    add = now.strftime("%y%m%d_%H%M%S")
    filename = filename + '_' + add
    return filename

def writeCSVcont(data, filename):
    filename = addTimestamp(filename) + '.csv'
    file = open(f'data/{filename}', 'w')
    csvwriter = csv.writer(file)
    count = 0
    for i in data:
        if count == 0:
            header = data[1].keys()
            csvwriter.writerow(header)
            count+=1
        csvwriter.writerow(i.values())
    file.close()
    return filename

data = gatherBS(100004)
#writeCSVinit(data, 'evchargers.csv')
recent = writeCSVcont(data, 'evchargers')
addData(data,'evchargers.csv', recent)
print('Neue Tabelle geschrieben: ' + recent)


