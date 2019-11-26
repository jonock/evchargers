import pandas as pd
import requests

from credentials import dwToken


# DataWrapper API Connection
def dataWrapperConnect():
    print(dwToken + ' ist der Token. Erfolgreich geladen')
    headers = {
        'Authorization': f'Bearer {dwToken}',
    }

    response = requests.get('https://api.datawrapper.de/account', headers=headers)
    print(response.text)
    return response


def createDWChart(title="Test"):
    headers = {
        'Authorization': f'Bearer {dwToken}',
    }

    data = {
        "title": title,
        "type": "d3-lines"
    }

    response = requests.post('https://api.datawrapper.de/v3/charts', headers=headers, data=data)
    resp = response.json()
    print('New Chart created with id :' + resp['id'])
    id = resp['id']
    return id


def updatedwchart(id, data, timeframe='test'):
    data.to_csv('dataupload.csv', encoding='utf8')
    data = data.to_csv(encoding='utf8')
    url = f'https://api.datawrapper.de/v3/charts/{id}/data'
    headers = {
        'authorization': f'Bearer {dwToken}',
        'content-type': 'text/csv'
    }
    dataupdate = ((requests.put(url=url, headers=headers, data=data)))

    # Beschreibung Updaten
    url = f'https://api.datawrapper.de/v3/charts/{id}'
    headers = {
        'authorization': f'Bearer {dwToken}'
    }
    message = 'Zeitraum der Daten: ' + timeframe
    payload = {
        'metadata': {
            'annotate': {
                'notes': f'{message}'
            }
        }
    }
    #    payload = json.dumps(payload)
    description = ((requests.patch(url=url, headers=headers, json=payload)))
    url = f'https://api.datawrapper.de/charts/{id}/publish'
    payload = ({'json': True})
    publish = (requests.post(url=url, headers=headers, json=payload))
    print(publish.json())


def addDWData(id, dataimp):
    headers = {
        'authorization': f'Bearer {dwToken}',
        'content-type': 'text/csv'
    }
    print(dataimp)
    data = dataimp.to_csv(f'data/dwcharts/{id}_data.csv', index=True, encoding='utf-8')
    print(repr(data))
    url = f'https://api.datawrapper.de/v3/charts/{id}/data'

    #    respo = requests.put(url, headers=headers, data=data)
    #    webbrowser.open(f'https://datawrapper.de/chart/{id}/upload')
    headers = {
        'authorization': f'Bearer {dwToken}'
    }
    print((requests.put(url=f'https://api.datawrapper.de/v3/charts/{id}/data', headers=headers, body=data).json()))


def getChartMetadata(id):
    headers = {
        'authorization': f'Bearer {dwToken}'
    }
    metadataJson = requests.get(url=f'https://api.datawrapper.de/v3/charts/{id}', headers=headers)
    metadataDict = metadataJson.json()
    print('Metadaten erhalten')
    return metadataDict, metadataJson


def metaDatatemp():
    metadata, metadataJson = getChartMetadata('f8YHe')
    pd.DataFrame.from_dict(metadata['metadata']['visualize']).to_csv('meta.csv')
