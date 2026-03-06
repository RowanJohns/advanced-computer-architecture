import sys
import asyncio

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
# load word at address rs+imm into register: LO rd rs imm
# store word from register: SW rs addr


# Control flow instructions

# branch: B lab
# branch equal: BEQ r1 r2 lab
# branch greater equal: BGE r1 r2 lab
# branch greater than: BGT r1 r2 lab
# branch less equal: BLE r1 r2 lab
# branch less than: BLT r1 r2 lab
# branch not equal: BNE r1 r2 lab
# jump to pc value in register: JR rs
# stop program: HALT


# Registers

# general purpose: r0 - r15 (16 total)
# special purpose: 
# IR - instruction register 
# PC - program counter 
# CYC - current cycle
# labels - dictionary of labels and their addresses in the program
# state: 0 - HALT, 1 - running

# used to determine if a line is a label
instructions = ["ADD", "ADDI", "SUB", "SUBI", "MUL", "DIV", "NOT", "AND", "OR", "XOR", "EQU", "NEQ", "GTE", "GTH", "LTE", "LTH", "MOVE", "LI", "LA", "LW", "LO", "SW", "B", "BEQ", "BGE", "BGT", "BLE", "BLT", "BNE", "JR", "HALT"]

# general purpose registers
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

# special purpose registers
special_registers = {
    "PC": 0,
    "CYC": 0,
    "labels": {},
    "state": 1,
    "exec_instructions": 0
}

# pipeline registers
# f is fetch unit, contains 2 instructions per cycle
# d is decode unit, contains 2 instructions per cycle
# e1 is ALU 1, contains the result and destination of 1 instruction per cycle
# e2 is ALU 2, contains the result and destination of 1 instruction per cycle
# b is branch unit, contains -1 if the previous branch was untaken and 1 if it was taken
# ls is load/store unit, contains contains the result and destination of 1 load or store per cycle 
pipeline_registers = {"f": [0,0], "d": [0,0], "e1": 0, "e2": 0, "b": 0, "ls": 0}

# the program will be stored in this array
program = []

# initialise 256 address memory
memory = [0 for _ in range(256)]

def print_metrics():
    # Print all useful metrics at the end of execution
    print("Execution finished, here are some key metrics:")
    print(f"Number of cycles: {special_registers["CYC"]}")
    print(f"Number of instructions executed: {special_registers["exec_instructions"]}")
    print(f"Average instructions executed per cycle: {special_registers["exec_instructions"]/special_registers["CYC"]}")
    print(f"Final general purpose register values: {registers}")
    print(f"Final pipeline register values: {pipeline_registers}")
    print(f"Final special register values: {special_registers}")

def fetch():
    # fetch 2 instructions per cycle
    for i in range(2):
        # Check whether the previous fetched was a branch or memory instruction, and if so, block until it is resolved (only one branch and load/store unit).
        if i == 1:
            match pipeline_registers["f"][0][0]:
                case "B" | "BEQ" | "BGE" | "BGT" | "BLE" | "BLT" | "BNE" | "JR" | "MOVE" | "LI" | "LA" | "LW" | "LO" | "SW":
                    break
        # If we have reached the end of the program, return
        if special_registers["PC"] < len(program):
            # split the current instruction into its components
            instruction = program[special_registers["PC"]].split(" ")
        else:
            return
        match instruction[0]:
            # fetch all but the first register value (first is the destination register)
            case "ADD" | "ADDI" | "SUB" | "SUBI" | "MUL" | "DIV" | "NOT" | "AND" | "OR" | "XOR" | "EQU" | "NEQ" | "GTE" | "GTH" | "LTE" | "LTH" | "MOVE" | "LO":
                # fetch any register values except the destination register
                for part in instruction:
                    if part in registers.keys():
                        # check that this is not the destination register
                        if instruction.index(part) != 1:
                            instruction[instruction.index(part)] = registers[part]
                pipeline_registers["f"][i] = instruction
            # fetch all register values
            case "SW" | "BEQ" | "BGE" | "BGT" | "BLE" | "BLT" | "BNE" | "JR":
                # fetch any register values
                for part in instruction:
                    if part in registers.keys():
                        instruction[instruction.index(part)] = registers[part]
                pipeline_registers["f"][i] = instruction
            case _:
                # store the instruction in the instruction register
                pipeline_registers["f"][i] = instruction
        special_registers["PC"] += 1
    print(f"End of fetch, PC: {special_registers["PC"]}")
            
            


