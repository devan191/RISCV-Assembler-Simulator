from constants import *
from helpers import *
from errors import *
import sys

try:
    input_filename = "input.txt"
    output_filename = "output.txt"
    outputfile = open(output_filename,'w+')
    #create a cool webpage for displaying results and ofc taking in input
    with open(input_filename, 'r') as inputfile:
        # creating a list of all lines in input txt file, each element in lines is a line
        lines_unrefined = inputfile.readlines() 
        # lines excludes all new line characters and empty lines
        lines = [line.strip() for line in lines_unrefined]
        non_empty_lines = [line for line in lines if line != '']
        
    line_no = 0
    PrgC = 0 # Program Counter
    PrgCMax = 4*(len(non_empty_lines) -1)
    check_pmem_exceeded(PrgCMax)

    labels_dict = {} 
    #empty dict for storing label:PC values here (Note PC has hex range from 00 to ff i.e 0 to 255 bytes each instruction consuming 4 bytes)

    # no label
    def R_type_encoder(token_1):
       
        op_code = '0110011'
        op_name = token_1[0]
        func3 = func3_dict[op_name]
        token_2 = token_1[1].split(",")
        check_valid_token_len(token_2,3,line_no)
        for reg in token_2:
            check_reg_error(reg,line_no)

        rd = registers_dict[token_2[0]]
        rs1 = registers_dict[token_2[1]]
        rs2 = registers_dict[token_2[2]]

        if op_name == 'sub':
            func7 = '0100000'
        else:
            func7 = '0000000'

        binstr = func7 + rs2 + rs1 + func3 + rd + op_code + '\n'
        outputfile.write(binstr)

    def I_type_encoder(token_1):

        op_name = token_1[0]
        if op_name == 'lw':
            op_code = '0000011'
        elif op_name == 'addi':
            op_code = '0010011'
        elif op_name == 'sltiu':
            op_code = '0010011'
        else:
            op_code = '1100111'
        func3 = func3_dict[op_name]

        token_2 = token_1[1].split(",") #token_2[0] has rd
        rd = token_2[0]
        check_I_type_token(token_2,line_no)
        if len(token_2) == 2:
            token_3 = token_2[1].split("(") #token_3[0] has imm[11:0] in decimal
            if token_3[0] == '':
                print('Syntax error on line',line_no)
                sys.exit()
            valid_imm(token_3[0],line_no)
            token_4 = token_3[1]          #token_4 has rs1)
            token_4 = token_4[:-1]        #token_4 has rs1
            rs1 = token_4
            imm = bin_ext_converter(int(token_3[0]),12,line_no)

        else:
            rs1 = token_2[1]
            valid_imm(token_2[2],line_no)
            imm = bin_ext_converter(int(token_2[2]),12,line_no)

        check_reg_error(rd,line_no)
        check_reg_error(rs1,line_no)
        rd = registers_dict[rd]
        rs1 = registers_dict[rs1]

        binstr = imm + rs1 + func3 + rd + op_code + "\n"
        outputfile.write(binstr)

    # no label
    def S_type_encoder(token_1):
       
        op_code = '0100011'

        op_name = token_1[0]
        func3 = func3_dict[op_name]
        token_2 = token_1[1].split(",") #token_2[0] has rs2

        if len(token_2) != 2:
            print("Syntax error on line",line_no)
            sys.exit()
        if (len(token_2) == 2) and ('' in token_2):
            print('Syntax error on line',line_no)
            sys.exit()
        token_3 = token_2[1].split("(") #token_3[0] has imm[11:0] in decimal
        if token_3[0] == '':
            print("Syntax error on line",line_no)
            sys.exit()

        valid_imm(token_3[0],line_no)
        token_4 = token_3[1]          #token_4 has rs1)
        token_4 = token_4[:-1]        #token_4 has rs1
        rs1 = token_4
        rs2 = token_2[0]
        check_reg_error(rs2,line_no)
        check_reg_error(rs1,line_no)
        rs2 = registers_dict[rs2]
        rs1 = registers_dict[rs1]
        imm = bin_ext_converter(int(token_3[0]),12,line_no)
        imm1 = imm[:-5]
        imm0 = imm[-5:]

        binstr = imm1 + rs2 + rs1+ func3 + imm0 + op_code + '\n'
        outputfile.write(binstr)

    # label
    def B_type_encoder(token_1):
       
        op_code = '1100011'

        op_name = token_1[0]
        func3 = func3_dict[op_name]

        token_2 = token_1[1].split(",") 
        check_valid_token_len(token_2,3,line_no)
        rs1 = token_2[0]
        rs2 = token_2[1]
        check_reg_error(rs1,line_no)
        check_reg_error(rs2,line_no)
        label = token_2[2]
        # if label is given
        if label in labels_dict:
            
            imm = labels_dict[label] - PrgC #doing absolute addr - current addr
            imm = bin_ext_converter(imm,13,line_no)
            imm1 = imm[0] + imm[2:8]
            imm0 = imm[-5:-1] + imm[1]
        #if direct imm given in decimal
        else:
            valid_imm(label,line_no)
            imm = int(label)
            imm = bin_ext_converter(imm,13,line_no)
            imm1 = imm[0] + imm[2:8]
            imm0 = imm[-5:-1] + imm[1]
        
        rs1 = registers_dict[rs1]
        rs2 = registers_dict[rs2]

        binstr = imm1 + rs2 + rs1+ func3 + imm0 + op_code + '\n'
        outputfile.write(binstr)

    #no label
    def U_type_encoder(token_1):
     
        op_name = token_1[0]
        token_2 = token_1[1].split(",")
        check_valid_token_len(token_2,2,line_no)
        rd = token_2[0]
        check_reg_error(rd,line_no)
        rd = registers_dict[rd]
        valid_imm(token_2[1],line_no)
        imm = int(token_2[1])
        imm = bin_ext_converter(imm,32,line_no)
        imm = imm[0:20]
        if op_name == 'lui':
            op_code = '0110111'
        else:
            op_code = '0010111'
        
        binstr = imm + rd + op_code + '\n'
        outputfile.write(binstr)

    #label
    def J_type_encoder(token_1):
        
        op_code = '1101111'
        op_name = token_1[0]
        token_2 = token_1[1].split(",")
        check_valid_token_len(token_2,2,line_no)
        rd = token_2[0]
        check_reg_error(rd,line_no)
        rd = registers_dict[rd]
        label = token_2[1]

        # if label is given
        if label in labels_dict:
            imm = labels_dict[label] - PrgC #doing absolute addr - current addr
            imm = bin_ext_converter(imm,21,line_no)
            imm = imm[0] + imm[-11:-1] + imm[9] + imm[1:9]

        #if direct imm given in decimal
        else:
            valid_imm(label,line_no)
            imm = int(label)
            imm = bin_ext_converter(imm,21,line_no)
            imm = imm[0] + imm[-11:-1] + imm[9] + imm[1:9]

        binstr = imm + rd + op_code + '\n'
        outputfile.write(binstr)

        
    def Label_type_encoder(opname,token_1):
        
        token_1.remove(opname)
        new_line = " ".join(token_1)
        instr_identifier(new_line)


    def instr_identifier(line):
        
        token_1 = line.split() #token_1 contains tokens split about white spaces
        opname = token_1[0]
        
        if opname[-1] == ":":
            Label_type_encoder(opname,token_1)
        elif opname in R_type_instr:
            R_type_encoder(token_1)
        elif opname in I_type_instr:
            I_type_encoder(token_1)
        elif opname in S_type_instr:
            S_type_encoder(token_1)
        elif opname in B_type_instr:
            B_type_encoder(token_1)
        elif opname in U_type_instr:
            U_type_encoder(token_1)
        elif opname in J_type_instr:
            J_type_encoder(token_1)
        else:
            print("Syntax error on line",line_no,"\n","Unknown operation name!")
            sys.exit()

    #collecting all labels first
    for i in range(len(lines)):
        line_no += 1
        line = lines[i]
        if(line == ''):
            continue
        token_1 = line.split()
        opname = token_1[0]
        label = opname[0:-1]
        check_label_syntax_error(token_1,line_no,opname)
        check_label_redef_error(label,line_no,labels_dict)
        if opname[-1] == ':':
            labels_dict.update({label:PrgC})
            
        PrgC += 4

    line_no = 0
    PrgC = 0 # Program Counter
    #iterating through lines of input assembly code
    while(PrgC <= PrgCMax):
        line_no += 1
        line = lines[line_no-1]
        if(line == ''):
            continue
        instr_identifier(line)
        PrgC += 4

    outputfile.close()
except SystemExit:
    # error already printed to stderr, just exit
    sys.exit(1)