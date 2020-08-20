#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include "hash_table.h"

void ht_setup(struct ht *table){
    for(int i = 0; i < SIZE; i++){
        table->hashArr[i] = NULL;
    }
}

int ht_hash(struct ht *table, char const *input){
    unsigned int result = 31;
    for(int i = 0; i <strlen(input); i++){
        result = result*37 + input[i];
    }
    return result % SIZE;
}

struct data *ht_search(struct ht *table,const char *grp_name){
    int hashIndex = ht_hash(table,grp_name);
    while(table->hashArr[hashIndex] != NULL){
        if(strcmp(table->hashArr[hashIndex]->grp_name, grp_name ) == 0){return table->hashArr[hashIndex];}

        ++hashIndex;
        hashIndex %= SIZE;
    }
    return NULL;
}

//int ht_search_utest(struct ht *table,const char *grp_name){
//    int hashIndex = ht_hash(table,grp_name);
//    while(table->hashArr[hashIndex] != NULL){
//        if(strcmp(table->hashArr[hashIndex]->grp_name, grp_name ) == 0){return hashIndex;}
//
//        ++hashIndex;
//        hashIndex %= SIZE;
//    }
//    return 0;
//}

struct data *ht_insert(struct ht *table,char *grp_name){
    struct data *item = (struct data*) malloc(sizeof(struct data));
    item->grp_name = grp_name;
    item->grp_id = malloc(sizeof(int));

    //get hash
    int hashIndex = ht_hash(table,grp_name);
    while(table->hashArr[hashIndex] != NULL && table->hashArr[hashIndex]->grp_name != NULL){
        ++hashIndex;
        hashIndex %= SIZE;
    }
    table->hashArr[hashIndex] = item;
    return item;
}

void ht_clean_up(struct ht *table){
    for(int i = 0; i < SIZE; i++){
        if(table->hashArr[i] != NULL){
            free(table->hashArr[i]->grp_id);
        }
        free(table->hashArr[i]);
    }
}

void ht_showAll(struct ht *table){
    for(int i = 0; i < SIZE; i++){
        if(table->hashArr[i] != NULL){
            //printf("group name: %s, group id: %d\n", table->hashArr[i]->grp_name,table->hashArr[i]->grp_id );
            printf("group name: %s, group id: %d\n", table->hashArr[i]->grp_name, i );
        }

    }
}
//
//int main(){
//    struct ht table;
//    ht_setup(&table);
//    ht_insert(&table,"Metadata");
//    ht_insert(&table,"DatasetIdentification");
//    ht_insert(&table,"Extent");
//    ht_insert(&table,"geographic");
//    ht_insert(&table,"easegrid");
//
//    ht_showAll(&table);
//    printf("\n\n\n");
//
//    printf("Metadata index = 66: %d\n", ht_search_utest(&table,"Metadata") == 66);
//    printf("DatasetIdentification index = 3: %d\n", ht_search_utest(&table,"DatasetIdentification") == 3);
//    printf("Extent index = 237: %d\n", ht_search_utest(&table,"Extent") == 237);
//    printf("geographic index = 171: %d\n", ht_search_utest(&table,"geographic") == 171);
//    printf("easegrid index = 82: %d\n", ht_search_utest(&table,"easegrid") == 82);
//
//    return 0;
//}