def decode():
    execute_state = [-1,-1]
    for i in range(2):
        if pipeline_registers["f"][i] != 0:
            # move the instruction into the decode pipeline register
            pipeline_registers["d"][i] = pipeline_registers["f"][i]
            match (pipeline_registers["d"][i][0]):
                # determine what to do next
                case "HALT":
                    print_metrics()
                    special_registers["state"] = 0
                    exit()
                case "ADD" | "ADDI" | "SUB" | "SUBI" | "MUL" | "DIV" | "NOT" | "AND" | "OR" | "XOR" | "EQU" | "NEQ" | "GTE" | "GTH" | "LTE" | "LTH":  
                    execute_state[i] = 0
                case "B" | "BEQ" | "BGE" | "BGT" | "BLE" | "BLT" | "BNE" | "JR":
                    execute_state[i] = 1
                case "MOVE" | "LI" | "LA" | "LW" | "LO" | "SW":
                    execute_state[i] = 2
    return execute_state

def alu_1():
    match (pipeline_registers["d"][0]):
        # Store an array with [destination, value] into the execute pipeline register. These values will be written to their destinations in the writeback function.
        case "ADD":
            pipeline_registers["e1"] = [pipeline_registers["d"][0][1], int(pipeline_registers["d"][0][2]) + int(pipeline_registers["d"][0][3])]
        case "ADDI":
            pipeline_registers["e1"] = [pipeline_registers["d"][0][1], registers[pipeline_registers["d"][0][1]] + int(pipeline_registers["d"][0][2])]
        case "SUB":
            pipeline_registers["e1"] = [pipeline_registers["d"][0][1], int(pipeline_registers["d"][0][2]) - int(pipeline_registers["d"][0][3])]
        case "SUBI":
            pipeline_registers["e1"] = [pipeline_registers["d"][0][1], registers[pipeline_registers["d"][0][1]] - int(pipeline_registers["d"][0][2])]
        case "MUL":
            pipeline_registers["e1"] = [pipeline_registers["d"][0][1], int(pipeline_registers["d"][0][2]) * int(pipeline_registers["d"][0][3])]
        case "DIV":
            pipeline_registers["e1"] = [pipeline_registers["d"][0][1], int(pipeline_registers["d"][0][2]) / int(pipeline_registers["d"][0][3])]
        case "NOT":
            pipeline_registers["e1"] = [pipeline_registers["d"][0][1], ~int(pipeline_registers["d"][0][2])]
        case "AND":
            pipeline_registers["e1"] = [pipeline_registers["d"][0][1], int(pipeline_registers["d"][0][2]) & int(pipeline_registers["d"][0][3])]
        case "OR":
            pipeline_registers["e1"] = [pipeline_registers["d"][0][1], int(pipeline_registers["d"][0][2]) | int(pipeline_registers["d"][0][3])]
        case "XOR":
            pipeline_registers["e1"] = [pipeline_registers["d"][0][1], int(pipeline_registers["d"][0][2]) ^ int(pipeline_registers["d"][0][3])]
        case "EQU":
            pipeline_registers["e1"] = [pipeline_registers["d"][0][1], int(pipeline_registers["d"][0][2]) == int(pipeline_registers["d"][0][3])]
        case "NEQ":
            pipeline_registers["e1"] = [pipeline_registers["d"][0][1], int(pipeline_registers["d"][0][2]) != int(pipeline_registers["d"][0][3])]
        case "GTE":
            pipeline_registers["e1"] = [pipeline_registers["d"][0][1], int(pipeline_registers["d"][0][2]) >= int(pipeline_registers["d"][0][3])]
        case "GTH":
            pipeline_registers["e1"] = [pipeline_registers["d"][0][1], int(pipeline_registers["d"][0][2]) > int(pipeline_registers["d"][0][3])]
        case "LTE":
            pipeline_registers["e1"] = [pipeline_registers["d"][0][1], int(pipeline_registers["d"][0][2]) <= int(pipeline_registers["d"][0][3])]
        case "LTH":
            pipeline_registers["e1"] = [pipeline_registers["d"][0][1], int(pipeline_registers["d"][0][2]) < int(pipeline_registers["d"][0][3])]
    pipeline_registers["f"][0] = 0
    special_registers["exec_instructions"] += 1

