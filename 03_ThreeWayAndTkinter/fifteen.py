import tkinter as tk
import random


class Fifteen(tk.Tk):
    def __init__(self, master=None):
        super().__init__(master)
        self.build_service()
        self.build_game()

        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

    def build_game(self):
        self.game_frame = tk.Frame()
        self.game_frame.config(background="#121222")
        self.game_frame.grid(column=0, row=1)
        for i in range(4):
            for j in range(4):
                if i == j == 3:
                    break
                b = tk.Button(self.game_frame, text=f'{i * 4 + j + 1:2}',
                              background="#242434", fg="#FFFFFF", font=("Courier", 20))

                def handler(b=b):
                    self.push_tile(b)
                b['command'] = handler
                b.grid(column=j, row=i, sticky='NEWS')

        for i in range(4):
            self.game_frame.columnconfigure(i, weight=1)
            self.game_frame.rowconfigure(i, weight=1)
        self.game_frame.grid(sticky='NEWS')

    def push_tile(self, clicked_b):
        all_b = self.game_frame.children.values()
        occupied_cells = set()
        for b in all_b:
            info = b.grid_info()
            occupied_cells.add((info["row"], info["column"]))
        info = clicked_b.grid_info()
        c_r, c_c = info["row"], info["column"]
        for pos in [(c_r - 1, c_c), (c_r + 1, c_c), (c_r, c_c - 1), (c_r, c_c + 1)]:
            if 0 <= pos[0] < 4 and 0 <= pos[1] < 4:
                if pos not in occupied_cells:
                    clicked_b.grid(column=pos[1], row=pos[0])
                    break
        for b in self.game_frame.children.values():
            info = b.grid_info()
            if int(b['text']) != info["row"] * 4 + info["column"] + 1:
                break
        else:
            root = tk.Tk()
            root.config(background="#121222")

            def dest():
                root.destroy()
                self.shuffle()
            button = tk.Button(root, text="Hooray!", command=dest,
                               background="#242434", fg="#FFFFFF", font=("Courier", 20))
            root.columnconfigure(0, weight=1)
            root.rowconfigure(0, weight=1)
            button.grid()

    def shuffle(self):
        all_b = self.game_frame.children.values()
        occupied_cells = set([(i, j) for i in range(4) for j in range(4)])
        pos_to_b = {}
        for b in all_b:
            info = b.grid_info()
            pos = (info["row"], info["column"])
            occupied_cells.remove(pos)
            pos_to_b[pos] = b
        empty_cell = occupied_cells.pop()
        for i in range(1000):
            c_r, c_c = empty_cell
            pos = random.choice([(c_r - 1, c_c), (c_r + 1, c_c), (c_r, c_c - 1), (c_r, c_c + 1)])
            if 0 <= pos[0] < 4 and 0 <= pos[1] < 4:
                b = pos_to_b[pos]
                del pos_to_b[pos]
                pos_to_b[empty_cell] = b
                b.grid(column=empty_cell[0], row=empty_cell[1])
                empty_cell = pos

    def build_service(self):
        self.service_frame = tk.Frame()
        self.service_frame.config(background="#121222")
        self.service_frame.grid(column=0, row=0)
        self.new_b = tk.Button(self.service_frame, text='New', command=self.shuffle,
                               background="#242434", fg="#FFFFFF", font=("Courier", 15))
        self.exit_b = tk.Button(self.service_frame, text='Exit', command=self.quit,
                                background="#242434", fg="#FFFFFF", font=("Courier", 15))
        self.new_b.grid(column=0, row=0)
        self.exit_b.grid(column=1, row=0)
        self.service_frame.columnconfigure(0, weight=1)
        self.service_frame.columnconfigure(1, weight=1)
        self.service_frame.grid(sticky='NEWS')


if __name__ == "__main__":
    game = Fifteen()
    game.title('Fifteen')
    game.mainloop()
