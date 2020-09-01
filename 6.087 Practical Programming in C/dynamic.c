#include <stdlib.h>

struct node {
    int data;
    struct node* next;
};

struct node* head;

struct node* nalloc(int data) {
    struct node* p = (struct node*)malloc(sizeof(struct node));
    if (p != NULL) {
        p->data = data;
        p->next = NULL;
    }
    return p;
}

struct node* addfront(struct node* head, int data) {
    struct node* p = nalloc(data);
    if (p == NULL) return head;
    p->next = head;
    return p;
}

void nodeiter(struct node* head, void f(struct node*)) {
    for (struct node* p = head; p != NULL; p=p->next) {
        f(p);
    }
}

struct tnode {
    int data;
    struct tnode* left;
    struct tnode* right;
};
