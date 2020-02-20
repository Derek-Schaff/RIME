#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <netcdf.h>
#include "status_updater.h"
#define ERRCODE 2
#define ERR(e) {printf("Error: %s\n", nc_strerror(e)); exit(ERRCODE);}

/*
 *
 */

int conv_netCDF(__uint8_t *data,int data_set_rows, int data_set_cols,int meta_num, char *meta_fields[], char *meta_vals[], char **output_path, char **log_path){
    int ncid, x_dimid, y_dimid, varid;
    int retval;
    size_t chunks[2];
    int shuffle, deflate, deflate_level;
    int dimids[2];
    shuffle = NC_SHUFFLE;
    deflate = 1;
    deflate_level = 1;

    statusUpdate("Creating netCDF file.", *log_path);
    if ((retval = nc_create(*output_path, NC_NETCDF4, &ncid)))
        ERR(retval);
    /* Define the dimensions. */
    if ((retval = nc_def_dim(ncid, "x", data_set_rows, &x_dimid)))
        ERR(retval);
    if ((retval = nc_def_dim(ncid, "y", data_set_cols, &y_dimid)))
        ERR(retval);

    /* Set up variable data. */
    dimids[0] = x_dimid;
    dimids[1] = y_dimid;
    chunks[0] = data_set_rows/4;
    chunks[1] = data_set_cols/4;
    /* Define the variable. */
    if ((retval = nc_def_var(ncid, "data", NC_INT, 2,
                             dimids, &varid)))
    ERR(retval);
    if ((retval = nc_def_var_chunking(ncid, varid, 0, &chunks[0])))
    ERR(retval);
    if ((retval = nc_def_var_deflate(ncid, varid, shuffle, deflate,
                                     deflate_level)))
    ERR(retval);

    /*insert meta data*/
    statusUpdate("Writing meta data into netCDF file.", *log_path);
    for(int i = 0; i < meta_num; i++){
        if(( retval = nc_put_att_text(ncid,varid,meta_fields[i],sizeof(meta_fields[i]),meta_vals[i]))) ERR(retval);
    }

    statusUpdate("Writing data into netCDF file.", *log_path);
    if ((retval = nc_put_var_ubyte(ncid, varid, &data[0])))
    ERR(retval);

    if ((retval = nc_close(ncid)))
    ERR(retval);

    statusUpdate("Finishing and closing netCDF file.", *log_path);
    return 0;
}

//int main(int argc, char *argv[]){
//    char *fields[] = {"one","two","three"};
//    char *vals[] = {"whoop 1","whoop 2","whoop 3"};
//    __uint8_t data[] = {1,2,3,4,5,6,7,8,9};
//
//    conv_netCDF(data,3,3,3,fields,vals,&argv[1],&argv[2]);
//
//
//}

