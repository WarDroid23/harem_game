# utils/random_utils.py
import random

def nahodny_vyber(seznam):
    return random.choice(seznam)

def nahodne_cislo(minimum, maximum):
    return random.randint(minimum, maximum)

def sance(procento):
    return random.random() < procento
