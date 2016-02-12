#!/usr/bin/env python
# -*- coding: utf-8 -*-

import threading
import time
from random import randrange

class WorkerThread(threading.Thread):

    def __init__(self, PrintQueue, JobQueue, ThreadNr):
        
        #super init, if this thread is inited from something other than main?
        #super(WorkerThread, self).__init__()
        
        #normal init
        threading.Thread.__init__(self)
        
        self.SafePrint = PrintQueue
        self.thrdnr = ThreadNr
        self.JobQueue = JobQueue
        

    def run(self):
        self.SafePrint.put("WorkerThread-%s: Starting.." % (self.thrdnr))
        self._stop = threading.Event()

        #while not self.stopped():
        while not self.JobQueue.empty():
            try:
                job = self.JobQueue.get(True, 1)
                self.SafePrint.put("WorkerThread-%s: Running Job: %s" % (self.thrdnr, job))
                
                self.WorkFunction(job, *self.args)
                #time.sleep(2)
                
                self.JobQueue.task_done()
                self.SafePrint.put("WorkerThread-%s: Completed Job: %s" % (self.thrdnr, job))
                time.sleep(0.1)
                
                if self.stopped():
                    break
            #except self.JobQueue.Empty:
            #    self.SafePrint.put("WorkerThread-%s: No jobs left" %(self.thrdnr))
            except:
                raise
            
            
        self.SafePrint.put("WorkerThread-%s: Done!" % (self.thrdnr))

        #might be needed.. if no super init..
        #threading.Thread.__init__(self)

    def stop(self):
        self.SafePrint.put("WorkerThread-%s: Stop triggered! Will exit when current job is done" % (self.thrdnr))
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()

    def load_function(self, custom_func, *args):
        self.args = (args)
        self.WorkFunction = custom_func