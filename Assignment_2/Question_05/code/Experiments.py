from experiment_6_7 import experiment as exp1
from experiment_6_8 import experiment as exp2
from experiment_6_9 import experiment as exp3
from utils import printResult

def main():
    seperator = "\n"+"="*80+"\n" 
    print(seperator)
    print("\n"+" "*35 + "Experiment 6.7\n")
    printResult(exp1()) 

    print(seperator)
    print("\n"+" "*35 + "Experiment 6.7\n")
    printResult(exp2()) 

    print(seperator)
    print("\n"+" "*35 + "Experiment 6.7\n")
    printResult(exp3()) 

if __name__=="__main__":
    main()