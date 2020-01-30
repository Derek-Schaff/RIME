#ifndef PARSER_H
#define PARSER_H

struct parsedFiles{ //struct to be able to return both string array, and array length
    char** files;
    int numFiles;
};

struct parsedFiles parseDir(char* inpDir);

#endif
