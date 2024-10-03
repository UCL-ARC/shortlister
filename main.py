from controller import *
import argparse

parser = argparse.ArgumentParser(description="loads shortlist data from role directory")

parser.add_argument("rolepath",type=str)

args = parser.parse_args()

control = Controller(args)