
#include <test.h>
#include <string.h>

static void testcase (){
  TEST(strcmp("abc123", 
#hidden-string "abc123"
  ) == 0);
}

void __stdcall testsuite (){
  testcase();
}
