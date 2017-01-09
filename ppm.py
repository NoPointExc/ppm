#!/usr/bin/python
from Tkinter import *
import random
from collections import deque
from player import *
from util import *
from config import *

#TODO:
#   -2) define class Util
#   3) License
#   4) fix doc
#   -5) add number system.
#   -7) play in turn
#   8) add machine player
#   -9) notify win
#   -10) add current player identification
#   -11) redefine Opertaions class
#   12) larger GUI.
#   -13) add a config file

class MainFrame(Frame):
    """
    main game interface.

    """

    def make_led_frame(self):
        frame = Frame(master = self)
        Label(master = frame, text='4-bit LED/next randoms/code digits').pack(side = TOP)

        #4-bit LED
        self.led_selected = StringVar(self, 0)
        self.led_four_bits = [StringVar(self, num_to_str(i, NUMBER_SYSTEM)) for i in self.four_bits]
        for i in range(4):
            Radiobutton(master = frame, textvariable = self.led_four_bits[i], variable = self.led_selected, value = str(i),
                                           indicatoron = 0, height = 2, width = 2)\
                .pack(side=LEFT)
        
        #3-bit Random number
        self.led_rand = [StringVar(self, num_to_str(r, NUMBER_SYSTEM)) for r in self.next_randoms]
        for r in self.led_rand:
            Label(master = frame, textvariable = r, fg = 'blue').pack(side = LEFT)

        #2-bit code digit.
        self.led_code = [StringVar(self, num_to_str(c, NUMBER_SYSTEM)) for c in self.code_digits]
        for c in self.led_code:
            Label(master = frame, textvariable = c, fg = 'red').pack(side = LEFT)
        return frame

    def make_player_frame(self, player):
        frame = Frame(master = self)
        Label(master = frame, text = player.name).pack()
        Label(master = frame, textvariable = self.current_player_text[player.id]).pack()
        Label(master = frame, textvariable = self.score_texts[player.id]).pack()
        Button(master = frame, text = 'add', command = (lambda: self.on_add(player))).pack(side = 'left')
        Button(master = frame, text = 'replace', command = (lambda: self.on_replace(player))).pack(side = 'right')
        Button(master = frame, text = 'skip', command = (lambda: self.on_skip(player))).pack(side = 'right')
        return frame

    def make_pop_up(self, text = ''):
        label = Label(master = Toplevel(), text=text, height=0, width=20)
        label.pack()

    def on_add(self, player):
        """add clicked"""
        print 'on add click' + str(player.id)
        self.update(player, player.add)

    def on_replace(self, player):
        """replace clicked"""
        print 'on replace click' + str(player.id)
        self.update(player, player.replace)

    def on_skip(self, player):
        print 'on replace click' + str(player.id)
        self.update(player, player.skip)

    def update(self, player, op, selected = None):
        if self.players[self.current_player] != player:
            self.make_pop_up('current player is {}'.format(self.players[self.current_player].name))
            return
        #update led
        if not selected:
            selected = int(self.led_selected.get())
        next_random = self.next_randoms[0]
        if op != player.skip:
            next_random = self.get_next_random()
        self.set_led_array(self.next_randoms, self.led_rand)
        self.four_bits[selected] = op(self.four_bits[selected], next_random)
        self.set_led_array(self.four_bits, self.led_four_bits)
        #calculate earn points
        regular_reward = self.four_bits[selected]
        adjance = get_adjance(selected, self.four_bits)        
        code_reward = get_code_reward(selected, self.four_bits, self.code_digits)
        earn_points = regular_reward * (2 ** adjance)
        if code_reward == 1:
            earn_points = earn_points * 8
        elif code_reward == 2:
            earn_points = earn_points + self.code_digits[0] * 16 + self.code_digits[1]
        player.points = player.points + earn_points
        print 'regular_reward = {}, adjance = {}, code_reward = {} bit(s), earn_points = {}'.format(regular_reward, adjance, code_reward, earn_points)
        self.next_player()
        #update plyer score in UI
        if player.points >= 255:
            self.make_pop_up('{} wins with {} points'.format(player.name, player.points))

        self.score_texts[player.id].set(num_to_str(player.points, NUMBER_SYSTEM))
        for p in self.players:
            if p.id == self.current_player:
                self.current_player_text[p.id].set('is playing...')
            else:
                self.current_player_text[p.id].set('is waiting...')

    def set_led_array(self, vals, led_array):
        for i in range(len(vals)):
            led_array[i].set(num_to_str(vals[i], NUMBER_SYSTEM))


    def get_next_random(self):
        next_random=self.next_randoms.popleft()
        self.next_randoms.append(random.randint(RANDOM_RANGE[0],RANDOM_RANGE[1]))
        #update UI
        return next_random

    def next_player(self):
        if self.current_player + 1 == len(self.players):
            self.current_player = 0
        else:
            self.current_player = self.current_player + 1
        return self.players[self.current_player]

    def init_gui(self):
        root = Tk()
        root.title('ppm')
        Frame.__init__(self, root)
        #attach ScoreFrame
        self.make_led_frame().pack()
        #attach playFrames
        self.score_texts={}
        self.current_player_text={}
        for p in self.players:
            self.score_texts[p.id]=StringVar(self, num_to_str(0, NUMBER_SYSTEM))
            if self.current_player == p.id:
                self.current_player_text[p.id]=StringVar(self, 'is playing...')
            else:
                self.current_player_text[p.id]=StringVar(self, 'is waiting...')            
            self.make_player_frame(p).pack(side = 'left')        
        self.pack()

    def __init__(self):
        self.players = [Player(0), Player(1)]
        self.current_player = 0
        self.four_bits = [random.randint(0,15) for i in range(4)]
        self.code_digits = [random.randint(0,15) for i in range(2)]
        self.next_randoms = deque([random.randint(RANDOM_RANGE[0],RANDOM_RANGE[1]) for i in range(3)])
        self.init_gui()
        print RANDOM_RANGE

def main():
    main_frame=MainFrame()
    main_frame.mainloop()


if __name__ == '__main__':
    main()

