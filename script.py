import requests
import json
import csv


def gatherSBB():
    response = requests.get(
        'https://data.sbb.ch/api/records/1.0/search/?dataset=ist-daten-sbb&facet=betreiber_id&facet=produkt_id&facet=linien_id&facet=linien_text&facet=verkehrsmittel_text&facet=faellt_aus_tf&facet=bpuic&facet=ankunftszeit&facet=an_prognose&facet=an_prognose_status&facet=ab_prognose_status&facet=ankunftsverspatung&facet=abfahrtsverspatung&refine.verkehrsmittel_text=NJ')
    resp = json.loads(response.text)
    print(resp)


gatherSBB()
