---
title: atcoder-toolsのPython提出時にAttributeErrorが発生する2023
# menu_order: 1
post_status: publish # publish, draft, pending, future
# post_excerpt: This is a post excerpt
# post_date: 2022-09-01 20:14:59 # 2022-09-01 20:14:59
# stick_post: no # yes, no
taxonomy:
    category:
        - AtCoder
        - tool
    post_tag:
        - tech
# custom_fields:
#     field1: value 1
#     field2: value 2
---

# 概要

下記の記事から2年以上の月日が流れ、同じエラーが別の原因で出ていたのでその備忘録。
https://zenn.dev/ky7245/articles/ad6c4bd0932be6

今回も AttributeError ですが、原因が少し違います。

```sh
$ atcoder-tools submit -u
2023-04-19 22:23:52,384 INFO: config is loaded from USER_CONFIG_PATH([$HOME here]/.atcodertools.toml)
2023-04-19 22:23:52,386 INFO: Loaded session from [$HOME here]/.local/share/atcoder-tools/cookie.txt
2023-04-19 22:23:52,756 INFO: Successfully Logged in using the previous session cache.
2023-04-19 22:23:52,756 INFO: If you'd like to invalidate the cache, delete [$HOME here]/.local/share/atcoder-tools/cookie.txt.
2023-04-19 22:23:52,761 INFO: Inferred exec file: ./main.py
# in_1.txt ... PASSED 67 ms
# in_2.txt ... PASSED 63 ms
# in_3.txt ... PASSED 74 ms
Passed all test cases!!!
2023-04-19 22:23:52,966 INFO: Submitting ./main.py as python
Traceback (most recent call last):
  File "[$HOME here]/.local/bin/atcoder-tools", line 8, in <module>
    sys.exit(main())
  File "[$HOME here]/.local/lib/python3.10/site-packages/atcodertools/atcoder_tools.py", line 67, in main
    exit_program(submit_main(prog, args))
  File "[$HOME here]/.local/lib/python3.10/site-packages/atcodertools/tools/submit.py", line 173, in main
    submission = client.submit_source_code(
  File "[$HOME here]/.local/lib/python3.10/site-packages/atcodertools/client/atcoder.py", line 179, in submit_source_code
    "option", text=lang_option_pattern).get("value")
AttributeError: 'NoneType' object has no attribute 'get'
```

# 原因

今回は HTML 上で Python に該当するプルダウンの値が `Python (3.8.2)` になっていることです。
（正確には、AtCoder Tools が AtCoder の変更に追随していないことです）
![image](/_images/at-attr-error1.png)

スタックトレースを一つずつ追ってみます。

>   File "[$HOME here]/.local/lib/python3.10/site-packages/atcodertools/client/atcoder.py", line 179, in submit_source_code
>     "option", text=lang_option_pattern).get("value")
> AttributeError: 'NoneType' object has no attribute 'get'

これはよく見ますが、get という関数がオブジェクトに存在しないことを示します。
ただ、「オブジェクトに存在しない」は少し遠回しに感じるかもしれません。
実際は、エラーの通り `NoneType` オブジェクトなので、これ以前にオブジェクトの作成に失敗している可能性が高いと見ることが出来ます。

