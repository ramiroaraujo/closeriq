# recursive approach
def triple_num_recursive(n):
    if n == 1:
        return 2
    elif n == 2:
        return 2
    elif n == 3:
        return 3
    else:
        return triple_num_recursive(n - 1) + \
               triple_num_recursive(n - 2) + \
               triple_num_recursive(n - 3)


# non recursive approach
def triple_num(n):
    if n == 1:
        return 2
    elif n == 2:
        return 2
    elif n == 3:
        return 3
    else:
        values = [2, 2, 3]
        # loop n - 3 times, move last 2 values to the left and calculate last
        # as the sum of the 3 values
        for i in range(n - 3):
            values = [values[1], values[2], values[0] + values[1] + values[2]]

    return values.pop()


if __name__ == '__main__':
    print('triple num recursive:')
    print(triple_num_recursive(4))
    print(triple_num_recursive(5))
    print(triple_num_recursive(6))
    print(triple_num_recursive(7))
    print(triple_num_recursive(8))

    print('\ntriple num non recursive:')
    print(triple_num(4))
    print(triple_num(5))
    print(triple_num(6))
    print(triple_num(7))
    print(triple_num(8))
