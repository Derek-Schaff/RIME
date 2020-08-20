#include <stdio.h>
#include <time.h>
#include <unistd.h>

#ifndef STATUS_UPDATER_H
#define STATUS_UPDATER_H

int pushToGui();
int pushToWeb();
int statusUpdate(char* message, char* log_path);

#endif //STATUS_UPDATER_H
