'''
输出：
*.var: 变量名表
*.pro: 过程名表
*.err: 错误表
'''

class var_unit():
    def __init__(self, v_name, v_proc, v_kind, v_type, v_lev, v_dar):
        self.v_name = v_name #变量名
        self.v_proc = v_proc #所属过程
        self.v_kind = v_kind #0为变量，1为形参
        self.v_type = v_type #变量类型
        self.v_lev  = v_lev  #变量层次
        self.v_dar  = v_dar  #变量在表中的位置
    
    def printer(self, output_path):
        with open(output_path, mode='a',encoding='utf-8') as s:
            line = (str(self.v_name)).ljust(10) + (str(self.v_proc)).ljust(10) + (str(self.v_kind)).ljust(10) \
                  + (str(self.v_type)).ljust(10) + (str(self.v_lev)).ljust(10) + (str(self.v_dar)).ljust(10) +'\n'
            s.write(line)


class pro_unit():
    def __init__(self, p_name, p_type, p_lev, f_adr, l_adr):
        self.p_name = p_name #过程名
        self.p_type = p_type #过程类型
        self.p_lev  = p_lev  #过程层次
        self.f_adr  = f_adr  #第一个变量在变量表中的位置
        self.l_adr  = l_adr  #最后一个变量在变量表中的位置

    def printer(self, output_path):
        with open(output_path, mode='a',encoding='utf-8') as s:
            line = (str(self.p_name)).ljust(10) +(str(self.p_type)).ljust(10) + (str(self.p_lev)).ljust(10) \
                  + (str(self.f_adr)).ljust(10) + (str(self.l_adr)).ljust(10) +'\n'
            s.write(line)

