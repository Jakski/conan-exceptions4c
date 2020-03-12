#include <stdio.h>

#include <e4c.h>

int test1(void)
{
  throw(NotEnoughMemoryException, "Not enough memory");
}

int main()
{
  e4c_context_begin(E4C_FALSE);
  try {
    test1();
  } catch(NotEnoughMemoryException) {
    printf("Catched OOM error.\n");
  }
  e4c_context_end();
  return 0;
}
