# -*- coding: utf-8 -*-
"""
BLack Jack GUI Project
Created on Fri Nov 20 01:56:24 2020

@author: andre
"""

import random
import tkinter
from tkinter import ttk
from tkinter import messagebox
from PIL import ImageTk,Image
import functools


class Card:
    '''
    A class representing a card, hold a rank and a suit. Ranks can be either 
    integers or strings and suits will be strings
    '''    
    def __init__(self, rank, suit):        
        self._rank = rank        
        self._suit = suit    
    
    def get_rank(self):        
        return self._rank    
    
    def get_suit(self):        
        return self._suit    
    
    def __str__(self):
        # ["Ace", 2, 3, 4, 5, 6, 7, 8, 9, 10, "Jack", "Queen", "King"]
        if self._suit == "Spades":
            suit = "S"
        if self._suit == "Hearts":
            suit = "H"
        if self._suit == "Diamonds":
            suit = "D"
        if self._suit == "Clubs":
            suit = "C"
        if self._rank == "Ace":
            rank = "A"
        elif self._rank == "Jack":
            rank = "J"
        elif self._rank == "Queen":
            rank = "Q"
        elif self._rank == "King":
            rank = "K"
        else:
            rank = self.get_rank()
        return str(rank) + suit
        '''
        if self._suit == "Spades":
            suit = "\u2660"
        if self._suit == "Hearts":
            suit = "\u2661"
        if self._suit == "Diamonds":
            suit = "\u2666"
        if self._suit == "Clubs":
            suit = "\u2667"
        return str(self._rank) + " " + suit
        '''

class Deck:
    '''
    A class representing a list of cards and functions to modify cards
    '''
    def __init__(self, ranks, suits):        
        # ranks = [1, 2, 3, 4, 5]        
        # suits = ["S", "H"]        
        self._cards = []        
        for r in ranks:            
            for s in suits:                
                self._cards.append(Card(r, s))    
                
    def get_deck(self):        
        return self._cards    
    
    def draw_card(self):        
        return self._cards.pop()    
    
    def shuffle(self):        
        random.shuffle(self._cards)        
        random.shuffle(self._cards)
            
class Hand:
    '''
    A class representing a player's hand, holding many cards in a list
    '''    
    def __init__(self):        
        self._cards = []    
    def get_cards(self):        
        return self._cards    
    def give_card(self, card):        
        self._cards.append(card)
    def print_card(self):        
        for card in self._cards:            
            print(card)

class Casino:
    '''
    A class representing a player's record at the casino, holding integers 
    represeting the amount of cash they hold, their current bet, their win loss
    record, and their net gains. The player starts with $20, hence the 
    initialization to 20 
    '''
    def __init__(self):
        self._current_total = 20
        self._current_bet = 0
        self._total_losses = 0
        self._total_wins = 0
        self._total_gains = 0
        
    def get_total(self):
        return self._current_total
    
    def get_current_bet(self):
        return self._current_bet
    
    def place_bet(self, bet):
        self._current_bet = bet
        
    def finalize_bet(self, W_or_L):
        if W_or_L == True:
            self._current_total += self.get_current_bet()
            self._total_wins += 1
            self._total_gains += self.get_current_bet()
        if W_or_L == False:
            self._current_total -= self.get_current_bet()
            self._total_losses += 1
            self._total_gains -= self.get_current_bet()
            
    def get_total_losses(self):
        return self._total_losses
    
    def get_total_wins(self):
        return self._total_wins
    
    def get_total_gains(self):
        return self._total_gains
    
    def print_record(self):
        return (f"Player Record\nCash held: {self.get_total()}\nWins     : {self.get_total_wins()}\nLosses   : {self.get_total_losses()}\nNet      : {self.get_total_gains()}")

class Table:
    '''
    Table parent class, holds the code to help run the game
    '''
    def __init__(self):
        self._dealer = None
        self._player = None
        self._deck = None
        
    def new_deck(self, rank, suits):
        self._deck = Deck(rank, suits)
        self._deck.shuffle()
        
    def draw_cards(self, number_of_cards):
        self._player = Hand()
        self._dealer = Hand()
        for i in range(number_of_cards):
            self.give_dealer_card()
            self.give_player_card()
            
    def give_player_card(self):
        active_card = self._deck.draw_card()
        self._player.give_card(active_card)
        
    def give_dealer_card(self):
        active_card = self._deck.draw_card()
        self._dealer.give_card(active_card)
    def get_dealer(self):
        return self._dealer
    
    def get_player(self):
        return self._player
    
    def check_winner(self):
        pass
 
