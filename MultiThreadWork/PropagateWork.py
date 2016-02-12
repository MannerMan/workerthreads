#!/usr/bin/env python
# -*- coding: utf-8 -*-

#system imports
import Queue
import time

class PropagateWork():
    def __init__(self, SafePrint, WorkerThreads, InterruptWatch, CheckProgress):
        
        #Instance PrintQueue
        self.PrintQueue = Queue.Queue('PrintQueue')
        
        #Instance JobQueue
        self.JobQueue = Queue.Queue('JobQueue')
        
        #Instance SafePrint Here
        self.SafePrint = SafePrint(self.PrintQueue)
        #Instance Checkprogress
        self.CheckProgress = CheckProgress(self.PrintQueue, self.JobQueue)
        
        self.WorkerThread = WorkerThreads
        self.InterruptWatch = InterruptWatch
        
        #Instance list of Threads
        self.ThreadInstanceList = []
        
    def BeginWork(self, num_threads, SpawnDelay, WorkFunction, *args):
        self.WorkFunction = WorkFunction
        
        #start SafePrint
        self.SafePrint.start()
        
        #Start CheckProgress
        self.CheckProgress.start()

        #For the number of threads in our num_thread variable
        for ThreadNr in range(num_threads):
            #Instance Workerthread and feed it with printqueue, Jobqueue, and a number
            WorkerThread = self.WorkerThread(self.PrintQueue, self.JobQueue, ThreadNr)
            #Now load our Workerthread instance with the function we want to run, plus any extra arguments
            WorkerThread.load_function(self.WorkFunction, *args)
            #Sleep some to create even load
            time.sleep(SpawnDelay)
            #Now start the thread
            WorkerThread.start()
            #And add this instance to our list of threads, we can then use this to stop our threads if needed
            self.ThreadInstanceList.append(WorkerThread)
        
        #Instance InterruptWatch, give it PrintQueue for printing, JobQueue so it can know when to exit clean, 
        #and instances of WorkerThreads & SafePrint so it can kill these threads if requested or if JobQueue is empty 
        InterruptWatch = self.InterruptWatch(self.PrintQueue, self.ThreadInstanceList, self.CheckProgress, self.SafePrint, self.JobQueue)
        
        #Start Interruptwatch
        InterruptWatch.start()

    def PopulateJobQueue(self, ListOfJobs):
        print "Populating Job Queue.."
        for Job in ListOfJobs:
            self.JobQueue.put(Job)