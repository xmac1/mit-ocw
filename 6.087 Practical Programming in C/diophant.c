#include "euclid.h"
#include "stdio.h"
#include <string.h>

#define array_length(arr) (sizeof(arr) == 0 ? 0 : sizeof(arr) / sizeof((arr)[0]))

int main(void) {
    char* str = "Hello, World!";
    char* i = strchr(str, 'W');
    printf("find string: %s from %s\n", i, str);
}