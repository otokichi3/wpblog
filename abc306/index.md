---
title: abc306(a, b, c)
post_status: publish # publish, draft, pending, future
taxonomy:
    category:
        - AtCoder
    post_tag:
        - tech
---

# まえがき

C完でした。
unratedとなったためレート影響はありませんでした（が、C完まで22分は自己新だったのでちょっと悔しい）
https://atcoder.jp/users/otokichi3/history/share/abc306

# a

与えられた文字列の各文字をダブらせる問題です。
先頭からループでans変数に二回ずつ格納してダブらせました。

```python
N = int(input())
S = input()
ans = []
for i in range(N):
    ans.append(S[i])
    ans.append(S[i])
print(''.join(ans))
```

# b

0と1からなる長さ64の数列が与えられるので、それをリストに代入し、そのリストの添字で2のべき乗をかけます。
添字が0なら2^0、1なら2^1という具合です。

```python
A = list(map(int, input().split()))
ans = 0
for i in range(len(A)):
    ans += A[i] * pow(2, i)
print(ans)
```

# c

ちょっとややこしい問題ですが読み解ければコードを書くのは難しくありません。
N=3のとき1,2,3の3つの数字がそれぞれ3つ存在する数列が与えられるため、3つの数字の真ん中の添字を昇順に並び替えてその数字を出力します。
真ん中=2番目と考えることも出来ます。

```
3
1 1 3 2 3 2 2 3 1
```

上記のサンプルだと、2番目の1は添字2、2番目の2は添字6、2番目の3は添字5です。
数字を真ん中の添字の昇順に並び替えるので、`1 3 2`が答えになります。

辞書のキーをNで与えられた各数字とし、2番目に登場したらその添字を記録しておきます。
最後に辞書を値の昇順で並び替え、そのキーを出力して回答しています。

```python
N = int(input())
A = list(map(int, input().split()))
num = {}
for i in range(1, N+1):
   num[i] = False 
cnt = 0
for a in A:
    if a in num:
        if num[a] == False:
            num[a] = -1
        elif num[a] == -1:
            num[a] = cnt
        elif num[a] > 0:
            pass
    cnt += 1
sorted_items = sorted(num.items(), key=lambda x:x[1])
ans = []
for i in sorted_items:
    ans.append(str(i[0]))
print(' '.join(ans))
```
