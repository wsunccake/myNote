#include <stdio.h>
#include <stdlib.h>

struct node
{
    int data;
    struct node *next;
};
typedef struct node Node;

typedef struct
{
    Node *head;
} LinkedList;

void traverse(LinkedList ll)
{
    printf("traverse\n");
    Node *head = ll.head;
    while (head != NULL)
    {
        printf("%d ->", head->data);
        head = head->next;
    }
    printf("\n");
}

void append(LinkedList *ll, Node *n)
{
    if (ll->head == NULL)
    {
        ll->head = n;
        return;
    }

    Node *head = (ll->head);
    Node *p = head;
    while (p->next != NULL)
    {
        p = p->next;
    }
    p->next = n;
}

void pop(LinkedList *ll)
{
    if (ll->head->next == NULL)
    {
        ll->head = NULL;
        return;
    }

    Node *currentNode = ll->head;
    Node *nextNode = ll->head->next;
    while (nextNode->next != NULL)
    {
        currentNode = nextNode;
        nextNode = nextNode->next;
    }
    currentNode->next = NULL;
}

int main()
{
    Node node1 = {1, NULL};
    Node node2 = {2, NULL};
    Node node3 = {3, NULL};
    node1.next = &node2;
    node2.next = &node3;
    LinkedList *ll = malloc(sizeof(LinkedList));
    ll->head = &node1;
    traverse(*ll);

    Node node4 = {4, NULL};

    // append with not null node
    append(ll, &node4);
    traverse(*ll);

    // pop with not null node
    pop(ll);
    traverse(*ll);
    pop(ll);
    pop(ll);

    // pop with null node
    pop(ll);
    traverse(*ll);

    // append with null node
    LinkedList *ll2 = malloc(sizeof(LinkedList));
    Node node5 = {5, NULL};
    append(ll2, &node5);
    traverse(*ll2);
}
