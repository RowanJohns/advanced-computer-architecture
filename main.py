import sys

# Instruction Set (based on MIPS)

# Arithmetic instructions 
 
# addition: ADD rd r1 r2
# immediate addition: ADDI rd r1 imm
# subtraction: SUB rd r1 r2
# immediate subtraction: SUBI rd r1 imm
# multiplication: MUL rd r1 r2
# division: DIV rd r1 r2

# Logical instructions

# negation: NOT rd r1
# conjunction: AND rd r1 r2
# disjunction: OR rd r1 r2
# exclusive disjunction: XOR rd r1 r2


# Comparison instructions

# equality: EQU rd r1 r2
# inequality: NEQ rd r1 r2
# greater or equal: GTE rd r1 r2
# greater than: GTH rd r1 r2
# less or equal: LTE rd r1 r2
# less than: LTH rd r1 r2


# Memory access instructions

# move from reg to reg: MOVE rd rs
# load immediate into register: LI rd imm
# load address into register: LA rd addr
# load word into register: LW rd addr
# store word from register: SW rs addr


# Control flow instructions

# branch: B lab
# branch equal: BEQ r1 r2 lab
# branch greater equal: BGE r1 r2 lab
# branch greater than: BGT r1 r2 lab
# branch less equal: BLE r1 r2 lab
# branch less than: BLT r1 r2 lab
# branch not equal: BNE r1 r2 lab
# jump to instruction in register: JR rs
# stop program: HALT


# Registers

# general purpose: r0 - r15 (16 total)
# special purpose: 


# Program states:
# 0 - startup
# 1 - fetch instruction
# 10 - fetch register values
# 11 - fetch all but first register values (ignore destination register)
# 2 - decode
# 3 - execute
# 4 - finish

# used to determine if a line is a label
instructions = ["ADD", "ADDI", "SUB", "SUBI", "MUL", "DIV", "NOT", "AND", "OR", "XOR", "EQU", "NEQ", "GTE", "GTH", "LTE", "LTH", "MOVE", "LI", "LA", "LW", "SW", "B", "BEQ", "BGE", "BGT", "BLE", "BLT", "BNE", "JR", "HALT"]

registers = {
    "r0": 0, 
    "r1": 0, 
    "r2": 0, 
    "r3": 0, 
    "r4": 0, 
    "r5": 0, 
    "r6": 0, 
    "r7": 0, 
    "r8": 0, 
    "r9": 0, 
    "r10": 0, 
    "r11": 0, 
    "r12": 0, 
    "r13": 0, 
    "r14": 0, 
    "r15": 0
}
special_registers = {
    "IR": [],
    "PC": 0,
    "labels": {}
}
program = []

def fetch(state: int) -> int:
    print("[DBG] Fetching")
    match state:
        case 1:
            # fetch current instruction
            # split the current instruction into its components
            instruction = program[special_registers["PC"]].split(" ")
            # store the instruction in the instruction register
            special_registers["IR"] = instruction
            print("[DBG] Instruction: ", instruction)
            return 2
        case 10:
            instruction = special_registers["IR"]
            # fetch any register values
            for part in instruction:
                if part in registers.keys():
                    instruction[instruction.index(part)] = registers[part]
            special_registers["IR"] = instruction
            print("[DBG] Instruction: ", instruction)
            # at this point the instruction is ready to execute
            return 3
        case 11:
            instruction = special_registers["IR"]
            # fetch any register values except the destination register
            for part in instruction:
                if part in registers.keys():
                    # check that this is not the destination register
                    if instruction.index(part) != 1:
                        instruction[instruction.index(part)] = registers[part]
            special_registers["IR"] = instruction
            print("[DBG] Instruction: ", instruction)
            # at this point the instruction is ready to execute
            return 3


def decode(state: int) -> int:
    print("[DBG] Decoding")
    match (special_registers["IR"][0]):
        # arithmetic opcodes
        case "ADD" | "ADDI" | "SUB" | "SUBI" | "MUL" | "DIV":
            return 11
        # logical opcodes
        case "NOT" | "AND" | "OR" | "XOR":
            return 11
        # comparison opcodes
        case "EQU" | "NEQ" | "GTE" | "GTH" | "LTE" | "LTH":
            return 11
        # memory access opcodes
        case "MOVE":
            return 11
        case "LI" | "LA" | "LW":
            return 3
        case "SW":
            return 10
        # control flow opcodes
        case "B":
            return 3
        case "BEQ" | "BGE" | "BGT" | "BLE" | "BLT" | "BNE" | "JR":
            return 10
        case "HALT":
            print(registers)
            return 4
        case _:
            print("[DBG] Found label, storing...")
            special_registers["labels"].update({special_registers["IR"][0]: special_registers["PC"]})
            special_registers["PC"] += 1
            return 1

