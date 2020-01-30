#include <stdio.h>
#include <dirent.h>
#include <sys/stat.h>
#include <string.h>
#include <stdlib.h> //for exit()
#include "parser.h"
#define maxLen 250

struct parsedFiles parseDir(char* inpDir){
    struct parsedFiles parsed;
    char dir[maxLen];
    DIR *folder;
    struct dirent *entry;
    struct stat filestat;
    char tmp[maxLen];
    parsed.numFiles = 0;
    strcpy(dir,inpDir);

    /*count files in dir for array size*/
    folder = opendir(dir);
    if(folder == NULL){
        printf("Unable to read directory :( \n");
        exit(0);
    }
    while(entry = readdir(folder)){
        if(entry->d_type != DT_DIR){
            parsed.numFiles++;
        }
    }
    closedir(folder);

    /* assemble the array*/
    /* allocate memory for the 2D array holding the file paths.
     * memory must be allocated to pass the array along to other functions*/
    char **binFiles = malloc(parsed.numFiles * sizeof(char*));
    for(int i = 0; i < parsed.numFiles; ++i){
        binFiles[i] = malloc(maxLen * sizeof(char));
    }
    folder = opendir(dir);
    int i = 0;
    while(entry = readdir(folder)){
        if(entry->d_type != DT_DIR){ //check if file is not a directory
            strcpy(tmp,dir);
            strcat(tmp,"/");
            strcat(tmp,entry->d_name); //assemble full file path
            strcpy(binFiles[i],tmp);
            i++;
        }
    }
    parsed.files = binFiles;
    return parsed;
}