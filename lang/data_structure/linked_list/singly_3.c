#include <stdio.h>
#include <stdlib.h>

struct list_head
{
    struct list_head *next;
};
typedef struct list_head List_Head;

struct node
{
    int data;
    List_Head list;
};
typedef struct node Node;

Node *init_node(int data)
{
    Node *node = malloc(sizeof(Node));
    node->data = data;
    node->list.next = &node->list;
    return node;
}

void list_add_tail(Node *n, List_Head *l)
{
    List_Head *h = l;
    while (h->next != h)
    {
        h = h->next;
    }
    h->next = &n->list;
}

List_Head *container_of(int n, List_Head *l)
{
    List_Head *t = l;
    for (int i = 0; i < n; i++)
    {
        t = t->next;
    }
    printf("container: %d\n", *(t - 1));
    printf("container: %d\n", *(t - 1));
    return t - 1;
}

void struct_info()
{
    printf("List_Head: %lu\n", sizeof(List_Head));
    printf("Node: %lu\n", sizeof(Node));
}

void ex()
{
    // char flag = 1 + 2 + 4 + 8 + 16;
    char flag = 16;

    List_Head *list = malloc(sizeof(List_Head));
    list->next = list;
    if (flag & 1)
    {
        printf("address:\n");
        printf("list: %u\n", list);
        printf("list->next: %u\n", list->next);

        printf("\n\n\n");
    }

    Node *node1 = malloc(sizeof(Node));
    node1->data = 1000;
    node1->list.next = &node1->list;
    list->next = &node1->list;
    if (flag & 2)
    {
        printf("value:\n");
        printf("*(list->next - 1): %d\n", *(list->next - 1));
        printf("node1->data: %d\n", node1->data);
        printf("\n");

        printf("address:\n");
        printf("list: %u\n", list);
        printf("list->next: %u\n", list->next);
        printf("list->next->next: %u\n", list->next->next);

        printf("&node1->list: %u\n", &node1->list);
        printf("&node1->list.next: %u\n", &node1->list.next);
        printf("\n\n\n");
    }

    Node *node2 = init_node(2000);
    node1->list.next = &node2->list;
    // list->next->next = &node2->list;
    if (flag & 4)
    {
        printf("value\n");
        printf("*(list->next - 1): %d\n", *(list->next - 1));
        printf("*(list->next->next - 1): %d\n", *(list->next->next - 1));
        printf("node1->data: %d\n", node1->data);
        printf("node2->data: %d\n", node2->data);
        printf("\n");

        printf("address\n");
        printf("list: %u\n", list);
        printf("list->next: %u\n", list->next);
        printf("list->next->next: %u\n", list->next->next);
        printf("list->next->next->next: %u\n", list->next->next->next);

        printf("&node1->list: %u\n", &node1->list);
        printf("&node1->list.next: %u // error\n", &node1->list.next);

        printf("&node2->list: %u\n", &node2->list);
        printf("&node2->list.next: %u\n", &node2->list.next);
        printf("\n\n\n");
    }

    Node *node3 = init_node(3000);
    // node2->list.next = &node3->list;
    list->next->next->next = &node3->list;
    if (flag & 8)
    {
        printf("value\n");
        printf("*(list->next - 1): %d\n", *(list->next - 1));
        printf("*(list->next->next - 1): %d\n", *(list->next->next - 1));
        printf("*(list->next->next->next - 1): %d\n", *(list->next->next->next - 1));
        printf("node1->data: %d\n", node1->data);
        printf("node2->data: %d\n", node2->data);
        printf("node3->data: %d\n", node3->data);
        printf("\n");

        printf("address\n");
        printf("list: %u\n", list);
        printf("list->next: %u\n", list->next);
        printf("list->next->next: %u\n", list->next->next);
        printf("list->next->next->next: %u\n", list->next->next->next);
        printf("list->next->next->next->next: %u\n", list->next->next->next->next);

        printf("&node1->list: %u\n", &node1->list);
        printf("&node1->list.next: %u // error\n", &node1->list.next);

        printf("&node2->list: %u\n", &node2->list);
        printf("&node2->list.next: %u //error\n", &node2->list.next);

        printf("&node3->list: %u\n", &node3->list);
        printf("&node3->list.next: %u\n", &node3->list.next);
        printf("\n\n\n");
    }

    Node *node4 = init_node(4000);
    list_add_tail(node4, list);
    if (flag & 16)
    {
        printf("value\n");
        printf("*(list->next - 1): %d\n", *(list->next - 1));
        printf("*(list->next->next - 1): %d\n", *(list->next->next - 1));
        printf("*(list->next->next->next - 1): %d\n", *(list->next->next->next - 1));
        printf("*(list->next->next->next->next - 1): %d\n", *(list->next->next->next->next - 1));
        printf("node1->data: %d\n", node1->data);
        printf("node2->data: %d\n", node2->data);
        printf("node3->data: %d\n", node3->data);
        printf("node4->data: %d\n", node4->data);
        printf("\n");

        printf("address\n");
        printf("list: %u\n", list);
        printf("list->next: %u\n", list->next);
        printf("list->next->next: %u\n", list->next->next);
        printf("list->next->next->next: %u\n", list->next->next->next);
        printf("list->next->next->next->next: %u\n", list->next->next->next->next);
        printf("list->next->next->next->next->next: %u\n", list->next->next->next->next->next);

        printf("&node1->list: %u\n", &node1->list);
        printf("&node1->list.next: %u // error\n", &node1->list.next);

        printf("&node2->list: %u\n", &node2->list);
        printf("&node2->list.next: %u //error\n", &node2->list.next);

        printf("&node3->list: %u\n", &node3->list);
        printf("&node3->list.next: %u // error\n", &node3->list.next);

        printf("&node4->list: %u\n", &node4->list);
        printf("&node4->list.next: %u\n", &node4->list.next);
        printf("\n\n\n");
    }

    List_Head *i = container_of(1, list);
    printf("i: %d\n", *i);

    free(node4);
    free(node3);
    free(node2);
    free(node1);
    free(list);
}

int main()
{
    struct_info();
    ex();

    return 0;
}