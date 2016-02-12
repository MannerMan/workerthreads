#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import signal
import datetime

class InterruptWatch():

    def __init__(self, PrintQueue, ThreadInstanceList, CheckProgress, SafePrint, JobQueue):
        self.PrintQueue = PrintQueue
        self.ThreadInstanceList = ThreadInstanceList
        self.SafePrintThread = SafePrint
        self.JobQueue = JobQueue
        self.CheckProgress = CheckProgress
        
        self.TotalJobs = self.CheckProgress.TotalJobs

        self.is_stopped = False

    def signal_handler(self, signal, frame):
        
        self.stop()
        
        self.PrintQueue.put('InterruptWatch: You pressed Ctrl+C, stopping threads..')
        
        self.CheckProgress.stop()
        self.CheckProgress.join()
        
        for Thread in self.ThreadInstanceList:
            Thread.stop()
        
        #Wait for threads to exit
        for Thread in self.ThreadInstanceList:
            Thread.join()
            
        self.PrintQueue.put("InterruptWatch: Workerthreads done")
            
        #And wait for printjobs if any
        self.PrintQueue.join()
        
        #then stop safeprint
        self.SafePrintThread.stop()


    def start(self):
        self.PrintQueue.put('InterruptWatch: Starting..')
        
        #get current date so we can make a time-estimate when we're done
        StartTime = datetime.datetime.now()
        
        signal.signal(signal.SIGINT, self.signal_handler)
        
        #main thread gets stuck here, we either continue on empty JobQueue or Interrupt
        while not self.JobQueue.empty() and not self.stopped():
            time.sleep(0.1)
        
        #if Interruptwatch is not stopped, we just join JobQueue to let all jobs finish and then stop Safeprint
        if not self.stopped():
            self.CheckProgress.stop()
            self.JobQueue.join()
            self.CheckProgress.join()
            self.SafePrintThread.stop()
            
            #Get our endtime
            EndTime = datetime.datetime.now()
            
            #Calculate some timings
            self.CalculateJobTime(StartTime, EndTime)
            
    def CalculateJobTime(self, StartTime, EndTime):
        TotalTime = EndTime - StartTime
        msg =  "Operation took: " + str(TotalTime.seconds//3600) +" hours and " + str((TotalTime.seconds//60)%60)+" minutes"
        self.PrintQueue.put('InterruptWatch: '+msg)
        
        AvgJobTime = round(TotalTime.total_seconds() / self.TotalJobs, 1)
        self.PrintQueue.put('InterruptWatch: Job avarage process time: '+str(AvgJobTime)+" seconds")
        
    def stop(self):
        self.is_stopped = True

    def stopped(self):
        return self.is_stopped
