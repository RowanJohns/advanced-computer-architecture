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
    "r0": [0,-1], 
    "r1": [0,-1], 
    "r2": [0,-1], 
    "r3": [0,-1], 
    "r4": [0,-1], 
    "r5": [0,-1], 
    "r6": [0,-1], 
    "r7": [0,-1], 
    "r8": [0,-1], 
    "r9": [0,-1], 
    "r10": [0,-1], 
    "r11": [0,-1], 
    "r12": [0,-1], 
    "r13": [0,-1], 
    "r14": [0,-1], 
    "r15": [0,-1]
}

# reservation stations
# Op = opcode
# Qj, Qk = the RS that will produce the relevant source operand (0 if they are in Vj/Vk)
# Vj, Vk = the values of the source operands
# label = the label to jump to (branch buffer only)
# A = memory address (load buffer only)
# Rob = corresponding ROB entry
# Busy = whether this RS is in use
# list at the end is [head, tail] pointers

# reservation station 1
rs1 = [
    {"Op": 0, "Qj": 0, "Qk": 0, "Vj": 0, "Vk": 0, "Rob": -1, "Busy": 0},
    {"Op": 0, "Qj": 0, "Qk": 0, "Vj": 0, "Vk": 0, "Rob": -1, "Busy": 0},
    {"Op": 0, "Qj": 0, "Qk": 0, "Vj": 0, "Vk": 0, "Rob": -1, "Busy": 0},
    {"Op": 0, "Qj": 0, "Qk": 0, "Vj": 0, "Vk": 0, "Rob": -1, "Busy": 0},
    [0,0]
]

# reservation station 2
rs2 = [
    {"Op": 0, "Qj": 0, "Qk": 0, "Vj": 0, "Vk": 0, "Rob": -1, "Busy": 0},
    {"Op": 0, "Qj": 0, "Qk": 0, "Vj": 0, "Vk": 0, "Rob": -1, "Busy": 0},
    {"Op": 0, "Qj": 0, "Qk": 0, "Vj": 0, "Vk": 0, "Rob": -1, "Busy": 0},
    {"Op": 0, "Qj": 0, "Qk": 0, "Vj": 0, "Vk": 0, "Rob": -1, "Busy": 0},
    [0,0]
]

branch_buffer = [
    {"Op": 0, "Qj": 0, "Qk": 0, "Vj": 0, "Vk": 0, "label": 0, "Rob": -1, "Busy": 0},
    {"Op": 0, "Qj": 0, "Qk": 0, "Vj": 0, "Vk": 0, "label": 0, "Rob": -1, "Busy": 0},
    {"Op": 0, "Qj": 0, "Qk": 0, "Vj": 0, "Vk": 0, "label": 0, "Rob": -1, "Busy": 0},
    {"Op": 0, "Qj": 0, "Qk": 0, "Vj": 0, "Vk": 0, "label": 0, "Rob": -1, "Busy": 0},
    [0,0]
]

