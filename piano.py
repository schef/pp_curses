#!/usr/bin/python3
import curses
import tones

class Piano:
    def __init__(self, stdscr, numOfKeys, lowestC):
        self.y = int((curses.LINES - 1) / 5) * 4
        self.x = int((curses.COLS - 1) / 2 - (numOfKeys / 2))
        self.numOfKeys = numOfKeys
        self.midiBase = lowestC
        self.position = self.getPosFromMidi(self.midiBase)
        self.stdscr = stdscr
        self.active = False
        self.playingTones = []
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)
        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.init_pair(3, curses.COLOR_RED, curses.COLOR_MAGENTA)
    def getX(self):
        return(self.x)
    def getY(self):
        return(self.y)
    def getRow(self, pos):
        ##1#3##6#8#10#
        #0#2#45#7#9#11
        if (pos % 12) in (1, 3, 6, 8, 10):
          return(1)
        elif (pos % 12) in (0, 2, 4, 5, 7, 9, 11):
          return(2)
    def drawCursor(self):
        self.stdscr.addch(0 + self.y, self.x + self.position, curses.ACS_CKBOARD, curses.color_pair(3))
        self.stdscr.addch(1 + self.y, self.x + self.position, curses.ACS_CKBOARD, curses.color_pair(3))
    def getMidiFromPos(self):
        return(self.position + self.midiBase)
    def getPosFromMidi(self, midi):
        return(midi - self.midiBase)
    def drawStatus(self):
        self.stdscr.addstr(-1 + self.y, self.x, "midi: " + str(self.getMidiFromPos()), curses.color_pair(0))
        self.stdscr.addstr(-1 + self.y, self.x + 9, "lilypond: " + str(tones.tone(self.getMidiFromPos()).getLilypond()), curses.color_pair(0))
    def drawKeys(self):
        for i in range(self.numOfKeys):
                self.stdscr.addstr(0 + self.y, i + self.x, ' ', curses.color_pair(self.getRow(i)))
                self.stdscr.addstr(1 + self.y, i + self.x, ' ', curses.color_pair(self.getRow(i)))
                self.stdscr.addstr(0 + self.y, i + self.x, ' ', curses.color_pair(self.getRow(i)))
                self.stdscr.addstr(1 + self.y, i + self.x, ' ', curses.color_pair(self.getRow(i)))
    def drawBorder(self):
        for i in range(self.numOfKeys):
            self.stdscr.addch(-2 + self.y, i + self.x, curses.ACS_HLINE, curses.color_pair(0))
            self.stdscr.addch(2 + self.y, i + self.x, curses.ACS_HLINE, curses.color_pair(0))
        for i in range(3):
            self.stdscr.addch( -1 + i + self.y, -1 + self.x, curses.ACS_VLINE, curses.color_pair(0))
            self.stdscr.addch( -1 + i + self.y, self.numOfKeys + self.x, curses.ACS_VLINE, curses.color_pair(0))
        self.stdscr.addch( -2 + self.y, -1 + self.x, curses.ACS_ULCORNER, curses.color_pair(0))
        self.stdscr.addch( 2 + self.y, -1 + self.x, curses.ACS_LLCORNER, curses.color_pair(0))
        self.stdscr.addch( -2 + self.y, self.numOfKeys + self.x, curses.ACS_URCORNER, curses.color_pair(0))
        self.stdscr.addch( 2 + self.y, self.numOfKeys + self.x, curses.ACS_LRCORNER, curses.color_pair(0))
    def drawTones(self, tones):
        for y,tone in enumerate(tones):
            #if(y == 0): self.position = self.getPosFromMidi(tone)
            if((y + 1) > 9):
                self.stdscr.addstr(0 + self.y, self.x + self.getPosFromMidi(tone.getMidi()), str(int((y + 1) / 10)), curses.color_pair(self.getRow(self.getPosFromMidi(tone.getMidi()))))
                self.stdscr.addstr(1 + self.y, self.x + self.getPosFromMidi(tone.getMidi()), str((y + 1) % 10), curses.color_pair(self.getRow(self.getPosFromMidi(tone.getMidi()))))
            else:
                self.stdscr.addstr(1 + self.y, self.x + self.getPosFromMidi(tone.getMidi()), str(y + 1), curses.color_pair(self.getRow(self.getPosFromMidi(tone.getMidi()))))
    def update(self, midi, state):
        if(state): self.playingTones.append(midi)
        else: self.playingTones.remove(midi)
    def draw(self):
        self.drawKeys()
        self.drawBorder()
        self.drawStatus()
        if (self.active): self.drawCursor()
        self.drawTones(self.playingTones)
    def setActive(self, status):
        self.active = status
    def isActive(self):
        return(self.active)
    def left(self):
        if (self.position > 0): self.position -= 1
    def right(self):
        if (self.position < self.numOfKeys - 1): self.position += 1
    def sleft(self):
        self.position -= 12
        if (self.position < 0): self.position = 0
    def sright(self):
        self.position += 12
        if (self.position > self.numOfKeys - 1): self.position = self.numOfKeys - 1
    def setPosition(self, position):
        self.position = position
        if (self.position > self.numOfKeys - 1): self.position = self.numOfKeys - 1
        if (self.position < 0): self.position = 0
    def keyPress(self, key):
        if key == curses.KEY_LEFT:
            if(self.isActive()): self.left()
        elif key == curses.KEY_RIGHT:
            if(self.isActive()): self.right()
        elif key == curses.KEY_SLEFT:
            if(self.isActive()): self.sleft()
        elif key == curses.KEY_SRIGHT:
            if(self.isActive()): self.sright()
        elif key == ord('\n'): #play tone over cursor
            if(self.isActive()): return("playCurrent")
        return("")
