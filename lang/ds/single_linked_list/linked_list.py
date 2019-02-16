import abc


class LinkedList(abc.ABC):

    @abc.abstractmethod
    def insert(self, data, position):
        """insert data to position"""

    @abc.abstractmethod
    def delete(self, position):
        """delete data in poistion"""

    @abc.abstractmethod
    def traverse(self):
        """traverse all node/data"""

    # @abc.abstractmethod
    # def is_empty(self):
    #     """is empty"""


class LinkedNode:
    def __init__(self, data, next_node=None):
        self.data = data
        self.next = next_node
