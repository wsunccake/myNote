#include <stdio.h>
#include <stdlib.h>

struct node
{
    int data;
    struct node *next;
};
typedef struct node Node;

void traverse(Node *head)
{
    printf("traverse\n");
    while (head != NULL)
    {
        printf("%d ->", head->data);
        head = head->next;
    }
    printf("\n");
}

void append(Node **head, Node *n)
{
    if (*head == NULL)
    {
        *head = n;
        return;
    }

    Node *p = *head;
    while (p->next != NULL)
    {
        p = p->next;
    }
    p->next = n;
}

void pop(Node ** head)
{
    if ((*head)->next == NULL) {
        *head = NULL;
        return;
    }

    Node *currentNode = *head;
    Node *nextNode = (*head)->next;
    while (nextNode->next != NULL)
    {
        currentNode = nextNode;
        nextNode = nextNode->next;
    }
    currentNode->next = NULL;
}


int main()
{
    Node *node1 = (Node *)malloc(sizeof(Node));
    Node *node2 = (Node *)malloc(sizeof(Node));
    Node *node3 = (Node *)malloc(sizeof(Node));
    node1->data = 1;
    node1->next = node2;
    node2->data = 2;
    node2->next = node3;
    node3->data = 3;

    traverse(node1);

    Node *node4 = (Node *)malloc(sizeof(Node));
    node4->data = 4;

    // append with not null node
    append(&node1, node4);
    traverse(node1);

    // pop with not null node
    pop(&node1);
    traverse(node1);

    pop(&node1);
    traverse(node1);

    pop(&node1);
    traverse(node1);

    // pop with null node
    pop(&node1);
    traverse(node1);

    Node *node0 = NULL;
    traverse(node0);

    Node *node5 = (Node *)malloc(sizeof(Node));
    node5->data = 5;
    // append with null node
    append(&node0, node5);
    traverse(node0);
}
