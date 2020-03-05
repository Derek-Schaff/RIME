#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <netcdf.h>
#include "status_updater.h"
#define ERRCODE 2
#define ERR(e) {printf("Error: %s\n", nc_strerror(e)); exit(ERRCODE);}

/* compile with gcc -lm -lnetcdf
 *
 */

int conv_netCDF(__uint8_t *data,int data_set_rows, int data_set_cols,int meta_num, char *meta_fields[], char *meta_vals[], char *output_path, char *log_path){
    int ncid, x_dimid, y_dimid, varid;
    int retval;
    size_t chunks[2];
    int shuffle, deflate, deflate_level;
    int dimids[2];

    if ((retval = nc_create(output_path, NC_NETCDF4, &ncid)))
        ERR(retval);

    /* Define the dimensions. */
    if ((retval = nc_def_dim(ncid, "x", data_set_rows, &x_dimid)))
        ERR(retval);
    if ((retval = nc_def_dim(ncid, "y", data_set_cols, &y_dimid)))
        ERR(retval);

    /* Set up variable data. */
    dimids[0] = x_dimid;
    dimids[1] = y_dimid;

    /* Define the variable. */
    if ((retval = nc_def_var(ncid, "data", NC_INT, 2, dimids, &varid)))
    ERR(retval);

    /*insert meta data*/
    for(int i = 0; i < meta_num; i++){
        if(( retval = nc_put_att_text(ncid,varid,meta_fields[i],sizeof(meta_fields[i]),meta_vals[i]))) ERR(retval);
    }

    if ((retval = nc_put_var_ubyte(ncid, varid, &data[0])))
    ERR(retval);

    if ((retval = nc_close(ncid)))
    ERR(retval);

    return 0;
}

