import colorama as cl
from functions import *
from simulator import *

if __name__ == '__main__':
    
    rtn = initialize_system()

    if rtn == 1:
        print("Starting local execution...")
        #TODO code functions for local execution and execute them here.
    elif rtn == 2:
        while True:
            print(cl.Style.BRIGHT + "Want to enter developer mode and execute the simulator?(Y/N) ",end='')
            ans = str(input())
            if (ans.lower() == 'y'): 
                print(cl.Fore.YELLOW + "Starting simulator...")
                run_sim()
                break
            elif ans.lower() == 'n':
                print("Exiting program...")
                break
            else:
                print("...invalid input...")
