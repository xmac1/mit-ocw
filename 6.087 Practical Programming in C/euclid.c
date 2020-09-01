#include "euclid.h"

int gcd(int a, int b)
{
    while(b) {
        int tmp = b;
        b = a % b;
        a = tmp;
    }
    return a;
}

int ext_euclid(int a, int b) {
    x = y = 0;
    if (a < b) {
        int tmp = a;
        a = b;
        b = tmp;
    }
    while (b > 0) {
        int quo = a / b;
        int rem = a % b;
        x = quo;
        y = rem;
        a = b;
        b = rem;
    }
    return a;
}