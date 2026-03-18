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

# groups of instructions (for pattern matching)
instructions = ["ADD", "ADDI", "SUB", "SUBI", "MUL", "DIV", "NOT", "AND", "OR", "XOR", "EQU", "NEQ", "GTE", "GTH", "LTE", "LTH", "MOVE", "LI", "LA", "LW", "LO", "SW", "B", "BEQ", "BGE", "BGT", "BLE", "BLT", "BNE", "JR", "HALT"]
al_instructions = ["ADD", "ADDI", "SUB", "SUBI", "MUL", "DIV", "NOT", "AND", "OR", "XOR", "EQU", "NEQ", "GTE", "GTH", "LTE", "LTH"]
fp_instructions = ["MUL", "DIV"]
b_instructions = ["B", "BEQ", "BGE", "BGT", "BLE", "BLT", "BNE", "JR"]
mem_instructions = ["MOVE", "LI", "LA", "LW", "LO", "SW"]

# general purpose registers
# layout: {"register name": [value, rob_index]}
registers = {
    "r0": [0,4], 
    "r1": [0,4], 
    "r2": [0,4], 
    "r3": [0,4], 
    "r4": [0,4], 
    "r5": [0,4], 
    "r6": [0,4], 
    "r7": [0,4], 
    "r8": [0,4], 
    "r9": [0,4], 
    "r10": [0,4], 
    "r11": [0,4], 
    "r12": [0,4], 
    "r13": [0,4], 
    "r14": [0,4], 
    "r15": [0,4]
}

# reservation stations
# Op = opcode
# Qj, Qk = the RS that will produce the relevant source operand (0 if they are in Vj/Vk)
# Vj, Vk = the values of the source operands
# A = memory address (load/store buffers only)
# Busy = whether this RS is in use
# list at the end is [head, tail] pointers

# reservation station 1
rs1 = [
    {"Op": 0, "Qj": 0, "Qk": 0, "Vj": 0, "Vk": 0, "Busy": 0},
    {"Op": 0, "Qj": 0, "Qk": 0, "Vj": 0, "Vk": 0, "Busy": 0},
    {"Op": 0, "Qj": 0, "Qk": 0, "Vj": 0, "Vk": 0, "Busy": 0},
    {"Op": 0, "Qj": 0, "Qk": 0, "Vj": 0, "Vk": 0, "Busy": 0},
    [0,0]
]

# reservation station 2
rs2 = [
    {"Op": 0, "Qj": 0, "Qk": 0, "Vj": 0, "Vk": 0, "Busy": 0},
    {"Op": 0, "Qj": 0, "Qk": 0, "Vj": 0, "Vk": 0, "Busy": 0},
    {"Op": 0, "Qj": 0, "Qk": 0, "Vj": 0, "Vk": 0, "Busy": 0},
    {"Op": 0, "Qj": 0, "Qk": 0, "Vj": 0, "Vk": 0, "Busy": 0},
    [0,0]
]

branch_buffer = [
    {"Op": 0, "Qj": 0, "Qk": 0, "Vj": 0, "Vk": 0, "Busy": 0},
    {"Op": 0, "Qj": 0, "Qk": 0, "Vj": 0, "Vk": 0, "Busy": 0},
    {"Op": 0, "Qj": 0, "Qk": 0, "Vj": 0, "Vk": 0, "Busy": 0},
    {"Op": 0, "Qj": 0, "Qk": 0, "Vj": 0, "Vk": 0, "Busy": 0},
    [0,0]
]

load_buffer = [
    {"Op": 0, "Qj": 0, "Qk": 0, "Vj": 0, "Vk": 0, "A": 0, "Busy": 0},
    {"Op": 0, "Qj": 0, "Qk": 0, "Vj": 0, "Vk": 0, "A": 0, "Busy": 0},
    {"Op": 0, "Qj": 0, "Qk": 0, "Vj": 0, "Vk": 0, "A": 0, "Busy": 0},
    {"Op": 0, "Qj": 0, "Qk": 0, "Vj": 0, "Vk": 0, "A": 0, "Busy": 0},
    [0,0]
]

# re-order buffer
rob = [
    {"Op": 0, "Dest": 0, "Value": 0, "Ready": 0},
    {"Op": 0, "Dest": 0, "Value": 0, "Ready": 0},
    {"Op": 0, "Dest": 0, "Value": 0, "Ready": 0},
    {"Op": 0, "Dest": 0, "Value": 0, "Ready": 0},
    {"Op": 0, "Dest": 0, "Value": 0, "Ready": 0},
    {"Op": 0, "Dest": 0, "Value": 0, "Ready": 0},
    {"Op": 0, "Dest": 0, "Value": 0, "Ready": 0},
    {"Op": 0, "Dest": 0, "Value": 0, "Ready": 0},
    [0,0]
]

# common data bus
# each entry will have a value and destination tag [val, tag]
cdb = {"rs1": 0, "rs2": 0, "lb": 0, "sb": 0}

# special purpose registers
# PC = program counter, int
# CYC = current cycle, int
# labels = {label:PC}, dict
# state = program state, int
# exec_instructions = total instructions executed, int
special_registers = {
    "PC": 0,
    "CYC": 0,
    "labels": {},
    "state": 1,
    "exec_instructions": 0
}

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
    # print(f"Final pipeline register values: {pipeline_registers}")
    print(f"Final special register values: {special_registers}")

