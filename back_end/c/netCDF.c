#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <netcdf.h>
#include <stdint.h>
#include "status_updater.h"
#include "hash_table.h"

#define ERRCODE 2
#define ERR(e) {printf("Error: %s\n", nc_strerror(e)); exit(ERRCODE);}

/* compile with gcc -lm -lnetcdf
 *
 */
int insert_meta(char *meta_vars,char *meta_vals, int ncid,int varid, int retval,ht *table){
    char *token;
    char *string = strdup(meta_vars);
    char *dup = strdup(string);
    char delim;
    int *prev_id = 0;
    int temp_id;
    struct data *ret;
    token = strtok(string, "/|\0");
    while(token != NULL){
        delim = dup[token - string + strlen(token)];
        if(delim == '/' || delim == '|'){
            ret = ht_search(table,token);
            if(ret == NULL){ //group does not exist
                ret = ht_insert(table,token); //create group

                if(prev_id == 0){ // first group in dir, set parent id to ncid
                    prev_id = ret->grp_id; //set new id for newly created group
                    nc_def_grp(ncid,token,prev_id); //ncid is file id, prev_id is groups id
                }
                else{ // not first group in dir/ set id to prev_id as set in previous loop
                    nc_def_grp(*prev_id,token,ret->grp_id); // define group with previous id as parent id
                    prev_id = ret->grp_id;
                }
            }
            else{ //group already exists
                prev_id = ret->grp_id;; // set prev_id to existing groups id
            }
        }
        else if(delim == '\0'){// token is now at the meta variable name
            if(prev_id == 0){ //Metadata variable is not part of any groups, set parent to ncid
                if(( retval = nc_put_att_text(ncid,varid,token,strlen(meta_vals),meta_vals))) ERR(retval);
            }
            else{ // meta data part of group, use prev_id as parent id
                if(( retval = nc_put_att_text(*prev_id,varid,token,strlen(meta_vals),meta_vals))) ERR(retval);
            }
        }
        token = strtok(NULL, "/|\0");
    }
    free(dup);
    return 0;
}

int conv_netCDF(__uint8_t *data,int data_set_rows, int data_set_cols,int meta_num, char *meta_vars[],char *meta_vals[], char *output_path, char *log_path){
    int ncid, x_dimid, y_dimid, varid, varid2;
    int retval;
    size_t chunks[2];
    int shuffle, deflate, deflate_level;
    int dimids[2];
    struct ht table;
    ht_setup(&table);
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
        insert_meta(meta_vars[i],meta_vals[i],ncid,NC_GLOBAL,retval,&table);
    }

    if ((retval = nc_put_var_ubyte(ncid, varid, &data[0])))
    ERR(retval);

    if ((retval = nc_close(ncid)))
    ERR(retval);

    ht_clean_up(&table);
    return 0;
}

//int main(int argc, char *argv[]){
//    struct data *id;
//    struct ht table;
//    ht_setup(&table);
//    ht_insert(&table,"GrpA");
//    ht_insert(&table,"GrpB");
//    id = ht_search(&table,"Grp");
//    if( id != NULL){
//        printf("in table id: %d\n",id->grp_id);
//    }
//    else{printf("Not in table\n");}
//    ht_showAll(&table);
//
//    return 0;
//
//    __uint8_t data[9] = {1,2,3,4,5,6,7,8,9};
//    char *metFields[] = {"GrpA/GrpB/GrpC|Var1","GrpA/GrpB/GrpD|Var2","GrpE|Var3"};
//    char *metaVals[] = {"Val1","Val2","Val3"};
//    conv_netCDF(data,3,3,3,metFields,metaVals,"/home/turkishdisko/test.nc","/home/turkishdisko/log.txt");
//    return 0;
//}