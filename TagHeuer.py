"""
~~~ Tag Heuer Time Module ~~~

               🟥🟥🟥🟥🟥
            🟥🟥🟥🟥🟥🟥🟥🟥🟥
         🟫🟫🟫🟨🟨⬛🟨
      🟫🟨🟫🟨🟨🟨⬛🟨🟨🟨
      🟫🟨🟫🟫🟨🟨🟨⬛🟨🟨🟨
        🟫🟨🟨🟨🟨⬛⬛⬛⬛
          🟨🟨🟨🟨🟨🟨🟨

This module takes inspiration from the iconic Tag Heuer Formula 1 Mario Kart
[https://www.tagheuer.com/us/en/timepieces/collections/tag-heuer-formula-1/44-mm-calibre-16-automatic/CAZ201E.FC6517.html]

The Tag Heuer Time Module is helpful to measure performance within other programs. 
It helps us reduce our functions' time complexity and maximize computation efficiency.
Time is precious. Always create software with this in mind. 

TODO
Look into decorators and wrappers
"""
import time 
import cProfile
import random

# func_times = { "function name" : [START, END, RUNTIME] }
START   = 0
END     = 1
RUNTIME = 2

class TimeTracker:
    func_times = {} 
    time_zero  = 0

    def __init__(self):
        """ Constructor """
        self.func_times = {}
        self.time_zero  = time.time()

    
    def start(self, func_name : str) -> None:
        """ Records function start time """
        now = time.time() - self.time_zero
        self.func_times[func_name] = [now, None, None]
    

    def end(self, func_name : str) -> None:
        """ Records function end time """
        now = time.time() - self.time_zero
        try:
            this = self.func_times[func_name]
            this[END] = now
            this[RUNTIME] = this[END] - this[START]
        except KeyError:
            print("ERROR - Invalid function name passed to func_end.\nFunction name does not exist in func_times.\nMake sure to use func_start first")
            exit(1)

    
    def report(self) -> None:
        """ Creates and prints a report of all registered functions' runtimes """
        TUP_RUNTIME = 0
        TUP_NAME    = 1
        # runtimes = [(runtime_1, func_1), (runtime_2, func_2), etc.]
        runtimes    = [] 
        total       = 0

        # Get info from each function
        for f, times in self.func_times.items():
            # Skip incomplete functions
            if times[RUNTIME] is None:
                continue

            # For complete functions
            this_runtime = times[RUNTIME]
            total += this_runtime
            runtimes.append((this_runtime, f))
        
        # Prepare report
        REPORT_WIDTH = 70
        sep_line = "-" * REPORT_WIDTH
        mid_sep_line = "|" + "-" * 32 + "+" + "-" * 12 + "+" + "-" * 22 + "|"
        # print title
        print("\n~~~ Time Tracker Report ~~~\n")
        # print header
        name_header = "FUNCTION NAME"
        weight_header = "WEIGHT (%)"
        runtime_header = "RUNTIME (sec)"
        print(sep_line)
        print(f"| {name_header:^30} | {weight_header:^9} | {runtime_header:^20} |")
        print(mid_sep_line)


        # print elements
        runtimes.sort(reverse = True)
        for tup in runtimes:
            # get and format name
            name = tup[TUP_NAME]
            if len(name) > 30:
                name = name[:27] + "..."
            # get and format runtime
            runtime = tup[TUP_RUNTIME]
            runtime = int(round(runtime, 0))
            # get weight of total time in %
            if total == 0:
                total = 1
            weight = tup[TUP_RUNTIME] / total * 100
            weight = int(round(weight, 0))
            # print row
            print(f"| {name:<30} |  {weight:^9} | {runtime:20} |")
        
        # print total row
        total_header = "TOTAL"
        total = int(round(total, 0))
        print(mid_sep_line)
        print(f"| {total_header:>30} | {100:^10} | {total:>20} |")
        print(sep_line)


    def compare(self, f1 : str, f2 : str, input_size=0 ) -> None:
        """ 
        Compares the performance of 2 functions. 
        Useful to test 2 implementations of the same solution. 
        """ 
        try:
            f1_time = self.func_times[f1][RUNTIME]
        except:
            print(f"ERROR : Provided wrong function {f1} to TimeTracker.compare(f1, f2)")
            exit(1)
        
        try:
            f2_time = self.func_times[f2][RUNTIME]
        except:
            print("ERROR : Provided wrong function f2 to TimeTracker.compare(f1, f2)")
            exit(1)

        if f1_time is None or f2_time is None:
            print("ERROR : From TimeTracker.compare() --> f1 and/or f2 does not have a runtime yet. ")
            exit(1)
        
        print(f"\n~~~ Comparing {f1} to {f2} ~~~\n")
        # Assume f1 is slow
        fast = f2
        slow = f1
        fast_time = f2_time
        slow_time = f1_time

        # Change if f1 is fast
        if f1_time < f2_time:
            fast = f1
            slow = f2
            fast_time = f1_time
            slow_time = f2_time

        if fast_time == 0:
            fast_time = 1

        if slow_time == 0:
            slow_time = 1
        
        # % faster
        percent_faster = abs(((fast_time - slow_time) / slow_time) * 100)
        percent_faster = int(round(percent_faster, 0))

        # % slower
        percent_slower = abs(((slow_time - fast_time) / fast_time) * 100)
        percent_slower = int(round(percent_slower, 0))

        if input_size != 0:
            print(f"Input size:")
            print(f"n = {input_size}\n")
        print(f"How much faster is {fast}:")
        print(f"{fast} is {percent_faster}% faster\n")
        print(f"How mush slower is {slow}:")
        print(f"{slow} is {percent_slower}% slower\n")


            
        

        


        

        


