# advanced-computer-architecture
ACA mini project coursework 2026

I'm calling this ChipGloss 👾💄👹

Superscalar processor simulator complete with an instruction set

# Instruction Set (based on MIPS)
### Arithmetic instructions 
addition: ADD rd r1 r2\n
immediate addition: ADDI rd r1 imm\n
subtraction: SUB rd r1 r2\n
immediate subtraction: SUBI rd r1 imm\n
multiplication: MUL rd r1 r2\n
division: DIV rd r1 r2\n

### Logical instructions
negation: NOT rd r1\n
conjunction: AND rd r1 r2\n
disjunction: OR rd r1 r2\n
exclusive disjunction: XOR rd r1 r2\n

### Comparison instructions
equality: EQU rd r1 r2\n
inequality: NEQ rd r1 r2\n
greater or equal: GTE rd r1 r2\n
greater than: GTH rd r1 r2\n
less or equal: LTE rd r1 r2\n
less than: LTH rd r1 r2\n

### Memory access instructions
move from reg to reg: MOVE rd rs\n
load immediate into register: LI rd imm\n
load address into register: LA rd addr\n
load word into register: LW rd addr\n
store word from register: SW rs addr\n

### Control flow instructions
branch: B lab\n
branch equal: BEQ r1 r2 lab\n
branch greater equal: BGE r1 r2 lab\n
branch greater than: BGT r1 r2 lab\n
branch less equal: BLE r1 r2 lab\n
branch less than: BLT r1 r2 lab\n
branch not equal: BNE r1 r2 lab\n
jump to pc value in register: JR rs\n
stop program: HALT

### Registers
general purpose: r0 - r15 (16 total)\n
