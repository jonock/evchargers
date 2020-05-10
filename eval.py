from datetime import datetime
from datetime import timedelta


import pandas as pd

import datakicker as dk
from credentials import chartid1, chartid2, chartid3


def importdata():
    data = pd.read_csv('data/evchargers.csv')
    return data


def uniquelist(list1):
    uniquedrop = list1.drop_duplicates(subset=['addresse', 'parkingfield'])
    return uniquedrop


def uniquelistident(list1):
    uniquedrop = list1.drop_duplicates(subset=['identifier'])
    return uniquedrop

def iteratechargers():
    entry1 = None
    summary = pd.DataFrame()
    faulty = pd.DataFrame()
    for index, row in unique.iterrows():
        thischarger = data[(data.addresse == row.addresse) & (data.parkingfield == row.parkingfield)]
        ident = str(row.addresse).replace(' ', '')[:10] + '_' + str(row.parkingfield)
        identlong = str(row.addresse)[:20] + '_' + str(row.parkingfield)

        for ind, entry in thischarger.iterrows():
            if entry1 is not None:
                entry2 = entry
                timediff = datetime.strptime(entry2.timestamp[:19], '%Y-%m-%dT%H:%M:%S') - datetime.strptime(
                    entry1.timestamp[:19], '%Y-%m-%dT%H:%M:%S')
                if timediff.total_seconds() < 90000:
                    difflist.append(timediff.total_seconds())
                else:
                    difflist.append(0)
                entry1 = entry2
            else:
                entry1 = entry
                difflist = []
        entry1 = None
        entry2 = None
        difflist.append(0)
        thischarger['differences'] = difflist
        thischarger.to_csv(f'data/chargers/{ident}.csv', index=False, header=True)
        summarytemp = thischarger.groupby('status').sum()
        summarytempdf = summarytemp['differences']
        summarytempdf = summarytempdf.rename(identlong)
        if summarytempdf.size > 1:
            summary = summary.append(summarytempdf)
        else:
            faulty = faulty.append(summarytempdf)
        print(ident + ' geschrieben')

    summary.to_csv('data/chargers/summary.csv', index=True, header=True)
    faulty.to_csv('data/chargers/faulty.csv', index=True, header=True)

    return (summary)

def dailyevaluations(data):
    averages = pd.DataFrame(columns = ['charger', 'timeavailable', 'timeoccupied', 'timeother', 'ratiooccupied'])
    unique = uniquelistident(data)['identifier']
    datanew = data
    newvals = pd.DataFrame(
        columns=['status', 'power', 'parkingfield', 'timestamp', 'geo_point_2d', 'totalparkings', 'location',
                 'addresse', 'identifier', 'difference'])
    for id in unique:
        datanewtemp = datanew.loc[datanew['identifier'] == id]
        mindate = min(datanewtemp['timestamp'])[:10]
        maxdate = max(datanewtemp['timestamp'])[:10]
        date = mindate
        dateo = datetime.strptime(date, '%Y-%m-%d').date()
        maxdateo = datetime.strptime(maxdate, '%Y-%m-%d').date()
        while dateo < maxdateo:
            dates = datetime.strftime(dateo, '%Y-%m-%d')
            thisday = datanewtemp.loc[datanewtemp['timestamp'].str.contains(dates)]
            entry1 = None
            for ind, entry in thisday.iterrows():
                if entry1 is not None:
                    entry2 = entry
                    timediff = datetime.strptime(entry2.timestamp[:19], '%Y-%m-%dT%H:%M:%S') - datetime.strptime(
                        entry1.timestamp[:19], '%Y-%m-%dT%H:%M:%S')
                    if timediff.total_seconds() < 90000:
                        entry['difference']=timediff.total_seconds()
                        newvals = newvals.append(entry, ignore_index=True)
                    else:
                        difflist.append(0)
                    entry1 = entry2
                else:
                    entry1 = entry
            entry1 = None
            entry2 = None
            dateo = dateo + timedelta(days=1)
            date = datetime.strftime(dateo, '%Y-%m-%d')
        print(id)
    newvals.to_csv('data/altered_with_timediff.csv')

def alterdata():
    altered = pd.DataFrame(columns = ['status', 'power', 'parkingfield', 'timestamp', 'geo_point_2d', 'totalparkings', 'location', 'addresse', 'identifier'])
    datanew = data
    datanew['identifier'] = 0
    datanew['identifier'] = datanew['addresse'].str.replace(' ','')+ '_' + datanew['parkingfield'].map(str)
    unique = uniquelistident(datanew)['identifier']
    for id in unique:
        datanewtemp = datanew.loc[datanew['identifier'] == id]
        mindate = min(datanewtemp['timestamp'])[:10]
        maxdate = max(datanewtemp['timestamp'])[:10]
        date = mindate
        dateo = datetime.strptime(date, '%Y-%m-%d').date()
        maxdateo = datetime.strptime(maxdate, '%Y-%m-%d').date()
        temp = datanewtemp.iloc[0]
        while dateo < maxdateo:
            dates = datetime.strftime(dateo, '%Y-%m-%d')
            datep = dateo + timedelta(days=1)
            dateps = datetime.strftime(datep, '%Y-%m-%d')
            datanewtemps = datanewtemp.loc[datanewtemp['timestamp'].str.contains(dates)]
            if len(datanewtemps) == 0:
                print(id + dates + ' leer')
                temp['timestamp'] = dates + 'T00:00:00+00:00'
                temp['status'] = 'EMPTYDAY'
                print(temp)
                datanewtemps = datanewtemps.append(temp, ignore_index=True)
            else:
                #looking for last entry of date
                ts = max(datanewtemps['timestamp'])
                #preparing appending entry
                temp = datanewtemps.loc[datanewtemps['timestamp'] == ts]
                temp['timestamp'] = dates + 'T23:59:59+00:00'
                datanewtemps = datanewtemps.append(temp, ignore_index=True)
                #appending entry for next day
                temp['timestamp'] = dateps + 'T00:00:00+00:00'
                datanewtemps = datanewtemps.append(temp, ignore_index=True)


            altered = altered.append(datanewtemps, ignore_index=True)
            dateo = dateo + timedelta(days=1)
            date = datetime.strftime(dateo, '%Y-%m-%d')

    altered.to_csv('data/altereddata.csv', index=True, header=True)
    return(altered)


