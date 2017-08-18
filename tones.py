#!/usr/bin/python3
import re

class lilypondUniversalConverter:
    reOctaves = re.compile('[^\',]')
    reDuration = re.compile('[^[0-9]]')
    reName = re.compile('[^[abcdefghisABCDEFGHIS]')
    whiteMidiBase = (0, 2, 4, 5, 7, 9, 11)
    blackMidiBase = (1, 3, 6, 8, 10)
    lilypondOctaveToMidiOctave = {
        ",,," : 1,
        ",," : 2,
        "," : 3,
        "" : 4,
        "'" : 5,
        "''" : 6,
        "'''" : 7
    }
    nameToMidiBase = {
        "c" : 0,
        "cis" : 1,
        "des" : 1,
        "d" : 2,
        "es" : 3,
        "dis" : 3,
        "e" : 4,
        "fes" : 4,
        "f" : 5,
        "eis" : 5,
        "fis" : 6,
        "ges" : 6,
        "g" : 7,
        "as" : 8,
        "gis" : 8,
        "a" : 9,
        "b" : 10,
        "ais" : 10,
        "h" : 11,
    }
    def getOctaveFromLilypond(self, lilypond):
        return(self.reOctaves.sub('', lilypond))
    def getNameFromLilypond(self, lilypond):
        return(self.reName.sub('', lilypond))
    def getDurationFromLilypond(self, lilypond):
        return(self.reDuration.sub('', lilypond))
    def getMidiFromLilypond(self, lilypond):
        octave = self.getOctaveFromLilypond(lilypond)
        name = self.getNameFromLilypond(lilypond)
        duration = self.getDurationFromLilypond(lilypond)
        midi = self.nameToMidiBase[name] + self.lilypondOctaveToMidiOctave[octave] * 12
        return(midi)
    def getMidiBaseFromMidi(self, midi):
        return(midi % 12)
    def getNameFromMidi(self, midi):
        myMidiBase = self.getMidiBaseFromMidi(midi)
        for name, midiBase in self.nameToMidiBase.items():
            if myMidiBase == midiBase:
                return(name)
    def getMidiOctaveFromMidi(self, midi):
        return(int(midi / 12))
    def getOctaveFromMidi(self, midi):
        myMidiOctave = self.getMidiOctaveFromMidi(midi)
        for lilypondOctave, midiOctave in self.lilypondOctaveToMidiOctave.items():
            if myMidiOctave == midiOctave:
                return(lilypondOctave)
    def getLilypondFromMidi(self, midi):
        name = self.getNameFromMidi(midi)
        octave = self.getOctaveFromMidi(midi)
        return(name + octave)
    def isMidiBlack(self, midi):
        midiBase = self.getMidiBaseFromMidi(midi)
        if(midiBase in self.blackMidiBase):
            return(True)
        return(False)
    def isLilypondBlack(self, lilypond):
        midi = self.getMidiFromLilypond(lilypond)
        return(self.isMidiBlack(midi))
    def isMidiWhite(self, midi):
        midiBase = self.getMidiBaseFromMidi(midi)
        if(midiBase in self.whiteMidiBase):
            return(True)
        return(False)
    def isLilypondWhite(self, lilypond):
        midi = self.getMidiFromLilypond(lilypond)
        return(self.isMidiWhite(midi))

class tone:
    midi = 0
    midiBase = 0
    name = ""
    lilypond = ""
    converter = lilypondUniversalConverter()
    def __init__(self, unknown):
        if(isinstance(unknown, str)):
            self.lilypond = unknown
            self.midi = self.converter.getMidiFromLilypond(self.lilypond)
        else:
            self.midi = unknown
            self.lilypond = self.converter.getLilypondFromMidi(self.midi)
        self.midiBase = self.converter.getMidiBaseFromMidi(self.midi)
        self.name = self.converter.getNameFromLilypond(self.lilypond)
    def getMidi(self):
        return(self.midi)
    def getMidiBase(self):
        return(self.midi)
    def getName(self):
        return(self.name)
    def getLilypond(self):
        return(self.lilypond)
