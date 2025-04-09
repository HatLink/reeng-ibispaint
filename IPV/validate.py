import datetime
import struct
import sys, os, errno

def readFormattedStringFromData(dat, idx):
    strlen = dat[idx:idx+2]
    strlen = int.from_bytes(strlen, 'big')
    return str(dat[idx+2:idx+2+strlen], 'utf-8')

def parseChunkData(ident, lengt, dat, endi):
    # Keep your existing parseChunkData implementation here
    # ... (same as original code)
    pass

def scanForChunks(data):
    tabulator = 0
    lens = []
    i = 0
    file_size = len(data)
    while i < file_size:
        # Check if there's enough space for the chunk header
        if i + 12 > file_size:
            i += 1
            continue
            
        identifier = data[i:i+4]
        length = int.from_bytes(data[i+4:i+8], 'big')
        
        for lennn in lens:
            if i == lennn:
                lens.remove(lennn)
                tabulator -= 1


        # Check if chunk data fits in the file
        if i + 8 + length + 4 > file_size:
            i += 1
            continue
            
        ending = int.from_bytes(data[i+8+length:i+8+length+4], 'big', signed=True)
        
        if ending == -(length + 8):
            lens.append(i+length)
            tabulator += 1
            data_part = data[i+8:i+8+length]
            #print(f"Found valid chunk at offset {i} (0x{i:X})")
            print(f"chunk chunk_at_0x{i:X} @ 0x{i:X};")
            #print(f"{" " * tabulator}Chunk: {identifier.hex()}, Length: {length} bytes, Valid: True")
            #print(f"{" " * tabulator}Chunk: {identifier.hex()} at 0x{i:X}, Length: {length} bytes, Valid: True")
            #parseChunkData(identifier, length, data_part, ending)
            
        i += 1  # Check next byte position

if len(sys.argv) < 2:
    print("No input file supplied")
    exit(errno.ENOENT)

with open(sys.argv[1], 'rb') as f:
    file_data = f.read()

#print(f"Brute-forcing chunks in file: {sys.argv[1]}")
scanForChunks(file_data)