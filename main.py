from controller import *
import argparse

#this creates an instance of parser
parser = argparse.ArgumentParser(description="loads shortlist data from role directory")

#creates some argument you can use when running the file
parser.add_argument("rolepath",type=str)

# set the value of the argument parsed in so it can be accessed later 
args = parser.parse_args()

# accesses the rolepath from argument parsed

try:
    control = Controller(args.rolepath)
    control.show_boot_message()
except FileNotFoundError:
    print("Sorry, relevant files cannot be found in the directory, exiting the program...")
