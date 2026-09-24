
/**
 * @file
 * hidden-string.py を複数ファイルに適用した状態で適切にビルドできるかを検証します。
 */

#include <test.h>
#include <string.h>

//難読化されたファイルのヘッダをインクスルードする

#include "external-string.h"
#include "external-string2.h"

static void testcase (){
  TEST(strcmp(get_external_string(), get_external_string2()) == 0);
}

void __stdcall testsuite_multiple_files (){
  testcase();
}
