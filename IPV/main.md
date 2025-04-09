# IbisPaint Vector file

An .ipv file contians artwork data, it can be either an Illustration, Animation, or Brush (as of version 13)

Todo: rewrite this so all information is in one place instead of split between imhex and python scripts

## Findings

### Minimum requirements for an ipv file

a single 0x01000100 chunk is required for ibispaint to recognize a file and add it to the gallary and make it editable, all other chunks are optional (tho begin session, preview, end session would usually be inlcuded if created with ibispaint)

### Strings

Strings in this file are plaintext and have the length preappended with a big endien 16 bit integer without null termination

### Resolution

The resolution of an artwork is stored in multiple places as a big endian 32 bit integer pair.
Changing all of the resolution bytes is accepted when importing, see demonstration project: [freeAnimationX by PGXD/HatLink on Github](https://github.com/Pr0G4m1ngXD/freeAnimationX)

### PNG

Artworks embed a PNG for each layer, its a valid PNG as if you were to export the layer from the editor import and a preview PNG
There are also RPNG? what the fuck is an RPNG (role playing network graphic)

-   Imports: For every import a png is added at original quality
-   Layers: For every layer a png exists. it will look corrupted but it is a valid png file
-   Preview: One PNG file containing the thumbnail you see in the list

### Backups/Sessions

Theres multiple copies of the project metadata if editing more than once (possibly for speedpaint accuracy between sessions, unsure)

### Metadata

Artwork title and Artist name is stored after the session as Strings

### Brush strokes

For each brush stroke information is known:

-   Brush name String
-   float x y
-   optional float pressure tiltx tilty

### Chunks

a chunk is defined by an identifier (4 bytes)
followed by a be uint32 lenght
then data starts
finally chunk ends with a an be int32 that is the negative amount of lengh

embedded chunks in chunks in chunks (chunkception) also exists

#### Creation Header

identified by 01 00 01 00

big endian double storing the unix timestamp for creation time

resolution

identifier string that is 10 characters long

artwork type (1 byte)

#### Begin Header

identified by 01 00 02 00

4 unknon bytes

Strings:

-   App Name: The app used to create the artwork
-   Version: The version of the app used to create
-   Device name: The name of the device used to create

#### Metadata

identified by 01 00 06 00

### UUID and Hash(unsure)

if missing 0x03000600 or 0x01000200 chunk a uuid will generate in metadata

### Unknown

Many things are unknown
