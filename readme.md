# EV Chargers in Basel, Switzerland

The main script gets the datasets from the open data portal of the canton BS (Basel-Stadt, not the other thing)

## Evaluations
Data gets cleaned - differences calculated, cleaned and pushed via the Datawrapper API 
The Charts with the 'dirty' Data are still in the script to demonstrate the 'datacleaning' steps. 

## More information
The Charts are used in this [blogpost](https://rideable.ch/belegung-ladestationen-iwb-auswertung/) and the data-cleaning is explained further.

## Setup
1. In order to get the script to run, update the credentials_dummy.py file and rename it to 'credentials.py' (You need a Datawrapper Token and three Chart-IDs from Datawrapper)
2. Create the folder ./data/chargers
3. Run script.py first and evaluations.py afterwards
4. Enjoy!
