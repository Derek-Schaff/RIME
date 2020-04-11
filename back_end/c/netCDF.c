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



int insert_meta(char *meta_vars,char *meta_vals, int ncid,int varid, int retval,int grp_offset,ht_t *groups){
    char *token;
    char *string = strdup(meta_vars);
    char *dup = strdup(string);
    char delim;
    int prev_id = 0;
    int temp_id;

    token = strtok(string, "/|\0");
    while(token != NULL){
        printf("is this working\n");
        delim = dup[token - string + strlen(token)];
        if(delim == '/' || delim == '|'){
            if(ht_get(groups,token) == NULL){ // group does not exist add it
                if(prev_id == 0){ //first group in the group dir
                    printf("1 %d\n",prev_id);
                    prev_id = 1;
                    nc_def_grp(ncid,token,&prev_id);
                }//aaaaaaaaaaaaa
                else{
                    printf("2 %d\n",prev_id);
                    temp_id = prev_id;
                    prev_id = 1;
                    printf("2x %d\n",prev_id);
                    nc_def_grp(temp_id,token,&prev_id);
                }
            }
            else{ //group already exists
                if(prev_id == 0){ //first group in the group dir
                    printf("3 %d\n",prev_id);
                    prev_id = *ht_get(groups,token);
                    nc_def_grp(ncid,token,&prev_id);
                }
                else{
                    printf("4 %d\n",prev_id);
                    temp_id = prev_id;
                    prev_id = 1;
                    nc_def_grp(temp_id,token,&prev_id);
                }
            }
        }
        else if(delim == '\0'){
            if(prev_id == 0){
                printf("4 %d\n",prev_id);
                if(( retval = nc_put_att_text(ncid,varid,token,strlen(meta_vals),meta_vals))) ERR(retval);
            }
            else{
                printf("5 %d\n",prev_id);
                //insert attribute with prev_id as ncid
                if(( retval = nc_put_att_text(prev_id,varid,token,strlen(meta_vals),meta_vals))) ERR(retval);
            }
        }
        token = strtok(NULL, "/|\0");

    };
    free(dup);
    return 0;
}

int conv_netCDF(__uint8_t *data,int data_set_rows, int data_set_cols,int meta_num, char *meta_vars[],char *meta_vals[], char *output_path, char *log_path){
    int ncid, x_dimid, y_dimid, varid, varid2;
    int retval;
    size_t chunks[2];
    int shuffle, deflate, deflate_level;
    int dimids[2];
    int *grp_offset;
    *grp_offset = 1;
    ht_t *groups = ht_create();


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
        insert_meta(meta_vars[i],meta_vals[i],ncid,NC_GLOBAL,retval,1,groups);
        printf("%d\n",ht_get(groups,"Metadata"));
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