load_buffer = [
    {"Op": 0, "Qj": 0, "Qk": 0, "Vj": 0, "Vk": 0, "A": 0, "Rob": -1, "Busy": 0},
    {"Op": 0, "Qj": 0, "Qk": 0, "Vj": 0, "Vk": 0, "A": 0, "Rob": -1, "Busy": 0},
    {"Op": 0, "Qj": 0, "Qk": 0, "Vj": 0, "Vk": 0, "A": 0, "Rob": -1, "Busy": 0},
    {"Op": 0, "Qj": 0, "Qk": 0, "Vj": 0, "Vk": 0, "A": 0, "Rob": -1, "Busy": 0},
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
cdb = {"rs1": 0, "rs2": 0, "lb": 0, "rob": 0}

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
    print(f"Final special register values: {special_registers}")

def fetch():
    # check if we have reached the end of the program
    if special_registers["PC"] < len(program):
        # get an instruction from the head of the instruction queue
        instruction = program[special_registers["PC"]].split(" ")
        print(f"Current instruction: {instruction}")
    else:
        return
    # the type of opcode determines which reservation station to use
    op = instruction[0]
    if op in al_instructions:
        reservation_station = rs1
    elif op in fp_instructions:
        reservation_station = rs2
    elif op in b_instructions:
        reservation_station = branch_buffer
    elif op in mem_instructions:
        address_unit(instruction)
        return
    elif op == "HALT":
        # should update ROB or just have program keep running until ROB is clear
        special_registers["state"] = 0
        return
    else:
        special_registers["labels"].update({op:special_registers["PC"]})
        return

    # generic reservation station population
    
    rs_index = reservation_station[4][1] # tail pointer

    if rs_index < 4:
        
        rob_index = rob[8][1] # tail pointer

        # update the register file with the rob entry that will update the destination register
        registers[instruction[1]][1] = rob_index

        # update the rob entry
        rob[rob_index].update({"Op": op, "Dest": instruction[1]})

        # increment the rob tail pointer
        rob[8][1] = rob[8][1] + 1

        # put the values we have so far into the reservation station slot
        reservation_station[rs_index].update({"Op": op, "Busy": 1, "Rob": rob_index})

        # find out whether any source registers are waiting for their value
        for i in range(2,4):

            if instruction[i] in registers.keys():
                # if Qi != -1, it is the rob index where the value will be produced
                if registers[instruction[i]][1] != -1:
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
            elif instruction[i] is int:
                # update Vj, Vk accordingly
                if i == 2:
                    reservation_station[rs_index].update({"Vj": registers[instruction[i]][0]})
                elif i == 3:
                    reservation_station[rs_index].update({"Vk": registers[instruction[i]][0]})

        if op in b_instructions:
            if op == "B":
                reservation_station[rs_index].update({"label": instruction[1]})
            elif op != "JR":
                reservation_station[rs_index].update({"label": instruction[3]})

        # increment PC
        special_registers["PC"] += 1

        # increment the rs tail pointer
        reservation_station[4][1] = reservation_station[4][1] + 1
        print(f"Updated RS: {reservation_station[rs_index]}")
            
def decode_execute():
    # check reservation stations for ready instructions
    for rs in [rs1, rs2]:
        for i in range(rs[4][0], rs[4][1]):
            if rs[i]["Qj"] == 0 and rs[i]["Qk"] == 0 and rs[i]["Busy"] == 1:
                match rs[i]["Op"]:
                    case "MUL" | "DIV":
                        alu_fp(i)
                    case _:
                        alu(i)
    # check load buffer for ready instructions
    for i in range(load_buffer[4][0], load_buffer[4][1]):
        if load_buffer[i]["Qj"] == 0 and load_buffer[i]["Qk"] == 0 and load_buffer[i]["Busy"] == 1:
            memory_unit(i)
    # check branch buffer for ready instructions
    for i in range(branch_buffer[4][0], branch_buffer[4][1]):
        if branch_buffer[i]["Qj"] == 0 and branch_buffer[i]["Qk"] == 0 and branch_buffer[i]["Busy"] == 1:
            branch_unit(i)


# add, sub and logical calculations
def alu(index):
    match (rs1[index]["Op"]):
        # Send an array with [value, tag] onto the CDB. These values will be written to their destinations in the writeback function.
        case "ADD":
            cdb["rs1"] = [int(rs1[index]["Vj"]) + int(rs1[index]["Vk"]), index]
        case "ADDI":
            cdb["rs1"] = [registers[int(rs1[index]["Vj"])] + int(rs1[index]["Vk"]), index]
        case "SUB":
            cdb["rs1"] = [int(rs1[index]["Vj"]) - int(rs1[index]["Vk"]), index]
        case "SUBI":
            cdb["rs1"] = [registers[int(rs1[index]["Vj"])] - int(rs1[index]["Vk"]), index]
        case "NOT":
            cdb["rs1"] = [~int(rs1[index]["Vk"]), index]
        case "AND":
            cdb["rs1"] = [int(rs1[index]["Vj"]) & int(rs1[index]["Vk"]), index]
        case "OR":
            cdb["rs1"] = [int(rs1[index]["Vj"]) | int(rs1[index]["Vk"]), index]
        case "XOR":
            cdb["rs1"] = [int(rs1[index]["Vj"]) ^ int(rs1[index]["Vk"]), index]
        case "EQU":
            cdb["rs1"] = [int(rs1[index]["Vj"]) == int(rs1[index]["Vk"]), index]
        case "NEQ":
            cdb["rs1"] = [int(rs1[index]["Vj"]) != int(rs1[index]["Vk"]), index]
        case "GTE":
            cdb["rs1"] = [int(rs1[index]["Vj"]) >= int(rs1[index]["Vk"]), index]
        case "GTH":
            cdb["rs1"] = [int(rs1[index]["Vj"]) > int(rs1[index]["Vk"]), index]
        case "LTE":
            cdb["rs1"] = [int(rs1[index]["Vj"]) <= int(rs1[index]["Vk"]), index]
        case "LTH":
            cdb["rs1"] = [int(rs1[index]["Vj"]) < int(rs1[index]["Vk"]), index]
    del rs1[index]
    rs1.insert(3, {"Op": 0, "Qj": 0, "Qk": 0, "Vj": 0, "Vk": 0, "Rob": -1, "Busy": 0})
    rs1[4][1] -= 1

# mul and div calculations
def alu_fp(index):
    match (rs1[index]["Op"]):
        # Send an array with [value, tag] onto the CDB. These values will be written to their destinations in the writeback function.
        case "MUL":
            cdb["rs2"] = [int(rs1[index]["Vj"]) * int(rs1[index]["Vk"]), index]
        case "DIV":
            cdb["rs2"] = [int(rs1[index]["Vj"]) / int(rs1[index]["Vk"]), index]
    del rs2[index]
    rs2.insert(3, {"Op": 0, "Qj": 0, "Qk": 0, "Vj": 0, "Vk": 0, "Rob": -1, "Busy": 0})
    rs2[4][1] -= 1

def branch_unit(index):
    # For branches, we do nothing in the writeback stage so we don't need to store destination and result
    # TODO: Store -1 for any untaken branches and 1 for a taken branch
    if branch_buffer[index]["label"] not in special_registers["labels"].keys():
        raise Exception(f"Label not found: {branch_buffer[index]["label"]}")
    
    match branch_buffer[index]["Op"]:
        case "B":
            special_registers["PC"] = special_registers["labels"][branch_buffer[index]["Vj"]]
        case "BEQ":
            if branch_buffer[index]["Vk"] == branch_buffer[index]["Vj"]:
                special_registers["PC"] = special_registers["labels"][branch_buffer[index]["label"]]
        case "BGE":
            if branch_buffer[index]["Vk"] >= branch_buffer[index]["Vj"]:
                special_registers["PC"] = special_registers["labels"][branch_buffer[index]["label"]]
        case "BGT":
            if branch_buffer[index]["Vk"] > branch_buffer[index]["Vj"]:
                special_registers["PC"] = special_registers["labels"][branch_buffer[index]["label"]]
        case "BLE":
            if branch_buffer[index]["Vk"] <= branch_buffer[index]["Vj"]:
                special_registers["PC"] = special_registers["labels"][branch_buffer[index]["label"]]
        case "BLT":
            if branch_buffer[index]["Vk"] < branch_buffer[index]["Vj"]:
                special_registers["PC"] = special_registers["labels"][branch_buffer[index]["label"]]
        case "BNE":
            if branch_buffer[index]["Vk"] != branch_buffer[index]["Vj"]:
                special_registers["PC"] = special_registers["labels"][branch_buffer[index]["label"]]
        case "JR":
            special_registers["PC"] = branch_buffer[index]["Vk"]

def address_unit(instruction):
    # loads are sent to the load buffer and stores are sent to the ROB only
    rob_index = rob[8][0]
    lb_index = load_buffer[4][0]
    op = instruction[0]
    match op:
        case "SW":
            # send the store to the ROB to deal with during writeback
            rob[rob_index].update({"Op": "SW", "Dest": instruction[1], "Value": instruction[2]})
        case _:
            # update the ROB
            rob[rob_index].update({"Op": op, "Dest": instruction[1]})

            # update the register file + rs ROB field
            registers[instruction[1]][1] = rob_index

            # update the load buffer
            load_buffer[lb_index].update({"Op": op, "Busy": 1, "Rob": rob_index})
            if op == "LA" or op == "LW":
                load_buffer[lb_index].update({"A": instruction[2]})
            elif op == "LI":
                # update Vj, Vk accordingly
                load_buffer[lb_index].update({"Vj": int(instruction[2])})

            # find out whether any source registers are waiting for their value
            if instruction[2] in registers.keys():
                # if Qi != -1, it is the rob index where the value will be produced
                if registers[instruction[1]][1] != -1:
                    # update Qj accordingly
                    load_buffer[lb_index].update({"Qj": registers[instruction[2]][1]})
                
                # if Qi is 0, we can safely use the value in that register
                else:
                    # update Vj accordingly
                    if op == "LO":
                        load_buffer[lb_index].update({"Vj": registers[instruction[2]][0] + instruction[3]})
                    else:
                        load_buffer[lb_index].update({"Vj": registers[instruction[2]][0]})
            
            # increment PC
            special_registers["PC"] += 1

    rob[8][1] = rob[8][1] + 1
    if load_buffer[4][1] < 3:
        load_buffer[4][1] = load_buffer[4][1] + 1
    print(f"Updated LB: {load_buffer[lb_index]}")
    print(rob)
    return

def memory_unit(index):
    # Send an array with [value, destination] onto the CDB. These values will be written to their destinations in the writeback function.
    cdb["lb"] = [load_buffer[index]["Vj"], load_buffer[index]["Rob"]]
    del load_buffer[index]
    load_buffer.insert(3, {"Op": 0, "Qj": 0, "Qk": 0, "Vj": 0, "Vk": 0, "A": 0, "Rob": -1, "Busy": 0})
    load_buffer[4][1] -= 1
    

def writeback():
    print(f"CDB: {cdb}")
    # Check each cdb entry and update reservation stations
    for key in cdb.keys():
        match key:
            case "rob":
                if cdb["rob"] != 0:
                    # is the value a register address?
                    if cdb["rob"][0] in registers.keys():
                        # if the register has no ROB index attatched to it, the value is ready to use
                        if registers[cdb["rob"][0]][1] == -1:
                            # put the register value into the ROB value field
                            rob[cdb["rob"][1]]["Value"] = registers[cdb["rob"][0]][0]
                    # if not, it is just a value
                    else:
                        rob[cdb["rob"][1]]["Value"] = cdb["rob"][0]
                    rob[cdb["rob"][1]]["Ready"] = 1
                    cdb["rob"] = 0
            case _:
                if cdb[key] != 0:
                    rob[cdb[key][1]]["Value"] = cdb[key][0]
                    rob[cdb[key][1]]["Ready"] = 1
                    cdb[key] = 0
    # store head ROB value if ready
    print(f"ROB: {rob}")
    head = rob[8][0]
    if rob[head]["Ready"] == 1:
        if rob[head]["Dest"] in registers.keys():
            value = [rob[head]["Value"], -1]
            # check if the register has another ROB entry attatched to it
            for i in range(rob[8][0]+1,rob[8][1]):
                if rob[i]["Dest"] == rob[head]["Dest"]:
                    value[1] = i
                    break
            registers[rob[head]["Dest"]] = value
        # clear rob entry
        del rob[0]
        rob.insert(7, {"Op": 0, "Dest": 0, "Value": 0, "Ready": 0})
        rob[8][1] -= 1
        special_registers["exec_instructions"] += 1
        print(f"Writeback done, ROB: {rob}")


def cycle():
    fetch()
    print(f"CYC[{special_registers["CYC"]}]: Tick 1, fetch complete")
    decode_execute()
    print(f"CYC[{special_registers["CYC"]}]: Tick 2, decode complete")
    print(f"CYC[{special_registers["CYC"]}]: Tick 3, execution complete")
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
    while (special_registers["CYC"] < 5):
        cycle()
    print("---Finished program---")

main()