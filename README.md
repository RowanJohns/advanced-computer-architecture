# advanced-computer-architecture
ACA mini project coursework 2026

I'm calling this ChipGloss 👾💄👹

Superscalar processor simulator complete with an instruction set

# Instruction Set (based on MIPS)
### Arithmetic instructions 
addition: ADD rd r1 r2
immediate addition: ADDI rd r1 imm
subtraction: SUB rd r1 r2
immediate subtraction: SUBI rd r1 imm
multiplication: MUL rd r1 r2
division: DIV rd r1 r2

### Logical instructions
negation: NOT rd r1
conjunction: AND rd r1 r2
disjunction: OR rd r1 r2
exclusive disjunction: XOR rd r1 r2

### Comparison instructions
equality: EQU rd r1 r2
inequality: NEQ rd r1 r2
greater or equal: GTE rd r1 r2
greater than: GTH rd r1 r2
less or equal: LTE rd r1 r2
less than: LTH rd r1 r2

### Memory access instructions
move from reg to reg: MOVE rd rs
load immediate into register: LI rd imm
load address into register: LA rd addr
load word into register: LW rd addr
store word from register: SW rs addr

### Control flow instructions
branch: B lab
branch equal: BEQ r1 r2 lab
branch greater equal: BGE r1 r2 lab
branch greater than: BGT r1 r2 lab
branch less equal: BLE r1 r2 lab
branch less than: BLT r1 r2 lab
branch not equal: BNE r1 r2 lab
jump to pc value in register: JR rs
stop program: HALT

### Registers
general purpose: r0 - r15 (16 total)
