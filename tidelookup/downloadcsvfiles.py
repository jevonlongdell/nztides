import os
import glob
import urllib.request
import urllib.parse

# Delete all .csv files in csvfiles directory before downloading new ones
csv_dir = 'csvfiles'
os.makedirs(csv_dir, exist_ok=True)

for f in glob.glob(os.path.join(csv_dir, '*.csv')):
    if os.path.isfile(f):
        os.remove(f)
# alternatively, probably cleaner to use git: git rm "tidelookup/csvfiles/*.csv" 

lines = []

#takes linz csv files and turns them into binary format for android app

# ports = ['Auckland','Bluff','Dunedin','Gisborne','Lyttelton','Marsden Point','Napier','Nelson','Onehunga','Picton','Port Chalmers','Port Taranaki','Tauranga','Timaru','Wellington','Westport', 'Whitianga']
ports = ['Akaroa', 'Anakakata Bay', 'Anawhata', 'Auckland', 'Ben Gunn Wharf', 'Bluff', 'Castlepoint', 'Charleston', 'Dargaville', 'Deep Cove', 'Dog Island', 'Dunedin', 'Elaine Bay', 'Elie Bay', 'Fishing Rock - Raoul Island', 'Flour Cask Bay', 'Fresh Water Basin', 'Gisborne', 'Green Island', 'Halfmoon Bay - Oban', 'Havelock', 'Helensville', 'Huruhi Harbour', 'Jackson Bay', 'Kaikōura', 'Kaingaroa - Chatham Island', 'Kaiteriteri', 'Kaituna River Entrance', 'Kawhia', 'Korotiti Bay', 'Leigh', 'Long Island', 'Lottin Point - Wakatiri', 'Lyttelton', 'Mana Marina', 'Man o\'War Bay', 'Manu Bay', 'Māpua', 'Marsden Point', 'Matiatia Bay', 'Motuara Island', 'Moturiki Island', 'Napier', 'Nelson', 'New Brighton Pier', 'North Cape - Otou', 'Oamaru', 'Ōkukari Bay', 'Omaha Bridge', 'Ōmokoroa', 'Onehunga', 'Opononi', 'Ōpōtiki Wharf', 'Opua', 'Owenga - Chatham Island', 'Paratutae Island', 'Picton', 'Port Chalmers', 'Port Ōhope Wharf', 'Port Taranaki', 'Pouto Point', 'Raglan', 'Rangatira Point', 'Rangitaiki River Entrance', 'Richmond Bay', 'Riverton - Aparima', 'Scott Base', 'Spit Wharf', 'Sumner Head', 'Tamaki River', 'Tarakohe', 'Tauranga', 'Te Weka Bay', 'Thames', 'Timaru', 'Town Basin', 'Waihopai River Entrance', 'Waitangi - Chatham Island', 'Weiti River Entrance', 'Welcombe Bay', 'Wellington', 'Westport', 'Whakatāne', 'Whanganui River Entrance', 'Whangārei', 'Whangaroa', 'Whitianga', 'Wilson Bay']
years = [2025,2026,2027]

for port in ports:
    for year in years:
        print("Downloading ",port,year)
        port_encoded = urllib.parse.quote(port)
        url = f'https://static.charts.linz.govt.nz/tide-tables/maj-ports/csv/{port_encoded}%20{year}.csv'
        resp = urllib.request.urlopen(url)
        with open(os.path.join(csv_dir, f'{port}_{year}.csv'), 'wb') as fp:
            fp.write(resp.read())

print('-------------------------------------------------------------------------------')
print('here is a Java variable declaration for portdisplaynames using the current ports list. This makes it easy to copy the array directly into NZTides.java')
print('final private String[] portdisplaynames = {"' + '\", "'.join(ports) + '"};')
