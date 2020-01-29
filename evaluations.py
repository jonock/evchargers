from datetime import datetime

import pandas as pd

import datakicker as dk
from credentials import chartid1, chartid2, chartid3


def importdata():
    data = pd.read_csv('data/evchargers.csv')
    return data


def uniquelist(list1):
    uniquedrop = list1.drop_duplicates(subset=['addresse', 'parkingfield'])
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


data = importdata()
unique = uniquelist(data)
summaryclean = iteratechargers()
summaryd1 = iteratechargersd()
summaryd2 = iteratechargersd2()
datasize = len(data.index) - 1
timeframe0 = datetime.strptime(data.iloc[1, 3][:19], '%Y-%m-%dT%H:%M:%S')
timeframe1 = datetime.strptime(data.iloc[(datasize), 3][:19], '%Y-%m-%dT%H:%M:%S')
timeframe = datetime.strftime(timeframe0, "%d.%m.%Y, %H:%M") + ' bis zum ' + datetime.strftime(timeframe1,
                                                                                               "%d.%m.%Y, %H:%M")
print(timeframe)
print('finito')
dk.updatedwchart(chartid1, summaryclean, timeframe)
dk.updatedwchart(chartid2, summaryd1, timeframe)
dk.updatedwchart(chartid3, summaryd2, timeframe)
