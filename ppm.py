#!/usr/bin/python
from Tkinter import *
import random
from collections import deque

#TODO:
#    1) random 0-9 , not 1-16
#    2) fix score do not update

class MainFrame(Frame):
    """
    main game interface.

    """

    def makeLEDFrame(self):
        frame = Frame(master = self)
        Label(master = frame, text='Current Values').pack(side = TOP)
        self.led_selected = StringVar(self, 0)
        self.led_array = [StringVar(self, '   0') for i in range(4)]
        for i in range(0, 4):
            Radiobutton(master = frame, textvariable=self.led_array[i], variable=self.led_selected, value=str(i),
                                           indicatoron=0)\
                .pack(side=LEFT)
        return frame

    def makePlayerFrame(self, title, score, onAdd=None, onReplace=None):
        frame = Frame(master = self)
        if onAdd==None: onAdd=lambda:None 
        if onReplace==None: onReplace=lambda:None 
        Label(master = frame, text = title).pack()
        Label(master = frame, textvariable = score).pack()
        Button(master = frame, text = 'add', command = onAdd).pack(side = 'left')
        Button(master = frame, text = 'replace', command = onReplace).pack(side = 'right')
        return frame

    def initGUI(self):
        root = Tk()
        root.title('ppm')
        Frame.__init__(self, root)
        #attach ScoreFrame
        self.makeLEDFrame().pack()
        #attach playFrames
        self.score_texts={}
        for p in self.players:
            self.score_texts[p.id]=StringVar(self, '  0')
            self.makePlayerFrame(p.name, self.score_texts[p.id], (lambda: self.onAdd(p)), (lambda: self.onReplace(p))).pack(side = 'left')        
        self.pack()

    def onAdd(self, player):
        """add clicked"""
        print 'on add click' + str(player.id)
        self.update(player, lambda val,rand: (val+rand) % 16)

    def onReplace(self, player):
        """replace clicked"""
        print 'on replace click' + str(player.id)
        self.update(player, lambda val,rand: rand % 16)

    def update(self, player, op):
        #update led
        led_vals=self.getLED()
        print 'before' + str(led_vals)
        selected=int(self.led_selected.get())
        next_random=self.nextRand()
        led_vals[selected]=op(led_vals[selected], next_random)
        print 'after' + str(led_vals)
        self.setLED(led_vals)
        #calculate eran
        adjance=getAdjance(selected, led_vals)        
        print 'adjance='+str(adjance)
        code_reward=getCodeReward(selected, led_vals, self.code_digits)
        #print 'code_reward' + str(code_reward)
        player.score=led_vals[selected] * (2**adjance)
        if code_reward==1:
            player.score=player.score * 8
        else:
            player.score=led_vals[2] * 16 + led_vals[3]
        #update plyer score in UI
        self.score_texts[player.id].set(player.score)
        print self.score_texts

    def getLED(self):
        """return LED values[0,1,2,3]"""
        result=[]
        for str_num in self.led_array:
            result.append(str2num(str_num))
        return result

    def setLED(self, led_vals):
        for i in range(len(led_vals)):
            self.led_array[i].set(num2str(led_vals[i]))

    def nextRand(self):
        next_random=self.next_randoms.popleft()
        self.next_randoms.append(random.randint(1,16))
        return next_random

    def __init__(self):
        self.players=[Player(0), Player(1)]
        self.code_digits=[random.randint(1,16) for i in range(2)]
        self.next_randoms=deque([random.randint(1,16) for i in range(3)])
        self.initGUI()



class Player():
    """base player class, should be implement by all players"""

    def __init__(self, id, name=None):
        self.score=0
        self.id=id
        self.name=name if name else 'player'+str(id)
    
def str2num(str_val, num_sys=10):
    """formate score, tranlete to num_sys(decimial, hex, ...)"""
    return int(str_val.get())

def num2str(val):
    return str(val)

def getAdjance(index, arr):
    result=0
    left=index - 1
    while(left > 0 and arr[left] == arr[index]):
        left=left - 1
        result=result + 1
    
    right=index + 1
    while (right < len(arr) and arr[right] == arr[index]):
        right=right + 1
        result=result + 1

    return result

def getCodeReward(index, arr, code_digits):    
    result=0
    if index < 2:
        return result
    if arr[2] == code_digits[0]: result=result + 1    
    if arr[3] == code_digits[1]: result=result + 1
    return result

def main():
    main_frame=MainFrame()
    main_frame.mainloop()


if __name__ == '__main__':
    main()

