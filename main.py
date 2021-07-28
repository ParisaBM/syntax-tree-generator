from tkinter import *
from tkinter import ttk
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import nltk
from nltk.grammar import Nonterminal, Production, CFG
import json
import re

def parse(s):
    tokens = nltk.word_tokenize(s)
    tagged = nltk.pos_tag(tokens)
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
    print(s)
    return s

plt.rc('text', usetex=True)
plt.rc('text.latex', preamble=r"\usepackage{qtree}")

# Use TkAgg in the backend of tkinter application
matplotlib.use('TkAgg')

# Create an instance of tkinter frame
win = Tk()

# Set the size of the window
win.geometry("1920x1080")

# Set the title of the window
win.title("LaTex Viewer")

# Define a function to get the figure output
def graph(text):
   # Get the Entry Input
   tmptext = entry.get()
   # Clear any previous Syntax from the figure
   wx.clear()
   wx.text(0.2, 0.6, parse(tmptext), fontsize = 15)
   canvas.draw()
# Create a Frame object
frame = Frame(win)
frame.pack()
# Create an Entry widget
var = StringVar()
entry = Entry(frame, width=70, textvariable=var)
entry.pack()

# Add a label widget in the frame
label = Label(frame)
label.pack()

# Define the figure size and plot the figure
fig = matplotlib.figure.Figure(figsize=(20, 14), dpi=100)
wx = fig.add_subplot(111)
canvas = FigureCanvasTkAgg(fig, master=label)
canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=1)

# Set the visibility of the Canvas figure
wx.get_xaxis().set_visible(False)
wx.get_yaxis().set_visible(False)

win.bind('<Return>', graph)
win.mainloop()
