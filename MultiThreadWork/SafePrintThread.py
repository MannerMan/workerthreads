#!/usr/bin/env python
# -*- coding: utf-8 -*-

import threading
import time
import datetime

class SafePrintThread(threading.Thread):

    def __init__(self, PrintQueue):
        super(SafePrintThread, self).__init__()
        self.PrintQueue = PrintQueue

    def run(self):
        self.PrintQueue.put("SafePrintThread: Starting..")
        self._stop = threading.Event()
        
        while True:
            time.sleep(0.02)
            
            #If safeprint is stopped
            if self.stopped():
                #Finish off the last messages
                self.PrintQueue.put("SafePrintThread: Stop triggered, finishing up..")
                #while there is stuff to print
                while not self.PrintQueue.empty():
                    #get value from printqueue
                    value = self.PrintQueue.get(True, 1)
                    
                    #Create a timestamp
                    currstamp = str(datetime.datetime.now().strftime('%H:%M:%S.%f'))
                    
                    #Print our timestamp + value 
                    print "["+currstamp[:-3]+"] "+value
                    
                    #mark as done
                    self.PrintQueue.task_done()
                    
                #No more stuff to print, break free
                print "SafePrintThread: No more messages, breaking PrintQueue.."
                #Join to clean exit
                self.PrintQueue.join()
                break
            
            try:
                #get value from printqueue
                value = self.PrintQueue.get(True, 0)
                #Mark as done
                self.PrintQueue.task_done()
            except:
                continue
            
            #Create a timestamp
            currstamp = str(datetime.datetime.now().strftime('%H:%M:%S.%f'))
            #Print our timestamp + value 
            print "["+currstamp[:-3]+"] "+value
        
        print "SafePrintThread: Dying.."

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()