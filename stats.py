#!/usr/bin/env python

import shutil

import cards


all_cards = cards.load_cards()

cards.count_colors(all_cards)

print("Number of cards:")
print(len(all_cards))
