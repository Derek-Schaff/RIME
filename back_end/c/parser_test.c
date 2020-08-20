#include <stdio.h>
#include <dirent.h>
#include <sys/stat.h>
#include <string.h>
#include <stdlib.h> //for exit()
#include "parser.h"
#include "status_updater.h"

int main(int argc, char *argv[]){
    //parser test
    /*
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
     */


    //status updater test
    /*for(int i = 0; i < 10 ; i++){
        statusUpdate("this is test line","/home/turkishdisko/CLionProjects/RIME/back_end/status_test");
        sleep(2);
    }*/
    return 0;
}
