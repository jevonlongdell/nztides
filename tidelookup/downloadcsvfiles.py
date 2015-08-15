import urllib2
import calendar
import time
import sys
import os
import struct
import math
import string
lines = []

#takes linz csv files and turns them into binary format for android app



ports = ['Auckland','Bluff','Dunedin','Gisborne','Lyttelton','Marsden Point','Napier','Nelson','Onehunga','Picton','Port Chalmers','Port Taranaki','Tauranga','Timaru','Wellington','Westport']


for port in ports:
    for year in [2019]:
        print("Downloading ",port,year)
        resp = urllib2.urlopen('http://www.linz.govt.nz/docs/hydro/tidal-info/tide-tables/maj-ports/csv/%s%s%d.csv'%(port.replace(' ','%20'),'%20',year))
        fp = open('csvfiles/%s_%d.csv'%(port,year),'w')
        fp.write(resp.read())

                               

