# utags_moto

Encode and Decode motorolla utags images
Usage:
```
#Decoding:
$ python decode.py utags >utags_decoded
# utags_decoded will contain the list of decoded utags

#Encoding:
# get the size of the utags image, something like:
$ ls --block-size=1 -s utags
524288 ../utags
# substities the size below (524288)
$ python encode.py utags_decoded utagsNew <size-of-image>
# utagsNew is the encoded image
```
