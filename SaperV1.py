import tkinter as tk

from random import shuffle

from tkinter.messagebox import showinfo

colors ={
    0: "white",
    1: "blue",
    2: "#008200",
    3: "#FF0000",
    4: "#000084",
    5: "840000",
    6: "#008284",
    7: "#840084",
    8: "#000000",
}



class MyButton(tk.Button):


    def __init__(self, master, x, y, number = 0,  *args, **kwargs ):
        super(MyButton,self). __init__(master,width = 3, font = "Colibri 15 bold", *args, **kwargs)
        self.x = x
        self.y = y
        self.number = number
        self.is_mine = False
        self.count_bomb = 0
        self.is_open = False

    def __repr__(self):
        return f"MyButton{self.x} {self.y} {self.number} {self.is_mine}"


class MineSweeper:

    window = tk.Tk()
    ROW = 7
    COLUMNS = 10
    MINES = 10
    IS_GAME_OVER = False
    IS_FIRST_CLICK = True


    def __init__(self):
        self.buttons = []
        for i in range (MineSweeper.ROW + 2):
            temp = []

            for j in range (MineSweeper.COLUMNS + 2):
                btn = MyButton(MineSweeper.window,x = i, y = j)
                btn.config(command = lambda button =btn: self.click(button))
                temp.append(btn)
            self.buttons.append(temp)

    def click(self, clicked_button: MyButton):
        if MineSweeper.IS_GAME_OVER:
            return

        if MineSweeper.IS_FIRST_CLICK:
            self.insert_mines(clicked_button.number)
            self.count_mines_in_buttons()
            self.print_buttons()
            MineSweeper.IS_FIRST_CLICK = False


        if clicked_button.is_mine:
            clicked_button.config(text = "*", background = "red", disabledforeground = "black")
            clicked_button.is_open = True
            MineSweeper.IS_GAME_OVER = True
            showinfo("Game over", "you losed")
            for i in range (1,MineSweeper.ROW +1):
                for j in range (1,MineSweeper.COLUMNS + 1):
                    btn = self.buttons[i][j]
                    if btn.is_mine:
                        btn["text"] = "*"
        else:
            color = colors.get(clicked_button.count_bomb, "black")
            if clicked_button.count_bomb:
                clicked_button.config(text = clicked_button.count_bomb,disabledforeground = color)
                clicked_button.is_open = True
                
            else:
                self.breadth_first_search(clicked_button)
        clicked_button.config(state = "disabled")
        clicked_button.config(relief  = tk.SUNKEN)

    def breadth_first_search(self, btn: MyButton):
        queue = [btn]
        while queue:

            cur_btn = queue.pop()
            color = colors.get(cur_btn.count_bomb, "black")
            if cur_btn.count_bomb:
                cur_btn.config(text = cur_btn.count_bomb,disabledforeground = color)
            else:
                cur_btn.config(text = " ",disabledforeground = color)
            cur_btn.is_open = True
            cur_btn.config(state = "disabled")
            cur_btn.config(relief  = tk.SUNKEN)

            if cur_btn.count_bomb == 0:              
                x, y = cur_btn.x, cur_btn.y
                for dx in [-1,0,1]:
                    for dy in [-1,0,1]:
                       #if not abs(dx - dy) == 1:
                       #    continue 

                        next_btn = self.buttons[x + dx][y + dy]
                        if not next_btn.is_open and 1 <= next_btn.x <= MineSweeper.ROW and 1 <= next_btn.y <= MineSweeper.COLUMNS and next_btn not in queue:
                            queue.append(next_btn)
                            

    def reload(self):
        [child.destroy() for child in self.window.winfo_children()]  
        self.__init__() 
        self.create_widgets()
        MineSweeper.IS_FIRST_CLICK = True        

    def create_widgets(self): 
        menubar = tk.Menu(self.window)
        self.window.config(menu = menubar)
        settings_menu = tk.Menu(menubar, tearoff = 0)
        settings_menu.add_command(label = "To play", command = self.reload)
        settings_menu.add_command(label = "Settings")
        settings_menu.add_command(label = "To leave", command = self.window.destroy)
        menubar.add_cascade(label = "File", menu = settings_menu)

        count = 1      
        for i in range (1,MineSweeper.ROW +1):
            for j in range (1,MineSweeper.COLUMNS + 1):
                btn = self.buttons[i][j]
                btn.number = count
                btn.grid(row = i, column = j, stick = "wnes")
                count +=1
        for i in range (1,MineSweeper.ROW +1):
            tk.Grid.rowconfigure(self.window, i  , weight = 1)
        for i in range (1,MineSweeper.COLUMNS +1):
            tk.Grid.columnconfigure(self.window, i , weight = 1)

    def open_all_buttons(self):
        for i in range (MineSweeper.ROW +2):
            for j in range (MineSweeper.COLUMNS + 2):
                btn = self.buttons[i][j]
                if btn.is_mine:
                    btn.config(text = "*", background = "red", disabledforeground = "black")
                    color = colors.get(btn.count_bomb, "black")
                    btn.config(text = btn.count_bomb,fg = color)
                


    def start(self):
        self.create_widgets()
       
        #self.open_all_buttons()
        
        
     
        MineSweeper.window.mainloop()


    def insert_mines(self, number:int):
        index_mines = self.get_mines_places(number)
        print(index_mines)       
        for i in range (1,MineSweeper.ROW +1):
            for j in range (1,MineSweeper.COLUMNS + 1):
                btn = self.buttons[i][j]
                if btn.number in index_mines:
                    btn.is_mine = True
                



    def count_mines_in_buttons(self):
        for i in range (1,MineSweeper.ROW +1):
            for j in range (1,MineSweeper.COLUMNS + 1):
                btn = self.buttons[i][j]
                count_bomb = 0
                if not btn.is_mine:
                    for row_dx in [-1, 0 ,1]:
                        for col_dx in [-1, 0 ,1]:
                            neighbour = self.buttons[i + row_dx][j + col_dx]
                            if neighbour.is_mine:
                                count_bomb += 1

                btn.count_bomb = count_bomb




    def print_buttons(self):
        for i in range (1,MineSweeper.ROW +1):
            for j in range (1,MineSweeper.COLUMNS + 1):
                btn = self.buttons[i][j]
                if btn.is_mine:
                    print("B", end = " ")
                else:
                    print(btn.count_bomb,end = " ")
            print()
    @staticmethod
    def get_mines_places(exclude_number: int):
        indexes = list(range(1,MineSweeper.COLUMNS * MineSweeper.ROW + 1))
        print(f"Kick button number {exclude_number}")
        indexes.remove(exclude_number)
        shuffle(indexes)
        return indexes[:MineSweeper.MINES]


game = MineSweeper()
game.start()










