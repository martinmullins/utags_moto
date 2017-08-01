import struct

def decodebool(f,s):
    data, = struct.unpack(">B",f.read(1))
    data = bool(data)
    f.read(3) #align 
    return data

def encodebool(f,utag):
    f.write(struct.pack(">B",utag["data"]))
    f.write('\x00'*3) #align

def decodestr(f,s):
    typ=">"+str(s)+"c"
    data = ''.join(struct.unpack(typ,f.read(s)))
    if s%4:
        f.read(4-s%4) #align

    return data

def encodestr(f,utag):
    s = utag["size"]
    assert s == len(utag["data"])
    pos = f.tell()+s
    if s%4:
        pos += 4-s%4
    f.write(utag["data"])
    f.seek(pos)

class TypeConv:
    dataTypes = {
        ":bool": {
            "encode":encodebool,
            "decode":decodebool,
        },
        ":str": {
            "encode":encodestr,
            "decode":decodestr
        },
        ":llong": {
            "type": "<q",
            "size": 8,
        },
        ":ullong": {
            "type": "<Q",
            "size": 8,
        },
    }


    def decode(self,name,f,s):
        """ pass the name, the filestream and the size of the data """
        data = None
        typ = ""

        for k in TypeConv.dataTypes.keys():
            if name.endswith(k):
                typ = k
                if "decode" in TypeConv.dataTypes[k].keys():
                    data = TypeConv.dataTypes[k]["decode"](f,s)
                else:
                    assert TypeConv.dataTypes[k]["size"] == s, "incorrect size"
                    data, = struct.unpack(TypeConv.dataTypes[k]["type"],
                            f.read(TypeConv.dataTypes[k]["size"]))
                break

        if data == None: #assume raw data
            typ = "raw"
            data = decodestr(f,s)

        return data,typ

    def encodeName(self, f, name):
        """ helper function for writing a utags name, pad to 32 bytes """
        offset = f.tell()+32
        f.write(name)
        f.seek(offset)

    def encodeProps(self, f, utag):
        f.write(struct.pack(">3I",
            utag["size"],
            utag["flags"],
            utag["utility"]))

    def encode(self,utag,f):
        self.encodeName(f,utag["name"])
        self.encodeProps(f,utag)
        
        for k in TypeConv.dataTypes.keys():
            if utag["type"] == k:
                if "encode" in TypeConv.dataTypes[k].keys():
                    TypeConv.dataTypes[k]["encode"](f,utag)
                else:
                    assert TypeConv.dataTypes[k]["size"] == utag["size"], "incorrect size"
                    f.write(struct.pack(TypeConv.dataTypes[k]["type"],
                            utag["data"]))
                return

        #else write raw
        encodestr(f,utag)
        return