class grammar_analyzer():
    def __init__(self, code_list, error_file):

        # while ['ELON','24'] in code_list:
        #     code_list.remove(['ELON','24'])
        # code_list.remove(['EOF','25'])
        # print(code_list)

        self.code_list = code_list
        self.code_list_len = len(self.code_list)
        self.list_current = 0
        self.line_current = 1
        self.error_file = error_file
        self.var_list = []
        self.pro_list = []
        self.current_level = 0 # 嵌套层

    def advance(self):
        '''
        处理移进
        '''
        print(self.code_list[self.list_current][0])
        self.list_current = self.list_current + 1
        if self.code_list[self.list_current][0] == 'ELON': # 换行
            self.list_current = self.list_current + 1
            self.line_current = self.line_current + 1


    def error(self, error_code, symbol):
        '''
        处理报错
        '''
        if error_code == 'symbol_not_found':
            with open(self.error_file, 'a') as err_file:
                err_file.write('Line '+str(self.line_current)+', Symbol Not Found: '+ str(symbol)+'\n')
        elif error_code == 'symbol_not_match':
            with open(self.error_file, 'a') as err_file:
                err_file.write('Line '+str(self.line_current)+', Symbol Not Match: '+ str(symbol)+'\n')
        elif error_code == 'symbol_not_defined':
            with open(self.error_file, 'a') as err_file:
                err_file.write('Line '+str(self.line_current)+', Symbol Not Defined: '+ str(symbol)+'\n')
    def A(self):
        '''
        <程序>→<分程序>
        A→B
        '''
        
        self.B()

    def B(self):
        '''
        <分程序>→begin <说明语句表>; <执行语句表> end
        '''
        if self.code_list[self.list_current][0] == 'begin' :
            self.advance() #advance
            self.C() #说明语句表
            # print(self.code_list[self.list_current])
            if self.code_list[self.list_current][0] == ';':
                self.advance() #advance
                self.I() #执行语句表
                if self.code_list[self.list_current][0] == 'end':
                    self.advance() #advance
                    
            else:
                self.error('symbol_not_found', ';')
        
        return

    def C(self):
        '''
        <说明语句表>→<说明语句>│<说明语句表>;<说明语句>
        C->D|C;D
        D;D;D

        C ->DC'
        C'->e|;DC'

        D;D;D
        '''
        self.D()
        self.C_()
    
    def C_(self):
        if self.code_list[self.list_current + 1][0] == 'integer' or (self.code_list[self.list_current + 1][0] == 'ELON' and self.code_list[self.list_current + 2][0] == 'integer'): # ;DC 代表还要继续，只能对ELON进行硬读
            self.advance() #advance，读入一个分号
            self.D()
            self.C_()
        else:
            pass
    
    def D(self):
        '''
        <说明语句>→<变量说明>│<函数说明>
        '''
        if self.code_list[self.list_current+1][1] == '10' or (self.code_list[self.list_current + 1][0] == 'ELON' and self.code_list[self.list_current + 2][1] == '10'): #变量说明
            self.E()
        elif self.code_list[self.list_current+1][0] == 'function' or (self.code_list[self.list_current + 1][0] == 'ELON' and self.code_list[self.list_current + 2][0] == 'function'): #函数说明
            self.F()
        else:
            self.error('symbol_not_found', 'neither variable nor function')
    
    def E(self):
        '''
        <变量说明>→integer <变量>
        '''
        if self.code_list[self.list_current][0] == 'integer':
            self.advance()
            v_name = self.code_list[self.list_current][0]
            
            if len(self.pro_list):
                v_proc = self.pro_list[-1].p_name
            else:
                v_proc = 'main'
            v_kind = 0
            v_type = 'integer'
            v_lev = 1
            v_dar = len(self.var_list)
            self.var_list.append(var_unit(v_name, v_proc, v_kind, v_type, v_lev, v_dar))
            self.advance()
            # 登记变量

    def F(self):
        '''
        <函数说明>→integer function <标识符>（<参数>）；<函数体>
        '''
        if self.code_list[self.list_current][0] == 'integer':
            self.advance()
            if self.code_list[self.list_current][0] == 'function':
                self.advance()
                if self.code_list[self.list_current][1] == '10':
                    p_name = self.code_list[self.list_current][0]
                    self.advance()
                    if self.code_list[self.list_current][0] == '(':
                        self.advance()
                        self.G() #参数
                        if self.code_list[self.list_current][0] == ')':
                            self.advance()
                            if self.code_list[self.list_current][0] == ';':
                                self.advance()
                                self.current_level = self.current_level +1 # 嵌套标记
                                p_type = 'integer'
                                index = len(self.var_list) 
                                self.pro_list.append(pro_unit(p_name, p_type, self.current_level, index, index))
                                self.H() # 函数体
                                self.current_level = self.current_level -1
                            else:
                                self.error('symbol_not_found',';')
                        else:
                            self.error('symbol_not_found',')')
                    else:
                        self.error('symbol_not_found','(')
                else:
                    self.error('symbol_not_defined',None)
            else:
                self.error('symbol_not_found','function')
            
        else:
            pass
    
    def G(self):
        '''
        <参数>→<变量>
        '''
        v_name = self.code_list[self.list_current][0]
        
        if len(self.pro_list):
            v_proc = self.pro_list[-1].p_name
        else:
            v_proc  = 'main'
        v_kind = 0
        v_type = 'integer'
        v_lev = self.current_level
        v_dar = len(self.var_list) 
        self.var_list.append(var_unit(v_name, v_proc, v_kind, v_type, v_lev, v_dar))
        self.advance()
        return 

    def H(self):
        '''
        <函数体>→begin <说明语句表>；<执行语句表> end
        '''
        if self.code_list[self.list_current][0] == 'begin':
            self.advance()
            self.C()
            if self.code_list[self.list_current][0] == ';':
                self.advance()
                self.I()
                if self.code_list[self.list_current][0] == 'end':
                    self.advance()
                else:
                    self.error('symbol_not_found','end')
            else:
                self.error('symbol_not_found', ';')
        else:
            self.error('symbol_not_found','begin')
            

    
    def I(self):
        '''
        <执行语句表>→<执行语句>│<执行语句表>；<执行语句>
        '''
        self.J()
        self.I_()
    
    def I_(self):
        if self.code_list[self.list_current][0] == ';':
            self.advance() #advance
            self.J()
            self.I_()
        else:
            pass
        

    def J(self):
        '''
        <执行语句>→<读语句>│<写语句>│<赋值语句>│<条件语句>
        '''
        if self.code_list[self.list_current][0] == 'read':
            self.advance()
            self.K()
        elif self.code_list[self.list_current][0] == 'write':
            self.advance()
            self.L()
        elif self.code_list[self.list_current][1] == '10':
            # self.advance()
            self.M()
        elif self.code_list[self.list_current][0] == 'if':
            # self.advance()
            self.N()
        else:
            pass
        # self.list_current = self.list_current + 2

    
    def K(self):
        '''
        read
        '''
        if self.code_list[self.list_current][0] == '(':
            self.advance()
            if self.code_list[self.list_current][1] == '10':
                self.advance()
                if self.code_list[self.list_current][0] == ')':
                    self.advance()
                else:
                    self.error('symbol_not_found',')')
            else:
                self.error('symbol_not_found','variable')
        else:
            self.error('symbol_not_found','(')
    
    def L(self):
        '''
        write
        '''
        if self.code_list[self.list_current][0] == '(':
            self.advance()
            if self.code_list[self.list_current][1] == '10':
                self.advance()
                if self.code_list[self.list_current][0] == ')':
                    self.advance()
                else:
                    self.error('symbol_not_found',')')
            else:
                self.error('symbol_not_found','variable')
        else:
            self.error('symbol_not_found','(')


    def M(self):
        '''
        赋值语句
        由于变量登记问题暂时不考虑这块的识别
        '''
        if self.code_list[self.list_current][1] == '10':
            self.advance()
            if self.code_list[self.list_current][0] == ':=':
                self.advance()
                self.P()
            else:
                self.error('symbol_not_found',':=')
        else:
            self.error('symbol_not_found','variable')

    def N(self):
        '''
        条件
        <条件语句>→if<条件表达式>then<执行语句>else <执行语句>
        '''
        if self.code_list[self.list_current][0] == 'if':
            self.advance()
            self.O()
            if self.code_list[self.list_current][0] == 'then':
                self.advance()
                self.J()
                if self.code_list[self.list_current][0] == 'else':
                    self.advance()
                    self.J()
            else:
                self.error('symbol_not_found','then')
        else:
            self.error('symbol_not_found','if')

    def O(self):
        '''
        <条件表达式>→<算术表达式><关系运算符><算术表达式>
        '''
        self.P()
        if self.code_list[self.list_current][0] in ['<','<=','>','>=','=','<>']:
            self.advance()
            self.P()
        else:
            self.error('symbol_not_found','relative symbol')

        
    def P(self):
        '''
        算术表达式
        <算术表达式>→<算术表达式>-<项>│<项>
        '''
        self.Q()
        self.P_()
    
    def P_(self):
        if self.code_list[self.list_current][0] == '-':
            self.advance()
            self.Q()
            self.P_()
        else:
            pass

    def Q(self):
        '''
        <项>→<项>*<因子>│<因子>
        '''
        self.R()
        self.Q_()

    def Q_(self):
        
        if self.code_list[self.list_current][0] == '*':
            self.advance()
            self.R()
            self.Q_()
        else:
            pass

    def R(self):
        '''
        <因子>→<变量>│<常数>│<函数调用>
        '''
        if self.code_list[self.list_current][1] == '10':
            # 也许思路可以改为在变量表里？
            if self.code_list[self.list_current+1][0] == '(':
                self.advance()
                self.S() # 函数调用
            else:
                # self.advance()
                #直接前移，目前指针指向变量
