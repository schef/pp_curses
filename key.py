#!/usr/bin/python3
import curses
import player
import pool
import tones
import practices
import piano
from observable import Observable
from observer import Observer

class cursesCursor:
    def __init__(self, stdscr):
        self.y = 0
        self.x = 0
        self.stdscr = stdscr
        self.active = True;
    def up(self):
        if (self.y > 0): self.y -= 1
    def down(self):
        if (self.y < curses.LINES - 1): self.y += 1
    def left(self):
        if (self.x > 0): self.x -= 1
    def right(self):
        if (self.x < curses.COLS - 1): self.x += 1
    def getY(self):
        return(self.y)
    def getX(self):
        return(self.x)
    def draw(self):
        self.stdscr.move(self.getY(), self.getX())
    def setActive(self, status):
        self.active = status
        if(self.active): curses.curs_set(True)
        else: curses.curs_set(False)
    def isActive(self):
        return(self.active)

class Menu:
    def __init__(self, stdscr):
        self.y = int((curses.LINES - 1) / 5) * 1
        self.x = int((curses.COLS - 1) / 2)
        self.stdscr = stdscr
        self.active = False;
        self.list = ["play", "next", "play harmonicly (show)", "play melodicly (show)"]
    def up(self):
        if (self.y > 0): self.y -= 1
    def down(self):
        if (self.y < curses.LINES - 1): self.y += 1
    def getY(self):
        return(self.y)
    def getX(self):
        return(self.x)
    def draw(self):
        for y,i in enumerate(self.list):
            self.stdscr.addstr(self.getY() + y, self.getX() - (int(len(i)/2)), i)
    def setActive(self, status):
        self.active = status
        if(self.active): curses.curs_set(True)
        else: curses.curs_set(False)
    def isActive(self):
        return(self.active)

class Draw:
    def __init__(self, stdscr):
        self.mode = 0
        self.stdscr = stdscr
        self.stdscr.nodelay(True)
        self.cursor = cursesCursor(self.stdscr)
        self.pool = pool.tonesPool(start = "c", end = "c''", toneFilter = ["white"])
        self.piano = piano.Piano(self.stdscr, self.pool.getPianoSize(), self.pool.getPianoLowestC())
        self.player = player.Player()
        self.player.observable.register(self.piano)
        self.practices = practices.Practices()
        self.menu = Menu(self.stdscr)
        self.draw()
        self.main()
    def draw(self):
        self.stdscr.clear()
        self.piano.draw()
        self.menu.draw()
        self.printMode()
        self.cursor.draw()
        self.stdscr.refresh()
    def changeMode(self):
        self.mode += 1
        if(self.mode == 2): self.mode = 0
        if (self.mode == 0):
            self.cursor.setActive(True)
            self.piano.setActive(False)
        elif (self.mode == 1):
            self.cursor.setActive(False)
            self.piano.setActive(True)
    def printMode(self):
        self.stdscr.addstr(0, 0, str(self.mode))
        
    def main(self):

        while True:
            c = self.stdscr.getch()
            if c == ord('q'):
                break  # Exit the while loop
            elif c == curses.KEY_UP:
                if(self.cursor.isActive()): self.cursor.up()
            elif c == curses.KEY_DOWN:
                if(self.cursor.isActive()): self.cursor.down()
            elif c == curses.KEY_LEFT:
                if(self.cursor.isActive()): self.cursor.left()
                elif(self.piano.isActive()): self.piano.left()
            elif c == curses.KEY_RIGHT:
                if(self.cursor.isActive()): self.cursor.right()
                elif(self.piano.isActive()): self.piano.right()
            elif c == curses.KEY_SLEFT:
                if(self.piano.isActive()): self.piano.sleft()
            elif c == curses.KEY_SRIGHT:
                if(self.piano.isActive()): self.piano.sright()
            elif c == ord('\t'):
                self.changeMode()
            elif c == ord('a'): #list all tones in pool
                self.player.playHarmonicly(self.pool.pool)
            elif c == ord('\n'): #play current tone over cursor
                if(self.piano.isActive()): self.player.playMelodicly([tones.tone(self.piano.getMidiFromPos())])
            elif c == ord('m'):
                self.player.playMelodicly(self.practices.randomPool)
            elif c == ord('h'):
                self.player.playHarmonicly(self.practices.randomPool)
            elif c == ord('g'):
                self.practices.setRandom2SepBy1FromPool(self.pool.pool)
            elif c == ord('p'):
                self.player.playHarmonicly(self.practices.randomPool, hide=True)
                
            self.draw()

curses.wrapper(Draw)
