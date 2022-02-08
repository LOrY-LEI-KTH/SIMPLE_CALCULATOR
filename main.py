# Created by Yuchen Lei
# Created on 2022/2/7
import sys
import logging
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.WARNING)

class Register:
    """ Class for register.

    This class describes the attributes and behaviors of a register object.

    Attributes:
    _val: 
        An integer value stored in the register.
    _access_val_flag: 
        An boolean indicating if the value can be accessed directly.When operations with 
        other registers are not defined, flag is True, the value can be accessed directly; 
        When operations with other registers are defined, flag is False, the value can be 
        accessed after the operations between different registers.
    """
    def __init__(self):
        self._val = 0
        self._access_val_flag = True  

    def get_val(self):
        return self._val

    def get_flag(self):
        return self._access_val_flag

    def set_flag(self,flag):  
        self._access_val_flag = flag

    def operation_val(self, val, op): 
        """Performs operation with numerical value"""
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


class Calculator:
    """ Class for calculator.

    This class describes the attributes and behaviors of a calculator object.

    Attributes:
    _reg_dict: 
        A dictionary to store the register objects and names of the registers. 
        The value of the dictionary is Register object, and the key is string.
        For example: 

        {"A": <Register object A>, "B": <Register object B>}
    _reg_op_dict: 
        A dictionary to store operations of a register between other registers. 
        The value of the dictionary is array, and the key is string.
        For example: 

        {"A":[["add","B"],["subtract","C"]]}
    _op_list:
        An array to store the the supported operations. 
    """    
    def __init__(self):
        self._reg_dict = {}
        self._reg_op_dict = {}
        self._op_list = ["add", "subtract", "multiply"] 
    
    def create_reg(self,reg_name):
        """Creates a register obeject and add to dictionary."""
        self._reg_dict[reg_name] = Register()  # create register object
        self._reg_op_dict[reg_name] = []  # create array to store operations with other registers

    def operation_reg(self, reg_val_1, reg_val_2, op): 
        """Performs operation with register."""
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
        """ Reads lines from input and perform different functionsalities accordingly.

        This function can either take its input from the standard input stream, or from a file.
        Any name consisting of alphanumeric characters are allowed as register names, except pure 
        numeric names (e.g. "123"). All inputs are case insensitive. There are three possible number 
        of words in one line, i.e. 1, 2, 3. There are four possible syntaxes, i.e. print <register>, quit, 
        <register> <operation> <value>, <register_1> <operation> <register_2>. Conditions are examined 
        for the above syntaxes. Invalid commands will be ignored, and warnings will be logged to 
        the console.
        
        Args:
        from_file:
            An boolean indicating if the input is taken from a file. 

        file_name:
            A string indicating the name of the txt file to open.
        """
        if from_file:  # if taking the input from a file
            with open(file_name) as f:
                lines = f.readlines()
            num_lines = len(lines)  # number of lines in a file
            idx = 0
        else:
            pass

        while True:
            if from_file:
                if idx < num_lines:  # if not reach the EOF, read a line
                    line = lines[idx]
                    idx += 1
                else:  # if reach the EOF, quit the program
                    break
            else:
                line = input()
            line = line.lower() # convert input to lower case
            num_word = len(line.split())  # how many words in one line, e.g. print <register> 2 words
            if num_word == 1:
                """quit"""
                if line == "quit": 
                    break  # quit the program
                else:
                    logging.warning("command invalid")
                    continue
            elif num_word == 2: 
                """print <register>"""
                reg_name = line.split()[1]
                if line.split()[0] != "print":
                    logging.warning("command invalid")
                    continue
                elif line.split()[0] == "print" and reg_name in self._reg_dict.keys():
                    try:
                        self.print_reg(reg_name)
                    except RecursionError: 
                        # if the operations between registers can't be solved, raise RecursionError.
                        # the error and the invalid print command will be ignored, and a warning is raised.
                        logging.warning("Operations between registers are invalid")
                        continue
                else:
                    logging.warning("register not defined")
                    continue
            elif num_word == 3:
                if line.split()[2].isdecimal():  # if the 3rd word is a numerical value 
                    """<register> <operation> <value>"""
                    op = line.split()[1]
                    reg_name = line.split()[0]
                    val = int(line.split()[2])  # str -> int # the calculator only supports integer operations
                    if reg_name not in self._reg_dict.keys() and not reg_name.isdecimal(): 
                        # create the register if the reg_name doesn't exist and is not a pure numeric name.
                        self.create_reg(reg_name)
                    elif reg_name.isdecimal():
                        logging.warning("register name consists of only numbers")
                        continue  # invalid command, continue to next loop
                    if op in self._op_list:
                        self._reg_dict[reg_name].operation_val(val, op)
                    else:
                        logging.warning("operation not supported")
                        continue
                else:   
                    """<register_1> <operation> <register_2>"""
                    op = line.split()[1]
                    reg_name_1 = line.split()[0]
                    reg_name_2 = line.split()[2]

                    if reg_name_1 not in self._reg_dict.keys() and not reg_name_1.isdecimal(): 
                        # create the register if the reg_name doesn't exist and is not a pure numeric name.
                        self.create_reg(reg_name_1)
                    elif reg_name_1.isdecimal():
                        logging.warning("register name consists of only numbers")
                        continue
                    if reg_name_2 not in self._reg_dict.keys() and not reg_name_2.isdecimal(): 
                        # create the register if the reg_name doesn't exist and is not a pure numeric name.
                        self.create_reg(reg_name_2)
                    elif reg_name_2.isdecimal():
                        logging.warning("register name consists of only numbers")
                        continue
                    if op in self._op_list:
                        if self._reg_dict[reg_name_1].get_flag():
                            self._reg_dict[reg_name_1].set_flag(False)  # set the register to unaccessible
                        self._reg_op_dict[reg_name_1].append([op,reg_name_2])  # e.g. ["subtract","C"]
                    else:
                        logging.warning("operation not supported")
                        continue
            else:
                logging.warning("The number of words is invalid, only suport 1/2/3 word(s)")
                continue

    def print_reg(self, reg_name):
        print(self.get_reg_val(reg_name))

    def get_reg_val(self, reg_name_1):
        """A recrusive method to get the value of the register after operations with other registers.

        The operation between register can be described as follows: <register_1> <operation> <register_2>. 
        One register can have several operations with other registers, but not all the values of the 
        other registers are accessible (because these registers may also have operations with registers). 
        Therefore, the value of the register after operations with other registers can be computed recrusively.

        Args:
        reg_name_1:
            A string indicating the name of the register (register on the left).
        
        Returns:
        reg_val_1:
            A integer value of the register after operations with other registers.

        Raises:
        RecursionError:
            An error occurred when operations between registers are not solvable. For example:

            When input is 
            A add B
            B add A
            print A
            The maximum recursion depth will be exceeded.
        """
        if self._reg_dict[reg_name_1].get_flag(): # if register is accessible, return the value.
            return self._reg_dict[reg_name_1].get_val()
        else: 
            # if register is not accessible, first compute the operations with other registers,
            # and then return the value.
            op_reg_arr = self._reg_op_dict[reg_name_1]  # get all the operations with other registers
            reg_val_1 = self._reg_dict[reg_name_1].get_val()
            for op_reg in op_reg_arr:
                op = op_reg[0]
                reg_name_2 = op_reg[1]  # the name of the other register (register on the right)
                reg_val_2 = self.get_reg_val(reg_name_2)
                reg_val_1 = self.operation_reg(reg_val_1, reg_val_2, op)
            return reg_val_1


def main():
    cal = Calculator()  # create a calculator object
    if len(sys.argv) == 2:  # load the input from a file
        cal.read_line(from_file=True, file_name=sys.argv[1])
    elif len(sys.argv) == 1:  # load the input from the standard input stream
        cal.read_line(from_file=False)
    else:
        logging.warning("Not right number of arguments entered")


if __name__ == '__main__':
    main()




