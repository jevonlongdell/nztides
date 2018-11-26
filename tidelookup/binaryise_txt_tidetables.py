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

#takes linz csv files and turns them into binary format for android app



#ports = ['Auckland','Bluff','Dunedin','Gisborne','Lyttelton','Marsden Point','Napier','Nelson','Onehunga','Picton','Port Chalmers','Port Taranaki','Tauranga','Timaru','Wellington','Westport']


ports = ['Anawhata', 'Auckland', 'Ben Gunn', 'Bluff', 'Castlepoint', 'Deep Cove', 'Dunedin', 'Flour Cask Bay', 'French Bay', 'Fresh Water Basin', 'Gisborne', 'Green Island', 'Havelock', 'Huruhi Harbour', 'Jackson Bay', 'Kaikoura', 'Kaingaroa', 'Kaiteriteri', 'Kaituna River', 'Kawhia', 'Korotiti Bay', 'Leigh', 'Lottin Point', 'Lyttelton', 'Mana', 'Man o\'War Bay', 'Mapua', 'Marsden Point', 'Matiatia Bay', 'Napier', 'Nelson', 'North Cape (Otou)', 'Oamaru', 'Oban', 'Omokoroa', 'Onehunga', 'Opotiki Wharf', 'Opua', 'Owenga', 'Paratutae Island', 'Picton', 'Port Chalmers', 'Port Ohope Wharf', 'Port Taranaki', 'Pouto Point', 'Raglan', 'Rocky Point',  'Spit Wharf', 'Sumner', 'Tarakohe', 'Tauranga', 'Timaru', 'Waiorua Bay', 'Whanganui River Entrance', 'Wellington', 'Westport', 'Whakatane', 'Whangarei', 'Whangaroa', 'Whitianga']

portfilenames = ['Anawhata', 'Auckland', 'Ben Gunn', 'Bluff', 'Castlepoint', 'Deep Cove', 'Dunedin', 'Flour Cask Bay', 'French Bay', 'Fresh Water Basin', 'Gisborne', 'Green Island', 'Havelock', 'Huruhi Harbour', 'Jackson Bay', 'Kaikoura', 'Kaingaroa', 'Kaiteriteri', 'Kaituna River', 'Kawhia', 'Korotiti Bay', 'Leigh', 'Lottin Point', 'Lyttelton', 'Mana', 'Mano War Bay', 'Mapua', 'Marsden Point', 'Matiatia Bay', 'Napier', 'Nelson', 'North Cape (Otou)', 'Oamaru', 'Oban', 'Omokoroa', 'Onehunga', 'Opotiki Wharf', 'Opua', 'Owenga', 'Paratutae Island', 'Picton', 'Port Chalmers', 'Port Ohope Wharf', 'Port Taranaki', 'Pouto Point', 'Raglan', 'Rocky Point', 'Spit Wharf', 'Sumner', 'Tarakohe', 'Tauranga', 'Timaru', 'Waiorua Bay',  'WhanganuiRiverEntrance', 'Wellington', 'Westport', 'Whakatane', 'Whangarei', 'Whangaroa', 'Whitianga']


#nztime = timezone('Pacific/Auckland')



for kk in range(len(ports)):
    port = ports[kk]

    times = []
    hts = []
    print "Starting: " + port


    for i in [2018,2019,2020]:
        print i
        if i==2016:
            try:
                fp = open("txtfiles/%s_%d.txt"%(portfilenames[kk].replace(' ',''),i),'r')           
            except IOError:
                print "couldn't open \"csvfiles/%s_%d.csv\", assuming we dont have any more data for %s"%(port,i,port)
                input("press enter to continue")
                break
        elif True: # i==2017 or i==2018:
            filenames = glob.glob("txtfiles/???%s_%d.txt"%(portfilenames[kk].replace(' ',''),i))
            assert(len(filenames)<=1) #there should only be one text file that 
            try:
                fp = open(filenames[0],'r')
            except (IOError,IndexError):
                if len(filenames)==0:
                    filenames = [portfilenames[kk]]
                print  "couldn't open datafile %s for %s,%d, assuming we dont have any more data for %s"%(filenames[0],port,i,port)
                raw_input("Press Enter to continue...")
                break
        else:
            print "the value of i, %d didn't make sense"%(i,)
            assert(1==2)


            
        header =  fp.readline().strip()[3:].replace('  ',' ')
        print header, port
        assert(header==port) #these should be the same
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
                

    of = open('%s.tdat'%(port.lower()),'w')
    print "writing %s.dat"%(port,)
    #first line of tdat file is the port name
    of.write('[%s]\n'%(string.capwords(port)))
    #then an integer representing the date of the last tide
    of.write(struct.pack('i',times[-1]))
    print "the last time in this datafile will be " + time.asctime(time.localtime(times[-1]))
    #then an integer representing the number of records
    of.write(struct.pack('i',len(hts)))
    print "For %s the number of tide records is %d, which is about %g years worth"%(port,len(hts),len(hts)/(4.0*365))
    #then for each record an integer valued time and a byte representing the height in decimeters
    for k in range(len(hts)):
        of.write(struct.pack('ib',times[k],int(round(hts[k]*10))))
        #print time.asctime(time.localtime(times[k]))
    of.close()
    
   # of = open('%s.txt'%(port,),'w')
   # for k in range(len(hts)):
   #     of.write('%d\n'%(times[k],))
   # of.close()
    print "-------------------------------"
        
    

#test
