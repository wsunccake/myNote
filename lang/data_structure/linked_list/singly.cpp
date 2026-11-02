#include <iostream>

class LinkedList {
private:
    // 定義內部節點結構
    struct Node {
        int data;
        Node* next;
        
        Node(int val) : data(val), next(nullptr) {}
    };

    Node* head; // 指向串列的第一個節點

public:
    // 建構子
    LinkedList() : head(nullptr) {}

    // 解構子：防止記憶體洩漏
    ~LinkedList() {
        Node* current = head;
        while (current != nullptr) {
            Node* nextNode = current->next;
            delete current;
            current = nextNode;
        }
    }

    // 1. 頭部插入
    void insert_front(int val) {
        Node* newNode = new Node(val);
        newNode->next = head;
        head = newNode;
    }

    // 2. 尾端新增 (Append)
    void append(int val) {
        Node* newNode = new Node(val);
        if (head == nullptr) {
            head = newNode;
            return;
        }

        Node* current = head;
        while (current->next != nullptr) {
            current = current->next;
        }
        current->next = newNode;
    }

    // 3. 刪除尾端節點 (Pop)
    void pop() {
        if (head == nullptr) return;

        if (head->next == nullptr) {
            delete head;
            head = nullptr;
            return;
        }

        Node* current = head;
        Node* nextNode = head->next;
        while (nextNode->next != nullptr) {
            current = nextNode;
            nextNode = nextNode->next;
        }

        delete nextNode;
        current->next = nullptr;
    }

    // 4. 依位置刪除節點
    void delete_node_by_position(int position) {
        if (head == nullptr) return;

        if (position == 0) {
            Node* temp = head;
            head = head->next;
            delete temp;
            return;
        }

        Node* current = head;
        int count = 0;
        while (current != nullptr && count < position - 1) {
            current = current->next;
            count++;
        }

        if (current != nullptr && current->next != nullptr) {
            Node* temp = current->next;
            current->next = temp->next;
            delete temp;
        }
    }

    // 5. 反轉串列 (Reverse)
    void reverse() {
        Node* prev = nullptr;
        Node* current = head;
        while (current != nullptr) {
            Node* nextNode = current->next;
            current->next = prev;
            prev = current;
            current = nextNode;
        }
        head = prev;
    }

    // 6. 顯示串列
    void display() const {
        Node* current = head;
        std::cout << "Linked List: ";
        while (current != nullptr) {
            std::cout << current->data << " -> ";
            current = current->next;
        }
        std::cout << "nullptr" << std::endl;
    }
};

int main() {
    LinkedList list;

    // 測試前端與尾端插入
    list.insert_front(3);
    list.insert_front(2);
    list.insert_front(1);
    list.append(7);
    list.append(8);
    
    std::cout << "Initial: ";
    list.display(); // 1 -> 2 -> 3 -> 7 -> 8 -> nullptr

    // 測試依位置刪除（刪除位置 2，即數值 3）
    list.delete_node_by_position(2);
    std::cout << "After delete pos 2: ";
    list.display(); // 1 -> 2 -> 7 -> 8 -> nullptr

    // 測試反轉
    list.reverse();
    std::cout << "After reverse: ";
    list.display(); // 8 -> 7 -> 2 -> 1 -> nullptr

    // 測試 pop
    list.pop();
    std::cout << "After pop: ";
    list.display(); // 8 -> 7 -> 2 -> nullptr

    return 0;
}