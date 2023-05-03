#!/usr/bin/env python3

def main():
    L = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
    ]
    print(*L, sep='\n')

    # [ 左回転 ]
    # zipで3つのリストを組み合わせる
    L2 = list(zip(*L))
    """
    (1, 4, 7)
    (2, 5, 8)
    (3, 6, 9)
    """

    # 3つのリストを逆順に並べ替える
    L3 = L2[::-1]
    """
    (3, 6, 9)
    (2, 5, 8)
    (1, 4, 7)
    """

    # [ 右回転 ]
    # 3つのリストを逆順に並べ替える
    L4 = L[::-1]
    """
    [7, 8, 9]
    [4, 5, 6]
    [1, 2, 3]
    """

    # zipで3つのリストを組み合わせる
    L5 = zip(*L4)
    """
    (7, 4, 1)
    (8, 5, 2)
    (9, 6, 3)
    """


if __name__ == "__main__":
    main()
