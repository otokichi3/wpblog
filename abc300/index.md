---
title: abc300(a, b, c)
post_status: publish # publish, draft, pending, future
taxonomy:
    category:
        - AtCoder
    post_tag:
        - tech
---

# まえがき

コンテスト中は b まででした。
c は明朝すぐ思いついて実装出来たので悔しい。
なぜ本番中に沼ったのか分からないほど。
https://atcoder.jp/users/otokichi3/history/share/abc300

# a

シンプルな if と for が使えるか、標準入力を受け取れるかどうかを問う問題です。

https://atcoder.jp/contests/abc300/tasks/abc300_a
https://atcoder.jp/contests/abc300/submissions/41022563

```python
#!/usr/bin/env python3
import sys


def solve(N: int, A: int, B: int, C: "List[int]"):
    for i in range(N):
        if (A + B) == C[i]:
            print(i + 1)
    return


def main():
    def iterate_tokens():
        for line in sys.stdin:
            for word in line.split():
                yield word

    tokens = iterate_tokens()
    N = int(next(tokens))  # type: int
    A = int(next(tokens))  # type: int
    B = int(next(tokens))  # type: int
    C = [int(next(tokens)) for _ in range(N)]  # type: "List[int]"
    solve(N, A, B, C)


if __name__ == "__main__":
    main()

```

# b

縦シフトと横シフトという概念を理解し、それを実装出来るかを問う問題でした。
Python のリストに対する insert は O(n) なので計算量に不安は抱えつつ提出。
ちなみに H, W はたかだか 30 なので、30 \* 30 = 900。
さらにAとBの各行を比較をするために H 回の演算をしても 900 \* 30 = 27000。
これは 10^6 なのでギリセーフという判断。
https://atcoder.jp/contests/abc300/tasks/abc300_b
https://atcoder.jp/contests/abc300/submissions/41061074

Python の関数の計算量の参考は以下より。
https://wiki.python.org/moin/TimeComplexity

以下のページによると Python のリストは C の配列らしく、先頭への要素追加はすべての要素のアドレスを型に応じてずらす必要があり O(n) となるよう。
https://qiita.com/Hironsan/items/68161ee16b1c9d7b25fb
※例えば int32 なら 4 バイト分すべて後ろにずらす、はず。

```python
#!/usr/bin/env python3

YES = "Yes"  # type: str
NO = "No"  # type: str


# 縦シフト
def vshift(A):
    a = A.pop(len(A) - 1)
    A.insert(0, a)
    return A


# 横シフト
def hshift(A):
    for i in range(len(A)):
        a = A[i].pop(len(A[i]) - 1)
        A[i].insert(0, a)
    return A


def solve(H, W, A, B):
    for _ in range(H):
        for _ in range(W):
            ok = True
            for i in range(H):
                if A[i] != B[i]:
                    ok = False
                    break
            if ok == True:
                print(YES)
                return
            hshift(A)
        vshift(A)
    print(NO)
    return


def main():
    H, W = map(int, input().split())
    A = ["."] * H
    B = ["."] * H
    for i in range(H):
        A[i] = list(input())
    for i in range(H):
        B[i] = list(input())
    solve(H, W, A, B)


if __name__ == "__main__":
    main()

```

# c

`#` で構成されるバツ印の大きさを記録して大きさごとにカウントする、という問題。
設問は5分ぐらいで理解出来たのに解法を思いつけず、翌朝のひらめきコードが以下の通り。

バツ印を構成する `#` のうち、その中心となる `#` からバツの大きさを測るという方法。
3重ループの構造になっていますが、H, W はたかだか 100、バツの大きさは 100 / 2 = 50 程度。
よって 100 \* 100 \* 50 = 500000 (10^5) なのでOK。

https://atcoder.jp/contests/abc300/tasks/abc300_c
https://atcoder.jp/contests/abc300/submissions/41061024

```python
#!/usr/bin/env python3


def solve(H, W, C):
    ans = [0] * min(H, W)
    for i in range(H - 1):
        for j in range(W - 1):
            # 最小のバツ
            if (
                C[i][j] == "#"
                and C[i - 1][j - 1] == "#"
                and C[i - 1][j + 1] == "#"
                and C[i + 1][j - 1] == "#"
                and C[i + 1][j + 1] == "#"
            ):
                n = 1
                while (
                    i + n + 1 < H and j + n + 1 < W and C[i + n + 1][j + n + 1] == "#"
                ):
                    n += 1
                ans[n - 1] += 1

    ans = [str(n) for n in ans]
    print(" ".join(ans))
    return


def main():
    H, W = map(int, input().split())
    C = ["."] * H
    for i in range(H):
        C[i] = list(input())
    solve(H, W, C)


if __name__ == "__main__":
    main()

```
