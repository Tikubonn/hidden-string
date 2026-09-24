#!/usr/bin/python3

import os
import io
import re
import sys
import json
import random
import argparse

"""C言語で書かれたプログラムの文字列リテラルに難読化処理を施します。

難読化処理を施すことにより、オブジェクトファイル内の .rdata セクション内に、生の文字列が残らなくなり、静的解析しづらくなります。
実行速度・実装の容易さを加味して、暗号方法には排他的論理和を採用しています。

License
-------

Copyright 2026 tikubonn

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

def hide_str (source:str, global_var_name:str, seed:int) -> tuple[str, str]:

  """文字列リテラルの内容から、難読されたC言語コードを作成します。

  Parameters
  ----------
  source : str
    文字列リテラルの内容です。
  global_var_name : str
    難読化された文字列リテラルの保存先となる大域変数名です。
  seed : int
    難読化の際に使用される乱数のシード値です。

  Returns
  -------
  tuple[str, str]
    作成された大域変数の定義コード・文字列リテラルの代替となる難読化されたコードの組です。
  """

  encoded = source.encode("utf-8") + b"\0" #NUL文字を添加する
  rand = random.Random(seed)
  mask = [rand.randint(0, 0xff) for _ in encoded]
  global_var_code = "static const volatile char {:s}[] = {{{:s}}};".format(
    global_var_name,
    ", ".join((
      "0x{:02x}".format(c ^ m) for c, m in zip(encoded, mask)
    ))
  )
  eval_code = "((const char[]){{{:s}}})".format(
    ", ".join((
      "{:s}[{:d}] ^ 0x{:02x}".format(global_var_name, i, m)
      for i, m in enumerate(mask)
    ))
  )
  return global_var_code, eval_code

"""難読化命令に一致する正規表現オブジェクトです。
"""

REGEXP_HIDDEN_STR:"re.Pattern" = re.compile(r"^#hidden-string\s+(\".*\")\s*$")

def hide_str_file (file:"io.TextIOBase", base_global_var_name:str) -> str:

  """ソースコードに記述された難読化命令の部分に難読化を行います。

  Parameters
  ----------
  file : io.TextIOBase
    ソースコードが記録されたファイルストリームです。
  base_global_var_name : str
    難読化の際に使用される大域変数の名前です。

  Returns
  -------
  str
    難読化されたC言語のソースコードです。
  """

  with io.StringIO() as stream:

    global_var_codes = []

    for line in file:
      m = REGEXP_HIDDEN_STR.match(line)
      if m:
        content, = m.groups()
        global_var_code, eval_code = hide_str(
          json.loads(content), #専用処理を組むのが面倒だったので JSON パーサを流用して文字列リテラルを解析する
          global_var_name="{:s}{:d}".format(base_global_var_name, len(global_var_codes) +1),
          seed=len(global_var_codes)
        )
        global_var_codes.append(global_var_code)
        stream.write(eval_code)
        stream.write("\n")
      else:
        stream.write(line)

    return "{:s}\n{:s}".format(
      "\n".join(global_var_codes),
      stream.getvalue()
    )

#本処理

if __name__ == "__main__":

  #引数の定義

  parser = argparse.ArgumentParser()
  parser.add_argument("file", nargs="?", type=str, default="")
  parser.add_argument("-o", "--output", nargs="?", type=str, default="")
  parser.add_argument("-e", "--encoding", nargs="?", type=str, default="utf-8")
  parser.add_argument("--global-var-name", nargs="?", type=str, default="__HIDDEN_STR")
  args = parser.parse_args()

  #難読化処理

  if args.file:
    input_file = open(args.file, "r", encoding=args.encoding)
  else:
    input_file = os.fdopen(os.dup(sys.stdin.fileno()), "r", encoding=args.encoding)
  with input_file:
    result = hide_str_file(input_file, args.global_var_name)

  #結果の保存

  if args.output:
    output_file = open(args.output, "w", encoding=args.encoding)
  else:
    output_file = os.fdopen(os.dup(sys.stdout.fileno()), "w", encoding=args.encoding)
  with output_file:
    output_file.write(result)
