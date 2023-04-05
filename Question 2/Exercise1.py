input_list = [2, 3, 7, 11, 10, 7, 15, 44, 5353, 64, 12, 53]


# solution 1
def find_sum(lst: list):
    result = []
    for i, ele in enumerate(lst):
        for ele_next in lst[i + 1:]:
            if ele + ele_next == 14:
                r = [ele, ele_next]
                result.append(r)
    print(result)


find_sum(input_list)



# solution 2
def find_sum2(lst: list):
    rs = []
    for i, ele in enumerate(lst):
        if (14 - ele) in lst[:i] or (14 - ele) in lst[i + 1:]:
            r = sorted([ele, 14 - ele])
            rs.append(r)
    print(rs)


find_sum2(input_list)
