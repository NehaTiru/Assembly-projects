import sys

# Dictionary for the different opcodes
# Each opcode is represented as a binary value and mapped to its corresponding instruction mnemonic
opcodes = {
    0b10001011000: "ADD",
    0b1001000100: "ADDI",
    0b10001010000: "AND",
    0b1001001000: "ANDI",
    0b000101: "B",
    0b01010100: "B.",
    0b100101: "BL",
    0b11010110000: "BR",
    0b10110101: "CBNZ",
    0b10110100: "CBZ",
    0b11001010000: "EOR",
    0b1101001000: "EORI",
    0b11111000010: "LDUR",
    0b11010011011: "LSL",
    0b11010011010: "LSR",
    0b10101010000: "ORR",
    0b1011001000: "ORRI",
    0b11111000000: "STUR",
    0b11001011000: "SUB",
    0b1101000100: "SUBI",
    0b1111000100: "SUBIS",
    0b11101011000: "SUBS",
    0b10011011000: "MUL",
    0b11111111101: "PRNT",
    0b11111111100: "PRNL",
    0b11111111110: "DUMP",
    0b11111111111: "HALT"
}

# Dictionary for the different conditions
# Each condition is represented as a hexadecimal value and mapped to its corresponding condition code
conditions = {
    0x0: "EQ",
    0x1: "NE",
    0x2: "HS",
    0x3: "LO",
    0x4: "MI",
    0x5: "PL",
    0x6: "VS",
    0x7: "VC",
    0x8: "HI",
    0x9: "LS",
    0xa: "GE",
    0xb: "LT",
    0xc: "GT",
    0xd: "LE"
}

# Variable to keep track of the current instruction count
# Used for generating labels in the disassembled output
instruction_count = 1

def disassemble(instruction):
    """
    Disassembles a single 32-bit instruction.

    Args:
        instruction (int): The 32-bit instruction to disassemble.

    Returns:
        None
    """
    global instruction_count
    
    # Initializing the string that will contain the disassembled instruction
    instruction_string = ""

    # ---------------------------------- Get Opcodes ---------------------------------------------

