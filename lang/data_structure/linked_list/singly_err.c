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

void append(Node *head, Node *n)
{
    if (head == NULL)
    {
        head = n; // fail to change
        return;
    }

    Node *p = head;
    while (p->next != NULL)
    {
        p = p->next;
    }
    p->next = n;
}

void pop(Node *head)
{
    if (head->next == NULL)
    {
        head = NULL; // fail to change
        return;
    }

    Node *currentNode = head;
    Node *nextNode = head->next;
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
    traverse(&node1);

    // append with not null node
    Node node4 = {4, NULL};
    append(&node1, &node4);
    traverse(&node1);

    Node *node0 = NULL;
    traverse(node0);

    Node node5 = {5, NULL};
    // append with null node
    append(node0, &node5);
    traverse(node0); // still be NULL not 5

    // pop with not null node
    pop(&node1);
    traverse(&node1);

    pop(&node1);
    traverse(&node1);

    pop(&node1);
    traverse(&node1);

    // pop with null node
    pop(&node1);
    traverse(&node1); // still be 1 not NULL
}