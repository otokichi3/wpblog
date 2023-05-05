---
title: Pythonにおける行列の90度回転 for AtCoder
post_status: publish # publish, draft, pending, future
taxonomy:
    category:
        - AtCoder
        - Python
    post_tag:
        - tech
---
[mathjax]

# まえがき

[abc298のb問題](https://atcoder.jp/contests/abc298/tasks/abc298_b)にて2つの行列を90度回転させて一致するかを問う問題が出ました。
Pythonでは、簡単に右／左回転を実現出来ますので、それを説明します。

# 回転とは

まずは右回転します。

以下の行列を

<img src="/_images/rotate1.png" width="96" alt="original matrix">

以下の行列にする。

<img src="/_images/rotate2.png" width="96" alt="matrix rotated right">

次は左回転です。

以下の行列を

<img src="/_images/rotate1.png" width="96" alt="original matrix">

以下の行列にする。

<img src="/_images/rotate3.png" width="96" alt="matrix rotated left">

回ってますね。

# 早速コードを見る

まずは右回転です。

```python
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
```

肝は次の二つですね。

* zip(*L)
* *L[::-1]

zip 関数とは、

> Pythonの組み込み関数zip()は複数のイテラブルオブジェクト（リストやタプルなど）の要素をまとめる関数。forループで複数のリストの要素を取得する際などに使う。

ものです（[参考](https://note.nkmk.me/python-zip-usage-for/)）
また、ここでは `*` を用いてアンパックをしています。
アンパックは、一つの代入文で複数の変数にコレクションを代入する方法ですが、ここでは複数のリストを展開する目的で使用しています。

次に `*L[::-1]` ですが、[nkmk](https://note.nkmk.me/python-slice-usage/) から引用すると、Pythonのスライスは

> startとstopに加えて、増分stepも指定可能。[start:stop:step]のように書く。

ことが出来ます。（C 言語や JavaScript の for ループの構造に似てますね）
`start` と `stop` を省略し、`step` に `-1` を指定し、リストを逆順にしています。

ちなみに、`zip(*L)` の変化を行列の**転置**といいます。
行と列を入れ替えるだけのことですが、言葉は覚えておくと良いと思います。