def alu_2():
    match (pipeline_registers["d"][1][0]):
        # Store an array with [destination, value] into the execute pipeline register. These values will be written to their destinations in the writeback function.
        case "ADD":
            pipeline_registers["e2"] = [pipeline_registers["d"][1][1], int(pipeline_registers["d"][1][2]) + int(pipeline_registers["d"][1][3])]
        case "ADDI":
            pipeline_registers["e2"] = [pipeline_registers["d"][1][1], registers[pipeline_registers["d"][1][1]] + int(pipeline_registers["d"][1][2])]
        case "SUB":
            pipeline_registers["e2"] = [pipeline_registers["d"][1][1], int(pipeline_registers["d"][1][2]) - int(pipeline_registers["d"][3])]
        case "SUBI":
            pipeline_registers["e2"] = [pipeline_registers["d"][1][1], registers[pipeline_registers["d"][1][1]] - int(pipeline_registers["d"][2])]
        case "MUL":
            pipeline_registers["e2"] = [pipeline_registers["d"][1][1], int(pipeline_registers["d"][1][2]) * int(pipeline_registers["d"][3])]
        case "DIV":
            pipeline_registers["e2"] = [pipeline_registers["d"][1][1], int(pipeline_registers["d"][1][2]) / int(pipeline_registers["d"][3])]
        case "NOT":
            pipeline_registers["e2"] = [pipeline_registers["d"][1][1], ~int(pipeline_registers["d"][1][2])]
        case "AND":
            pipeline_registers["e2"] = [pipeline_registers["d"][1][1], int(pipeline_registers["d"][1][2]) & int(pipeline_registers["d"][1][3])]
        case "OR":
            pipeline_registers["e2"] = [pipeline_registers["d"][1][1], int(pipeline_registers["d"][1][2]) | int(pipeline_registers["d"][1][3])]
        case "XOR":
            pipeline_registers["e2"] = [pipeline_registers["d"][1][1], int(pipeline_registers["d"][1][2]) ^ int(pipeline_registers["d"][1][3])]
        case "EQU":
            pipeline_registers["e2"] = [pipeline_registers["d"][1][1], int(pipeline_registers["d"][1][2]) == int(pipeline_registers["d"][1][3])]
        case "NEQ":
            pipeline_registers["e2"] = [pipeline_registers["d"][1][1], int(pipeline_registers["d"][1][2]) != int(pipeline_registers["d"][1][3])]
        case "GTE":
            pipeline_registers["e2"] = [pipeline_registers["d"][1][1], int(pipeline_registers["d"][1][2]) >= int(pipeline_registers["d"][1][3])]
        case "GTH":
            pipeline_registers["e2"] = [pipeline_registers["d"][1][1], int(pipeline_registers["d"][1][2]) > int(pipeline_registers["d"][1][3])]
        case "LTE":
            pipeline_registers["e2"] = [pipeline_registers["d"][1][1], int(pipeline_registers["d"][1][2]) <= int(pipeline_registers["d"][1][3])]
        case "LTH":
            pipeline_registers["e2"] = [pipeline_registers["d"][1][1], int(pipeline_registers["d"][1][2]) < int(pipeline_registers["d"][1][3])]
    pipeline_registers["f"][1] = 0
    special_registers["exec_instructions"] += 1