# Next iteratechargers sequences just for illustration purposes
def iteratechargersd2():
    entry1 = None
    summary = pd.DataFrame()
    faulty = pd.DataFrame()
    for index, row in unique.iterrows():
        thischarger = data[(data.addresse == row.addresse) & (data.parkingfield == row.parkingfield)]
        ident = str(row.addresse).replace(' ','')[:10] + '_' + str(row.parkingfield)
        identlong = str(row.addresse)[:20] + '_' +str(row.parkingfield)

        for ind, entry in thischarger.iterrows():
            if entry1 is not None:
                entry2 = entry
                timediff = datetime.strptime(entry2.timestamp[:19], '%Y-%m-%dT%H:%M:%S') - datetime.strptime(entry1.timestamp[:19], '%Y-%m-%dT%H:%M:%S')
                difflist.append(timediff.total_seconds())
                entry1 = entry2
            else:
                entry1 = entry
                difflist = []
        entry1 = None
        entry2 = None
        difflist.append(0)
        thischarger['differences'] = difflist
        # thischarger.to_csv(f'data/chargers/{ident}.csv', index=False, header = True)
        summarytemp = thischarger.groupby('status').sum()
        summarytempdf = summarytemp['differences']
        summarytempdf = summarytempdf.rename(identlong)
        if summarytempdf.size > 1:
            summary = summary.append(summarytempdf)
        else:
            faulty = faulty.append(summarytempdf)
        print(ident + ' geschrieben')

    summary.to_csv('data/chargers/summary.csv', index=True, header=True)
    faulty.to_csv('data/chargers/faulty.csv', index=True, header=True)

    return (summary)


def iteratechargersd():
    entry1 = None
    summary = pd.DataFrame()
    faulty = pd.DataFrame()
    for index, row in unique.iterrows():
        thischarger = data[(data.addresse == row.addresse) & (data.parkingfield == row.parkingfield)]
        ident = str(row.addresse).replace(' ', '')[:10] + '_' + str(row.parkingfield)
        identlong = str(row.addresse)[:20] + '_' + str(row.parkingfield)

        for ind, entry in thischarger.iterrows():
            if entry1 is not None:
                entry2 = entry
                timediff = datetime.strptime(entry2.timestamp[:19], '%Y-%m-%dT%H:%M:%S') - datetime.strptime(
                    entry1.timestamp[:19], '%Y-%m-%dT%H:%M:%S')
                difflist.append(timediff.total_seconds())
                entry1 = entry2
            else:
                entry1 = entry
                difflist = []
        entry1 = None
        entry2 = None
        difflist.append(0)
        thischarger['differences'] = difflist
        # thischarger.to_csv(f'data/chargers/{ident}.csv', index=False, header = True)
        summarytemp = thischarger.groupby('status').sum()
        summarytempdf = summarytemp['differences']
        summarytempdf = summarytempdf.rename(identlong)
        if summarytempdf.size > 0:
            summary = summary.append(summarytempdf)
        else:
            faulty = faulty.append(summarytempdf)
        print(ident + ' geschrieben')

    summary.to_csv('data/chargers/summarydirty1.csv', index=True, header=True)

    return (summary)

def test_alter_data():
    global data
    data = importdata()
    global unique
    unique = uniquelist(data)
    global altereddata
    altereddata = alterdata()

def test_process_daily():
    data = pd.read_csv('data/altereddata.csv')
    dailyevaluations(data)

def runevals():
    global data
    data = importdata()
    global unique
    unique = uniquelist(data)
    global altereddata
    altereddata = alterdata()
    summaryclean = iteratechargers()
    summaryd1 = iteratechargersd()
    summaryd2 = iteratechargersd2()
    datasize = len(data.index) - 1
    timeframe0 = datetime.strptime(data.iloc[1, 3][:19], '%Y-%m-%dT%H:%M:%S')
    timeframe1 = datetime.strptime(data.iloc[(datasize), 3][:19], '%Y-%m-%dT%H:%M:%S')
    timeframe = datetime.strftime(timeframe0, "%d.%m.%Y, %H:%M") + ' bis zum ' + datetime.strftime(timeframe1,"%d.%m.%Y, %H:%M")
    print(timeframe)
    print('finito')
    dk.updatedwchart(chartid1, summaryclean, timeframe)
    dk.updatedwchart(chartid2, summaryd1, timeframe)
    dk.updatedwchart(chartid3, summaryd2, timeframe)
