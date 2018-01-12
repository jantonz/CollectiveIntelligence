# -*- coding: utf-8 -*-
"""
Collective Intelligence

Chapter 2: Making recommendations
"""
# Nested dictionary of movie critics and their ratings of a small set of movies
critics={"Lisa Rose": {"Lady in the Water": 2.5, "Snakes on a Plane": 3.5, "Just My Luck": 3.0, "Superman Returns": 3.5, "You, Me and Dupree": 2.5, "The Night Listener": 3.0}, "Gene Seymour": {"Lady in the Water": 2.5, "Snakes on a Plane": 3.5, "Just My Luck": 1.5, "Superman Returns": 5.0, "The Night Listener": 3.0, "You, Me and Dupree": 3.5}, "Michael Philipps": {"Lady in the Water": 2.5, "Snakes on a Plane": 3.0, "Superman Returns": 3.5, "The Night Listener": 4.0, "You, Me and Dupree": 2.5}, "Mick LaSalle": {"Lady in the Water": 3.0, "Snakes on a Plane": 3.5, "Just My Luck": 2.0, "Superman Returns": 3.0, "The Night Listener": 3.0, "You, Me and Dupree": 2.0}, "Jack Mathews": {"Lady in the Water": 3.0, "Snakes on a Plane": 4.0, "The Night Listener": 3.0, "Supermant Returns": 5.0, "You, Me and Dupree": 3.5}, "Toby": {"Snakes on a Plane": 4.5, "You, Me and Dupree": 1.0, "Superman Returns": 4.0}}


## Euclidean distance score
#This returns a distance-based similarity score for person1 and person2

# Equation of Euclidean distance:

from math import sqrt

def sim_distance(prefs, person1, person2):
    # "prefs" is the dictionary name 
    # Get the list of shared items (si)
    si = {}
    for item in prefs[person1]:
        if item in prefs[person2]:
            si[item] = 1
    
    # If they have no item in comon, return 0
    if len(si)==0: return 0
   
    # Add up the squares of all the differences
    sum_of_squares = sum([pow(prefs[person1][item]-prefs[person2][item], 2) 
                        for item in prefs[person1] if item in prefs[person2]])
    return 1 / (1 + sqrt(sum_of_squares))
    # The list of shared items "si" has not been used so far
    
## Pearson correlation score
# This returns the Pearson correlation coefficient between p1 and p2

# Equation of Pearson score:
    
def sim_pearson(prefs, p1, p2):
    # "prefs" is the dictionary name
    # Get the list of shared items (si)
    si = {}
    for item in prefs[p1]:
        if item in prefs[p2]:
            si[item] = 1
    
    # Find the number of similar elements         
    n = len(si)
    
    # If the number of similar elements (ratings in common) is 0, return 0
    if n == 0: return 0
    
    # Add up all the preferences
    sum1 = sum([prefs[p1][it] for it in si])
    sum2 = sum([prefs[p2][it] for it in si])
    
    # Sum up the squares
    sum1Sq = sum([pow(prefs[p1][it], 2) for it in si])
    sum2Sq = sum([pow(prefs[p2][it], 2) for it in si])

    # Sum up the products
    pSum = sum([prefs[p1][it] * prefs[p2][it] for it in si])
    
    # Calculate Pearson score
    num = pSum - (sum1 * sum2 / n) # numerator
    den = sqrt((sum1Sq - pow(sum1, 2)/n) * (sum2Sq - pow(sum2, 2)/n)) # denominator
    if den == 0: return 0
    
    r = num / den
    
    return r

## Ranking the critics