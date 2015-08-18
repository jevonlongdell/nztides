ports={}

ports['auckland']='Auckland'
ports['bluff']='Bluff'
ports['dunedin']='Dunedin'
ports['gisborne']='Gisborne'
ports['lyttelton']='Lyttelton'
ports['marsden point']='Marsden Point'
ports['napier']='Napier'
ports['nelson']='Nelson'
ports['onehunga']='Onehunga'
ports['picton']='Picton'
ports['port chalmers']='Port Chalmers'
ports['taranaki']='Taranaki'
ports['tauranga']='Tauranga'
ports['timaru']='Timaru'
ports['wellington']='Wellington'
ports['westport']='Westport'


fp = open('temp.sh','w')

for y in ['2014','2015','2016','2017','2018']:
    for p in ports.keys():
        cmd = 'wget -v \"http://www.linz.govt.nz/docs/hydro/tidal-info/tide-tables/maj-ports/csv/%s %s.csv\" -O \"%s\"/%s.csv\n'%(ports[p],y,p,y,)
        fp.write(cmd)
fp.close()
