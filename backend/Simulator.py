import sys
from simconstants import *
from simhelpers import *
from errors import *

try:
    #have to fix issues when imm/label values go out of memory range - datamem_dict gives key error - check for similar errors

    input_filename = "siminput.txt"
    output_filename = "simoutput.txt"
    outputfile = open(output_filename,'w+')
    with open(input_filename, 'r') as inputfile:
        # creating a list of all lines in input txt file, each element in lines is a line
        lines_unrefined = inputfile.readlines() 
        # lines excludes all new line characters and empty lines
        lines = [line.strip() for line in lines_unrefined]
        non_empty_lines = [line for line in lines if line != '']

    PrgC = 0 # Program Counter
    PrgCMax = 4*(len(non_empty_lines)-1)
    if PrgCMax > 255:
        print_and_exit('Error: Program memory exceeded:no of instr > 64')
        sys.exit()

    stackCounter = 32 #for tracking variables don't exceed stack memory

    def reset_zero():
        reg_data[reg_dict['00000']] = '00000000000000000000000000000000'

    def mem_stat_print():
        outputstr = 'Data Memory stats :-\n\n'
        for i in range(65536,65661,4):
            mem_address= f"0x{i:08x}"
            outputstr += mem_address +": " + str(bin2dec(datamem_dict[i])) +'\n'
     
        outputfile.write(outputstr)
        
    def reg_print():
        global PrgC
        outstr = ''
        prgc_address = f"0x{PrgC:08x}"
        outstr += 'Program Counter:- ' + prgc_address +'\n'+ 'Register values:: [ '
        for reg in reg_data:
            outstr += "{"+ reg + ":" + str(bin2dec(reg_data[reg])) + "} "
        outstr += "]\n\n"

        outputfile.write(outstr)
        
    reg_data = {
        # all data stored in a signed 32 bit binary string
        'zero': '00000000000000000000000000000000', #hard-wired 0
        'ra':   '00000000000000000000000000000000',
        'sp':   '00000000000000000000000100000000', #starts from 256
        'gp':   '00000000000000000000000000000000',
        'tp':   '00000000000000000000000000000000',
        't0':   '00000000000000000000000000000000',
        't1':   '00000000000000000000000000000000',
        't2':   '00000000000000000000000000000000',
        's0':   '00000000000000000000000000000000',
        's1':   '00000000000000000000000000000000',
        'a0':   '00000000000000000000000000000000',
        'a1':   '00000000000000000000000000000000',
        'a2':   '00000000000000000000000000000000',
        'a3':   '00000000000000000000000000000000',
        'a4':   '00000000000000000000000000000000',
        'a5':   '00000000000000000000000000000000',
        'a6':   '00000000000000000000000000000000',
        'a7':   '00000000000000000000000000000000',
        's2':   '00000000000000000000000000000000',
        's3':   '00000000000000000000000000000000',
        's4':   '00000000000000000000000000000000',
        's5':   '00000000000000000000000000000000',
        's6':   '00000000000000000000000000000000',
        's7':   '00000000000000000000000000000000',
        's8':   '00000000000000000000000000000000',
        's9':   '00000000000000000000000000000000',
        's10':  '00000000000000000000000000000000',
        's11':  '00000000000000000000000000000000',
        't3':   '00000000000000000000000000000000',
        't4':   '00000000000000000000000000000000',
        't5':   '00000000000000000000000000000000',
        't6':   '00000000000000000000000000000000',
    }

    datamem_dict = {
        mem_addr: '00000000000000000000000000000000' for mem_addr in range(65536,65661,4)
    }

    def R_type_enc(line):
        global outstr
        global PrgC
        global stackCounter

        func7 = line[0:7]
        rs2 = line[7:12]
        rs1 = line[12:17]
        func3 = line[17:20]
        rd = line[20:25]

        if func3 == '000':
            if func7 == '0000000':
                reg_data[reg_dict[rd]] = add_signed_binary(reg_data[reg_dict[rs1]],reg_data[reg_dict[rs2]])
            elif func7 == '0100000':
                if rs1 == '00000':
                    reg_data[reg_dict[rd]] = twos_comp(reg_data[reg_dict[rs2]])
                else:
                    x = twos_comp(reg_data[reg_dict[rs2]])
                    reg_data[reg_dict[rd]] = add_signed_binary(reg_data[reg_dict[rs1]],x)

        elif func3 == '001':
            y = unsign_bin2dec(reg_data[reg_dict[rs2]][-5:])
            x = bin2dec(reg_data[reg_dict[rs1]])
            z = x << y
            reg_data[reg_dict[rd]] = dec2bin_sext(z,32)
            

        elif func3 == '010':
            a = bin2dec(reg_data[reg_dict[rs1]])
            b = bin2dec(reg_data[reg_dict[rs2]])
            if a < b:
                reg_data[reg_dict[rd]] = dec2bin_sext(1,32)

        elif func3 == '011':
            a = unsign_bin2dec(reg_data[reg_dict[rs1]])
            b = unsign_bin2dec(reg_data[reg_dict[rs2]])
            if a < b:
                reg_data[reg_dict[rd]] = dec2bin_sext(1,32)
        
        elif func3 == '100':
            reg_data[reg_dict[rd]] = ''.join('1' if bit1 != bit2 else '0' for bit1, bit2 in zip(reg_data[reg_dict[rs1]], reg_data[reg_dict[rs2]]))

        elif func3 == '101':
            x = unsign_bin2dec(reg_data[reg_dict[rs2]][-5:])
            z = '0'*x + reg_data[reg_dict[rs1]][0:-x]
            reg_data[reg_dict[rd]] = z

        elif func3 == '110':
            reg_data[reg_dict[rd]] = ''.join('1' if bit1 == '1' or bit2 == '1' else '0' for bit1, bit2 in zip(reg_data[reg_dict[rs1]], reg_data[reg_dict[rs2]]))
        
        elif func3 == '111':
            reg_data[reg_dict[rd]] = ''.join('1' if bit1 == '1' and bit2 == '1' else '0' for bit1, bit2 in zip(reg_data[reg_dict[rs1]], reg_data[reg_dict[rs2]]))
        
        reset_zero()
        reg_print()
        PrgC = PrgC + 4
        
        
    def I_type_enc(line):
        global outstr
        global PrgC
        global stackCounter
        
        imm = line[0:12]
        x = bin2dec(imm)
        rs1 = line[12:17]
        func3 = line[17:20]
        rd = line[20:25]
        opcode = line[25:]

        if func3 == '010':
            reg_data[reg_dict[rd]] = datamem_dict[bin2dec(add_signed_binary(reg_data[reg_dict[rs1]],dec2bin_sext(x,32)))]
            reset_zero()
            reg_print()
            PrgC = PrgC + 4
             
        elif func3 == '011':
            a = unsign_bin2dec(reg_data[reg_dict[rs1]])
            b = unsign_bin2dec(imm)
            if a < b:
                reg_data[reg_dict[rd]] = dec2bin_sext(1,32)
            reset_zero()
            reg_print()
            PrgC = PrgC + 4

        elif func3 == '000':
            if opcode == '0010011':
                reg_data[reg_dict[rd]] = add_signed_binary(reg_data[reg_dict[rs1]],dec2bin_sext(x,32))
                reset_zero()
                reg_print()
                PrgC = PrgC + 4
                
            else:
                reg_data[reg_dict[rd]] = dec2bin_sext((PrgC+4),32)
                reset_zero()
                reg_print()
                PrgC = add_signed_binary(reg_data[reg_dict[rs1]],dec2bin_sext(x,32))
                PrgC = PrgC[:-1] + '0'
                PrgC = bin2dec(PrgC)
                
    def S_type_enc(line):
        global outstr
        global PrgC
        global stackCounter

        imm0 = line[0:7]
        rs2 = line[7:12]
        rs1 = line[12:17]
        func3 = line[17:20]
        imm1 = line[20:25]
        imm = imm0 + imm1
        x = bin2dec(imm)

        datamem_dict[bin2dec(add_signed_binary(reg_data[reg_dict[rs1]],dec2bin_sext(x,32)))] = reg_data[reg_dict[rs2]]
        reset_zero()
        reg_print()
        PrgC = PrgC + 4

    def B_type_enc(line):
        global outstr
        global PrgC
        global stackCounter

        imm1 = line[0]
        imm3 = line[1:7]
        rs2 = line[7:12]
        rs1 = line[12:17]
        func3 = line[17:20]
        imm4 = line[20:24]
        imm2 = line[24]
        imm = imm1 + imm2 + imm3 + imm4 + '0'
        x = bin2dec(imm)
        a = bin2dec(reg_data[reg_dict[rs1]])
        b = bin2dec(reg_data[reg_dict[rs2]])
        
        if func3 == '000':
            if a == b:
                reset_zero()
                reg_print()
                PrgC = PrgC + x
            else:
                reset_zero()
                reg_print()
                PrgC = PrgC + 4

        elif func3 == '001':
            if a != b:
                reset_zero()
                reg_print()
                PrgC = PrgC + x
            else:
                reset_zero()
                reg_print()
                PrgC = PrgC + 4

        elif func3 == '100':
            if a < b:
                reset_zero()
                reg_print()
                PrgC = PrgC + x
            else:
                reset_zero()
                reg_print()
                PrgC = PrgC + 4

        elif func3 == '101':
            if a >= b:
                reset_zero()
                reg_print()
                PrgC = PrgC + x
            else:
                reset_zero()
                reg_print()
                PrgC = PrgC + 4

        elif func3 == '110':
            if unsign_bin2dec(a) < unsign_bin2dec(b):
                reset_zero()
                reg_print()
                PrgC = PrgC + x
            else:
                reset_zero()
                reg_print()
                PrgC = PrgC + 4

        elif func3 == '111':
            if unsign_bin2dec(a) >= unsign_bin2dec(b):
                reset_zero()
                reg_print()
                PrgC = PrgC + x
            else:
                reset_zero()
                reg_print()
                PrgC = PrgC + 4

    def U_type_enc(line):
        global outstr
        global PrgC
        global stackCounter
        
        imm = line[0:20] + '000000000000'
        rd = line[20:25]
        opcode = line[25:]

        if opcode == '0110111':
            reg_data[reg_dict[rd]] = imm
            reset_zero()
            reg_print()
            PrgC = PrgC + 4
        else:
            reg_data[reg_dict[rd]] = add_signed_binary(imm,dec2bin_sext(PrgC,32))
            reset_zero()
            reg_print()
            PrgC = PrgC + 4

    def J_type_enc(line):
        global outstr
        global PrgC
        global stackCounter
        
        imm1 = line[0]
        imm4 = line[1:11]
        imm3 = line[11]
        imm2 = line[12:20]
        rd = line[20:25]
        imm = imm1 + imm2 + imm3 + imm4 + '0'
       
        x = bin2dec(imm)
        reg_data[reg_dict[rd]] = dec2bin_sext((PrgC+4),32)
        reset_zero()
        reg_print()
        PrgC = add_signed_binary(dec2bin_sext(x,32),dec2bin_sext(PrgC,32))
        PrgC = PrgC[:-1] + '0'
        PrgC = bin2dec(PrgC)

    def instr_Ident(line):
        global PrgC
        opcode= line[-7:]
        if opcode == '0110011':
            R_type_enc(line)

        elif opcode == '0000011':
            I_type_enc(line)

        elif opcode == '0010011':
            I_type_enc(line)

        elif opcode == '1100111':
            I_type_enc(line)

        elif opcode == '0100011':
            S_type_enc(line)

        elif opcode == '1100011':
            B_type_enc(line)
        
        elif opcode == '0110111':
            U_type_enc(line)

        elif opcode == '0010111':
            U_type_enc(line)

        elif opcode == '1101111':
            J_type_enc(line)

    while(PrgC <= PrgCMax):
        line = non_empty_lines[int(PrgC/4)]
        if line == '00000000000000000000000001100011': #virtual halt
            reset_zero()
            reg_print()
            mem_stat_print()
            break
        instr_Ident(line)

    outputfile.close()
except SimulationError as e:
    print(str(e), file=sys.stderr)
    sys.exit(1)
except SystemExit:
    sys.exit(1)