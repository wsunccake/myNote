#[derive(Debug)]
struct Node<T> {
    data: T,
    next: Option<Box<Node<T>>>,
}

impl<T> Node<T> {
    fn new(data: T) -> Self {
        Node { data, next: None }
    }
}

struct SinglyLinkedList<T> {
    head: Option<Box<Node<T>>>,
}

impl<T> SinglyLinkedList<T> {
    fn new() -> Self {
        SinglyLinkedList { head: None }
    }

    fn insert_front(&mut self, data: T) {
        let mut new_node = Box::new(Node::new(data));
        new_node.next = self.head.take();
        self.head = Some(new_node);
    }

    fn insert_end(&mut self, data: T) {
        let mut new_node = Box::new(Node::new(data));
        if self.head.is_none() {
            self.head = Some(new_node);
            return;
        }

        let mut current_node = self.head.as_mut().unwrap();
        while let Some(ref mut next_node) = current_node.next {
            current_node = next_node;
        }

        current_node.next = Some(new_node);
    }

    fn delete_node_by_position(&mut self, position: usize) {
        let mut current = &mut self.head;
        let mut count = 0;

        // Traverse the linked list
        while let Some(node) = current {
            if position == 0 {
                self.head = node.next.take();
                return;
            }

            if count == position - 1 {
                node.next = node.next.take().unwrap().next;
                return;
            }

            current = &mut node.next;
            count += 1;
        }
    }

    fn reverse(&mut self) {
        let mut prev = None;
        let mut current = self.head.take();

        // Traverse the linked list
        while let Some(mut node) = current {
            let next = node.next.take();
            node.next = prev.take();
            prev = Some(node);
            current = next;
        }

        self.head = prev;
    }

    // fn remove(&mut self, v: T) -> Option<usize> {
    //     let mut current = &mut self.head;
    //     loop {
    //         match current {
    //             None => return None,
    //             Some(node) if node.data == v => {
    //                 *current = node.next.take();
    //                 return Some(v);
    //             }
    //             Some(node) => {
    //                 current = &mut node.next;
    //             }
    //         }
    //     }
    // }
}

fn main() {
    let mut list: SinglyLinkedList<i32> = SinglyLinkedList::new();

    println!("Empty Linked List: {:?}", list.head);

    list.insert_front(3);
    list.insert_front(2);
    list.insert_front(1);

    list.insert_end(7);
    list.insert_end(8);
    list.insert_end(9);

    println!("Linked List: {:#?}", list.head);

    list.delete_node_by_position(2);

    println!("Delete node: {:#?}", list.head);

    list.reverse();

    println!("Reversed: {:#?}", list.head);
}
