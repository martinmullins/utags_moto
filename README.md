# utags_moto
## Decoding
```
$ python decode.py utags >utags_decoded
```
utags_decoded will contain the list of decoded utags.
It is possbile to add,remove and edit the files. A feature/limitation is that if a utag's string/raw data are modified, ensure the size field matches the edits to the string/raw data length.

## Encoding
It is now possible to encode the utags_decoded file back into a utag image.

Firstly, Find the size of the original image, on linux:
```
$ ls --block-size=1 -s utags
524288 ../utags
```
Substitute the size below:
```
$ python encode.py utags_decoded utagsNew <size-of-image>
```
utagsNew is the encoded image and can be flashed to the device (review the file first).

## Reviewing
Review the images.
```
$ xxd utags utagsOrig.hex
$ xxd utagsNew utagsNew.hex
$ vimdiff utagsNew utagsOrig
```

## Additional Info
Took the format of the image from the kernel driver: kernel/drivers/misc/utag
```
struct utag {
	char                       name[32];             /*     0    32 */
	char                       name_only[32];        /*    32    32 */
	/* --- cacheline 1 boundary (64 bytes) --- */
	uint32_t                   size;                 /*    64     4 */
	uint32_t                   flags;                /*    68     4 */
	uint32_t                   util;                 /*    72     4 */
	void *                     payload;              /*    76     4 */
	struct utag *              next;                 /*    80     4 */
	struct utag *              prev;                 /*    84     4 */

	/* size: 88, cachelines: 2, members: 8 */
	/* last cacheline: 24 bytes */
};
```
Ignored name_only, and next/prev linked list pointers.