def fetch():
    # fetch 2 instructions into the reservation stations per cycle
    for i in range(2):
        # check if we have reached the end of the program
        if special_registers["PC"] < len(program):
            # get an instruction from the head of the instruction queue
            instruction = program[special_registers["PC"]].split(" ")
        else:
            return
    # the type of opcode determines which reservation station to use
    op = instruction[0]
    if op in al_instructions:
        reservation_station = rs1
    elif op in fp_instructions:
        reservation_station = rs2
    elif op in b_instructions:
        # TODO: think about how branches can be dealt with out of order (add delay)
        reservation_station = branch_buffer
    elif op in mem_instructions:
        address_unit(instruction)
        return
    elif op == "HALT":
        special_registers["state"] = 0
        return
    else:
        special_registers["labels"].update({op:special_registers["PC"]})
        return

    # generic reservation station population

    # find a slot that is free
    if 0 in [rs["Busy"] for rs in reservation_station]:

        rob_index = rob[8][1] # tail pointer
        rs_index = reservation_station[4][1] # tail pointer

        # update the register file with the rob entry that will update the destination register
        registers[instruction[1]][1] = rob_index

        # update the rob entry
        rob[rob_index].update({"Op": op, "Dest": registers[instruction[1]][1]})

        # increment the rob tail pointer
        rob[8][1] = rob[8][1] + 1

        # put the values we have so far into the reservation station slot
        reservation_station[rs_index].update({"Op": op, "Busy": 1})

        # find out whether any source registers are waiting for their value
        for i in range(2,4):

            if instruction[i] in registers.keys():
                # if Qi < 8, it is the rob index where the value will be produced
                if registers[instruction[i]][1] < 8:
                    # update Qj, Qk accordingly
                    if i == 2:
                        reservation_station[rs_index].update({"Qj": registers[instruction[i]][1]})
                    elif i == 3:
                        reservation_station[rs_index].update({"Qk": registers[instruction[i]][1]})
                
                # if Qi is 0, we can safely use the value in that register
                else:
                    # update Vj, Vk accordingly
                    if i == 2:
                        reservation_station[rs_index].update({"Vj": registers[instruction[i]][0]})
                    elif i == 3:
                        reservation_station[rs_index].update({"Vk": registers[instruction[i]][0]})

        # increment the rs tail pointer
        reservation_station[4][1] = reservation_station[4][1] + 1
            
def decode():
    # TODO: rewrite this!!
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

# add, sub and logical calculations
def alu():
    # TODO: remove pipeline register dependence here
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

# mul and div calculations
def alu_fp():
    # TODO: remove pipeline register dependence here
    match (pipeline_registers["d"][1][0]):
        # Store an array with [destination, value] into the execute pipeline register. These values will be written to their destinations in the writeback function.
        case "MUL":
            pipeline_registers["e2"] = [pipeline_registers["d"][1][1], int(pipeline_registers["d"][1][2]) * int(pipeline_registers["d"][3])]
        case "DIV":
            pipeline_registers["e2"] = [pipeline_registers["d"][1][1], int(pipeline_registers["d"][1][2]) / int(pipeline_registers["d"][3])]
    pipeline_registers["f"][1] = 0
    special_registers["exec_instructions"] += 1

def branch_unit(instruction_index):
    # TODO: remove pipeline register dependence here
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

def address_unit(instruction):
    # loads are sent to the load buffer and stores are sent to the ROB only
    rob_index = rob[8][1]
    lb_index = load_buffer[4][1]
    op = instruction[0]
    match op:
        case "SW":
            # send the store to the ROB to deal with during writeback
            rob[rob_index].update({"Op": "SW", "Dest": instruction[1], "Value": instruction[2]})
        case _:
            # update the ROB
            rob[rob_index].update({"Op": op, "Dest": instruction[1]})

            # update the register file
            registers[instruction[1]][1] = rob_index

            # update the load buffer
            load_buffer[lb_index].update({"Op": op, "Busy": 1})
            if op == "LA" or op == "LW":
                load_buffer[lb_index].update({"A": instruction[2]})

            # find out whether any source registers are waiting for their value
            if instruction[2] in registers.keys():
                # if Qi < 8, it is the rob index where the value will be produced
                if registers[instruction[i]][1] < 8:
                    # update Qj accordingly
                    load_buffer[lb_index].update({"Qj": registers[instruction[2]][1]})
                
                # if Qi is 0, we can safely use the value in that register
                else:
                    # update Vj accordingly
                    if op == "LO":
                        load_buffer[lb_index].update({"Vj": registers[instruction[2]][0] + instruction[3]})
                    else:
                        load_buffer[lb_index].update({"Vj": registers[instruction[2]][0]})

    rob[8][1] = rob[8][1] + 1
    load_buffer[4][1] = load_buffer[4][1] + 1
    return

def memory_unit(instruction_index):
    # TODO: remove pipeline register dependence here
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
    # TODO: when the ROB has a register in the value field, replace it with the value only when that register doesn't have a ROB index attatched to it
    # TODO: for LO, make sure to add imm when writing back to load buf
    # TODO: remove pipeline register dependence here, implement CDB
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
    # TODO: match this with tomasulo flow chart
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