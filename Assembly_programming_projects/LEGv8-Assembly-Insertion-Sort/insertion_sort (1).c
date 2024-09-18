/* To compile this program:
 *   gcc insertion_sort.c -o insertion_sort
 * Change N and recompile to run on arrays of different sizes.
 *
 */

#define N 512

/* Here is a single-function version of insertion sort. This version is only here for reference.
 */
void insertion_sort_one_function_do_not_implement(long long *a,
                                                  long long n)
{
  long long i, j, t;
  
  for (i = 1; i < n; i++) {
    for (t = a[i], j = i - 1; j > -1 && a[j] > t; j--) {
      a[j + 1] = a[j];
    }
    a[j + 1] = t;
  }
}

/* Copies the value what into array a at index where */
void is_insert(long long *a, long long what, long long where)
{
  a[where] = what;
}

/* Given array a and index end where the items in a at indices less *
 * than end are in non-decreasing order, overwrites the item at     *
 * index end and shifts all elements larger than the element        *
 * originally at a[end] one position toward the end of the array,  *
 * thus creating a hole for the original a[end] in its sorted      *
 * position.  Returns the index of the hole.                        */
long long is_shift(long long *a, long long end)
{
  long long i, tmp;
  
  for (tmp = a[end], i = end - 1; i > -1 && a[i] > tmp; i--) {
    a[i + 1] = a[i];
  }

  return i + 1;
}

/* Sorts array a containing n elements into non-descending order. */
void insertion_sort(long long *a, long long n)
{
  long long i, value;

  for (i = 1; i < n; i++) {
    value = a[i];
    is_insert(a, value, is_shift(a, i));
  }
}

/* fill fills the array a (of n elements) with decreasing values from *
 * n - 1 to zero (reverse sorted order).                              */
void fill(long long *a, long long n) {
  long long i;
  
  for (i = 0; i < n; i++) {
    a[i] = n - i - 1;
  }
}

/* This is a standard, iterative binary search.  a is the base address *
 * of your array.  start is the base index of the search space in a.   *
 * end is the final index of the search space in a.  value is the      *
 * value that is being sought.  a must be in sorted order.  Returns    *
 * the index of the first element found wherein the value of the       *
 * element is value.  Returns -1 if value is not found in a.           */
long log binary_search(long long *a, long long start,
		       long long end, long long value)
{
  long long m;

  while (start <= end) {
    m = (((end + start) + 1) / 2);

    if (a[m] == value) {
      return m;
    }

    if (value > a[m]) {
      start = m + 1;
    } else {
      end = m - 1;
    }
  }
  
  return -1;
}

/* Your main function should allocate space for an array, call fill to   *
 * fill it with decreasing numbers, and then call insertion_sort to sort *
 * it.  Use the HALT emulator instruction to see the memory contents and *
 * confirm that your functions work.  You may choose any array size you  *
 * like (up to the default limit of memory, 4096 bytes or 512 8-byte     *
 * integers).                                                            *
 *                                                                       * 
 * After sorting, call binary search with 4 values: the smallest,        *
 * largest, and middle items in your array, followed by a value not in   *
 * the array.  After each call PRNT X0 to display the return value.      *
 *                                                                       *
 * After completing all of the above, HALT the emulator to force a core  *
 * dump so that you (and the TAs) can examine the contents of memory.    *
 *                                                                       *
 */
int main(int argc, char *argv[])
{
  /* In your LEGv8 program, main will not be a procedure.  Control will *
   * begin at the top of the file, so you should think of that as main. *
   * If control reaches the end of the file, the program will exit,     *
   * which you may think of as leaving main.                            */

  long long a[N];

  fill(a, N);

  insertion_sort(a, N);

  /* Returns 0 */
  binary_search(a, 0, N - 1, 0);
  /* Returns 511 (N - 1) */
  binary_search(a, 0, N - 1, N - 1);
  /* Returns 255 ((N - 1) / 2) */
  binary_search(a, 0, N - 1, N / 2);
  /* Returns -1 */
  binary_search(a, 0, N - 1, N);
  
  return 0;
}
