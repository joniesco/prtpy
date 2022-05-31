"""
Authors: Jonathan Escojido & Samuel Harroch

Since = 03-2022

We performed this module by keeping sums in Node fields instead of calculating every time

"""

from typing import List, Generator, Callable


class Node:
    def __init__(self,depth, cur_set, cur_set_sum, remaining_sums):
        self.depth = depth
        self.cur_set = cur_set
        self.cur_set_sum = cur_set_sum
        self.left = None
        self.right = None
        self.remaining_sums = remaining_sums


class InExclusionBinTree:

    def __init__(self, items: List, valueof: Callable, upper_bound, lower_bound):
        self.items = sorted(items, key=valueof, reverse=True)
        self.leaf_depth = len(items)
        self.valueof = valueof
        self.total_sum = sum(map(self.valueof, self.items))
        self.upper_bound = upper_bound
        self.lower_bound = lower_bound
        self.root = Node(0, [], 0, self.total_sum)  # root

    # inclusion
    def add_right(self, parent: Node):
        item_to_add = self.items[parent.depth]
        parent.right = Node(depth=parent.depth+1,
                            cur_set=parent.cur_set + [item_to_add],
                            cur_set_sum=parent.cur_set_sum + self.valueof(item_to_add),
                            remaining_sums=parent.remaining_sums - self.valueof(item_to_add))

    # exclusion
    def add_left(self, parent: Node):
        parent.left = Node(depth=parent.depth+1,
                           cur_set=parent.cur_set,
                           cur_set_sum=parent.cur_set_sum,
                           remaining_sums=parent.remaining_sums)

    def generate_tree(self) -> Generator:
        current_node = self.root
        return self.rec_generate_tree(current_node)

    def rec_generate_tree(self, current_node: Node) -> Generator:
        # prune
        if current_node.cur_set_sum > self.upper_bound or \
                (current_node.cur_set_sum + current_node.remaining_sums) < self.lower_bound:
            return
        # generate
        if current_node.depth == self.leaf_depth:
            yield current_node.cur_set
            return

        self.add_right(current_node)
        yield from self.rec_generate_tree(current_node.right)

        self.add_left(current_node)
        yield from self.rec_generate_tree(current_node.left)


if __name__ == '__main__':
    items = {"a": 1, "b": 2, "c": 3, "d": 3, "e": 5, "f": 9, "g": 9}
    item_names = items.keys()
    valueof = items.__getitem__

    t = InExclusionBinTree(item_names, valueof, upper_bound=10, lower_bound=7)
    for s in t.generate_tree():
        print(s)
