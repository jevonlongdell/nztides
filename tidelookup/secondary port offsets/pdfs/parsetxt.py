
fp = open ('sec_port_list.txt')

def floatj(st):
    if st=='-':
        return float('NaN')
    else:
        return float(st)
    


linetype_primaryport =0
linetype_heading = 1
linetype_secondaryport = 2

lines = fp.readlines()
fp.close()
primary_ports = []
secondary_ports = []

for line in lines:
    index = 0
    fields = line.split()
    foundint=0
    
    #find out what type of line it is in the table
    for k in range(len(fields)):
        if fields[k].isdigit():
            foundint=k
            break
    if foundint>0:
        linetype=linetype_secondaryport
    else:
        linetype=linetype_heading
    if fields[0]==fields[0].upper():
        assert(foundint>0)
        linetype = linetype_primaryport
    
    if linetype!=linetype_heading:
        wordsinname = foundint
    else:
        wordsinname = len(fields)

    #join the name back together
    name = fields[0]
    for k in range(1,wordsinname):
        name = name+' '+fields[k]
    fields = fields[wordsinname:]

    if linetype==linetype_primaryport:
        primaryport=name
        areaname = name
        port = {}
        port['name']=name
        port['latdeg']=int(fields[0])
        port['latmin']=int(fields[1])
        port['londeg']=int(fields[2])
        port['lonmin']=int(fields[3])
#        port['hwdeltat']=int(fields[4][:-2])*60+int(fields[4][-2:])
#        port['lwdeltat']=int(fields[5][:-2])*60+int(fields[5][-2:])
        assert(fields[4]=='hhmm')
        assert(fields[5]=='hhmm')
        port['mhws']=float(fields[6])
        port['mhwn']=float(fields[7])
        port['mlwn']=float(fields[8])
        port['mlws']=float(fields[9])
        port['msl']=float(fields[10])
        primary_ports.append(port)
    elif linetype==linetype_heading:
        arename = name
    else:
        assert(linetype==linetype_secondaryport)
        port = {}
        if len(fields)==13:
            assert fields[12]=='*'
            port['approximate']=True
        else:
            port['approximate']=False

        port['name']=name
        port['area']=areaname
        port['primaryport']=primaryport
        port['latdeg']=int(fields[0])
        port['latmin']=int(fields[1])
        port['londeg']=int(fields[2])
        port['lonmin']=int(fields[3])
        if fields[4]=='-':
            continue #without knowing the time deltas secondary port is next to useless
        port['hwdeltat']=int(fields[4][:-2])*60+int(fields[4][-2:])
        if fields[5]=='-':
            assert(port['approximate'])
            port['lwdeltat']=port['hwdeltat']
        else:
            port['lwdeltat']=int(fields[5][:-2])*60+int(fields[5][-2:])
        port['mhws']=floatj(fields[6])
        port['mhwn']=floatj(fields[7])
        port['mlwn']=floatj(fields[8])
        port['mlws']=floatj(fields[9])
        port['msl']=floatj(fields[10])
        port['rangeratio']=floatj(fields[11])

        secondary_ports.append(port)



fp = open('secondary_ports.kml','w')

fp.write("""<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2" xmlns:gx="http://www.google.com/kml/ext/2.2" xmlns:kml="http://www.opengis.net/kml/2.2" xmlns:atom="http://www.w3.org/2005/Atom">
<Document>
	<name>temp.kml</name>""")

for p in secondary_ports+primary_ports:
    
    lat = -(p['latdeg']+p['latmin']/60.0)
    lon = abs(p['londeg'])+p['lonmin']/60.0
    if p['londeg']<0:
        lon=lon*-1
    

    fp.write(""" 	<Placemark>
		<name>%s</name>
		<Point>
			<coordinates>%g,%g,0</coordinates>
		</Point>
	</Placemark>"""%(p['name'],lon,lat))

fp.write("""</Document>
</kml>""")

