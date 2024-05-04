#![allow(unused)]

#[derive(Debug)]
struct Node<T> {
    elem: T,
    next: Option<Box<Node<T>>>,
}

#[derive(Debug)]
pub struct SinglyLinkedList<T> {
    head: Option<Box<Node<T>>>,
}

impl<T> SinglyLinkedList<T> {
    pub fn new() -> Self {
        Self { head: None }
    }

    pub fn push_front(&mut self, elem: T) {
        let next: Option<Box<Node<T>>> = self.head.take();
        self.head = Some(Box::new(Node { elem, next }));
    }

    pub fn pop_front(&mut self) -> Option<T> {
        // let h: Option<Box<Node<T>>> = self.head;
        // ? with Option => type
        let head: Box<Node<T>> = self.head.take()?;
        self.head = head.next;
        Some(head.elem)
    }

    pub fn insert_after(&mut self, pos: usize, elem: T) -> Result<(), usize> {
        let mut curr = &mut self.head;
        let mut pos_ = pos;

        while pos_ > 0 {
            curr = match curr.as_mut() {
                Some(node) => &mut node.next,
                None => return Err(pos - pos_),
            };
            pos_ -= 1;
        }

        match curr.take() {
            Some(mut node) => {
                let new_node = Box::new(Node {
                    elem,
                    next: node.next,
                });
                node.next = Some(new_node);

                *curr = Some(node);
            }
            None => return Err(pos - pos_),
        }
        Ok(())
    }

    pub fn remove(&mut self, pos: usize) -> Option<T> {
        let mut curr = &mut self.head;
        let mut pos = pos;

        while pos > 0 {
            curr = &mut curr.as_mut()?.next;
            pos -= 1;
        }

        let node = curr.take()?;
        *curr = node.next;
        Some(node.elem)
    }
}

fn main() {
    let mut l = SinglyLinkedList::<i32>::new();
    l.push_front(1);
    l.push_front(2);
    l.push_front(4);
    println!("{:#?}", l);
}
