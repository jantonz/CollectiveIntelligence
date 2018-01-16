---
layout: page
title: Chapter 2 - Making recommendations
sidebar_link: true
---

### Summary

This is the implementation of a movie recommendation system. It takes information from a small dictionary with the names of movie critics and their 1-5 star score of several movies; this dictionary also has the user (Toby) 1-5 star score of several movies. A distance score between movie critics is calculated through 2 methods. Critics are ranked for similarity to Toby.

Nested dictionary of movie critics and their ratings of a small set of movies.


```python
critics={"Lisa Rose": {"Lady in the Water": 2.5, "Snakes on a Plane": 3.5, "Just My Luck": 3.0, "Superman Returns": 3.5, "You, Me and Dupree": 2.5, "The Night Listener": 3.0}, "Gene Seymour": {"Lady in the Water": 2.5, "Snakes on a Plane": 3.5, "Just My Luck": 1.5, "Superman Returns": 5.0, "The Night Listener": 3.0, "You, Me and Dupree": 3.5}, "Michael Philipps": {"Lady in the Water": 2.5, "Snakes on a Plane": 3.0, "Superman Returns": 3.5, "The Night Listener": 4.0, "You, Me and Dupree": 2.5}, "Mick LaSalle": {"Lady in the Water": 3.0, "Snakes on a Plane": 3.5, "Just My Luck": 2.0, "Superman Returns": 3.0, "The Night Listener": 3.0, "You, Me and Dupree": 2.0}, "Jack Mathews": {"Lady in the Water": 3.0, "Snakes on a Plane": 4.0, "The Night Listener": 3.0, "Supermant Returns": 5.0, "You, Me and Dupree": 3.5}, "Toby": {"Snakes on a Plane": 4.5, "You, Me and Dupree": 1.0, "Superman Returns": 4.0}}
```

### Euclidean distance score
This returns a distance-based similarity score for person1 and person2 following the equation of Euclidean distance:
$$\sqrt{\sum_{i=1}^{n} (p_{i} - q_{i})^2}$$


```python
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

```

### Pearson correlation score
This returns the Pearson correlation coefficient between p1 and p2 following the equation of Pearson score:
$$r = \frac{\sum XY - \frac{\sum X \sum Y}{N}}{\sqrt{\left( \sum X^2 - \frac{(\sum X)^2}{N}\right)\left(\sum Y^2-\frac{(\sum Y)^2}{N}\right)}}$$



```python
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

```

### Ranking the critics

Returns the best matches for person from the prefs dictionary. Number of results and similarity are optional parameters.



```python
def topMatches(prefs, person, n = 5, similarity = sim_pearson):
    scores = [(similarity(prefs, person, other), other) for other in prefs if other != person]
    
    #Sort the list so the highest scores appear at the top
    scores.sort()
    scores.reverse()
    return scores[0:n]
```

### Recommending items

Gets recommendations for a person by using a weighting average of every other user's rankings.

This code loops through every other person in the prefs dictionary. In each case, it calculates how similar they are to the person specified. It then loops through every item for which they've given a score. The score for each item is multiplied by the similarity and these products are added together. The scores are normalized by dividing by the similarity sum and the sorted results are returned.



```python
def getRecommendations(prefs, person, similarity = sim_pearson):
    totals = {}
    simSums = {}
    for other in prefs:
        # Don't compare it to myself
        if other == person: continue
        sim = similarity(prefs, person, other)
        
        # Ignore scores of zero or lower
        if sim =< 0: continue
        for item in prefs[other]: # Loop through every item
            
            # Only scores movies I haven't seen yet
            if item not in prefs[person] or prefs[person][item] == 0:
                
                # Similarity * Score
                totals.setdefault(item, 0)
                totals[item] += prefs[other][item]*sim
                
                # Sum of similarities
                simSums.setdefault(item, 0)
                simSums[item] += sim # simSums = simSums + sim
                
    # Create the normalized list
    rankings = [(total / simSums[item], item) for item,total in totals.items()]
    
    # Return the sorted list
    rankings.sort()
    rankings.reverse()
    return rankings
```
