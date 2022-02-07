# Created by Yuchen Lei
# Created on 2022/2/7
import sys
import logging
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.WARNING)

class register:
    def __init__(self):
        self._val = 0
        self._access_val_flag = True  
        # when flag is True, the value can be accessed directly; 
        # when flag is False, the value can be accessed after the operations between different registers
    def get_val(self):
        return self._val
    def get_flag(self):
        return self._access_val_flag
    def set_flag(self,flag):  
        self._access_val_flag = flag
    def operation_val(self, val, op): # the operation with value
        if op == "add":
            self.add(val)
        elif op == "subtract":
            self.subtract(val)
        elif op == "multiply":
            self.multiply(val)
        else:
            logging.warning("operation not supported")
    def add(self, val):
        self._val += val
    def subtract(self, val):
        self._val -= val       
    def multiply(self, val):
        self._val *= val   

class calculator:
    def __init__(self):
        self._reg_dict = {} # the dictionary to store the registers and names of the registers
        self._reg_op_dict = {} # the dictionary to store operations between different registers, e.g. {A:[["add","B"],["subtract","C"]]
        self._op_list = ["add", "subtract", "multiply"] # the supported operations 
    
    def create_reg(self,reg_name):
        self._reg_dict[reg_name] = register() # create register object
        self._reg_op_dict[reg_name] = [] # array to operations with other registers

    def operation_reg(self, reg_val_1, reg_val_2, op): 
        # the operation between registers
        if op == "add":
            result = reg_val_1 + reg_val_2
        elif op == "subtract":
            result = reg_val_1 - reg_val_2
        elif op == "multiply":
            result = reg_val_1 * reg_val_2
        else:
            logging.warning("operation not supported")
        return result
        
    def read_line(self, from_file, file_name=None):
        if from_file: # if taking the input from a file
            with open(file_name) as f:
                lines = f.readlines()
            num_lines = len(lines) # number of lines in a file
            idx = 0
        else:
            pass

        while True:
            if from_file:
                if idx < num_lines: # if not reach the EOF, read a line
                    line = lines[idx]
                    idx += 1
                else: # if reach the EOF, quit the program
                    break
            else:
                line = input()
            line = line.lower()
            num_word = len(line.split()) # how many words in one line, e.g. print <register> 2 words
            
            if num_word == 1:
                # quit
                if line == "quit": 
                    break # quit the program
                else:
                    logging.warning("command invalid")
                    continue
            elif num_word == 2: 
                # print <register>
                reg_name = line.split()[1]
                if line.split()[0] == "print" and reg_name in self._reg_dict.keys():
                    try:
                        self.print_reg(reg_name)
                    except RecursionError: # if the operations between registers can't be solved, raise RecursionError
                        logging.warning("Operations between registers are invalid")
                        continue
                else:
                   logging.warning("register not defined")
                   continue
            elif num_word == 3:
                if line.split()[2].isdecimal(): # if the 3rd word is a value 
                    # <register> <operation> <value>
                    op = line.split()[1]
                    reg_name = line.split()[0]
                    val = int(line.split()[2]) # str -> int # the calculator only supports integer operations
                    if reg_name not in self._reg_dict.keys() and not reg_name.isdecimal(): 
                    # create the register if the reg_name doesn't exist and is not a number.
                        self.create_reg(reg_name)
                    elif reg_name.isdecimal():
                        logging.warning("register name consist of only numbers")
                        continue # invalid command, continue to next loop
                    if op in self._op_list:
                        self._reg_dict[reg_name].operation_val(val, op)
                    else:
                        logging.warning("operation not supported")
                        continue
                else:   
                    # <register_1> <operation> <register_2>
                    op = line.split()[1]
                    reg_name_1 = line.split()[0]
                    reg_name_2 = line.split()[2]

                    if reg_name_1 not in self._reg_dict.keys() and not reg_name_1.isdecimal(): 
                    # create the register if the reg_name doesn't exist and is not a number.
                        self.create_reg(reg_name_1)
                    elif reg_name_1.isdecimal():
                        logging.warning("register name consist of only numbers")
                        continue # invalid command, continue to next loop
                    if reg_name_2 not in self._reg_dict.keys() and not reg_name_2.isdecimal(): 
                    # create the register if the reg_name doesn't exist and is not a number.
                        self.create_reg(reg_name_2)
                    elif reg_name_2.isdecimal():
                        logging.warning("register name can't consist of only numbers")
                        continue # invalid command, continue to next loop
                    if op in self._op_list:
                        if self._reg_dict[reg_name_1].get_flag(): # 
                            self._reg_dict[reg_name_1].set_flag(False)
                        self._reg_op_dict[reg_name_1].append([op,reg_name_2])
                    else:
                        logging.warning("operation not supported")
                        continue
            else:
                logging.warning("The number of words is invalid, only suport 1/2/3 word(s)")
                continue


    def print_reg(self, reg_name):
        print(self.get_reg_val(reg_name))

    def get_reg_val(self, reg_name_1):
        #
        if self._reg_dict[reg_name_1].get_flag():
            return self._reg_dict[reg_name_1].get_val()
        else:
            op_reg_arr = self._reg_op_dict[reg_name_1] # get all the operations with other registers, e.g.  {A:[["add","B"],["subtract","C"]]
            reg_val_1 = self._reg_dict[reg_name_1].get_val()
            for op_reg in op_reg_arr:
                op = op_reg[0]
                reg_name_2 = op_reg[1]
                reg_val_2 = self.get_reg_val(reg_name_2)
                reg_val_1 = self.operation_reg(reg_val_1, reg_val_2, op)
            return reg_val_1


def main():
    cal = calculator()
    if len(sys.argv) == 2: # load the input from a file
        cal.read_line(from_file=True, file_name=sys.argv[1])
    elif len(sys.argv) == 1: # load the input from the standard input stream
        cal.read_line(from_file=False)


if __name__ == '__main__':
    main()