# Extract the different opcodes from the instruction
    R_D_opcode = (instruction >> 21) & 0x7FF  # Extract the 11-bit R/D-type opcode

    I_opcode = (instruction >> 22) & 0x3FF # Extract the 10-bit I-type opcode

    CB_opcode = (instruction >> 24) & 0xFF # Extract the 8-bit CB-type opcode

    B_opcode = (instruction >> 26) & 0x3F # Extract the 6-bit B-type opcode

    # ---------------------------------- R and D type instructions  -------------------------------------
    # Check the type of instruction based on the opcode
    if R_D_opcode in opcodes:
        instruction_string += opcodes[R_D_opcode]

        # If the instruction is ADD, AND, EOR, ORR, SUB, SUBS, MUL
        if (R_D_opcode == 0b10001011000) or (R_D_opcode == 0b10001010000) or (R_D_opcode == 0b11001010000) or \
                (R_D_opcode == 0b10101010000) or (R_D_opcode == 0b11001011000) or (R_D_opcode == 0b11101011000) or \
                (R_D_opcode == 0b10011011000):

            Rd = instruction & 0x1F
            RdString = "X" + str(Rd)
            if Rd == 28:
                RdString = "SP"
            elif Rd == 29:
                RdString = "FP"
            elif Rd == 30:
                RdString = "LR"
            elif Rd == 31:
                RdString = "XZR"


            Rn = instruction >> 5 & 0x1F
            RnString = "X" + str(Rn)
            if Rn == 28:
                RnString = "SP"
            elif Rn == 29:
                RnString = "FP"
            elif Rn == 30:
                RnString = "LR"
            elif Rn == 31:
                RnString = "XZR"

            Rm = instruction >> 16 & 0x1F
            RmString = "X" + str(Rm)
            if Rm == 28:
                RmString = "SP"
            elif Rm == 29:
                RmString = "FP"
            elif Rm == 30:
                RmString = "LR"
            elif Rm == 31:
                RmString = "XZR"

            instruction_string += " " + RdString + ", " + RnString + ", " + RmString

        # If the instruction is BR
        elif R_D_opcode == 0b11010110000:

            Rn = instruction >> 5 & 0x1F
            RnString = "X" + str(Rn)
            if Rn == 28:
                RnString = "SP"
            elif Rn == 29:
                RnString = "FP"
            elif Rn == 30:
                RnString = "LR"
            elif Rn == 31:
                RnString = "XZR"

            instruction_string += " " + RnString

        # If the instruction is LSL, LSR
        elif (R_D_opcode == 0b11010011011) or (R_D_opcode == 0b11010011010):

            Rd = instruction & 0x1F
            RdString = "X" + str(Rd)
            if Rd == 28:
                RdString = "SP"
            elif Rd == 29:
                RdString = "FP"
            elif Rd == 30:
                RdString = "LR"
            elif Rd == 31:
                RdString = "XZR"


            Rn = instruction >> 5 & 0x1F
            RnString = "X" + str(Rn)
            if Rn == 28:
                RnString = "SP"
            elif Rn == 29:
                RnString = "FP"
            elif Rn == 30:
                RnString = "LR"
            elif Rn == 31:
                RnString = "XZR"

            shamt = instruction >> 10 & 0x3F
            # Number is negative (but disassembler won't treat it like one)
            if shamt >= 32:
                # Actually make it negative
                shamt -= 64

            instruction_string += " " + RdString + ", " + RnString + ", #" + str(shamt)

        # If the instruction is PRNT
        elif R_D_opcode == 0b11111111101:

            Rd = instruction & 0x1F
            RdString = "X" + str(Rd)
            if Rd == 28:
                RdString = "SP"
            elif Rd == 29:
                RdString = "FP"
            elif Rd == 30:
                RdString = "LR"
            elif Rd == 31:
                RdString = "XZR"

            instruction_string += " " + RdString

        # If the instruction is LDUR, STUR
        elif (R_D_opcode == 0b11111000010) or (R_D_opcode == 0b11111000000):

            Rt = instruction & 0x1F
            RtString = "X" + str(Rt)
            if Rt == 28:
                RtString = "SP"
            elif Rt == 29:
                RtString = "FP"
            elif Rt == 30:
                RtString = "LR"
            elif Rt == 31:
                RtString = "XZR"


            Rn = instruction >> 5 & 0x1F
            RnString = "X" + str(Rn)
            if Rn == 28:
                RnString = "SP"
            elif Rn == 29:
                RnString = "FP"
            elif Rn == 30:
                RnString = "LR"
            elif Rn == 31:
                RnString = "XZR"


            DTAddr = instruction >> 12 & 0x1FF
            # Number is negative
            if DTAddr >= 256:
                #make it negative
                DTAddr -= 512

            instruction_string += " " + RtString + ", [" + RnString + ", #" + str(DTAddr) + "]"

        else:
            # Nothing, just the instruction name
            pass

    # ------------------------------------- I type instructions  ----------------------------------------

    elif I_opcode in opcodes:
        instruction_string += opcodes[I_opcode]


        Rd = instruction & 0x1F
        RdString = "X" + str(Rd)
        if Rd == 28:
            RdString = "SP"
        elif Rd == 29:
            RdString = "FP"
        elif Rd == 30:
            RdString = "LR"
        elif Rd == 31:
            RdString = "XZR"

        Rn = instruction >> 5 & 0x1F
        RnString = "X" + str(Rn)
        if Rn == 28:
            RnString = "SP"
        elif Rn == 29:
            RnString = "FP"
        elif Rn == 30:
            RnString = "LR"
        elif Rn == 31:
            RnString = "XZR"

        ALUImm = instruction >> 10 & 0xFFF
        # Number is negative
        if ALUImm >= 2048:
            # make it negative
            ALUImm -= 4096

        instruction_string += " " + RdString + ", " + RnString + ", #" + str(ALUImm)

    # ------------------------------------- CB type instructions  ----------------------------------------

    elif CB_opcode in opcodes:
        instruction_string += opcodes[CB_opcode]

        # If the instruction is B.
        if CB_opcode == 0b01010100:

            cond = instruction & 0x1F
            condString = conditions[cond]
            instruction_string += condString


        BranchAddr = instruction >> 5 & 0x7FFFF
        # Number is negative 
        if BranchAddr >= 262144:
            # make it negative
            BranchAddr -= 524288

        instruction_string += " L" + str(instruction_count + BranchAddr)

# ------------------------------------- B type instructions  ----------------------------------------

    elif B_opcode in opcodes:

        BranchAddr = instruction & 0x3FFFFFF
        # Number is negative 
        if BranchAddr >= 33554432:
            # make it negative
            BranchAddr -= 67108864

        instruction_string += opcodes[B_opcode] + " L" + str(instruction_count + BranchAddr)

    # ------------------------------------ Instruction not found  --------------------------------------

    else:
        print("Opcode not found --> Error within program! Please check...")

    # -------------------------------- Print the Instruction ------------------------------------

    print("L" + str(instruction_count) + ": " + instruction_string)
    instruction_count += 1

def main():
    print("COMS 321 Programming Assignment 2\n")
    """
    The main function of the disassembler.

    Reads a binary file containing LEGv8 instructions and disassembles each instruction.

    Returns:
        None
    """
    if len(sys.argv) < 2:
        print("Usage: python PA2.py <test_file_name>")
        sys.exit(1)
    # Read 4 bytes from a file and construct the binary instruction
    try:
        # Open the binary file specified as a command-line argument
        with open(sys.argv[1], "rb") as instructions_file:
            while True:
                # Read 4 bytes (32 bits) at a time
                instruction_bytes = instructions_file.read(4)
                if len(instruction_bytes) < 4:
                    break
                # Construct the 32-bit instruction from the 4 bytes
                first_byte = instruction_bytes[0] & 0xFF
                first_byte_int = first_byte << 24

                second_byte = instruction_bytes[1] & 0xFF
                second_byte_int = second_byte << 16

                third_byte = instruction_bytes[2] & 0xFF
                third_byte_int = third_byte << 8
                fourth_byte = instruction_bytes[3] & 0xFF

                # [instruction] = [firstByte] + [secondByte] + [thirdByte] + [fourthByte]
                instruction = first_byte_int + second_byte_int + third_byte_int + fourth_byte
# Disassemble the instruction
                disassemble(instruction)

    except IOError as error:
        print(error)

if __name__ == "__main__":
    main()