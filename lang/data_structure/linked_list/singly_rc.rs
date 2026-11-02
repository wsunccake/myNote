use std::rc::Rc;
use std::cell::RefCell;

// 1. 定義節點
#[derive(Debug)]
struct Node<T> {
    data: T,
    next: Option<Rc<RefCell<Node<T>>>>,
}

impl<T> Node<T> {
    fn new(data: T) -> Self {
        Node { data, next: None }
    }
}

// 2. 定義鏈結串列
#[derive(Debug)]
struct RcLinkedList<T> {
    head: Option<Rc<RefCell<Node<T>>>>,
}

impl<T: std::fmt::Debug> RcLinkedList<T> {
    // 建立空串列
    fn new() -> Self {
        RcLinkedList { head: None }
    }

    // 在前方插入 (Push Front)
    fn push_front(&mut self, data: T) {
        let new_node = Rc::new(RefCell::new(Node {
            data,
            next: self.head.take(), // 拔走舊 head 接在新節點後面
        }));
        self.head = Some(new_node);
    }

    // 在尾端新增 (Push Back / Append)
    fn push_back(&mut self, data: T) {
        let new_node = Rc::new(RefCell::new(Node::new(data)));
        
        if self.head.is_none() {
            self.head = Some(new_node);
            return;
        }

        // 從 head 開始走訪
        let mut current = self.head.as_ref().unwrap().clone();
        loop {
            // 取得下一個節點的 Option<Rc<RefCell<Node>>>
            let next_opt = {
                let node_ref = current.borrow();
                node_ref.next.clone()
            };

            match next_opt {
                Some(next_node) => current = next_node,
                None => {
                    // 已經到尾端，透過 borrow_mut() 修改 next
                    current.borrow_mut().next = Some(new_node);
                    break;
                }
            }
        }
    }

    // 依據位置刪除節點
    fn delete_node_by_position(&mut self, position: usize) {
        if self.head.is_none() {
            return;
        }

        if position == 0 {
            let old_head = self.head.take();
            if let Some(node) = old_head {
                self.head = node.borrow_mut().next.take();
            }
            return;
        }

        let mut current = self.head.as_ref().unwrap().clone();
        let mut index = 0;

        loop {
            let next_opt = {
                let node_ref = current.borrow();
                node_ref.next.clone()
            };

            if let Some(next_node) = next_opt {
                if index + 1 == position {
                    // 跨過要刪除的節點
                    let new_next = {
                        let next_borrow = next_node.borrow();
                        next_borrow.next.clone()
                    };
                    current.borrow_mut().next = new_next;
                    return;
                }
                current = next_node;
                index += 1;
            } else {
                break;
            }
        }
    }

    // 反轉鏈結串列 (Reverse)
    fn reverse(&mut self) {
        let mut prev: Option<Rc<RefCell<Node<T>>>> = None;
        let mut current = self.head.take();

        while let Some(curr_node) = current {
            // 暫存下一個節點
            let next_node = curr_node.borrow_mut().next.take();
            // 將當前節點的 next 指向 prev
            curr_node.borrow_mut().next = prev;
            // 推進 prev 與 current
            prev = Some(curr_node);
            current = next_node;
        }

        self.head = prev;
    }

    // 列印串列
    fn display(&self) {
        let mut current = self.head.clone();
        print!("List: ");
        while let Some(node_rc) = current {
            let node = node_rc.borrow();
            print!("{:?} -> ", node.data);
            current = node.next.clone();
        }
        println!("None");
    }
}

fn main() {
    let mut list = RcLinkedList::new();

    list.push_front(3);
    list.push_front(2);
    list.push_front(1);

    list.push_back(7);
    list.push_back(8);

    print!("Initial ");
    list.display(); // 輸出: List: 1 -> 2 -> 3 -> 7 -> 8 -> None

    list.delete_node_by_position(2); // 刪除值為 3 的節點
    print!("After Delete position 2: ");
    list.display();

    list.reverse();
    print!("After Reverse: ");
    list.display();
}