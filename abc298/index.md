---
title: abc298(a, b, c)
post_status: publish # publish, draft, pending, future
taxonomy:
    category:
        - AtCoder
        # - tool
    post_tag:
        - tech
---

# まえがき

コンテスト中は a しか解けませんでした。
b の rotate が複雑そうで c を解いていて時間(60分)切れ。
実際 rotate はそんな難しくなかったんですけど。
※60分にしてるのは、入緑を目指す上で c までを60分で解くことにしたため

# A - Job Interview

以下を2つの条件として評価する問題です。

> 「良」と評価した面接官が少なくとも 1 人いる
> 「不可」と評価した面接官がいない

https://atcoder.jp/contests/abc298/tasks/abc298_a
https://atcoder.jp/contests/abc298/submissions/40635827

```python
#!/usr/bin/env python3
import sys

YES = "Yes"  # type: str
NO = "No"  # type: str


def solve(N: int, S: str):
    cond1 = False
    cond2 = True
    for i in range(N):
        if S[i] == "o":
            cond1 = True
        elif S[i] == "x":
            cond2 = False
    if cond1 and cond2:
        print('Yes')
    else:
        print('No')
    return


def main():
    def iterate_tokens():
        for line in sys.stdin:
            for word in line.split():
                yield word
    tokens = iterate_tokens()
    N = int(next(tokens))  # type: int
    S = next(tokens)  # type: str
    solve(N, S)

if __name__ == '__main__':
    main()
```

# B - Coloring Matrix

rotate むずすぎ、調べたら[行列の転置云々でいける](https://qiita.com/rudorufu1981/items/5341d9603ecb1f9c2e5c)らしいけどまったく分からんということでコンテスト中は断念。
ただよく読むとなんてことはなくて `同時に A(i,j)​をA(N+1−j,i)で置き換える` だけだった。
https://atcoder.jp/contests/abc298/tasks/abc298_b

以下は工夫なく地道に rotate を実装した提出。
https://atcoder.jp/contests/abc298/submissions/41016667

```python
#!/usr/bin/env python3
import sys

YES = "Yes"  # type: str
NO = "No"  # type: str


def rotate(N: int, A: "List[List[int]]"):
    res = [0] * N
    for i in range(N):
        res[i] = [0] * N
        for j in range(N):
            res[i][j] = A[N-j-1][i]
    return res

def solve(N: int, A: "List[List[int]]", B: "List[List[int]]"):
    for _ in range(4):
        ok = True
        for j in range(N):
            for k in range(N):
                if (A[j][k] == 1 and B[j][k] == 0):
                    ok = False
        if ok == True:
            print(YES)
            return
        else:
            A = rotate(N, A)
    print(NO)
    return


def main():
    def iterate_tokens():
        for line in sys.stdin:
            for word in line.split():
                yield word
    tokens = iterate_tokens()
    N = int(next(tokens))  # type: int
    A = [[int(next(tokens)) for _ in range(N)] for _ in range(N)]  # type: "List[List[int]]"
    B = [[int(next(tokens)) for _ in range(N)] for _ in range(N)]  # type: "List[List[int]]"
    solve(N, A, B)

if __name__ == '__main__':
    main()

```

そしてこちらは行列の転置を zip によって実現して rotate を実装した例。
rotate 関数だけ。

```python
def rotate(A: "List[List[int]]"):
    res = []
    for x in zip(*A[::-1]):
        res.append(x)
    return res
```

# C - Cards Query Problem

ポイントは、**数字が書かれたカードが入った箱**と**箱の番号を格納した箱**の二つの箱を用意することです。
ちなみに Python3 の int 型は[メモリの許す限り大きな値を扱える](https://note.nkmk.me/python-int-max-value/)ようですが、今回メモリ制限である1024MBを超えることはないはずです（下記参照）

```python
Q = 2 * pow(10, 5)
box = [Q] * ( Q - 1 ) # 3番目のクエリは1番目のクエリより後
card = [Q] * ( Q - 1 )
totalb = box.__sizeof__() + card.__sizeof__()
print(f'{totalb / 1024 / 1024:.0f}MB')
# 3MB
```

なお、提出にあたっては collections モジュールの defaultdict 関数を使いました。
defaultdict については[こちら](https://qiita.com/xza/items/72a1b07fcf64d1f4bdb7)に詳しいです。

```python
#!/usr/bin/env python3
from collections import defaultdict


def solve(N: int, Q: int):
    box = defaultdict(list)
    card = defaultdict(set)

    for _ in range(Q):
        q = list(map(int, input().split()))
        i = int(q[1])
        if q[0] == 1:
            j = int(q[2])
            box[j].append(i)
            card[i].add(j)
        elif q[0] == 2:
            print(*sorted(box[i]))
        else:
            print(*sorted(list(card[i])))


def main():
    N = int(input())
    Q = int(input())

    solve(N, Q)


if __name__ == "__main__":
    main()
```
