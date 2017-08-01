import sys
import pprint
import struct
from conv import TypeConv

def decode(filename):
    utags = []
    td = TypeConv()
    with open(filename,'rb') as f:
        name = f.read(32)
        while not name.startswith('\x00'):
            name = name.rstrip('\0')
            if "__UTAG_HEAD__" == name:
                f.read(12)
                pass
            elif "__UTAG_TAIL__" in name: #to be safe
                break
            else:
                s,flags,utility = struct.unpack(">3I",f.read(12))
                data,typ = td.decode(name,f,s)

                utags.append({
                    "name":name,
                    "size":s,
                    "flags":flags,
                    "utility":utility,
                    "data":data,
                    "type":typ
                    })

            name = f.read(32) 

    #pprint.pprint(utags)
    return utags

def main():
    try:
        fn = sys.argv[1]
    except IndexError:
        print "Usage: python decode.py <filename>\n\tProvide utags image to parse\n"
        return 1

    pprint.pprint(decode(fn))
    return 0


if __name__=='__main__':
    sys.exit(main())

