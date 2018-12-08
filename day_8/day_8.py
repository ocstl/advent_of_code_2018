#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Node:
    def __init__(self, nbr_children):
        self.nbr_children = nbr_children
        self.nbr_metadata = None
        self.children = list()
        self.metadata = list()

    def add_child(self, other):
        self.children.append(other)

    def add_metadata(self, metadata):
        self.metadata.extend(metadata)

    # Method used to fill the tree.
    def push(self, data):
        # While the node is defined with the number of children, the number of data points waits to be filled.
        if not self.nbr_metadata:
            self.nbr_metadata = data
            return True

        # Use the any function's short-circuiting logic. If one of the children return True, it manages to consume the
        # new data.
        if any(child.push(data) for child in self.children):
            return True

        # Create a new child if the node isn't filled up.
        if len(self.children) < self.nbr_children:
            self.children.append(Node(data))
            return True

        # Finally, try to add the data.
        if len(self.metadata) < self.nbr_metadata:
            self.metadata.append(data)
            return True

        return False

    def metadata_check(self):
        return sum(self.metadata) + sum(child.metadata_check() for child in self.children)

    def get_value(self):
        if self.nbr_children == 0:
            return sum(self.metadata)
        else:
            return sum(self.children[name-1].get_value() for name in self.metadata if 0 < name <= self.nbr_children)


def main(_args):
    with open("day_8.txt", "r") as f:
        data_list = list(map(int, f.read().split()))

    head_node = Node(data_list[0])
    for data in data_list[1:]:
        # Should always return True, otherwise there is a problem in the input data.
        assert(head_node.push(data))

    first_answer = head_node.metadata_check()
    print("The first answer is: {}".format(first_answer))

    second_answer = head_node.get_value()
    print("The second answer is: {}".format(second_answer))

    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
