#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <netcdf.h>
#include "status_updater.h"
#include "hash_table.h"

#define ERRCODE 2
#define ERR(e) {printf("Error: %s\n", nc_strerror(e)); exit(ERRCODE);}

/* compile with gcc -lm -lnetcdf
 *
 */

ht_t *groups;
int grp_offset = 1;

int insert_meta(char *meta_vars,char *meta_vals, int ncid,int varid, int retval){
    char *token;
    char *string = strdup(meta_vars);
    char *dup = strdup(string);
    char delim;
    int prev_id = 0;
    int temp_id;

    token = strtok(string, "/|\0");
    while(token != NULL){

        delim = dup[token - string + strlen(token)];
        if(delim == '/' || delim == '|'){
            if(ht_get(groups,token) == NULL){ // group does not exist add it
                if(prev_id == 0){ //first group in the group dir
                    prev_id = ncid+(grp_offset++);
                    nc_def_grp(ncid,token,&prev_id);
                    printf("first\n");
                }
                else{
                    temp_id = prev_id;
                    prev_id = ncid+(grp_offset++);
                    nc_def_grp(temp_id,token,&prev_id);
                    printf("second\n");
                }
            }
            else{ //group already exists
                if(prev_id == 0){ //first group in the group dir
                    prev_id = *ht_get(groups,token);
                    nc_def_grp(ncid,token,&prev_id);
                }
                else{
                    temp_id = prev_id;
                    prev_id = ncid+(grp_offset++);
                    nc_def_grp(temp_id,token,&prev_id);
                }
            }
        }
        else if(delim == '\0'){
            if(prev_id == 0){
                printf("prev_id = 0\n");
                if(( retval = nc_put_att_text(ncid,varid,token,strlen(meta_vals),meta_vals))) ERR(retval);
            }
            else{
                //insert attribute with prev_id as ncid
                printf("prev_id != 0\n");
                if(( retval = nc_put_att_text(prev_id,varid,token,strlen(meta_vals),meta_vals))) ERR(retval);
            }
        }
        token = strtok(NULL, "/|\0");
    }
    printf("%d\n",grp_offset);
    free(dup);
    return 0;
}

int conv_netCDF(__uint8_t *data,int data_set_rows, int data_set_cols,int meta_num, char *meta_vars[],char *meta_vals[], char *output_path, char *log_path){
    int ncid, x_dimid, y_dimid, varid, varid2;
    int retval;
    size_t chunks[2];
    int shuffle, deflate, deflate_level;
    int dimids[2];

    groups = ht_create();


    if ((retval = nc_create(output_path, NC_NETCDF4, &ncid)))
        ERR(retval);

    /* Define the dimensions. */
    if ((retval = nc_def_dim(ncid, "longitude", data_set_rows, &x_dimid)))
        ERR(retval);
    if ((retval = nc_def_dim(ncid, "latitude", data_set_cols, &y_dimid)))
        ERR(retval);

    /* Set up variable data. */
    dimids[0] = x_dimid;
    dimids[1] = y_dimid;
    /* Define the variable. */
    if ((retval = nc_def_var(ncid, "data", NC_INT, 2, dimids, &varid)))
    ERR(retval);



    /*insert meta data*/
    for(int i = 0; i < meta_num; i++){
        insert_meta(meta_vars[i],meta_vals[i],ncid,NC_GLOBAL,retval);
    }
    printf("ESDR: %d Acqui: %d\n",ht_get(groups,"ESDR"),ht_get(groups,"AcquisitionInformation"));
    if ((retval = nc_put_var_ubyte(ncid, varid, &data[0])))
    ERR(retval);

    if ((retval = nc_close(ncid)))
    ERR(retval);

    return 0;
}

//int main(int argc, char *argv[]){
//
//
//    return 0;
//}