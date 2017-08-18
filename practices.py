#!/usr/bin/python3
import random

class Practices:
    def __init__(self):
        self.randomPool = []
    def setRandomNFromPool(self, n, pool):
        self.randomPool = []
        pool = list(pool)
        for i in range(n):
            self.randomPool.append(random.choice(pool))
            pool.remove(self.randomPool[-1])
        self.randomPool.sort(key=lambda x: x.getMidi())
    def isRandomNFromGuess(self, n, guess):
        for i in range(n):
            if (guess[i].getMidi() != self.randomPool[i].getMidi()): return(False)
        return(True)
    def setRandom2SepBy1FromPool(self, pool):
        self.randomPool = []
        self.randomPool.append(random.choice(pool[:-2]))
        self.randomPool.append(pool[pool.index(self.randomPool[0]) + 2])
        for i in self.randomPool:
            print(i.getLilypond())

