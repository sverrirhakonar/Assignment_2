from abc import ABC, abstractmethod

class Strategy:
    @abstractmethod
    def generate_signals(self):
        pass

