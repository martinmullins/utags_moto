import struct

def decodebool(f,s):
    data, = struct.unpack(">B",f.read(1))
    data = bool(data)
    f.read(3) #align 
    return data

def encodebool(f,s):
    pass

def decodestr(f,s):
    typ=">"+str(s)+"c"
    data = ''.join(struct.unpack(typ,f.read(s)))
    align = s%4
    if s%4:
        f.read(4-s%4) #align

    return data

def encodestr(f,s):
    pass

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
