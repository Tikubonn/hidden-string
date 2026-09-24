
# hidden-string 

![](https://img.shields.io/badge/Python-3.12-blue)
![](https://img.shields.io/badge/License-MIT-blue)

## Overview

C言語で書かれたプログラムの文字列リテラルに難読化処理を施します。

難読化処理を施すことにより、オブジェクトファイル内の .rdata セクション内に、生の文字列が残らなくなり、静的解析しづらくなります。
実行速度・実装の容易さを加味して、暗号方法には排他的論理和を採用しています。

### Sample Code

```c
#include <stdio.h>

int main (){
  printf(
#hidden-string "hiho!\n"
  );
  return 0;
}
```

```bash
python hidden-string.py -e utf-8 -o sample.2.c sample.c
```

```c
#include <stdio.h>

const volatile char __HIDDEN_STR1[] = {0xad, 0xbe, 0x7c, 0xeb, 0xd9, 0xc5, 0x9b};

#include <stdio.h>

int main (){
  printf(
((const char[]){__HIDDEN_STR1[0] ^ 0xc5, __HIDDEN_STR1[1] ^ 0xd7, __HIDDEN_STR1[2] ^ 0x14, __HIDDEN_STR1[3] ^ 0x84, __HIDDEN_STR1[4] ^ 0xf8, __HIDDEN_STR1[5] ^ 0xcf, __HIDDEN_STR1[6] ^ 0x9b})
  );
  return 0;
}
```

## Install

単体のスクリプトファイルなので `pip` 等によるインストールは必要ありません。

## License 

© 2026 tikubonn

See [hidden-string.py](hidden-string.py) to license details.
