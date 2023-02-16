import curses
from curses import wrapper
import time
import os 
import pandas as pd
import random


if not os.path.exists("data-2.csv"):
    with open('data_2.csv','w') as f:
        f.write("username"+",")
        f.write("email"+",")
        f.write("phone_no"+",")
        f.write("WPM"+',')
        f.write("\n")
def generate_word(diff_choice,words_count):
    if diff_choice.lower() in ['1','e','easy']:
        #Get words from word_list.txt file which returns a random selection of 5 words in the form of a list
        with open("word_list.txt","r") as f:
            word_list = f.read().split("\n")
        a = random.sample(word_list,words_count)
        sentence = ' '.join(a)
        return sentence
    elif diff_choice.lower() in ['2','m','moderate'] : 
        with open('word_list_moderate.txt',"r") as f:
            word_list  = f.read().split("\n")
        a = random.sample(word_list,words_count)
        sentence = ' '.join(a)
        return sentence
    elif diff_choice.lower() in ['3','c','challenging']:
        with open('word_list_hard.txt','r') as f:
            word_list = f.read().split("\n")
        a = random.sample(word_list,words_count)
        sentence = ' '.join(a)
        return sentence

global wpm 
def start_screens(stdscr):
    
    stdscr.clear()
    stdscr.addstr(0,0,"Welcome to speed typing test!")
    stdscr.addstr(2,0,"Press any key to continue.",curses.color_pair(3))
    
    stdscr.refresh()
    stdscr.getkey()

def display(stdscr, target, current, wpm=0):
    stdscr.addstr(target)
    stdscr.addstr(1,0,f"WPM: {wpm}")

    for i, char in enumerate(current):
        correct_char = target[i]
        color = curses.color_pair(1)
        if correct_char != char:
            color = curses.color_pair(2)
        
        stdscr.addstr(0 ,i ,char, color)

def wpm_test(stdscr,diff_choice,words_count):
    target_text = generate_word(diff_choice,words_count)
    current_text = []
    wpm = 0
    start_time = time.time()
    stdscr.nodelay(True)

    while True:
        time_end = max(time.time() - start_time, 1)
        
        wpm = round((len(current_text)/ (time_end/60))/5)

        stdscr.clear()
        display(stdscr, target_text, current_text, wpm)
        stdscr.refresh()
        
        joined_text = "".join(current_text)
        if joined_text == (target_text):
            stdscr.nodelay(False)
            break

        try: 
            key = stdscr.getkey()
        except:
            continue

        if ord(key) == 27:
            break
        if key in ("KEY_BACKSPACE", "\b", "\x7f"):
            if len(current_text) > 0:
                current_text.pop()
        elif len(current_text) < len(target_text):
            current_text.append(key)

        global pk
        pk = wpm
        
def main(stdscr,diff_choice,word_count):
   

    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_BLACK)

    start_screens(stdscr)

    while True:

        wpm_test(stdscr,diff_choice,word_count)
        stdscr.clear()
        
        stdscr.addstr(f"\n*********** Score {pk} Wpm ************* ", curses.color_pair(3))
        with open('data_2.csv','a') as f:
            f.write(str(pk))
            f.write("\n")
            
        stdscr.addstr(2,0,f"Congratuations you completed the test.\n", curses.color_pair(1))
        stdscr.addstr("\n\nPress any key to continue or 'Esc' to escape.\n\n")

        key1 = stdscr.getkey()
        if ord(key1) == 27:
            stdscr.addstr(f"Thank you {username}.", curses.color_pair(3))
            #stdscr.getkey()
            break
        

while True:
        choice = input("   1.Play    2.View My Stats    3.Leaderboard    99.Exit\n\t")
        if choice.lower() in ["p", 'play', '1']:
            username = input("Enter your user: ")
            email = input("Enter your Email: ")
            phone_no = input("Enter Phone_no :")
            with open('data_2.csv',"a") as f:
                f.write(username+",")
                f.write(email+",")
                f.write(phone_no+",")
            diff_choice = input("Enter Difficulty  1.Easy    2.Moderate    3.Challenging\n\t")
            word_count = int(input("How many words"))
            
            wrapper(main,diff_choice,word_count)
        
        elif choice.lower() in ["r", 'records', 'view records', '2']:
            username = input("Username: ").strip().lower()
            df = pd.read_csv('data_2.csv')
            df.set_index('username',inplace=True)
            df.dropna(axis=1,inplace=True)
            row = df.loc[str(username)]
            print(row)
        
        elif choice.lower().split()[0] in ["l", 'leaderboard', '3']:
             df = pd.read_csv('data_2.csv')
             df.dropna(axis=1,inplace=True)
             df.sort_values(by=['WPM'])
             print(df.head(10))
        elif choice.lower() in ["e", 'exit', '99']:
            break
        
            
