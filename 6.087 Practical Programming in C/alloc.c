#include "file.h"

typedef long Align;

union header {
    struct {
        union header *ptr;
        unsigned size;
    } s;
    Align x;
};

typedef union header Header;

static Header base;
static Header *freep = NULL;

void *malloc(unsigned nbytes) {
    Header *p, *prevp;
    Header *morecore(unsigned);
    unsigned nunits;

    nunits = (nbytes + sizeof(Header) - 1) / sizeof(Header) + 1;
    if ((prevp = freep) == NULL) {
        base.s.ptr = freep = prevp = &base;
        base.s.size = 0;
    }

    for (p = prevp->s.ptr; ; prevp = p, p = p->s.ptr) {
        if (p->s.size >= nunits) {
            if (p->s.size == nunits) {
                prevp->s.ptr = p->s.ptr;
            }else {
                p->s.size -= nunits;
                p += p->s.size;
                p->s.size = nunits;
            }
            freep = prevp;
            return (void*)(p+1);
        }
        if (p == freep) {
            if ((p = morecore(nunits)) == NULL){
                return NULL;
            }
        }
    }
}


#define NALLOC 1024

void free(void*);

static Header* morecore(unsigned nu)
{
    char *cp, *sbrk(int);
    Header *up;
    if (nu < NALLOC) {
        nu = NALLOC;
    }
    cp = sbrk(nu * sizeof(Header));
    if (cp == (char*) -1) {
        return NULL;
    }
    up = (Header*) cp;
    up->s.size = nu;
    free((void*)(up+1));
    return freep;
}