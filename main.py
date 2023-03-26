import numpy as np
from binarytree import Node


def read_file(file_name):
    file = open(file_name, 'r')
    data = []
    s = 0
    for line in file.readlines():
        frequency = int(line.split(' ')[0])
        s += frequency
        if frequency <= 50000:
            continue
        word = line.split(' ')[1].strip()
        data.append([frequency, word])
    data.append(s)
    return data


def calc_probability(data):
    s = data.pop()
    for i in range(len(data)):
        probability = data[i][0] / s
        data[i].append(round(probability, 5))
    return data


def comp_table(data):
    n = len(data)
    cost_table = np.zeros([n + 1, n + 1])
    root_table = np.zeros([n, n], dtype=int)

    for i in range(n):
        cost_table[i][i + 1] = data[i][2]
        root_table[i][i] = i

    for d in range(2, n+1):
        for i in range(n - d+1):
            j = d + i
            minimum = np.iinfo(np.int64).max
            s = 0
            q = 0
            for l in range(i, j):
                q = cost_table[i][l] + cost_table[l + 1][j]
                s += data[l][2]
                if q < minimum:
                    minimum = q
                    root_table[i][j-1] = l
            cost_table[i][j] = minimum + s
    print(f'Optimal BST cost: {cost_table[0][len(cost_table)-1]}')
    print(f'Root: {root_table[0][len(root_table)-1]}')
    return root_table


def build_tree(data, root_table):
    n = len(root_table) - 1
    root = int(root_table[0][n])
    tree = Node(data[root][1])
    stack = [[tree, 0, n]]
    while stack:
        node = stack.pop()
        i = node[1]
        j = node[2]
        l = root_table[i][j]
        if l < j:
            v = int(root_table[l+1][j])
            new_node = Node(data[v][1])
            node[0].right = new_node
            stack.append([new_node, l+1, j])
        if i < l:
            v = int(root_table[i][l-1])
            new_node = Node(data[v][1])
            node[0].left = new_node
            stack.append([new_node, i, l-1])
    print(tree)
    return tree


def pocet_porovnani(tree, string, i=0, road=None):
    if road is None:
        road = []
    if tree is None:
        return i + 1, road
    road.append(tree.val)
    if tree.val == string:
        return i + 1, road

    if tree.val < string:
        return pocet_porovnani(tree.right, string, i+1, road)
    return pocet_porovnani(tree.left, string, i+1, road)


def main():
    file_name = 'dictionary.txt'
    data = read_file(file_name)
    data = calc_probability(data)
    data.sort(key=lambda x: x[1])
    # test_data = [[0, 0, 0.213], [0, 0, 0.02], [0, 0, 0.547], [0, 0, 0.1], [0, 0, 0.120]]
    root_table = comp_table(data)
    tree = build_tree(data, root_table)
    print(pocet_porovnani(tree, 'but'))
    print(pocet_porovnani(tree, 'bitten'))


if __name__ == '__main__':
    main()
