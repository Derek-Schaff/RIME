#include <stdio.h>
#include <dirent.h>
#include <sys/stat.h>
#include <string.h>
#include <stdlib.h> //for exit()
#include "parser.h"

int main(int argc, char *argv[]){
    printf("This is main.c using parser.h/c\n");

    if(argc < 2){
        printf("Usage: \n");
    }
    else{
        for(int i = 1; i < argc; i++){
            struct parsedFiles parsed = parseDir(argv[i]);
            char** fileArr = parsed.files;
            for(int i = 0; i < parsed.numFiles; i++){
                printf("%s\n", fileArr[i]);
            }
        }
    }
    return 0;
}
