from tkinter import *
import mjbk

ALL = N+E+S+W

class Application(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master.rowconfigure(0, weight=1)
        self.master.columnconfigure(0, weight=1)
        self.grid(sticky=ALL)

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(1, weight=1)

        self.text = Text(self)
        self.text.grid(row=0, columnspan=2)
        self.text.insert('1.0', 'Paste mojibake here...')

        self.b1 = Button(self, text='decode', command=self.handle)
        self.b1.grid(row=100, columnspan=1, sticky=ALL)
        self.b2 = Button(self, text='quit')
        self.b2.grid(row=100, column=1, columnspan=1,  sticky=ALL)

        self.output = Text(self)
        self.output.grid(row=101, columnspan=2)

    def handle(self):
        mojibake = self.text.get('1.0', 'end')
        decoded_text = mjbk.decoder_ring(mojibake)
        self.output.insert('1.0', decoded_text)



root = Tk()
app = Application(master=root)
app.mainloop()



