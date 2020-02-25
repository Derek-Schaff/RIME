#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <netcdf.h>
#include "status_updater.h"
#define ERRCODE 2
#define ERR(e) {printf("Error: %s\n", nc_strerror(e)); exit(ERRCODE);}
#define output
#define bin
/* compile with gcc -lm -lnetcdf
 *
 */

int conv_netCDF(){
    int ncid, x_dimid, y_dimid, varid;
    int retval;
    size_t chunks[2];
    int shuffle, deflate, deflate_level;
    int dimids[2];
//    shuffle = NC_SHUFFLE;
//    deflate = 1;
//    deflate_level = 1;
    char **log_path;
    char *fields[] = {"one","two","three"};
    char *vals[] = {"whoop 1","whoop 2","whoop 3"};

    __uint8_t data[1383*586];
    FILE *fp;
    fp = fopen("/home/turkishdisko/files.ntsg.umt.edu/data/FT_V3/DAILY_BINARY/AMSRE/2002/AMSRE_36V_AM_FT_2002_day170.bin","r");
    printf("3\n");
    fseek(fp,0,SEEK_SET);
    fread(data,sizeof(__uint8_t),1383*586,fp);

    statusUpdate("Creating netCDF file.", *log_path);
    if ((retval = nc_create("/home/turkishdisko/CLionProjects/RIME/back_end/c/test.nc", NC_NETCDF4, &ncid)))
    ERR(retval);
    /* Define the dimensions. */
    if ((retval = nc_def_dim(ncid, "x", 586, &x_dimid)))
    ERR(retval);
    if ((retval = nc_def_dim(ncid, "y", 1383, &y_dimid)))
    ERR(retval);

    /* Set up variable data. */
    dimids[0] = x_dimid;
    dimids[1] = y_dimid;
//    chunks[0] = data_set_rows/4;
//    chunks[1] = data_set_cols/4;
    /* Define the variable. */
    if ((retval = nc_def_var(ncid, "data", NC_INT, 2,
                             dimids, &varid)))
    ERR(retval);
//    if ((retval = nc_def_var_chunking(ncid, varid, 0, &chunks[0])))
//    ERR(retval);
//    if ((retval = nc_def_var_deflate(ncid, varid, shuffle, deflate,
//                                     deflate_level)))
//    ERR(retval);

    /*insert meta data*/
    statusUpdate("Writing meta data into netCDF file.", *log_path);
    for(int i = 0; i < 3; i++){
        if(( retval = nc_put_att_text(ncid,varid,fields[i],sizeof(fields[i]),vals[i]))) ERR(retval);
    }

    statusUpdate("Writing data into netCDF file.", *log_path);
    if ((retval = nc_put_var_ubyte(ncid, varid, &data[0])))
    ERR(retval);

    if ((retval = nc_close(ncid)))
    ERR(retval);

    statusUpdate("Finishing and closing netCDF file.", *log_path);
    return 0;
}
//
//int main(int argc, char *argv[]){
//    char *fields[] = {"one","two","three"};
//    char *vals[] = {"whoop 1","whoop 2","whoop 3"};
//    printf("1\n");
//    __uint8_t data[1383*586]; //= {1,2,3,4,5,6,7,8,9};
//    FILE *fp;
//    printf("2\n");
//    fp = fopen("/home/turkishdisko/files.ntsg.umt.edu/data/FT_V3/DAILY_BINARY/AMSRE/2002/AMSRE_36V_AM_FT_2002_day170.bin","r");
//    printf("3\n");
//    fseek(fp,0,SEEK_SET);
//    printf("3\n");
//    fread(data,sizeof(__uint8_t),1383*586,fp);
//    printf("4\n");
//    for(int i = 0; i < 1383*586; i++){
//        printf("%d\n",data[i]);
//    }
//    conv_netCDF(data,586,1383,3,fields,vals,&argv[1],&argv[2]);
//}

