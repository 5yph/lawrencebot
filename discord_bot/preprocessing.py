import json
from tkinter import filedialog

def preprocess(file):
    
    lines = file.readlines()
    
    new = open("processed.txt", 'w')
    
    # get rid of empty lines and list numbers
    # if asking multiple questions, only ask the first
    for line in lines:
        if not line.isspace():
            start = line.find(' ')
            end = line.find('?')
            out_line = line[start+1:end+1]
            new.write(out_line + '\n')
    
    new.close()
    
    return

if __name__ == "__main__":
    path = filedialog.askopenfilename()
    file = open(path, 'r')
    preprocess(file)
    file.close()