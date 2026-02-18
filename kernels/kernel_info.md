Kernel 1: simple_loop.txt
- loops from 0 to 10
- r0 is counter
- r1 is the number of loops to do
- r0 == r1 at the end

Kernel 2: factorial.txt
- recursively calculates the factorial of the number in r0
- stores the result in r1
- r2 stores the current number temporarily
- r3 is used for base case checking and unwinding
- r4 stores the return address for jumps  