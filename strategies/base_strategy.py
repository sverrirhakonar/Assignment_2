from abc import ABC, abstractmethod

class Strategy:
    @abstractmethod
    def generate_signals(self, price_data):
        pass

class BenchmarkStrategy(Strategy):

    def __init__(self, )

