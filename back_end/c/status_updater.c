#include "status_updater.h"

//int statusUpdate(char* message, char* log_path);

int statusUpdate(char *message, char *log_path) {
    time_t current_time = time(0);
    char timeBuffer[80];
    strftime(timeBuffer,80,"%x - %I:%M:%S %p",localtime(&current_time));
    FILE *logFile = fopen(log_path, "a");

    if(message == NULL){
        return -1;
    }
    //print to command line
    printf("%s: %s\n", timeBuffer, message);

    //append to log
    fprintf(logFile,"%s: %s\n", timeBuffer, message);
    fclose(logFile); // maybe close file just once somewhere else in system once updates are done

    //push message to gui
    pushToGui();

    //push message to web interface
    pushToWeb();

    return 0;
}

int pushToGui(){
    /* need to figure out best way to push
 * status update to python front end */
    return 0;
}
int pushToWeb(){
    /* implement once we have web interface
* in phase 4 */
    return 0;
}

//int main(){
//	statusUpdate("1","/home/turkishdisko/CLionProjects/RIME/back_end/c/t.txt");
////	sleep(2);
//	statusUpdate("2","/home/turkishdisko/CLionProjects/RIME/back_end/c/t.txt");
////	sleep(2);
//	statusUpdate("3","/home/turkishdisko/CLionProjects/RIME/back_end/c/t.txt");
//
//}
