#!/usr/bin/env python
# -*- coding: utf-8 -*-

import threading
import time

class ProgressCheckThread(threading.Thread):
    
    def __init__(self, PrintQueue, JobQueue):
        
        #normal init
        threading.Thread.__init__(self)
        
        self.PrintQueue = PrintQueue
        self.JobQueue = JobQueue
        
    def run(self):
        self.PrintQueue.put("ProgressThread: Starting..")
        self._stop = threading.Event()
        
        self.TotalJobs = self.JobQueue.qsize()
        self.PrintQueue.put("ProgressThread: "+str(self.TotalJobs)+" Jobs loaded into JobQueue")
        
        while True:
            for x in range(0, 30):
                if self.stopped():
                    break
                time.sleep(1)
            
            if not self.stopped():
                #Get the current Queue Size
                currsize = self.JobQueue.qsize()
                #Divide the current size with our total to get % left
                currval = float(currsize) / float(self.TotalJobs)
                #Some rounding and multiplying to get us up to xxx number
                currval = float(round(currval, 4) * 100)
                #lets take our % left minus 100 to get percent done
                percentdone = 100 - currval
                
                self.PrintQueue.put("ProgressThread: Jobs Completed: "+str(percentdone)+"%")
            
            if self.stopped():
                self.PrintQueue.put("ProgressThread: Breaking..")
                break
            
                
    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()
            
        