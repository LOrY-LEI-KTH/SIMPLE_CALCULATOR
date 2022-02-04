# Created by Yuchen Lei
# Created on 2022/2/7


class register:
    def __init__(self):
        self._value = 0
        self._get_value_flag = True  # when the flag is True, the value can be accessed.
    def get_value(self):
        return self._value
    def operation(self, value, op_name):
        if op_name == "add":
            self.add(value)
        elif op_name == "subtract":
            self.subtract(value)
        elif op_name == "multiply":
            self.multiply(value)
        else:
            print("no operation")

    def add(self, value):
        self._value += value
    def subtract(self, value):
        self._value -= value       
    def multiply(self, value):
        self._value *= value    

class calculator:
    def __init__(self):
        self._reg_dict = {} # the dictionary to store the registers and names of the registers
        self._reg_op_dict = {} # the dictionary to store operations between different registers, e.g. {A:[["add","B"],["subtract","C"]]
        self._op_list = ["add", "subtract", "multiply"] # the supported operations 
    
    def create_reg(self,reg_name):
        self._reg_dict[reg_name] = register()
        self._reg_op_dict[reg_name] = []
        # print(reg_name)

    # def 
        

    def read_line(self):
        while True:
            line = input()
            num_word = len(line.split()) # how many words in one line, e.g. print <register> 2 words
            
            if line == "quit": # when 
                break
            
            if num_word == 2: 
                # print <register>
                reg_name = line.split()[1]
                if line.split()[0] == "print" and reg_name in self._reg_dict.keys():
                    self.print_reg(reg_name)
                else:
                   print("no print")
        
            elif num_word == 3:
                if line.split()[2].isdecimal(): # if the 3rd word is a value 
                    # <register> <operation> <value>
                    op = line.split()[1]
                    reg_name = line.split()[0]
                    value = int(line.split()[2]) # str -> int
                    if reg_name not in self._reg_dict.keys(): # create the register if it doesn't exist
                        self.create_reg(reg_name)
                    # if op in self._op_list and reg_name in self._reg_dict.keys():
                    if op in self._op_list:
                        self._reg_dict[reg_name].operation(value, op)
                    else:
                        print("no operation")
                else:   
                    # <register_1> <operation> <register_2>
                    pass
                    # op = line.split()[1]
                    # reg_name_1 = line.split()[0]
                    # reg_name_2 = line.split()[2]

                    # if reg_name_1 not in self._reg_dict.keys(): # create the register if it doesn't exist
                    #     self.create_reg(reg_name_1)
                    # if reg_name_2 not in self._reg_dict.keys(): # create the register if it doesn't exist
                    #     self.create_reg(reg_name_2)
                    # if op in self._op_list:
                    #     self._reg_dict[reg_name].


            else: # 
                print("num_word not right nunber of words")



        
        
        pass

    def print_reg(self, reg_name):
        if self._reg_dict[reg_name]._get_value_flag:
            print(self._reg_dict[reg_name].get_value())
        else:
            pass


def main():
    cal = calculator()
    cal.read_line()
    pass


if __name__ == '__main__':
    main()




