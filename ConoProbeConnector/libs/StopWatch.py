# Author: Mikael Brudfors (brudfors@gmail.com)
# Date: Aug. 2015
# Free for anyone to use!

import time

# A StopWatch object with pause and reset functionality
class StopWatch():

  def __init__(self):
    self.startTime = 0.0
    self.startedTime = 0.0
    self.isRunning = False
    
  def start(self):
    if not self.isRunning:
      self.startTime = time.clock()
      self.isRunning = True
    else:
      print 'Timer alredy running!'
    
  def pause(self):
    if self.isRunning:
      stopTime = time.clock()
      self.startedTime += (stopTime - self.startTime)
      self.isRunning = False
    else:
      print 'Timer not running!'
      
  def getElapsedTime(self):
    if self.startTime == 0.0:
      return 0.0
    elif self.isRunning:
      return time.clock() - self.startTime + self.startedTime
    elif not self.isRunning:
      return self.startedTime
      
  def reset(self):
    self.startTime = time.clock()
    self.startedTime = 0.0