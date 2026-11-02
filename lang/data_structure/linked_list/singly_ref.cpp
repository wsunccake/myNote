#include <iostream>

class LinkedList {
private:
    struct Node {
        int data;
        Node* next;
        Node(int val) : data(val), next(nullptr) {}
    };

    Node* head;

public:
    LinkedList() : head(nullptr) {}

    ~LinkedList() {
        Node* current = head;
        while (current != nullptr) {
            Node* nextNode = current->next;
            delete current;
            current = nextNode;
        }
    }

    // 1. 尾端新增 (使用遞迴或參考指標尋找)
    void append(int val) {
        // 利用指標的參考 (Node*&)，直接找到最後一個結點的 next 地址
        Node*& last_ptr = get_last_ptr(head);
        last_ptr = new Node(val);
    }

    // 輔助函式：傳回「最後一個結點的 next 指標的參考」
    // 這完全取代了 C 語言的 Node** 雙重指標寫法！
    Node*& get_last_ptr(Node*& current_head) {
        if (current_head == nullptr || current_head->next == nullptr) {
            return current_head;
        }
        return get_last_ptr(current_head->next);
    }

    // 2. 依位置刪除 (使用 Node*& 讓指標修改更直覺)
    void delete_node_by_position(int position) {
        Node*& target_ptr = get_node_ptr_at(head, position);
        if (target_ptr != nullptr) {
            Node* temp = target_ptr;
            target_ptr = target_ptr->next; // 直接修改上一個結點的 next 指向
            delete temp;
        }
    }

    // 輔助函式：取得特定位置結點的指標參考
    Node*& get_node_ptr_at(Node*& current_head, int pos) {
        if (pos == 0 || current_head == nullptr) {
            return current_head;
        }
        return get_node_ptr_at(current_head->next, pos - 1);
    }

    // 3. 反轉串列
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

    // 4. 顯示串列
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

    list.append(10);
    list.append(20);
    list.append(30);
    list.append(40);

    std::cout << "Initial: ";
    list.display(); // 10 -> 20 -> 30 -> 40 -> nullptr

    // 測試刪除位置 2 的結點 (數值 30)
    list.delete_node_by_position(2);
    std::cout << "After delete pos 2: ";
    list.display(); // 10 -> 20 -> 40 -> nullptr

    // 測試反轉
    list.reverse();
    std::cout << "After reverse: ";
    list.display(); // 40 -> 20 -> 10 -> nullptr

    return 0;
}