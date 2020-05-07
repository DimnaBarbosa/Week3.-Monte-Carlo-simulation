import matplotlib.pyplot as plt
from numpy.random import seed
from numpy.random import rand
import numpy as np
import random as rm
import random

# TASK 1: Introduction to Monte Carlo Simulations
# generate 10 random numbers
seed(1)
values1 = rand(10)
values1y = values1 + 1

# generate 1000 random numbers
seed(1)
values2 = rand(1000)
values2y = values2 + 1

# generate 100000 random numbers
seed(1)
values3 = rand(100000)
values3y = values3 + 1

plt.scatter(values1y, values1, c='green')
plt.xlabel('Xi+1')
plt.ylabel('Xi')
plt.title('10 random numbers')
plt.show()

plt.scatter(values2y, values2, c='red')
plt.xlabel('Xi+1')
plt.ylabel('Xi')
plt.title('1000 random numbers')
plt.show()

plt.scatter(values3y, values3, c='blue')
plt.xlabel('Xi+1')
plt.ylabel('Xi')
plt.title('100,000 random numbers')
plt.show()


# function to calculate atom decay and survival on a duration of time
def atomDecay(atoms_t0, duration, hl):

    x_axis = np.arange(start=1, stop=duration, step=1)

    decayed = []
    decay = [0]
    survived = [1] * atoms_t0
    total_atoms = len(survived)
    survive = [total_atoms]

    for i in x_axis:
        atomnumber = []
        a = 0
        while a < total_atoms:
            atomnumber.append(random.random())
            a += 1
        p = (1 - (2 ** ((-i) / hl)))
        for b in atomnumber:
            if b > p:
                decayed.append(1)
                survived.pop(-1)
            else:
                pass

        decay.append(len(decayed))
        survive.append(len(survived))
        total_atoms = len(survived)

    print("Number of atoms at t=0: ", atoms_t0)
    print("Half-life: ", hl)
    print("Duration of the experiment: ", duration)

    x = np.arange(start=0, stop=duration, step=1)
    #decay
    plt.plot(x, decay, c='green', label="decay")
    #survival
    plt.plot(x, survive, c='orange', label="survival")
    plt.xlabel('Time')
    plt.ylabel('Number of atoms')
    plt.title('Atom decay and survival over time')
    plt.legend()
    plt.show()

# 3 simulations for each number of atoms
for i in range(3):
    atomDecay(25, 12, 5)
    atomDecay(250, 12, 5)
    atomDecay(5000, 12, 5)

# The difference between the repetitions of each number is small. The change it the curves for each repetition
# is bigger for lesser amount of atoms (so for 25 atoms than for 5000). The difference between repetitions occurs
# in the decay rates between 1rst and 3rf half life. These differences are clearly noticeable for 25 and 250 atoms
# and very lightly noticeable for 5000 atoms.

