# -*- coding: utf-8 -*-

from datetime import datetime, timedelta

class Stopwatch():
    def __init__(self):
        pass
    
    def start(self):
        self.start_time = datetime.now()
        
    def get_elapsed_time(self) -> timedelta:
        return datetime.now() - self.start_time