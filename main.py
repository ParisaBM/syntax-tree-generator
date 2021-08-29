from tkinter import *
from tkinter.ttk import *

import nltk
from nltk.grammar import Nonterminal, Production, CFG
import json
import re
from PIL import Image, ImageTk
from os import system
from pdf2image.pdf2image import convert_from_path

with open("template.tex") as template_file:
    template = template_file.read()
print(template)

def parse(s):
    tokens = nltk.word_tokenize(s)
    print(tokens)
    tagged = nltk.pos_tag(tokens)
    print(tagged)
    prod = nltk.data.load("file:english_grammar.cfg").productions()
    with open("pos.json") as pos_file:
        conversion = json.load(pos_file)
    for token in tagged:
        prod.append(Production(Nonterminal(conversion[token[1]]), [token[0]]))
    parser = nltk.parse.EarleyChartParser(CFG(Nonterminal("CP"), prod))
    for t in parser.parse(tokens):
        tree = t
    s = tree.pformat_latex_qtree().replace("bar", "'").replace("\n", " ")
    s = re.sub(r"\[\.([A-Z]+)\s([a-zA-Z]+)\s\]", r"{\1 \\\\ \2}", s)
    return s

def respond(_):
    s = parse(entry.get())
    tree_file = open("tree.tex", "w+")
    tree_file.write(template % s)
    tree_file.close()
    system("pdflatex tree.tex")
    img = ImageTk.PhotoImage(convert_from_path("tree.pdf")[0])
    panel.configure(image=img)
    panel.img = img
    system("rm tree*")

root = Tk()
entry = Entry(root)
entry.pack()
root.bind('<Return>', respond)
panel = Label(root)
panel.pack()
root.attributes('-fullscreen', True)
root.mainloop()