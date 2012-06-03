import calendar
import time
import sys
import os
import struct
import math
import string
lines = []

#takes linz csv files and turns them into binary format for android app



ports = ['auckland','bluff','dunedin','gisborne','lyttelton','marsden point','napier','nelson','onehunga','picton','port chalmers','taranaki','tauranga','timaru','wellington','westport']



for port in ports:

    times = []
    hts = []
    print "Starting: " + port


    for i in [2012,2013]:
        
        fp = open("%s/%d.csv"%(port,i),'r')
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
            for k in [4,6,8,10]:
                if f[k]=='':
                    break
                (hr,mn) = map(int,f[k].split(':'))
                ht = float(f[k+1])
                tm = calendar.timegm((yr,mon,day,hr,mn,0,0,0,0))-12*60*60
                times.append(tm)
                hts.append(ht)
                
    of = open('%s.tdat'%(port,),'w')
    print "writing %s.dat"%(port,)
    print "-------------------------------"
    #first line of tdat file is the port name
    of.write('[%s]\n'%(string.capwords(port),))
    #then an integer representing the date of the last tide
    of.write(struct.pack('i',times[-1]))
    #then an integer representing the number of records
    of.write(struct.pack('i',len(hts)))
    #then for each record an integer valued time and a byte representing the height in decimeters
    for k in range(len(hts)):
        of.write(struct.pack('ib',times[k],int(round(hts[k]*10))))
    #    print time.asctime(time.localtime(times[k]))
    of.close()
            

#test
