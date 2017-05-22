
import Tkinter as tk     # python 2
import tkFont as tkfont  # python 2
from heapq import *
from datetime import date


def clamp(n, minn, maxn = 500):
    return max(min(maxn, n), minn)

class Deck:
    def __init__(self,name,list_of_cards):
        self._name = name
        daily_lim = 2
        self._h = []
        for card in list_of_cards:
            heappush(self._h, card)
        self._todays_deck = [heappop(self._h) for i in range(daily_lim)]

    def next_card(self):
        card = heappop(self._todays_deck)
        heappush(self._h, card)
        return card
class Card:
    def __init__(self,name,question,answer):
        self._difficulty = 0.3 
        self._difficulty = clamp(self._difficulty,0,1)
        self._difficulty_weight = 3 - 1.7 * self._difficulty

        self.days_between_reviews = 1/(self._difficulty_weight ** 2)
        self.days_between_reviews = clamp(self.days_between_reviews, 1)
        self.date_last_reviewed = date.today().day
        self.percent_overdue = min(2,((date.today().day - self.date_last_reviewed) ** 2)/self.days_between_reviews)


        #All above are used to calculate which cards of the deck needs to be reviewed next


        self._name = name
        self._question = question
        self._answer = answer
        




deck_folders = [Deck("tester deck(Math)",[Card("Deck One","4*4","16"), Card("Deck Two","sqrt(4)","2")])]





class Smart_FlashCard_App(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)


        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (Main_Menu, Folders, Card_Front_Deck_One):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("Main_Menu")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


class Main_Menu(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        self._folder = tk.Button(master = self,text = "Deck Folder", command = lambda: controller.show_frame("Folders"))
        self._folder.grid(row = 0, column = 0, columnspan = 3)
        self._stats = tk.Button(master = self, text= "Current Statistics")
        self._stats.grid(row = 0, column = 3, columnspan = 3)

        self._folder.pack()
        self._stats.pack()


class Folders(tk.Frame):
    def __init__(self,parent,controller):

        #Deck_folders only has one Deck with two cards
        tk.Frame.__init__(self,parent)
        curr_row = 0
        
        for deck in deck_folders:
            curr = tk.Button(master = self, text = "Deck name: " + deck._name, command = lambda: controller.show_frame("Card_Front_Deck_One"))
            curr.grid(row = curr_row, column = 0)
            curr_row += 1 
            curr.pack()

class Card_Front_Deck_One(tk.Frame):
    def __init__(self,parent,controller):
        self._controller = controller
        tk.Frame.__init__(self,parent)
        self.curr_deck = deck_folders[0]
        self.this_card = self.curr_deck.next_card()
        
        self.question = tk.Label(master = self, text= self.this_card._question)
        self.question.pack()
        # question.grid()

        self.difficulty_buttons()
        
    def difficulty_buttons(self):
        self.again = tk.Button(master = self, text = "again", command = lambda: self.update_card(self.again))
        self.good = tk.Button(master = self, text ="good", command = lambda: self.update_card(self.good))
        self.easy = tk.Button(master = self, text = "easy", command = lambda: self.update_card(self.easy))
        self.again.grid()
        self.good.grid()
        self.easy.grid()
        self.again.pack()
        self.good.pack()
        self.easy.pack()

    def update_card(self,button):
        self.easy.pack_forget()
        self.good.pack_forget()
        self.again.pack_forget()
        self.answer = tk.Label(master = self, text = self.this_card._answer)
        self.answer.pack()
        self.next_button = tk.Button(master = self, text = "next", command = lambda: self.next())
        self.next_button.pack()
        self.this_card.date_last_reviewed = date.today()

        #update difficulty of card
        performance_rating = 0
        if button == self.easy:
            performance_rating = 0.7
        elif button == self.good:
            performance_rating = 0.5
        elif button == self.again:
            performance_rating = 0.1
        self.this_card._difficulty += self.this_card.percent_overdue * (1/17) * ((8) - (9*performance_rating))
        
        if button == self.again:
            heappush(self.curr_deck._todays_deck, self.this_card)



    def next(self):
        try:
            self.next_button.pack_forget()
            self.answer.pack_forget()
            self.this_card = deck_folders[0].next_card()
            self.question.configure(text =self.this_card._question)
            self.again.pack()
            self.good.pack()
            self.easy.pack()
        except:
            self.next_button.pack_forget()
            self.answer.pack_forget()
            self.question.pack_forget()
            self.done = tk.Label(master = self, text = "You are done with this Deck for today!")
            self.done.pack()


def main():    
    app = Smart_FlashCard_App()
    app.mainloop()
main()
