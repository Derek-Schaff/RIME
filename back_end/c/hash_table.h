//
// Created by turkishdisko on 4/12/20.
//

#ifndef RIME_HASH_TABLE_H
#define RIME_HASH_TABLE_H
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define SIZE  100

typedef struct ht{
    struct data* hashArr[SIZE];
}ht;

struct data{
    char *grp_name;
    int *grp_id;
};

void ht_setup(struct ht *table);
int ht_hash(struct ht *table, char const *input);

struct data *ht_search(struct ht *table,const char *grp_name);

void ht_insert(struct ht *table,char *grp_name);
void ht_showAll(struct ht *table);


#endif //RIME_HASH_TABLE_H
