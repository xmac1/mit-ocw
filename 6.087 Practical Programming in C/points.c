#include <stdio.h>

struct point {
    int x;
    int y;
};

struct employee {
    char fname[100];
    char lname[100];
    int age;
};

struct triangle {
    struct point ptA;
    struct point ptB;
    struct point ptC;
};

struct chain_element {
    int data;
    struct chain_element* next;
};

int main(void) {
    union {
        int idata;
        char sdata[4];
    } d;
    d.idata = 129;
    printf("low order bits: %d, high order bit: %d\n", d.sdata[0], d.sdata[1]);

}