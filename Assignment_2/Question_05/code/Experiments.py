from experiment_6_7 import experiment as exp1
from experiment_6_8 import experiment as exp2
from experiment_6_9 import experiment as exp3
from utils import printResult, printLabel

def main():
    printLabel("Experiment 6.7")
    printResult(exp1()) 

    printLabel("Experiment 6.8")
    printResult(exp2()) 

    printLabel("Experiment 6.9")
    printResult(exp3()) 

if __name__=="__main__":
    main()