from datetime import datetime, timedelta
from pytz import timezone
import datetime
import pytz
import time
import sys
import os
import struct
import math
import string
lines = []

#takes linz csv files and turns them into binary format for android app



ports = ['Auckland','Bluff','Dunedin','Gisborne','Lyttelton','Marsden Point','Napier','Nelson','Onehunga','Picton','Port Chalmers','Port Taranaki','Tauranga','Timaru','Wellington','Westport']

nztime = timezone('Pacific/Auckland')



for port in ports:

    times = []
    hts = []
    print "Starting: " + port


    for i in [2015,2016,2017,2018]:
        try:
            fp = open("csvfiles/%s_%d.csv"%(port,i),'r')
        except IOError:
            print "couldn't open \"csvfiles/%s_%d.csv\", assuming we dont have any more data for %s"%(port,i,port)
            break

            
        print fp.readline().strip().split(',')[1], port #these should be the same
        print fp.readline().strip().split(',')[1]
        #print 
        fp.readline()
        
        lines=[]
        while True:
            line = fp.readline()
            if line == '':
                break
            lines.append(line.strip())


        for line in lines:
            f = line.split(',')
            day = int(f[0])
            mon = int(f[2])
            yr = int(f[3])
            for k in range(4,len(f),2):
                if f[k]=='':
                    break
                (hr,mn) = map(int,f[k].split(':'))
                ht = float(f[k+1])
                tm = nztime.localize(datetime.datetime(yr,mon,day,hr,mn,0))
                #tm =  calendar.timegm((yr,mon,day,hr,mn,0,0,0,0))-12*60*60
                times.append(int((tm - datetime.datetime(1970, 1, 1, tzinfo=pytz.utc)).total_seconds()))
                hts.append(ht)
                
    #look for daylight savings transition stuffups
    for k in range(1,len(times)):
        diff=times[k]-times[k-1]

        if abs(diff-22350)>30*60:
            print(port,datetime.datetime.fromtimestamp(times[k]),diff/60./60.)

        #assert(diff>5.6*60*60)
        #if(diff>6.6*60*60):
        #    print(diff/60./60.)
        #    raise "merry hell"

    
    

    of = open('%s.tdat'%(port.lower(),),'w')
    print "writing %s.dat"%(port,)
    #first line of tdat file is the port name
    of.write('[%s]\n'%(string.capwords(port)))
    #then an integer representing the date of the last tide
    of.write(struct.pack('i',times[-1]))
    print "the last time in this datafile will be " + time.asctime(time.localtime(times[-1]))
    #then an integer representing the number of records
    of.write(struct.pack('i',len(hts)))
    print " the number of tide records is %d, which is about %g years worth"%(len(hts),len(hts)/(4.0*365))
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
