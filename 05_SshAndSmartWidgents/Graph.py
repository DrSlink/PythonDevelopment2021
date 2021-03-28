import tkinter as tk


class Graph(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tf = tk.Text(self)
        self.tf.grid(column=0, row=0)
        self.tf.tag_config('err', background="red")
        self.tf.bind('<KeyRelease>', self.update_draw)
        self.gf = tk.Canvas(self)
        self.gf.bind('<ButtonPress-1>', self.press)
        self.gf.bind('<B1-Motion>', self.motion)
        self.gf.grid(column=1, row=0)
        for column in range(self.grid_size()[0]):
            self.columnconfigure(column, weight=1)
        for row in range(self.grid_size()[1]):
            self.rowconfigure(row, weight=1)
        self.mainloop()

    def update_draw(self, _):
        text = self.tf.get(1.0, tk.END)
        for number, line in enumerate(text.split('\n'), start=1):
            if line:
                try:
                    f_id, x0, y0, x1, y1, *params = line.split(',')
                    eval(f'self.gf.coords({f_id}, {x0}, {y0}, {x1}, {y1})')
                    eval(f'self.gf.itemconfigure({f_id}, {", ".join(params)})')
                    self.tf.tag_remove('err', f'{number}.0', f'{number}.end+1c')
                except Exception as _:
                    self.tf.tag_add('err', f'{number}.0', f'{number}.end+1c')

    def press(self, event):
        self.lap = self.gf.find_overlapping(event.x, event.y, event.x, event.y)
        self.pos = event.x, event.y
        if not self.lap:
            self.f_id = self.gf.create_oval(event.x, event.y, event.x, event.y, width=2, outline='black', fill='white')
            c = f'{self.f_id}, {event.x}, {event.y}, {event.x}, {event.y}, width=2, outline="black", fill="white"\n'
            self.tf.insert(tk.END, c + '\n')

    def motion(self, event):
        text = self.tf.get(1.0, tk.END)
        self.tf.delete(1.0, tk.END)
        for c in text.split('\n'):
            worth_it = False
            if c:
                if self.lap:
                    if c.split(',')[0].strip() == str(self.lap[-1]):
                        worth_it = True
                        f_id, x0, y0, x1, y1, *params = c.split(',')
                        shift = event.x - self.pos[0], event.y - self.pos[1]
                        self.tf.insert(tk.END, ','.join(map(str, [f_id, int(x0) + shift[0],
                                                                  int(y0) + shift[1],
                                                                  int(x1) + shift[0],
                                                                  int(y1) + shift[1], *params])) + '\n')
                        self.pos = event.x, event.y
                else:
                    if c.split(',')[0].strip() == str(self.f_id):
                        worth_it = True
                        f_id, x0, y0, x1, y1, *params = c.split(',')
                        self.tf.insert(tk.END, ','.join(map(str, [f_id, x0, y0, event.x, event.y, *params])) + '\n')
                if not worth_it:
                    self.tf.insert(tk.END, c + '\n')
        self.update_draw(None)


if __name__ == '__main__':
    app = Graph()