class Black_Jack_table(Table):
    '''
    Black jack table. Child of table class
    '''
    def hand_to_score(self, hand):
        score = 0
        aces = 0
        for cards in hand.get_cards():
            if cards.get_rank() == "Jack" or  cards.get_rank() == "Queen" or cards.get_rank() == "King":
                score+=10
            elif cards.get_rank() == "Ace":
                aces += 1
            else: score+= cards.get_rank()
        #counts aces at the end to obtain highest score up to 21
        while aces > 0:
            if score+11>21:
                    score += 1
            else:
                score += 11
            aces -= 1
        return score
    
    def check_winner(self):
        p=self.hand_to_score(self.get_player())
        d=self.hand_to_score(self.get_dealer())
        if p == d:
            messagebox.showwarning("Tie", "No one wins")
            print("Tie")
            return 2
        elif p > 21 and d > 21:
            messagebox.showwarning("Tie", "No one wins")
            print("Tie")
            return 2
        elif p ==21 and d > 21:
            messagebox.showinfo("Win", "You won!")
            print("You win")
            return 1
        elif p >21 and d <= 21:
            messagebox.showerror("Lose", "You lost")
            print("You lose")
            return 0
        elif p <21 and d == 21:
            messagebox.showerror("Lose", "You lost")
            print("You lose")
            return 0
        elif p <= 21 and d >21:
            messagebox.showinfo("Win", "You won!")
            print("You win")
            return 1
        elif d > p:
            messagebox.showerror("Lose", "You lost")
            print("You lose")
            return 0
        elif d < p:
           messagebox.showinfo("Win", "You won!")
           print("You win")
           return 1
    
class Black_Jack_Back_End:
    def __init__(self):
        self._table = None
        self._player = None 
        self._hit = True
        self._bust = False
        self._game_state = 0
    
    def set_bet(self, bet):
        if self._game_state == 0:
            self._player = Casino()
        if self._game_state == 3:
            self._hit = True
            self._bust = False
        if self._game_state != 2:
            self._player.place_bet(bet)
            messagebox.showinfo("Betting", f"Betting ${bet}, draw to continue")
            print(f"Betting {bet}!")
            self._game_state = 1

    def game_start(self):
        if self._game_state == 1 :
            self._table = Black_Jack_table()
            ranks = ["Ace", 2, 3, 4, 5, 6, 7, 8, 9, 10, "Jack", "Queen", "King"]
            suits = ["Spades", "Hearts", "Diamonds", "Clubs"]
            #creates a new deck 
            self._table.new_deck(ranks, suits)
            self._table.draw_cards(2)
            self._game_state = 2
    
    def hit(self):
        if self._game_state == 2:
            if self._hit == True:
                self._table.give_player_card()
                if self._table.hand_to_score(self._table.get_player()) >= 21:
                    self._hit = False
                if self._table.hand_to_score(self._table.get_player()) > 21:
                    self._bust = True
            if self._hit == False:
                if self._bust == False:
                    while self._table.hand_to_score(self._table.get_dealer()) <21:
                        self._table.give_dealer_card()
                        if self._table.hand_to_score(self._table.get_dealer()) >  self._table.hand_to_score(self._table.get_player()):
                            break
                self.check_winner()
    
    def no_hit(self):
        if self._game_state ==2:
            self._hit = False
            self.hit()
        
    def check_winner(self):
        result = self._table.check_winner()
        if result == 1:
            self._player.finalize_bet(True)
        elif result == 0:
            self._player.finalize_bet(False)
        self._game_state = 3
        
