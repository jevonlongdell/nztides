#from datetime import datetime, timedelta
#from pytz import timezone
#import pytz
import calendar
import datetime
import time
import sys
import os
import struct
import math
import string
import glob
lines = []



def unwoke(st):
    macrons = 'āēīōūĀĒĪŌŪ'
    replacements = 'aeiouAEIOU'

    for (m,r) in zip(macrons,replacements):
        st = st.replace(m,r)

    return st


#takes linz csv files and turns them into binary format for android app



#ports = ['Auckland','Bluff','Dunedin','Gisborne','Lyttelton','Marsden Point','Napier','Nelson','Onehunga','Picton','Port Chalmers','Port Taranaki','Tauranga','Timaru','Wellington','Westport']


#ports = [ 'Akaroa',
#          'Anawhata',
#          'Auckland', 'Ben Gunn Wharf', 'Bluff', 'Castlepoint', 'Deep Cove', 'Dunedin', 'Flour Cask Bay', 'Fresh Water Basin', 'Gisborne', 'Green Island', 'Havelock', 'Huruhi Harbour', 'Jackson Bay', 'Kaikoura', 'Kaingaroa', 'Kaiteriteri', 'Kaituna River', 'Kawhia', 'Korotiti Bay', 'Leigh', 'Lottin Point', 'Lyttelton', 'Mana', 'Man o\'War Bay', 'Mapua', 'Marsden Point', 'Matiatia Bay', 'Napier', 'Nelson', 'North Cape (Otou)', 'Oamaru', 'Oban', 'Omokoroa', 'Onehunga', 'Opotiki Wharf', 'Opua', 'Owenga', 'Paratutae Island', 'Picton', 'Port Chalmers', 'Port Ohope Wharf', 'Port Taranaki', 'Pouto Point', 'Raglan',  'Rocky Point',  'Scott Base', 'Spit Wharf', 'Sumner', 'Tarakohe', 'Tauranga', 'Timaru', 'Waiorua Bay', 'Waitangi (Chatham Is)', 'Whanganui River Entrance', 'Welcombe Bay', 'Wellington', 'Westport', 'Whakatane', 'Whangarei', 'Whangaroa', 'Whitianga']

#portfilenames = ['Akaroa', 'Anawhata', 'Auckland', 'Ben Gunn Wharf', 'Bluff', 'Castlepoint', 'Deep Cove', 'Dunedin', 'Flour Cask Bay', 'Fresh Water Basin', 'Gisborne', 'Green Island', 'Havelock', 'Huruhi Harbour', 'Jackson Bay', 'Kaikoura', 'Kaingaroa', 'Kaiteriteri', 'Kaituna River', 'Kawhia', 'Korotiti Bay', 'Leigh', 'Lottin Point', 'Lyttelton', 'Mana', 'Man oWar Bay', 'Mapua', 'Marsden Point', 'Matiatia Bay', 'Napier', 'Nelson', 'North Cape (Otou)', 'Oamaru', 'Oban', 'Omokoroa', 'Onehunga', 'Opotiki Wharf', 'Opua', 'Owenga', 'Paratutae Island', 'Picton', 'Port Chalmers', 'Port Ohope Wharf', 'PortTaranaki', 'Pouto Point', 'Raglan', 'Rocky Point', 'Scott Base', 'Spit Wharf', 'Sumner', 'Tarakohe', 'Tauranga', 'Timaru', 'Waiorua Bay', 'Waitangi (Chatham Is)', 'Whanganui River Entrance', 'Welcombe Bay', 'Wellington', 'Westport', 'Whakatane', 'Whangarei', 'Whangaroa', 'Whitianga']





#nztime = timezone('Pacific/Auckland')


portfilenames = glob.glob('txtfiles/*_2022-23.txt')

portnames = [x.removeprefix('txtfiles/').removesuffix('_2022-23.txt').replace('_',' ') for x in portfilenames]



for (kk,(port,file)) in enumerate(zip(portnames,portfilenames)):
    
    times = []
    hts = []
    print("Starting: " + port)
    #try:
    fp = open(file,'r')
    #except (IOError,IndexError):
#            print("couldn't open datafile %s for %s,%d, assuming we dont have any more data for %s"%(filenames[0],port,i,port))
#            input("Press Enter to continue...")
#            break
        

            
    header =  fp.readline().strip()[3:].replace('  ',' ')
    print(header, port)
    assert(unwoke(header)==unwoke(port)) #these should be the same
    fp.readline()
    #print 
    fp.readline()
        
    lines=[]
    while True:
        line = fp.readline()
        if line == '':
            break
        lines.append(line.strip())


    for line in lines:
            f = [v for v in line.split(' ') if v!='']
            day = int(f[0])
            dow = f[1]
            mon = int(f[2][:-2])
            yr = int(f[2][-2:])
            yr=yr+2000
#            print day, dow, mon, yr
            for k in range(3,len(f),2):
                if f[k]=='9999':
                    break
                hr = int(f[k][:2])
                mn = int(f[k][2:])
                ht = float(f[k+1])
                #tm = nztime.localize(datetime.datetime(yr,mon,day,hr,mn,0))
                #times.append(int((tm - datetime.datetime(1970, 1, 1, tzinfo=pytz.utc)).total_seconds()))
                tm =  calendar.timegm((yr,mon,day,hr,mn,0,0,0,0))-12*60*60
                times.append(tm)
                hts.append(ht)
                

    of = open('%s.tdat'%(port),'wb')
    print("writing %s.dat"%(port,))
    #first line of tdat file is the port name
    of.write(f"[{port}]\n".encode())
    #then an integer representing the date of the last tide
    of.write(struct.pack('i',times[-1]))
    print("the last time in this datafile will be " + time.asctime(time.localtime(times[-1])))
    #then an integer representing the number of records
    of.write(struct.pack('i',len(hts)))
    print("For %s the number of tide records is %d, which is about %g years worth"%(port,len(hts),len(hts)/(4.0*365)))
    #then for each record an integer valued time and a byte representing the height in decimeters
    for k in range(len(hts)):
        of.write(struct.pack('ib',times[k],int(round(hts[k]*10))))
        #print time.asctime(time.localtime(times[k]))
    of.close()
    
   # of = open('%s.txt'%(port,),'w')
   # for k in range(len(hts)):
   #     of.write('%d\n'%(times[k],))
   # of.close()
    print("-------------------------------")
        

portnames.sort(key=unwoke)       

print("{",end='')
for (kk,p) in enumerate(portnames):
    if kk!=0:
        print(", ",end='')
    print(f"\"{p}\"",end='')
print("}")



#test