def execute(state: int) -> int:
    print(f"[DBG] Executing {special_registers["IR"]}")
    match (special_registers["IR"][0]):
        case "ADD":
            registers[special_registers["IR"][1]] = int(special_registers["IR"][2]) + int(special_registers["IR"][3])
        case "ADDI":
            registers[special_registers["IR"][1]] += int(special_registers["IR"][2])
        case "SUB":
            registers[special_registers["IR"][1]] = int(special_registers["IR"][2]) - int(special_registers["IR"][3])
        case "SUBI":
            registers[special_registers["IR"][1]] -= int(special_registers["IR"][2])
        case "MUL":
            registers[special_registers["IR"][1]] = int(special_registers["IR"][2]) * int(special_registers["IR"][3])
        case "DIV":
            registers[special_registers["IR"][1]] = int(special_registers["IR"][2]) / int(special_registers["IR"][3])
        case "NOT":
            registers[special_registers["IR"][1]] = ~int(special_registers["IR"][2])
        case "AND":
            registers[special_registers["IR"][1]] = int(special_registers["IR"][2]) & int(special_registers["IR"][3])
        case "OR":
            registers[special_registers["IR"][1]] = int(special_registers["IR"][2]) | int(special_registers["IR"][3])
        case "XOR":
            registers[special_registers["IR"][1]] = int(special_registers["IR"][2]) ^ int(special_registers["IR"][3])
        case "EQU":
            registers[special_registers["IR"][1]] = int(special_registers["IR"][2]) == int(special_registers["IR"][3])
        case "NEQ":
            registers[special_registers["IR"][1]] = int(special_registers["IR"][2]) != int(special_registers["IR"][3])
        case "GTE":
            registers[special_registers["IR"][1]] = int(special_registers["IR"][2]) >= int(special_registers["IR"][3])
        case "GTH":
            registers[special_registers["IR"][1]] = int(special_registers["IR"][2]) > int(special_registers["IR"][3])
        case "LTE":
            registers[special_registers["IR"][1]] = int(special_registers["IR"][2]) <= int(special_registers["IR"][3])
        case "LTH":
            registers[special_registers["IR"][1]] = int(special_registers["IR"][2]) < int(special_registers["IR"][3])
        case "MOVE" | "LI":
            registers[special_registers["IR"][1]] = int(special_registers["IR"][2])
        #TODO: implement these
        case "LA":
            pass
        case "LW":
            pass
        case "SW":
            pass
        case "B":
            if special_registers["IR"][1] in special_registers["labels"].keys():
                special_registers["PC"] = special_registers["labels"][special_registers["IR"][1]]
            else:
                raise Exception(f"Label not found: {special_registers["IR"][1]}")
        case "BEQ":
            if special_registers["IR"][1] == special_registers["IR"][2]:
                if special_registers["IR"][3] in special_registers["labels"].keys():
                    special_registers["PC"] = special_registers["labels"][special_registers["IR"][3]]
                else:
                    raise Exception(f"Label not found: {special_registers["IR"][3]}")
        case "BGE":
            if special_registers["IR"][1] >= special_registers["IR"][2]:
                if special_registers["IR"][3] in special_registers["labels"].keys():
                    special_registers["PC"] = special_registers["labels"][special_registers["IR"][3]]
                else:
                    raise Exception(f"Label not found: {special_registers["IR"][3]}")
        case "BGT":
            if special_registers["IR"][1] > special_registers["IR"][2]:
                if special_registers["IR"][3] in special_registers["labels"].keys():
                    special_registers["PC"] = special_registers["labels"][special_registers["IR"][3]]
                else:
                    raise Exception(f"Label not found: {special_registers["IR"][3]}")
        case "BLE":
            if special_registers["IR"][1] <= special_registers["IR"][2]:
                if special_registers["IR"][3] in special_registers["labels"].keys():
                    special_registers["PC"] = special_registers["labels"][special_registers["IR"][3]]
                else:
                    raise Exception(f"Label not found: {special_registers["IR"][3]}")
        case "BLT":
            if special_registers["IR"][1] < special_registers["IR"][2]:
                if special_registers["IR"][3] in special_registers["labels"].keys():
                    special_registers["PC"] = special_registers["labels"][special_registers["IR"][3]]
                else:
                    raise Exception(f"Label not found: {special_registers["IR"][3]}")
        case "BNE":
            if special_registers["IR"][1] != special_registers["IR"][2]:
                if special_registers["IR"][3] in special_registers["labels"].keys():
                    special_registers["PC"] = special_registers["labels"][special_registers["IR"][3]]
                else:
                    raise Exception(f"Label not found: {special_registers["IR"][3]}")
        case "JR":
            if special_registers["IR"][1] in special_registers["labels"].keys():
                special_registers["PC"] = special_registers["labels"][special_registers["IR"][3]]
            else:
                raise Exception(f"Label not found: {special_registers["IR"][1]}")
    special_registers["PC"] += 1
    return 1

def main():
    state = 1
    # read the program in from argv and store it in the program array
    filename = sys.argv[1]
    try: 
        program_file = open(filename)
    except FileNotFoundError, FileExistsError:
        return Exception("Issue with opening program file.")
    # store the file contents line by line
    line = program_file.readline()
    current_line = 0
    while line:
        # clean up the line
        line = line.lstrip()
        line = line.strip("\n")
        program.append(line)
        # check whether the line is a label, and store it for later if so
        if line[:1] not in instructions and line[:2] not in instructions and line[:3] not in instructions and line[:4] not in instructions:
            potential_label = line.split(" ")
            if len(potential_label) == 1:
                special_registers["labels"].update({line:current_line})
        line = program_file.readline()
        current_line += 1
    while (state != 4):
        print(f"[DBG] Current state: {state}")
        print(f"[DBG] Program Counter: {special_registers["PC"]}")
        match state:
            case 1 | 10 | 11:
                state = fetch(state)
            case 2:
                state = decode(state)
            case 3:
                state = execute(state)
            case _:
                print("State unrecognised, terminating...")
                break
    print("[DBG] Finished program.")

main()