#                if len(self.pro_list):
#                    v_proc = self.pro_list[-1].p_name
#                else:
#                     v_proc = 'main'
                # v_name = self.code_list[self.list_current][0]
                # v_kind = 0
                # v_type = 'integer'
                # v_lev = 1
                # v_dar = len(self.var_list) + 1
                # self.var_list.append(var_unit(v_name, v_proc, v_kind, v_type, v_lev, v_dar))
                self.advance()
                # 变量登记
        elif self.code_list[self.list_current][1] == '11':
            self.advance()
            # 常数
    
    def S(self):
        '''
        函数调用
        '''
        if self.code_list[self.list_current][0] == '(':
            self.advance()
            self.P()
            if self.code_list[self.list_current][0] == ')':
                self.advance()
            else:
                self.error('symbol_not_found',')')
        else:
            self.error('symbol_not_found','(')

    def print_files(self, var_path, pro_path):
        for i in self.var_list:
            i.printer(var_path)
        for j in self.pro_list:
            j.printer(pro_path)
    

if __name__ == "__main__":
    var_path = 'variable_list.var'
    pro_path = 'process_list.pro'
    err_file = 'error.err'
    input_file = 'output.dyd'

    with open(input_file, 'r') as a:
        codes = a.readlines()
        for i in range(len(codes)):
            codes[i] = codes[i].split()
    
    example = grammar_analyzer(codes, err_file)
    example.A()
    print(example.pro_list)
    example.print_files(var_path, pro_path)