


import datetime
import struct
import sys, os, errno, io

def readFormattedString(inputfile):
    lengthOfString = inputfile.read1(2)
    lengthOfString = int.from_bytes(lengthOfString, 'big')
    return inputfile.read(lengthOfString).decode("utf-8") 

def readFormattedStringFromData(dat, idx):
    strlen = dat[idx:idx+2]
    strlen = int.from_bytes(strlen, 'big')
    return str(dat[idx+2:idx+2+strlen], 'utf-8')

def readFormattedChunkFromData(dat, idx):
    chid = dat[idx:idx+4]
    chlen = dat[idx+4:idx+8]
    chlen = int.from_bytes(chlen,'big')
    data = dat[idx+8:idx+8+chlen]
    chcs = dat[idx+8+chlen:idx+8+chlen+4]
    if (chcs + chlen + 8 != 0):
        raise Exception("Chunk length missmatch") 
    return (chid, chlen, data)

def parseChunkData(ident, lengt, dat, endi):
    match ident:
        case b'\x01\x00\x01\x00':
            print("    Creation:")
            time = dat[:8]
            time = struct.unpack('>d', time)
            time = datetime.datetime.fromtimestamp(time[0])
            print("        Created at: " + str(time))
            width = dat[8:12]
            width = int.from_bytes(width, 'big')
            print("        Width: " + str(width))
            height = dat[12:16]
            height = int.from_bytes(height, 'big')
            print("        Height: " + str(height))
            strlen = dat[16:18]
            strlen = int.from_bytes(strlen, 'big')
            identity = dat[18:18+strlen]
            print("        ID: " + str(identity, 'utf-8','ignore'))
            artworktype = dat[18+strlen:18+strlen+1]
            artworktype = int.from_bytes(artworktype, 'big')
            match artworktype:
                case 0:
                    typename = "Illustration" # older verisons dont have this bit, but trying to read this is 0 so its correct!
                case 1:
                    typename = "Animation"
                case 2:
                    typename = "Brush Pattern (Mono)"
                case 3:
                    typename = "Brush Pattern (Color)"
                case 4:
                    typename = "Brush Pattern (Texture)"
                case 5:
                    typename = "Brush Pattern (Blurring)"
                case _:
                    typename = "Unknown (" + str(artworktype) + ")"
            print("        Artwork type: " + typename)
        case b'\x01\x00\x02\x00':
            print("    Data information:")
            time = dat[4:12]
            time = struct.unpack('>d', time)
            time = datetime.datetime.fromtimestamp(time[0])
            app = readFormattedStringFromData(dat, 12)
            ver = readFormattedStringFromData(dat, 12 + app.__len__() + 2)
            dev = readFormattedStringFromData(dat, 12 + app.__len__() + 2 + ver.__len__() + 2)
            print("        Unknown: " + str(dat[:4].hex(' ')))
            print("        Timestamp: " + str(time))
            print("        App: " + app)
            print("        Version: " + ver)
            print("        Device: " + dev)
            print("        Unknown: " + str(dat[12 + app.__len__() + 2 + ver.__len__() + 2 + dev.__len__() + 2:].hex(' ')))
        case b'\x01\x00\x03\x00':
            print("    Unknonwn Data:")
            time = dat[:8]
            time = struct.unpack('>d', time)
            time = datetime.datetime.fromtimestamp(time[0])
            print("        Timestamp: " + str(time))
            print("        Data: " + str(dat[8:16].hex(' ')))
        case b'\x02\x00\x03\x00':
            print("    Brushstroke (?):")
            time1 = dat[:8]
            time1 = struct.unpack('>d', time1)
            time1 = datetime.datetime.fromtimestamp(time1[0])
            time2 = dat[8:16]
            time2 = struct.unpack('>d', time2)
            time2 = datetime.datetime.fromtimestamp(time2[0])
            brlen = dat[36:40]
            brlen = int.from_bytes(brlen, 'big')
            print("        Begin: " + str(time1))
            print("        End: " + str(time2))
            print("        Unknown: " + str(dat[16:36].hex(' ')))
            print("        Length: " + str(brlen))
            # read chnunks
            offset = 0
            for i in range(brlen):
                #data = dat[40 + i * 40: 80 + i * 40] not all chunks are 40 big
                #data = struct.unpack('>IIdfffffI', data)
                #print(str(data))
                chunktype = dat[40 + offset: 44 + offset]
                chunklen = dat[44 + offset: 48 + offset]
                chunklen = int.from_bytes(chunklen, 'big')
                data = dat[48 + offset: 48 + offset + chunklen]
                chunktail = dat[48 + offset + chunklen: 52 + offset + chunklen]
                chunktail = int.from_bytes(chunktail, 'big', signed=True)
                offset += chunklen + 12
                if chunklen >= 8:
                    parameteramount = (chunklen - 8) / 4
                    buildable = ">d"
                    for k in range(int(parameteramount)):
                        buildable += "f"
                    data = struct.unpack(buildable, data)
                    strbuilder = str(data[1:])
                    print("            Chunk: " + chunktype.hex() + ", Length: " + str(chunklen) + ", Valid: " + ("True" if (chunktail + chunklen + 8 == 0) else "False") + ", Timestamp: " + str(datetime.datetime.fromtimestamp(data[0])) + ", Data: " + strbuilder)
                else:
                    print("            Empty? ")
        case b'\x03\x00\x06\x00':
            time1 = dat[:8]
            time1 = struct.unpack('>d', time1)
            time1 = datetime.datetime.fromtimestamp(time1[0])
            someint = int.from_bytes(dat[8:12],'big')
            print("    Unknown Chunk (partially implemented)")
            print("        Timestamp: " + str(time1))
            print("        Type: " + str(someint))
            chunkamount = int.from_bytes(dat[12:16],'big')
            #for i in chunkamount:
            #    resul = readFormattedChunkFromData(dat, 16)
            #    print("")
        case _:
            print("    Unknown Chunk (not implemented)")
            print("        Data: " + dat.hex(' '))


def readChunk(inputfile):
    identifier = inputfile.read(4)
    length = inputfile.read(4)
    length = int.from_bytes(length, 'big')
    data = inputfile.read(length)
    ending = inputfile.read(4)
    ending = int.from_bytes(ending, 'big', signed=True)
    if length != 0:
        match identifier:
                case b'\x01\x00\x01\x00':
                    typename = "Header"
                case b'\x01\x00\x02\x00':
                    typename = "Editing Start"
                case b'\x01\x00\x03\x00':
                    typename = "Timestamp?"
                case b'\x02\x00\x03\x00':
                    typename = "Brushstroke"
                case b'\x01\x00\x05\x00':
                    typename = "PNG?"
                case b'\x01\x00\x06\x00':
                    typename = "Session?"
                case _:
                    typename = "Unknown"
        print("Chunk: " + identifier.hex() + " (" + typename + "), Length: " + str(length) + " bytes, Valid: " + "True" if (ending + length + 8 == 0) else "False" )
        #print(identifier.hex() + "," + str(length) + "," + ending.hex())
        parseChunkData(identifier, length, data, ending)
        return True
    else:
        return False






if len(sys.argv) < 2:
    print("No input file supplied")
    exit(errno.ENOENT)

file = open(sys.argv[1], 'rb')


print("Parsing file: " + file.name)
try:
    while readChunk(file):
        pass
finally:
    file.close()

exit(0)