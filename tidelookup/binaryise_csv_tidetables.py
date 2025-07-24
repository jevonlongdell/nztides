from datetime import datetime
from pytz import timezone
import datetime
import pytz
import time
import struct
import string
from pathlib import Path
lines = []

#takes linz csv files and turns them into binary format for android app



ports = ['Akaroa', 'Anakakata Bay', 'Anawhata', 'Auckland', 'Ben Gunn Wharf', 'Bluff', 'Castlepoint', 'Charleston', 'Dargaville', 'Deep Cove', 'Dog Island', 'Dunedin', 'Elaine Bay', 'Elie Bay', 'Fishing Rock - Raoul Island', 'Flour Cask Bay', 'Fresh Water Basin', 'Gisborne', 'Green Island', 'Halfmoon Bay - Oban', 'Havelock', 'Helensville', 'Huruhi Harbour', 'Jackson Bay', 'Kaikōura', 'Kaingaroa - Chatham Island', 'Kaiteriteri', 'Kaituna River Entrance', 'Kawhia', 'Korotiti Bay', 'Leigh', 'Long Island', 'Lottin Point - Wakatiri', 'Lyttelton', 'Mana Marina', 'Man o\'War Bay', 'Manu Bay', 'Māpua', 'Marsden Point', 'Matiatia Bay', 'Motuara Island', 'Moturiki Island', 'Napier', 'Nelson', 'New Brighton Pier', 'North Cape - Otou', 'Oamaru', 'Ōkukari Bay', 'Omaha Bridge', 'Ōmokoroa', 'Onehunga', 'Opononi', 'Ōpōtiki Wharf', 'Opua', 'Owenga - Chatham Island', 'Paratutae Island', 'Picton', 'Port Chalmers', 'Port Ōhope Wharf', 'Port Taranaki', 'Pouto Point', 'Raglan', 'Rangatira Point', 'Rangitaiki River Entrance', 'Richmond Bay', 'Riverton - Aparima', 'Scott Base', 'Spit Wharf', 'Sumner Head', 'Tamaki River', 'Tarakohe', 'Tauranga', 'Te Weka Bay', 'Thames', 'Timaru', 'Town Basin', 'Waihopai River Entrance', 'Waitangi - Chatham Island', 'Weiti River Entrance', 'Welcombe Bay', 'Wellington', 'Westport', 'Whakatāne', 'Whanganui River Entrance', 'Whangārei', 'Whangaroa', 'Whitianga', 'Wilson Bay']
years = [2025,2026,2027]

nztime = timezone('Pacific/Auckland')

# Delete all .tdat files in assets directory before downloading new ones
assets_dir = Path(__file__).parent.parent / 'nztides_app' / 'app' / 'src' / 'main' / 'assets'
for f in assets_dir.glob('*.tdat'):
    if f.is_file():
        f.unlink()


for port in ports:

    times = []
    hts = []
    print("Starting: " + port)

    for year in years:
        fp = None
        csv_path = f"csvfiles/{port}_{year}.csv"
        csv_filename = Path(csv_path).name
        try:
            fp = open(csv_path,'r', encoding='utf-8-sig')
            # Try reading a line to trigger decode error if present
            pos = fp.tell()
            test_line = fp.readline()
            fp.seek(pos)
        except UnicodeDecodeError:
            if fp:
                fp.close()
            print(f"UnicodeDecodeError in '{csv_filename}', retrying as windows-1252")
            fp = open(csv_path,'r', encoding='windows-1252')
        except IOError:
            print(f"couldn't open '{csv_filename}', assuming we dont have any more data for {port}")
            break

        # Skip the first line (metadata/header)
        fp.readline()
        # Collect only lines that start with a digit (the day)
        lines = []
        while True:
            line = fp.readline().strip()
            if line == '':
                break
            if line and line[0].isdigit():
                lines.append(line)

        for line in lines:
            f = line.split(',')
            day = int(f[0])
            mon = int(f[2])
            yr = int(f[3])
            for k in range(4,len(f),2):
                if k+1 >= len(f) or f[k]=='' or f[k+1]=='':
                    break
                hr, mn = map(int, f[k].split(':'))
                ht = float(f[k+1])
                tm = nztime.localize(datetime.datetime(yr,mon,day,hr,mn,0))
                times.append(int((tm - datetime.datetime(1970, 1, 1, tzinfo=pytz.utc)).total_seconds()))
                hts.append(ht)
                
    #look for daylight savings transition stuffups
    for k in range(1,len(times)):
        diff=times[k]-times[k-1]

        if abs(diff-22350)>30*60:
            print(port,datetime.datetime.fromtimestamp(times[k]),diff/60./60.)

    
    

    of = open(assets_dir / f'{port}.tdat', 'wb')
    print(f"writing {port}.dat")
    #first line of tdat file is the port name
    of.write(f'[{port}]\n'.encode('utf-8'))
    #then an integer representing the date of the last tide
    of.write(struct.pack('i',times[-1]))
    print("the last time in this datafile will be " + time.asctime(time.localtime(times[-1])))
    #then an integer representing the number of records
    of.write(struct.pack('i',len(hts)))
    print(f" the number of tide records is {len(hts)}, which is about {len(hts)/(4.0*365):g} years worth")
    #then for each record an integer valued time and a byte representing the height in decimeters
    for k in range(len(hts)):
        of.write(struct.pack('ib',times[k],int(round(hts[k]*10))))
    of.close()
    print("-------------------------------")
        

#test
