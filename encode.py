import sys
import pprint
import struct
from conv import TypeConv

def encode(decodedfile,outfile,size):
    utags = []
    te = TypeConv()
    data = None

    with open(decodedfile,'r') as f:
        data = f.read()

    if not data:
        print "Bad input data"
        return 2

    try:
        data = eval(data)
    except SyntexError, e:
        print "Parse issues"
        print str(e)
        return 3

    pprint.pprint(data)

    with open(outfile,'wb') as f:
        #initialize file with all zeros
        f.write('\x00'*size)
        f.seek(0)

        # write the Header
        te.encodeName(f,"__UTAG_HEAD__")
        f.write('\x00'*12) #blank size,flags or utility

        #write utags
        for utag in data:
            te.encode(utag,f)

        # write the Tail
        te.encodeName(f,"__UTAG_TAIL__")
        f.write('\x00'*12) #blank size,flags or utility

    return 0

def usage():
    print "Usage: python",__file__,"<decodeddata> <outfile> <size>"
    print "\tdecodeddata: decoded data file"
    print "\t    outfile: resultant filname for the encoded image"
    print "\t       size: size of image\n"

def main():
    try:
        infile = sys.argv[1]
        outfile = sys.argv[2]
        size = int(sys.argv[3])
    except IndexError,TypeError:
        usage()
        return 1

    return encode(infile,outfile,size)

if __name__=='__main__':
    sys.exit(main())

