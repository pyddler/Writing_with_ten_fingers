#!/usr/bin/python3

import random
import time
import string
import sys
import psycopg2
import html


class CWriter:
    def __init__(self):
        self.exercise_count = 10
        self.exercise_sentence_length = 100
        self.exercise = str()
        self.choice_selected = None
        self.batch = None
        self.db = list()
        self.connect_db()
        self.log = str()
        self.reset = False

    def connect_db(self):
        self.db.append(psycopg2.connect(dbname="writing_with_ten_fingers", \
                user="writing_user", password="writing-password", host="127.0.0.1")) #move to xml
        self.db.append(self.db[0].cursor())


    @staticmethod
    def clear_terminal():
        #print(chr(27) + "[2J")
        print("\033[2J","\033[H")

    def select_exercise(self):
        choice_menu = f"For exercising all keyboard letters select 'a' for letters 'l' for words 'w', " \
                      f"for sentences 's' and for programming code 'c' or 'q' to quit."
        allowed_choice = ['a','l','w','s','c','q']
        allowed_code = ['p','c','c++']

        self.clear_terminal()
        print(choice_menu,"\n"*2)
        
        while True:
            choice_selected = sys.stdin.readline().strip()
            if(len(choice_selected) == 1 and choice_selected in allowed_choice):
                if(choice_selected == 'c'):
                    print("Please select what code to exercise (p - Python, c - C code, c++ - C++ code).")
                    code_selected = sys.stdin.readline().strip()
                    if(len(code_selected) == 1 and code_selected in allowed_code):
                        break
                else:
                    break
            self.clear_terminal()
            print(choice_menu,"\n"*3)
            print("Bad choice, try again.:")

        self.choice_selected = choice_selected
        if(choice_selected == 'l'):
            self.batch = string.ascii_letters
        elif(choice_selected == 'q'):
            quit()
        elif(choice_selected in ('s','c')):
            if(choice_selected == 'c'):
                group = f"{choice_selected}{code_selected}"
                print(group)
            else:
                group = 's'
            sql = f"select random() as rnd,e.id,eg.group_abb,eg.exercise_type,e.exercise " \
                  f"from exercises e " \
                  f"join exercise_group eg on eg.id = e.exercise_type " \
                  f"where eg.group_abb = '{group}' " \
                  f"order by rnd;"
            self.db[1].execute(sql)
            print(sql)
        else:
            self.batch = f'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ]]]]]' \
                         f'[[[[[((((((((()))))){{}}{{}}{{}}1112233344455566677788899' \
                         f'9000---===!!!@@@###$$$%%%^^^&&&***   ...///,,, <<>>\\\\""'


    def generate_exercise(self):
        if(self.choice_selected in ('s','c')):
            if(self.exercise == '' or self.reset):
                self.exercise = self.db[1].fetchone()
                self.reset = False
                if(self.exercise == None):
                    return None
                self.exercise = self.exercise[-1]
            exercise = self.exercise[:self.exercise_sentence_length]
            self.exercise = self.exercise[self.exercise_sentence_length:]
        else:
            exercise = "".join([random.choice(self.batch) \
                    for i in range(self.exercise_sentence_length)])
        return html.unescape(exercise).replace("\n"," ").rstrip()

        
    def writing_exercise(self):
        while True:
            self.select_exercise()
            for i in range(self.exercise_count):
                exercise = self.generate_exercise()
                if(exercise is None):
                    break
                self.clear_terminal()
                print("Please retype what you see under this sentence.:")
                print(exercise)
                t1 = time.perf_counter()
                user_input = input("\n")
                t2 = time.perf_counter()
                td = t2 - t1
                avg = td / self.exercise_sentence_length
                cpm = self.exercise_sentence_length * 60 / td
                if(exercise == user_input):
                    print("\n")
                    print("   Yaaayy    "*10,"Good job!")
                    print(f"Writen in {td} s.")
                    print(f"That is average time of {avg} s per press.")
                    print(f"And PpM of {cpm} (press/min).")
                    print("\n")
                else:
                    print("\n\nNayy:\n")
                    print("-"*10)
                    wrong_index = list()
                    wrong_list = list()
                    for num,(x,y) in enumerate(zip(user_input,exercise)):
                        if(x != y):
                            wrong_index.append(num)
                    print(exercise)
                    wrong_position = str()
                    prev = 0
                    for i in wrong_index:
                        pos = i - prev
                        wrong_position += "^".rjust(pos)
                        prev = i
                    print(wrong_position)
                    print(user_input)
                    print("-"*10)
                    print(f"Writen badly in {td} s.")
                print("Press Enter to continue, 'r' to reselect exercise or 'q' to quit.")
                x = input()
                if(x == 'q'):
                    quit()
                elif(x == 'r'):
                    self.reset = True
                    break

if(__name__ == "__main__"):
    prog = CWriter()
    prog.writing_exercise()
