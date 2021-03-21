import tkinter as tk


class InputLabel(tk.Label):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self['font'] = 'fixed'
        self.bind('<Button-1>', self.set_cursor)
        self.bind('<Key>', self.print_text)
        self.bind('<BackSpace>', self.backspace)
        self.bind('<Home>', self.home)
        self.bind('<Up>', self.home)
        self.bind('<End>', self.end)
        self.bind('<Down>', self.end)
        self.bind('<Left>', self.left)
        self.bind('<Right>', self.right)
        self.bind('<FocusIn>', self.focus_in)
        self.bind('<FocusOut>', self.focus_out)
        self.cursor = tk.Frame(self, width=2, height=12, background="gray")

    def focus_in(self, *args):
        self['borderwidth'] = 2
        self['relief'] = 'raised'

    def focus_out(self, *args):
        self['relief'] = 'flat'

    def set_cursor(self, press_event):
        self.focus_set()
        self.cursor.place(x=round(press_event.x / 8) * 8, y=4)

    def left(self, key_event):
        pos = self.cursor.winfo_x() // 8
        if pos > 0:
            self.cursor.place(x=(pos - 1) * 8, y=4)

    def right(self, key_event):
        pos = self.cursor.winfo_x() // 8
        if pos < len(self['text']):
            self.cursor.place(x=(pos + 1) * 8, y=4)

    def backspace(self, key_event):
        pos = self.cursor.winfo_x() // 8
        if pos > 0:
            self.cursor.place(x=(pos - 1) * 8, y=4)
            self['text'] = self['text'][:pos - 1] + self['text'][pos:]

    def home(self, key_event):
        self.cursor.place(x=0, y=4)

    def end(self, key_event):
        self.cursor.place(x=len(self['text']) * 8, y=4)

    def print_text(self, key_event):
        if key_event.char and key_event.char.isprintable():
            pos = self.cursor.winfo_x() // 8
            self.cursor.place(x=(pos + 1) * 8, y=4)
            self['text'] = self['text'][:pos] + key_event.char + self['text'][pos:]


if __name__ == '__main__':
    fr = tk.Frame()
    fr.grid()
    label = InputLabel(fr, text='Input text')
    label.grid(column=0, row=0)
    exit_b = tk.Button(fr.master, text='Exit', command=fr.quit)
    exit_b.grid(column=0, row=1, sticky='E')
    fr.master.mainloop()
