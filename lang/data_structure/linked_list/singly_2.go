package main

import "fmt"

type Node struct {
	data int
	next *Node
}

type LinkedList struct {
	head *Node
}

func (ll *LinkedList) traverse() {
	fmt.Print("traverse\n")
	node := ll.head
	for node != nil {
		fmt.Printf("%d -> ", node.data)
		node = node.next
	}
	fmt.Print("\n")
}

func (ll *LinkedList) append(node *Node) {
	if ll.head == nil {
		ll.head = node
		return
	}

	h := ll.head
	for h.next != nil {
		h = h.next
	}
	h.next = node
}

func (ll *LinkedList) pop() {
	if ll.head == nil {
		return
	}

	if ll.head.next == nil {
		ll.head = nil
		return
	}

	c := ll.head
	n := ll.head.next
	for n.next != nil {
		c = n
		n = n.next
	}
	c.next = nil
}

func main() {
	node1 := &Node{1, nil}
	node2 := &Node{2, nil}
	node3 := &Node{3, nil}
	ll := LinkedList{}

	ll.append(node1)
	ll.append(node2)
	ll.append(node3)
	ll.traverse()

	ll.pop()
	ll.pop()
	ll.pop()
	ll.traverse()
}
