# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from data_process import Data
import scoring
import json
import re
import random


def score():

    # hyperRED
    # how to score
    path_gold = "data/Datasets/HyperRED-Temporal/test.json"
    path_pred = "data/HyperRED-Temporal results/TSDRE.json"
    scoring.score_preds(path_pred, path_gold)


def main():
    score()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
