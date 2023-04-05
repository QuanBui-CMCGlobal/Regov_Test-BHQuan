myStr = str(input('Enter string:'))


def first_non_repeat_char(myStr: str):
    result = -1
    for idc, c in enumerate(myStr):
        if c not in myStr[idc + 1:] and c not in myStr[:idc]:
            result = f'{c}, {idc}'
            break
    print(result)


first_non_repeat_char(myStr)
