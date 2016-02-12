#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time

#my imports
import MultiThreadWork

#Settings
num_threads = 2
thread_start_delay = 2

somevar = 3
ListOfJobs = ['job1', 'job2', 'job3', 'job4', 'job5']

def WorkerFunction(job, somevar):
	#Just sleep
	time.sleep(somevar)

#Instance propagate work so we can send jobs to threads
#Feed it with SafePrint, WorkerThread, InterruptWatch and ProgressCheck
PropagateWork = MultiThreadWork.PropagateWork.PropagateWork(
    MultiThreadWork.SafePrintThread.SafePrintThread,
    MultiThreadWork.WorkerThread.WorkerThread,
    MultiThreadWork.InterruptWatch.InterruptWatch,
    MultiThreadWork.ProgressCheckThread.ProgressCheckThread
    )

#Populate our JobQueue With our ListOf Jobs
PropagateWork.PopulateJobQueue(ListOfJobs)

#Now, begin our work. We give BeginWork the number of threads we want to spawn, delay between spawns, and what function to trigger (WorkerFunction..)
#everything after that will be passed as arguments to our "WorkerFunction". 
PropagateWork.BeginWork(num_threads, thread_start_delay, WorkerFunction, somevar)

#use this instead to dump to file
#PgDumpToFile.Roles(PgDumpIp, PgDumpUser)
#PropagateWork.BeginWork(num_threads, thread_start_delay, PgDumpToFile.Schema, PgDumpIp, PgDumpUser)
