from  tkinter import *
from tkinter import ttk

window = Tk()
window.title('ALİ')

window.iconbitmap('snake_cup.ico')

#Setup the notebook (tabs)
notebook = ttk.Notebook(window)
frame1 = ttk.Frame(notebook)
frame2 = ttk.Frame(notebook)
notebook.add(frame1, text="BMI Calc")
notebook.add(frame2, text="Feet to Meters")
notebook.grid()

###Create tab frames
##app1 = App1(master=frame1)
##app1.grid()
##app2 = App2(master=frame2)
##app2.grid()


lbl1 = Label(frame1,text='bu birinci frame')
lbl1.pack(side=LEFT)
lbl2 = Label(frame2,text='bu iki iki iki 2222 frame')
lbl2.pack(side=RIGHT)

#Main loop
window.mainloop()