該当のコードは以下の通りです。（[ 本家コード ](https://github.com/kyuridenamida/atcoder-tools/blob/stable/atcodertools/client/atcoder.py#L178-L179)）

```
        language_number = language_select_area.find(
            "option", text=lang_option_pattern).get("value")
```

ちなみに、AtCoder Tools では Beautiful Soup というスクレイピングに用いられるライブラリを使って提出を実現しています。
コードの通りではありますが、`language_select_area` （言語選択プルダウン）から `find` によって何かを検索し、`get("value")` にてその値を取得しようとしています。
これは、HTML だと `select` タグ内 `option` に設定された value を意味します。

つまり、この時点で、「言語選択プルダウンから選択しようとした”何か”が見つからなかったためにエラーが出た」と推測出来ます。

その”何か”とは、`text=lang_option_pattern` です。
ここまで来れば深追いせずとも対処法は想像がつくと思いますが、あえてもう少し踏み込みます。


[ 166行目 ](https://github.com/kyuridenamida/atcoder-tools/blob/stable/atcodertools/client/atcoder.py#L166)において、`lang_option_pattern` には `lang.submission_lang_pattern` が代入されています。
```
            lang_option_pattern = lang.submission_lang_pattern
```

また、この `lang` オブジェクトは、[ submit_source_code の第3引数 ](https://github.com/kyuridenamida/atcoder-tools/blob/stable/atcodertools/client/atcoder.py#L158)ですので、呼び出し元を見てみましょう。

>  File "[$HOME here]/.local/lib/python3.10/site-packages/atcodertools/tools/submit.py", line 173, in main
>    submission = client.submit_source_code(

下記が呼び出し元です。
`metadata.lang` が該当します。

```
        submission = client.submit_source_code(
            metadata.problem.contest, metadata.problem, metadata.lang, source)
```

このメタデータは、`metadata_file` から読み込んでいます。

```
    try:
        metadata = Metadata.load_from(metadata_file)
```

そのファイルは、`metadata.json` です。
```
    metadata_file = os.path.join(args.dir, "metadata.json")
```

これはどこにあるかと言うと、
```
    parser.add_argument("--dir", '-d',
                        help="Target directory to test. [Default] Current directory",
                        default=".")
```
`--dir` オプションによってディレクトリを指定した場合はそのディレクトリ直下、そうでない場合はカレントディレクトリです。

見てみましょう。
```
$ cat metadata.json 
{
 "code_filename": "main.py",
 "judge": {
  "judge_type": "normal"
 },
 "lang": "python",
 "problem": {
  "alphabet": "A",
  "contest": {
   "contest_id": "abc299"
  },
  "problem_id": "abc299_a"
 },
 "sample_in_pattern": "in_*.txt",
 "sample_out_pattern": "out_*.txt",
 "timeout_ms": 2000
}
```

注目すべきは、`lang` です。上記だと `python` になってますね。

で、私はここで少し時間を食いました。
それは、`lang: Union[str, Language]` に str オブジェクトを渡していますが、以下の警告が出ていないからです。

```
            warnings.warn(
                "Parameter lang as a str object is deprecated. "
                "Please use 'atcodertools.common.language.Language' object instead",
                UserWarning)
```

つまり、Languageオブジェクトとして lang を関数に渡しているはずです。

・・・ということでコードを追いかけていると、実は `metadata = Metadata.load_from(metadata_file)` の `load_from` メソッドでファイルを読み込む以外の処理が行われていました。

```python:tools/models/metadata.py
    @classmethod
    def load_from(cls, filename):
        with open(filename) as f:
            return cls.from_dict(json.load(f))
```

`from_dict` を見てみると、

```python:tools/models/metadata.py
    @classmethod
    def from_dict(cls, dic):
        if "judge" in dic:
            judge_type = dic["judge"]["judge_type"]
            if judge_type == "normal":
                judge_method = NormalJudge.from_dict(dic["judge"])
            elif judge_type == "decimal":
                judge_method = DecimalJudge.from_dict(dic["judge"])
            else:
                raise Exception("invalid judge type")
        else:
            judge_method = NormalJudge()

        if "timeout_ms" in dic:
            timeout_ms = dic["timeout_ms"]
        else:
            timeout_ms = None

        return Metadata(
            problem=Problem.from_dict(dic["problem"]),
            code_filename=dic["code_filename"],
            sample_in_pattern=dic["sample_in_pattern"],
            sample_out_pattern=dic["sample_out_pattern"],
            lang=Language.from_name(dic["lang"]),
            judge_method=judge_method,
            timeout_ms=timeout_ms
        )
```

`lang=Language.from_name(dic["lang"])` という箇所があります。
これが以下の通り定義されており、`ALL_LANGUAGE` の要素を返します。
```python:atcodertools/common/language.py
    @classmethod
    def from_name(cls, name: str):
        for lang in ALL_LANGUAGES:
            if lang.name == name:
                return lang
        raise LanguageNotFoundError(
            "No language support for '{}'".format(ALL_LANGUAGE_NAMES))
```

`ALL_LANGUAGE` は `ALL_LANGUAGES = [CPP, JAVA, RUST, PYTHON, NIM, DLANG, CSHARP, SWIFT, GO, JULIA]` となっており、`PYTHON` は以下の通りです。
```python:atcodertools/common/language.py
PYTHON = Language(
    name="python",
    display_name="Python",
    extension="py",
    submission_lang_pattern=re.compile(".*Python3.*|^Python$"),
    default_code_generator=python.main,
    default_template_path=get_default_template_path('py'),
    compile_command="python3 -mpy_compile {filename}.py",
    test_command="python3 {filename}.py",
    exec_filename="{filename}.pyc"
)
```

そして、`submit_source_code` 関数で用いられる `lang_option_pattern` とは `lang.submission_lang_pattern` でした。
よって、覚えてますか？
”何か”とは、`re.compile(".*Python3.*|^Python$")` だったのでした。
これは正規表現をコンパイルしてオブジェクト化する文で、その正規表現が 2023/04/26 現在の `Python (3.8.2)` にマッチするかといえば、どうでしょうか？
**マッチしません。**

`.*Python3.*` は Python3 という文字列が想定されていますし、`^Python$` は後ろの ` (3.8.2)`がマッチしません。
よって、この正規表現を修正することで今回のエラーは解消出来るでしょう。

# 解決策

以下は一例です。

```
PYTHON = Language(
    name="python",
    display_name="Python",
    extension="py",
-    submission_lang_pattern=re.compile(".*Python3.*|^Python$"),
+    submission_lang_pattern=re.compile(".*Python.*|^Python$"),
    default_code_generator=python.main,
    default_template_path=get_default_template_path('py'),
    compile_command="python3 -mpy_compile {filename}.py",
    test_command="python3 {filename}.py",
    exec_filename="{filename}.pyc"
)
```

[Issue](https://github.com/kyuridenamida/atcoder-tools/issues/204) になっていてしかもより良い対応が[ コミット ](https://github.com/firewood/atcoder-tools/commit/2076bf853ba592b9271b6af1055ae8e7c721dcad)されてました。

```
+ submission_lang_pattern=re.compile(".*Python3.*|^Python$|^Python \\(3\\..*"),
```

Python (3.x.x) に対応する正規表現ですね。

ちなみにこのコミットは2023/04/28時点でフォークであり未マージのため stable ブランチをクローンすると本エラーに出会います。
