def lexical_analysis(source_file, output_file, error_file):
    with open(source_file, 'r') as source:
        lines = source.readlines()
        # 逐行分析源代码
        for i in range(len(lines)):
            # 每一行的分析
            line = lines[i]
            line_analysis(line, output_file, error_file, i)
            # 行尾
            eoln_insert(output_file)
        # 文件尾
        eof_insert(output_file)

def line_analysis(line, output_file, error_file, index):
    with open(output_file, 'a') as output:
        current_word = '' #代表当前识别的词
        line = line.lstrip()
        state = 0
        for i in range(len(line)):
            # 由于已经删完了开始的空格，故符号必然为字母/数字/符号
            #讨论标识符：
            #开头为字母，每次可以读取一个数字，结尾为非字母数字。读到这里进行判断

            #读到字母的时候，若current_word非空，考虑到字母数字参杂的标识符，或者是保留字，两种情况
            if line[i] in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
                           'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']:
                # if state == 0: # 代表current_word为空
                #     current_word = current_word + line[i] # 录入字母
                #     print(current_word)
                #     state = 1 # 进入状态1
                #     if
                if state == 0 or state == 1: #代表非空
                    if i+1 < len(line) - 1: # 往后搜索一下
                        if line[i+1] not in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
                                            'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
                                            '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']:
                            # 代表可能是标识符或者单词符号
                            current_word = current_word + line[i]
                            state = 2
                        else: # 代表扫到了字母或者数字
                            current_word = current_word + line[i] # 录入字母或数字
                            state = 1 # 维持状态1
                    else: # 已经扫到了尽头，可以结束了
                        current_word = current_word + line[i]
                        state = 2   

            elif line[i] in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']: #录入数字
                if state == 3 or state == 0:
                    if i+1 < len(line) - 1: # 往后搜索一下
                        if line[i+1] not in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']:
                            current_word = current_word + line[i]
                            state = 4 # 常数读取完毕
                        else:
                            current_word = current_word + line[i] # 录入字母
                            state = 3 # 维持状态3
                    else:
                        current_word = current_word + line[i]
                        state = 4 # 代表了扫到了行末的情况
            
            elif line[i] == '=':
                if state == 0:
                    state = 5
                elif state == 10:
                    state = 11
                elif state == 14:
                    state = 15
                elif state == 17:
                    state = 18
            
            elif line[i] == '-' and state == 0:
                state = 6
            
            elif line[i] == '*' and state == 0:
                state = 7
            
            elif line[i] == '(' and state == 0:
                state = 8
            
            elif line[i] == ')' and state == 0:
                state = 9

            elif line[i] == '<' and state == 0:
                state = 10
                if i < len(line) - 1:
                    if line[i+1] not in ['=', '>']:
                        state = 13
                else:
                    state = 13 # <识别
            
            elif line[i] == '>' and state == 0:
                state = 14
                if i < len(line) - 1:
                    if line[i+1] not in ['=']:
                        state = 16
                else:
                    state = 16 # <识别

            elif line[i] == ':' and state == 0:
                state = 17
                if i < len(line) - 1:
                    if line[i+1] not in ['=']:
                        state = 19
                else:
                    state = 19 # <识别
            elif line[i] == ';' and state == 0:
                state = 20

            elif line[i] == ' ' and state == 0:
                continue

            else:
                print('Line '+str(index+1)+', error3: unexpected token: '+ str(line[i]))

            if state == 2:
                origin_symbols = {'begin': 1, 'end': 2, 'integer': 3, 'if': 4, 'then': 5, "else": 6, 'function': 7, 'read': 8, 'while': 9}
                if current_word in origin_symbols:
                    if len(current_word)>16:
                        print('error1： length of variable is larger than 16')
                    else:
                        output.write((current_word +'  '+str(origin_symbols[current_word])).rjust(19) + '\n') # 识别出保留字
                    current_word = '' # 清空
                else:
                    # print(current_word)
                    output.write((current_word+' 10').rjust(19) + '\n') # 识别出标识符
                    current_word = '' # 清空
                state = 0
            elif state == 4:
                if len(current_word)>16:
                    print('Line '+str(index)+', error1: length of number is larger than 16')
                else:
                    output.write((current_word+' 11').rjust(19) + '\n') # 识别出常数
                current_word = '' # 清空
                state = 0
            elif state == 5:
                output.write(("= 12").rjust(19) + '\n')
                state = 0
            elif state == 6:
                output.write(("- 18").rjust(19) + '\n')
                state = 0
            elif state == 7:
                output.write(("* 19").rjust(19) + '\n')
                state = 0
            elif state == 8:
                output.write(("( 21").rjust(19) + '\n')
                state = 0
            elif state == 9:
                output.write((") 22").rjust(19) + '\n')
                state = 0
            elif state == 11:
                output.write(("<= 14").rjust(19) + '\n')
                state = 0
            elif state == 12:
                output.write(("<> 13").rjust(19) + '\n')
                state = 0
            elif state == 15:
                output.write((">= 16").rjust(19) + '\n')
                state = 0
            elif state == 16:
                output.write(("> 16").rjust(19) + '\n')
                state = 0
            elif state == 18:
                output.write((":= 20").rjust(19) + '\n')
                state = 0
            elif state == 19:
                print('Line '+str(index)+', error2: unexpected token after \':\'')
                state = 0
            elif state == 20:
                output.write(("; 23").rjust(19) + '\n')
                state = 0
            

def eoln_insert(file):
    with open(file, 'a') as output:
        output.write('ELON 24'.rjust(19) + '\n')

def eof_insert(file):
    with open(file, 'a') as output:
        output.write('EOF 25'.rjust(19) + '\n')

if __name__ == "__main__":
    source_file = "source.pas"
    output_file = "output.dyd"
    error_file  = "error.err"   
    lexical_analysis(source_file, output_file, error_file)