# TASK 2: Poker Face
# code partially from https://code.sololearn.com/cDuQ8Is5DO6q/#py
# create deck of cards
suits = ['clubs', 'diamonds', 'hearts', 'spades']
values = ['A', 2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K']


# random cards
def randomcard():
    randomsuit = random.choice(suits)
    randomvalue = random.choice(values)
    return [str(randomvalue), randomsuit]


# value and suit of the card
def cardvalue(card):
    return card[0]

def cardsuit(card):
    return card[1]

def flush(ourhand):
    ourhandsuit = []
    for card in ourhand:
        ourhandsuit.append(card[1])
    if ourhandsuit[1:] == ourhandsuit[:-1]:
        return True
    else:
        return False


# detect if values are present more than once, useful for pairs, 3 of a kind, four of a kind, full house
def valuesduplicated(ourhand):
    valueslist = []
    for card in ourhand:
        valueslist.append(card[0])

    counted = []
    checked = []
    for value in valueslist:
        if value not in checked:
            checked.append(value)
            if valueslist.count(value) == 2:
                counted.append([value, 2])
            if valueslist.count(value) == 3:
                counted.append([value, 3])
            if valueslist.count(value) == 4:
                counted.append([value, 4])

    return counted

# differentiate between hands having duplicated values: one pair, 2 pairs, 3 of a kind, four of a kind, full house
def storedupval(ourhand):
    duplist = valuesduplicated(ourhand)

    if len(duplist) == 0:
        return False

    if len(duplist) == 1:
        for listlist in duplist:
            if listlist[1] == 4:
                return 'FOUR OF A KIND'
            if listlist[1] == 3:
                return 'THREE OF A KIND'
            if listlist[1] == 2:
                return 'PAIR OF ' + str(listlist[0]) + 's'

# could be two pairs or a a full house (one pair and 3 of a kind)
    if len(duplist) == 2:
        for listlist in duplist:
            if listlist[1] == 3:
                return 'FULL HOUSE'

        twopairs = []
        for listlist in duplist:
            pair = str(listlist[0]) + 's'
            twopairs.append(pair)
        return 'TWO PAIRS OF ' + twopairs[0] + ' AND ' + twopairs[1]

# for poker hand straight, order of cards is important
def order_card_values(hand, values):
    ordered_hand = []
    for value in values:
        for card in hand:
            try:
                if int(card[0]) == value:
                    ordered_hand.append(card)
            except ValueError:

                if card[0] == value:
                    ordered_hand.append(card)
    return ordered_hand


def stringvalues(ordered_hand):
    player_values = []
    for card in ordered_hand:
        player_values.append(str(card[0]))

    lowaces = ''.join(player_values)

    trailaces = ''
    for letter in lowaces:
        if letter == 'A':
            trailaces += 'A'
    highaces = lowaces[len(trailaces):] + trailaces
    return [lowaces, highaces]

def straight():
    valorder = stringvalues(ordered_hand)
    for string in valorder:
        if string in 'A2345678910JQKA':
            return True
    else:
        return False

def highcard(ourhand):
    revval = values[::-1]
    for value in revval:
        for card in ourhand:
            if card[0] == 'A':
                return 'HIGH CARD ACE'
            if card[0] == value:
                return 'HIGH CARD ' + str(value)

# indicates type of hand. straight flush is the best (same suit and straight)
def indicatehand(ourhand):
    handdup = storedupval(ourhand)
    if straight() and flush(ourhand):
        return 'STRAIGHT FLUSH'
    elif handdup == 'FOUR OF A KIND':
        return 'FOUR OF A KIND'
    elif handdup == 'FULL HOUSE':
        return 'FULL HOUSE'
    elif flush(ourhand):
        return 'FLUSH'
    elif straight():
        return 'STRAIGHT'
    elif handdup == 'THREE OF A KIND':
        return 'THREE OF A KIND'
    elif handdup:
        return handdup
    else:
        return highcard(ourhand)


for i in range(100):
    # draw 5 cards
    i = 0
    hand = []
    while i < 5:
        drawncard = randomcard()
        hand.append(randomcard())
        i = i + 1
    print("You got:")
    for i in range(5):
        print(hand[i][0], "of", hand[i][1])
    ordered_hand=order_card_values(hand,values)
    print("You got: " + str(indicatehand(hand)))

# could not figure out how to implement the probabilities in this exercise

# TASK 3: Markov Chain Monte Carlo
# using a Markov chain for weather prediction

# possible events
states = ["Sunny", "Rainy"]
# possible sequence of events
possibleSequence = ["SS", "SR"], ["RR", "RS"]
# probabilities matrix
transitionMatrix = [[0.9, 0.1], [0.5, 0.5]]
transitionMatrix2 = [[0.8, 0.2], [0.4, 0.6]]

# function to implement Markov model, reference: http://firsttimeprogrammer.blogspot.com/2014/08/weather-forecast-through-markov-chains.html
def weatherForecast(days,transitionM):
    #weather for the starting day is chosen randomly. Starting day is not included in the 14 day forecast
    weatherToday = rm.choice(states)
    i = 0
    timessunny = 0
    print("Starting weather: ", weatherToday)
    while i < days:
        if weatherToday == "Sunny":
            change = np.random.choice(possibleSequence[0],replace=True,p=transitionM[0])
            if change == "SS":
                timessunny = timessunny + 1
                pass
            else:
                weatherToday = "Rainy"
        elif weatherToday == "Rainy":
            change = np.random.choice(possibleSequence[1],replace=True,p=transitionM[1])
            if change == "RR":
                pass
            else:
                weatherToday = "Sunny"
                timessunny = timessunny + 1
        print(weatherToday)
        i += 1
        #time.sleep(0.1)
    print("Sunny days: ", timessunny)
    return timessunny


sunnydays = []
differentM = []
# 50 simulations of forecasted weather for 14 days
for x in range(50):
    sunnydays.append(weatherForecast(14,transitionMatrix))
    differentM.append(weatherForecast(14,transitionMatrix2))
print(sunnydays)

# average days of sun and rain as number of simulations increases (gets accumulated)
averagesunny = np.full(shape=50, fill_value=0, dtype=np.int)
averagesunny2 = np.full(shape=50, fill_value=0, dtype=np.int)

averagerainy = np.full(shape=50, fill_value=0, dtype=np.int)
averagerainy2 = np.full(shape=50, fill_value=0, dtype=np.int)
sumday = 0
sumday2=0
simulation = 1

for i in range(50):
    sumday = sumday + sunnydays[i]
    averagesunny[i] = sumday/simulation
    rainydays = 14*simulation-sumday
    averagerainy[i] = rainydays/simulation

    sumday2 = sumday2 + differentM[i]
    averagesunny2[i] = sumday2/simulation
    rainydays2 = 14 * simulation - sumday2
    averagerainy2[i] = rainydays2 / simulation
    simulation = simulation + 1

print("Cumulative average of sunny days per simulation:", averagesunny)
print("Cumulative average of rainy days per simulation:", averagerainy)
print("Cumulative average of sunny days per simulation (2):", averagesunny2)
print("Cumulative average of rainy days per simulation (2):", averagerainy2)


# Plot the average number of Sunny and Rainy days on the y-axis and the number of simulations run so far on the x-axis
# plots for values obtained using predetermined matrix and modified matrix (2)
x1 = np.linspace(1, 50)
plt.plot(x1, averagesunny, c='blue', label="sunny average")
plt.plot(x1, averagerainy, c="green", label="rainy average")
plt.plot(x1, averagesunny2, c='red', label="sunny average2")
plt.plot(x1, averagerainy2, c="purple", label="rainy average2")

plt.xlabel('Number of simulation')
plt.ylabel('Average weather')
plt.title('Cumulative average of sunny and rainy days vs. number of simulations')
plt.legend()
plt.show()

# Making small amendment (+/- 0.1) on the probabilities ([[0.9, 0.1], [0.5, 0.5]] to [[0.8, 0.2], [0.4, 0.6]]) changes the outcome
# relatively little. The averages for both sets of probabilities coincide for many simulations, but at some points, differ by 1 day.
# For the first few simulations, the averages have bigger differences but very quickly the averages become closer and even equal.
# This indicates that even small modifications to the probabilities will change the outcome. Bigger modifications in prob. will entail bigger changes in outcome.