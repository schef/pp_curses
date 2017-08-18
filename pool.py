#!/usr/bin/python3
import tones
import player

class tonesPool:
    converter = tones.lilypondUniversalConverter() 
    pool = []
    def __init__(self, start = "c,", end = "c''", toneFilter = []):
        self.midiStart = self.converter.getMidiFromLilypond(start)
        self.midiEnd = self.converter.getMidiFromLilypond(end)
        self.pool = list(self.getPoolFromMidiRange(self.midiStart, self.midiEnd))
        if ("white" in toneFilter):
            self.pool = list(self.filterColor("white"))
            toneFilter.remove("white")
        if ("black" in toneFilter):
            self.pool = list(self.filterColor("black"))
            toneFilter.remove("black")
        if (toneFilter != []):
            self.pool = list(self.filterTones(toneFilter))
    def getPoolFromMidiRange(self, midiStart, midiEnd):
        tempPool = []
        for midi in range(midiStart, midiEnd + 1):
            tempPool.append(tones.tone(midi))
        return(tempPool)
    def filterColor(self, color):
        tempPool = list(self.pool)
        if color.lower() == "white":
            for tone in self.pool:
                if (self.converter.isMidiBlack(tone.getMidi())):
                   tempPool.remove(tone)
        elif color.lower() == "black":
            for tone in self.pool:
                if (self.converter.isMidiWhite(tone.getMidi())):
                   tempPool.remove(tone) 
        return(tempPool)
    def filterTones(self, toneFilter):
        tempPool = []
        for tone in self.pool:
            for filterTone in toneFilter:
                if tone.getName() == self.converter.getNameFromLilypond(filterTone):
                    tempPool.append(tone)
        return(tempPool)
    def getPianoSize(self):
        preSize = self.midiStart % 12
        postSize = abs(-12 + (self.midiEnd % 12))
        if(postSize == 12): postSize = 0
        return(self.midiEnd - self.midiStart + preSize + postSize + 1)
    def getPianoLowestC(self):
        preSize = self.midiStart % 12
        return(self.midiStart - preSize)
