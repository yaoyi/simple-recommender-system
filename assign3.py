import inspect
from math import sqrt

def lineno():
    """Returns the current line number in our program."""
    return inspect.currentframe().f_back.f_lineno

#Returns the best matches for person from the prefs dictionary
#Number of the results and similiraty function are optional params.
def getNeighbours(prefs,person,n=5):
    scores = [(similarity(prefs,person,other),other)
                for other in prefs if other != person]
    scores.sort()
    scores.reverse()
    return scores[0:n]

def similarity(prefs,p1,p2):
    #Get the list of mutually rated items
    si = {}
    for item in prefs[p1]:
        if item in prefs[p2]: 
            si[item] = 1

    #if they are no rating in common, return 0
    if len(si) == 0:
        return 0

    # print si
    #sum calculations
    n = len(si)

    #sum of all preferences
    sum1 = sum([prefs[p1][it] for it in si])
    sum2 = sum([prefs[p2][it] for it in si])

    #Sum of the squares
    sum1Sq = sum([pow(prefs[p1][it],2) for it in si])
    sum2Sq = sum([pow(prefs[p2][it],2) for it in si])

    #Sum of the products
    pSum = sum([prefs[p1][it] * prefs[p2][it] for it in si])

    #Calculate r (Pearson score)
    num = pSum - (sum1 * sum2/n)
    den = sqrt((sum1Sq - pow(sum1,2)/n) * (sum2Sq - pow(sum2,2)/n))
    if den == 0:
        return 0

    r = num/den

    return r

def convertScale(rating):
    scale = {
        '0': -1,
        '-5': 0.00,
        '-3': 0.25,
        '1': 0.50,
        '3': 0.75,
        '5': 1.00,
    }
    return scale[rating]


def loadDataset(path=""):
    """ To load the dataSet"
        Parameter: The folder where the data files are stored
        Return: the dictionary with the data
    """
    #Recover the titles of the books
    books = []
    for line in open(path+"books_list.txt"):
        line  = line.strip('\n').strip()
        books.append(line)
    #Load the data
    prefs = {}
    count = 0
    odd = 1
    for line in open(path+"books_ratings.txt"):
        line  = line.strip('\n').strip()

        if odd == 1:
            user = line
            odd = 0
            continue 
        ratings = line.split(" ")
        new_ratings = {}
        bookid = 0
        for rating in ratings:
            new_ratings[books[bookid]] = convertScale(rating)
            bookid += 1
        prefs[user] = new_ratings
        odd = 1
    return prefs

if __name__ == '__main__':
    prefs = loadDataset("")
    print getNeighbours(prefs, "Ben")
    # similarity(prefs, "Ben", "Reuven")