def branch_unit(instruction_index):
    # For branches, we do nothing in the writeback stage so we don't need to store destination and result
    # Store -1 in branch pipeline register for any untaken branches and 1 for a taken branch
    match pipeline_registers["d"][instruction_index][0]:
        case "B":
            if pipeline_registers["d"][instruction_index][1] in special_registers["labels"].keys():
                special_registers["PC"] = special_registers["labels"][pipeline_registers["d"][instruction_index][1]]
                pipeline_registers["b"] = 1
            else:
                raise Exception(f"Label not found: {pipeline_registers["d"][instruction_index][1]}")
            pipeline_registers["b"] = -1
        case "BEQ":
            if pipeline_registers["d"][instruction_index][1] == pipeline_registers["d"][instruction_index][2]:
                if pipeline_registers["d"][instruction_index][3] in special_registers["labels"].keys():
                    special_registers["PC"] = special_registers["labels"][pipeline_registers["d"][instruction_index][3]]
                    pipeline_registers["b"] = 1
                else:
                    raise Exception(f"Label not found: {pipeline_registers["d"][3]}")
            else:
                pipeline_registers["b"] = -1
        case "BGE":
            if pipeline_registers["d"][instruction_index][1] >= pipeline_registers["d"][instruction_index][2]:
                if pipeline_registers["d"][instruction_index][3] in special_registers["labels"].keys():
                    special_registers["PC"] = special_registers["labels"][pipeline_registers["d"][instruction_index][3]]
                    pipeline_registers["b"] = 1
                else:
                    raise Exception(f"Label not found: {pipeline_registers["d"][instruction_index][3]}")
            else:
                pipeline_registers["b"] = -1
        case "BGT":
            if pipeline_registers["d"][instruction_index][1] > pipeline_registers["d"][instruction_index][2]:
                if pipeline_registers["d"][instruction_index][3] in special_registers["labels"].keys():
                    special_registers["PC"] = special_registers["labels"][pipeline_registers["d"][instruction_index][3]]
                    pipeline_registers["b"] = 1
                else:
                    raise Exception(f"Label not found: {pipeline_registers["d"][instruction_index][3]}")
            else:
                pipeline_registers["b"] = -1
        case "BLE":
            if pipeline_registers["d"][instruction_index][1] <= pipeline_registers["d"][instruction_index][2]:
                if pipeline_registers["d"][instruction_index][3] in special_registers["labels"].keys():
                    special_registers["PC"] = special_registers["labels"][pipeline_registers["d"][instruction_index][3]]
                    pipeline_registers["b"] = 1
                else:
                    raise Exception(f"Label not found: {pipeline_registers["d"][instruction_index][3]}")
            else:
                pipeline_registers["b"] = -1
        case "BLT":
            if pipeline_registers["d"][instruction_index][1] < pipeline_registers["d"][instruction_index][2]:
                if pipeline_registers["d"][instruction_index][3] in special_registers["labels"].keys():
                    special_registers["PC"] = special_registers["labels"][pipeline_registers["d"][instruction_index][3]]
                    pipeline_registers["b"] = 1
                else:
                    raise Exception(f"Label not found: {pipeline_registers["d"][3]}")
            else:
                pipeline_registers["b"] = -1
        case "BNE":
            if pipeline_registers["d"][instruction_index][1] != pipeline_registers["d"][instruction_index][2]:
                if pipeline_registers["d"][instruction_index][3] in special_registers["labels"].keys():
                    special_registers["PC"] = special_registers["labels"][pipeline_registers["d"][instruction_index][3]]
                    pipeline_registers["b"] = 1
                else:
                    raise Exception(f"Label not found: {pipeline_registers["d"][instruction_index][3]}")
            else:
                pipeline_registers["b"] = -1
        case "JR":
            special_registers["PC"] = pipeline_registers["d"][instruction_index][1]
            pipeline_registers["b"] = 1
    pipeline_registers["f"][instruction_index] = 0
    special_registers["exec_instructions"] += 1

