# tools for finding in lists

def find_first1(l, pred):
    """
    Find first occurrence in list satisfying predicate.
    :param l: list.
    :param pred: predicate on the list elements.
    :return: index of first occurrence in list satisfying predicate; length of the list if not found.
    """
    length = len(l)
    index = length
    for i in range(length):
        if pred(l[i]):
            index = i
            break
    return index


def find_first2(l, pred1, pred2):
    """
    Find first occurrence in list satisfying two-step predicate.
    :param l: list.
    :param pred1: predicate on the list elements.
    :param pred2: predicate on two list elements.
    :return: index of first occurrence in list satisfying pred2(l[index-1], l[index])
    or pred1(l[0]) if only one elment in the list; length of the list if not found.
    """
    length = len(l)
    index = length
    if length > 0:
        if length == 1:
            if pred1(l[0]):
                index = 0
            else:
                index = 1
        else:
            for i in range(1, length):
                if pred2(l[i-1], l[i]):
                    index = i
                    break
    return index
