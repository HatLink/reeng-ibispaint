enum chunkType : u32 {
    Creation = 0x01000100,
    SessionBegin = 0x01000200,
    Unknown3x = 0x03000600,
    Brushstroke = 0x03000300,
    BrushDefinition = 0x03000100,
    Preview = 0x01000500,
    Input = 0x02000300,
    InputEntity = 0x02000301
};



// Used Types

using timestamp = be double;


struct resolutionPair {
    be u32 width;
    be u32 height;
};

struct formattedString {
    be u16 length;
    char string[length];
};

enum artworkType : u8 {
    Illustration,
    Animation, // introduced in 12.10
    BrushPatternMono, // this and below introduced in 13
    BrushPatternColor,
    BrushPatternTexture,
    BrushPatternBlurring
};


struct creationData {
    timestamp create_file_time;
    resolutionPair;
    formattedString identifier;
    artworkType;
};

struct sessionBeginData {
    padding[4];
    timestamp start_editing;
    formattedString;
    formattedString;
    formattedString;
    padding[32];
};


using countedChunk;
using chunk;
struct unknown3xData {
    timestamp;
    be u32;
    countedChunk ch1;
    countedChunk ch2;
    be u32;
    be u32;
    countedChunk ch3;
    padding[28];
    countedChunk ch4;
    countedChunk ch5;
    //chunk asdasdasd;
    padding[16];
};

struct brushstrokeData {
    timestamp;
    padding[13];
    countedChunk data;
    padding[17];
};

struct brushData {
    timestamp;
    padding[17];
    countedChunk;
    padding[8];
};



struct previewData {
    timestamp;
    be u32;
    padding[6];
    be u32 remaining;
    padding[remaining];
};


struct inputData {
    timestamp fromtime;
    timestamp twotime;
    padding[20];
    countedChunk inputArray;
    padding[16];
    chunk;
    padding[24];
    chunk;
};

struct inputEntityData {
    timestamp;
    be float x;
    be float y;
    be float pressure;
    be float tiltx;
    be float tilty;
};


struct chunk {
    be chunkType type;
    be u32 length;
    match (type){
        (chunkType::Creation): creationData;
        (chunkType::SessionBegin): sessionBeginData;
        (chunkType::Unknown3x): unknown3xData;
        (chunkType::Brushstroke): brushstrokeData;
        (chunkType::BrushDefinition): brushData;
        (chunkType::Preview): previewData;
        (chunkType::Input): inputData;
        (chunkType::InputEntity): inputEntityData;
        (_): padding[length];
    }
    be s32 checklength;
    //if (length + checklength + 8 != 0) {
    //    std::error("Checklength not matching");
    //}
} [[name(type)]];

struct countedChunk {
    be u32 count;
    chunk data[count];
};

import std.mem;

chunk IbisPaintVector[while(std::mem::read_unsigned($, 1))] @ 0x0;