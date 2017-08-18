#!/usr/bin/python3
import rtmidi
import time
from threading import Timer
from observable import Observable
from observer import Observer

class Player:
    def __init__(self):
        self.name = "svirko"
        self.velocity = 112
        self.duration = 1
        self.midiout = rtmidi.MidiOut()
        self.midiout.open_virtual_port(self.name.encode('utf-8'))
        self.observable = Observable()
        self.active = False
        self.hide = False
    def toneOn(self, tone):
        self.midiout.send_message([0x90, tone.getMidi(), self.velocity])
        if(self.hide == False): self.observable.update_observers(tone, 1)
    def toneOff(self, tone):
        self.midiout.send_message([0x80, tone.getMidi(), 0])
        if(self.hide == False): self.observable.update_observers(tone, 0)
    def playMelodicly(self, tones, tone = None, hide = False):
        if(self.active and tone == None): return
        else:
            self.active = True
            self.hide = hide
            tones = list(tones)
        if(tone != None): self.toneOff(tone)
        if( len(tones) > 0):
            tone = tones.pop(0)
            self.toneOn(tone)
            Timer(self.duration, self.playMelodicly, [tones, tone, hide]).start()
        else:
            self.active = False
    def playHarmonicly(self, tones, off = False, hide = False):
        if(self.active and off == False): return
        else:
            self.active = True
            self.hide = hide
        for tone in tones:
            if(off): self.toneOff(tone)
            else: self.toneOn(tone)
        if(off == False): Timer(self.duration, self.playHarmonicly, [tones, True, hide]).start()
        else:
            self.active = False