def load_store_unit(instruction_index):
    # Store an array with [destination, value] into the load/store pipeline register. These values will be written to their destinations in the writeback function.
    match pipeline_registers["d"][instruction_index][0]:
        case "MOVE" | "LI" | "LA":
            pipeline_registers["ls"] = [pipeline_registers["d"][instruction_index][1], int(pipeline_registers["d"][instruction_index][2])]
        case "LW":
            pipeline_registers["ls"] = [pipeline_registers["d"][instruction_index][1], memory[int(pipeline_registers["d"][instruction_index][2])]]
        case "LO":
            pipeline_registers["ls"] = [pipeline_registers["d"][instruction_index][1], memory[int(pipeline_registers["d"][instruction_index][2])+pipeline_registers["d"][instruction_index][3]]]
        case "SW":
            pipeline_registers["ls"] = [int(pipeline_registers["d"][instruction_index][2]), pipeline_registers["d"][instruction_index][1]]
    pipeline_registers["f"][instruction_index] = 0
    special_registers["exec_instructions"] += 1

def writeback():
    # Check load/store register
    if pipeline_registers["ls"] != 0:
        # Check whether the destination is a register
        if pipeline_registers["ls"][0] in registers.keys():
            registers[pipeline_registers["ls"][0]] = pipeline_registers["ls"][1]
            # reset load/store register
            pipeline_registers["ls"] = 0
        # Next check for a valid memory address
        elif pipeline_registers["ls"][0] >= 0 and pipeline_registers["ls"][0] < 256:
            memory[pipeline_registers["ls"][0]] = pipeline_registers["ls"][1]
            # reset load/store register
            pipeline_registers["ls"] = 0
        # If the destination is neither of these, something has gone awry
        else:
            raise Exception(f"Writeback failed: invalid destination {pipeline_registers["ls"][0]} in {pipeline_registers["ls"]}")
    # Check execution registers
    for i in range(2):
        # Check whether there is something to write back in the execution register
        if pipeline_registers[f"e{i+1}"] != 0:
            # ALU instructions can only have register destinations
            if pipeline_registers[f"e{i+1}"][0] in registers.keys():
                registers[pipeline_registers[f"e{i+1}"][0]] = pipeline_registers[f"e{i+1}"][1]
                # reset execute register
                pipeline_registers[f"e{i+1}"] = 0
            else:
                raise Exception(f"Writeback failed: invalid destination {pipeline_registers[f"e{i}"][0]} in {pipeline_registers[f"e{i}"]}")
    pipeline_registers["d"] = [0,0]
        
def cycle():
    fetch()
    print(f"CYC[{special_registers["CYC"]}]: Tick 1, fetched {pipeline_registers["f"]}")
    # execute states: 0 = ALU, 1 = Branch, 2 = Load/Store
    execute_state = decode()
    print(f"CYC[{special_registers["CYC"]}]: Tick 2, decoded {pipeline_registers["d"]}")
    # send the first decoded instruction to the right execution unit
    print(f"Execution state: {execute_state}")
    match execute_state[0]:
        case 0:
            alu_1()
        case 1:
            branch_unit(0)
        case 2:
            load_store_unit(0)
        case -1:
            pass
        case _:
            raise Exception(f"Execute state {execute_state[0]} unrecognised.")
    # and the second instruction
    match execute_state[1]:
        case 0:
            alu_2()
        case 1:
            branch_unit(1)
        case 2:
            load_store_unit(1)
        case -1:
            pass
        case _:
            raise Exception(f"Execute state {execute_state[1]} unrecognised.")
    print(f"CYC[{special_registers["CYC"]}]: Tick 3, execution registers e1:{pipeline_registers["e1"]}, e2:{pipeline_registers["e2"]}, b:{pipeline_registers["b"]}, ls:{pipeline_registers["ls"]}")
    writeback()
    print(f"CYC[{special_registers["CYC"]}]: Tick 4, writeback complete, registers state {registers}")
    special_registers["CYC"] += 1

def main():
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
    print("\n",program,"\n")
    print("---Starting program---")
    # program loop
    while (special_registers["state"] != 0):
        cycle()
    print("---Finished program---")

main()