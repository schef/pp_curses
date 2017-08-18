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
        self.active = False;
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
    def keyPress(self, key):
        if key == curses.KEY_UP:
            if(self.isActive()): self.up()
        elif key == curses.KEY_DOWN:
            if(self.isActive()): self.down()
        elif key == curses.KEY_LEFT:
            if(self.isActive()): self.left()
        elif key == curses.KEY_RIGHT:
            if(self.isActive()): self.right()
        return("")

class Command:
    def __init__(self, name, command):
        self.name = name
        self.command = command
    def getName(self):
        return(self.name)
    def getLen(self):
        return(len(self.name))
    def getCommand(self):
        return(self.command)

class Menu:
    def __init__(self, stdscr):
        self.y = int((curses.LINES - 1) / 5) * 1
        self.x = int((curses.COLS - 1) / 2)
        self.stdscr = stdscr
        self.active = False;
        self.position = 0
        self.list = [
                Command("play (listen and sing)", "playHidden"),
                Command("next", "nextPractice"),
                Command("play harmonicly (show)", "playHarmonicly"),
                Command("play melodicly (show)", "playMelodicly"),
                Command("reset practice", "resetPractice")
                ]
    def up(self):
        if (self.position > 0): self.position -= 1
    def down(self):
        if (self.position < len(self.list) - 1): self.position += 1
    def getY(self):
        return(self.y)
    def getX(self):
        return(self.x)
    def draw(self):
        for y,command in enumerate(self.list):
            if(self.position == y and self.isActive()):
                self.stdscr.addstr(self.getY() + y, self.getX() - (int(command.getLen()/2)), command.getName(), curses.color_pair(3))
            else:
                self.stdscr.addstr(self.getY() + y, self.getX() - (int(command.getLen()/2)), command.getName(), curses.color_pair(0))
    def setActive(self, status):
        self.active = status
    def isActive(self):
        return(self.active)
    def keyPress(self, key):
        if key == curses.KEY_UP:
            if(self.isActive()): self.up()
        elif key == curses.KEY_DOWN:
            if(self.isActive()): self.down()
        elif key == ord('\n'):
            if(self.isActive()): return(self.list[self.position].getCommand())
        return("")

class StatusBar:
    template = "STATUS BAR: [ Round: xxx ]"
    round = 1
    def __init__(self, stdscr):
        self.stdscr = stdscr
    def draw(self):
        self.stdscr.addstr(0, 0, self.template, curses.A_BOLD)
        self.drawRound()
    def drawRound(self):
        self.stdscr.addstr(0, self.template.find("xxx"), str(self.round).zfill(3), curses.color_pair(2))
    def setRound(self, num):
        self.round = num
    def increaseRound(self):
        self.round += 1

class Draw:
    modeName = [
            "testing curser mode",
            "Piano mode (use <- and -> to select a tone and Return to play)",
            "Menu mode (use ^ and v to select and Return to execute)"
            ]
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
        self.practices.setRandom2SepBy1FromPool(self.pool.pool)
        self.menu = Menu(self.stdscr)
        self.statusBar = StatusBar(self.stdscr)
        self.draw()
        self.main()
    def callCommand(self, commandName):
        if (commandName == "playHidden"): self.player.playHarmonicly(self.practices.randomPool, hide=True)
        elif (commandName == "playMelodicly"): self.player.playMelodicly(self.practices.randomPool)
        elif (commandName == "playHarmonicly"): self.player.playHarmonicly(self.practices.randomPool)
        elif (commandName == "playCurrent"): self.player.playMelodicly([tones.tone(self.piano.getMidiFromPos())])
        elif (commandName == "playAll"): self.player.playHarmonicly(self.pool.pool)
        elif (commandName == "nextPractice"):
            self.practices.setRandom2SepBy1FromPool(self.pool.pool)
            self.statusBar.increaseRound()
        elif (commandName == "resetPractice"):
            self.practices.setRandom2SepBy1FromPool(self.pool.pool)
            self.statusBar.setRound(1)
    def draw(self):
        self.stdscr.clear()
        self.piano.draw()
        self.menu.draw()
        self.printMode()
        self.cursor.draw()
        self.statusBar.draw()
        self.stdscr.refresh()
    def changeMode(self):
        self.mode += 1
        if(self.mode == 3): self.mode = 1
        if (self.mode == 0):
            self.cursor.setActive(True)
            self.piano.setActive(False)
            self.menu.setActive(False)
        elif (self.mode == 1):
            self.cursor.setActive(False)
            self.piano.setActive(True)
            self.menu.setActive(False)
        elif (self.mode == 2):
            self.cursor.setActive(False)
            self.piano.setActive(False)
            self.menu.setActive(True)
    def printMode(self):
        self.stdscr.addstr(curses.LINES - 1, 0, str("MODE: "), curses.A_BOLD)
        self.stdscr.addstr(curses.LINES - 1, 0 + len("MODE :"), self.modeName[self.mode])
    def main(self):
        self.cursor.setActive(False)
        self.piano.setActive(False)
        self.menu.setActive(True)
        self.mode = 2
        while True:
            key = self.stdscr.getch()
            self.callCommand(self.cursor.keyPress(key))
            self.callCommand(self.piano.keyPress(key))
            self.callCommand(self.menu.keyPress(key))
            if key == ord('q'):
                break  # Exit the while loop
            elif key == ord('\t'):
                self.changeMode()
            self.draw()


curses.wrapper(Draw)
