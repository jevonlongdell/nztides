import struct

fp = open('dunedin.tdat','r')

portname = fp.readline()

print portname
print struct.unpack('i',fp.read(4))
nrec  = struct.unpack('i',fp.read(4))[0]

for k in range(nrec):
    print struct.unpack('i',fp.read(4))[0], struct.unpack('B',fp.read(1))[0]
