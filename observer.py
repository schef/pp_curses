#!/usr/bin/python3
from abc import ABCMeta, abstractmethod
 
class Observer(object):
    __metaclass__ = ABCMeta
 
    @abstractmethod
    def update(self, midi, state):
        pass