class Black_Jack_GUI:
    def __init__(self, root):
        root.title("Black Jack")
        self._backend=Black_Jack_Back_End()
        #Title Card
        self._title_card = tkinter.Label(text="Black Jack!", fg="green",)
        self._title_card.grid(row= 1 , column = 1, columnspan=3, padx=20, pady=10)
        #Dealer hand label and notebook
        self._dealer_hand_label = tkinter.Label(text="Dealer's Hand")
        self._dealer_hand_label.grid(row=2, column = 1)
        
        self._dealer_notebook = ttk.Notebook(root)
        self._dealer_notebook.grid(row = 3, column= 1, columnspan=5)
        #Player hand label and notebook
        self._player_hand_label = tkinter.Label(text="Player's Hand")
        self._player_hand_label.grid(row=4, column = 1)
        
        self._player_notebook =  ttk.Notebook(root)
        self._player_notebook.grid(row = 5, column = 1, columnspan=5)                
        #Player's record
        self._player_record = ttk.Label(root, text = "\n\nEnter a bet before drawing\n\n")
        self._player_record.grid(row=2, column = 15)
        #Start button
        self._start_button = ttk.Button(root, text = "Draw",
                                        command=self.draw_button)
        self._start_button.grid(row = 3, column = 15)
        
        #Bet Buttons, 1, 5, and 10 
        self._bet_button= dict()
        bet_buttons = [1, 5, 10]
        rw = 7
        clm = 10
        for i in bet_buttons:
            button_fx = functools.partial(self.bet_button, i)
            temp = ttk.Button(root, text = i, command = button_fx)
            temp.grid(row = rw, column = clm)
            self._bet_button[i] = temp
            clm+=1
        #Hit Button
        self._hit_button = ttk.Button(root, text = "Hit", command = self.hit_button)
        self._hit_button.grid(row =7, column =1)
        #Pass Button
        self._pass_button = ttk.Button(root, text = "Pass", command = self.pass_button)
        self._pass_button.grid(row =7, column =2)
        
    def test_button(self):
        self._start_button.config(text = "bingbong!")
        self.update_record()
    
    def draw_button(self):
        self._backend.game_start()
        self.clear_notebook()
        self.update_notebook()
        self.update_record()
        
    def bet_button(self, value):
        if self._backend._game_state == 1:
            self.clear_notebook()
            self.clear_notebook()
        if self._backend._game_state == 3:
            self.clear_notebook()
            self.clear_notebook()
        self._backend.set_bet(value)
               
    def hit_button(self):
        if self._backend._game_state == 2:
            self._backend.hit()
            self.clear_notebook()
            self.clear_notebook()
            self.update_notebook()
            self.update_record()
                    
    def pass_button(self):
        if self._backend._game_state == 2:
            self._backend.no_hit()
            self.clear_notebook()
            self.clear_notebook()
            self.update_notebook()
            self.update_record()
        
    def update_notebook(self):
        dealer = self._backend._table.get_dealer()
        dealer_score = self._backend._table.hand_to_score(dealer)
        player = self._backend._table.get_player()
        player_score = self._backend._table.hand_to_score(player)
        for i in dealer.get_cards():
            txt =(f"Total Score: {dealer_score}")
            filename= str(i) +".png"
            photo = ImageTk.PhotoImage(Image.open(filename))
            temp = tkinter.Label(self._dealer_notebook, 
                             image = photo, 
                             text = txt, 
                             compound = "top")
            temp.image = photo
            #temp_desc = tkinter.Label(temp, pady =60).grid()
            self._dealer_notebook.add(temp, text=i)
        for i in player.get_cards():
            txt =(f"Total Score: {player_score}")
            filename= str(i) +".png"
            photo = ImageTk.PhotoImage(Image.open(filename))
            temp = ttk.Label(self._player_notebook, 
                             image = photo,
                             text =txt,
                             compound = "top")
            temp.image = photo
            #temp_desc = tkinter.Label(temp, pady = 60).grid()
            self._player_notebook.add(temp, text=i)
        
    def clear_notebook(self):
        for i in self._player_notebook.winfo_children():
            if str(i) == self._player_notebook.select():
                i.destroy()
        for i in self._dealer_notebook.winfo_children():
            if str(i) == self._dealer_notebook.select():
                i.destroy()
        for i in self._player_notebook.winfo_children():
            if str(i) == self._player_notebook.select():
                i.destroy()
        for i in self._dealer_notebook.winfo_children():
            if str(i) == self._dealer_notebook.select():
                i.destroy()
    
    def update_record(self):
        string = self._backend._player.print_record()
        self._player_record.config(text = string)

if __name__ == "__main__":
    random.seed(1)
    root = tkinter.Tk()
    root.minsize(500,500)
    root.maxsize(2000,2000)
    app = Black_Jack_GUI(root)
    root.mainloop()