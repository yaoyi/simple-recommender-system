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
    books = []
    for line in open(path+"books_list.txt"):
        line  = line.strip('\n').strip()
        books.append(line)
    #Load the data
    testPrefs = {}
    prefs = {}
    users = []
    
    index = 1
    userid = 0
    for line in open(path+"books_ratings.txt"):
        line  = line.strip('\n').strip()
        if index % 2 == 1:
            users.append(line)
            index += 1
            continue 
        ratings = line.split(" ")
        testRatings = {}
        allRatings = {}
        count = 0
        bookid = 0
        valid = 0
        for rating in ratings:
            if rating != '0' and count < 2:
                testRatings[bookid] = convertScale(rating)
                allRatings[bookid] = convertScale(rating)
                count += 1
            else:
                if rating != '0':
                    valid = 1
                allRatings[bookid] = convertScale(rating)
            bookid += 1
        if valid == 1:
            testPrefs[userid] = testRatings
        prefs[userid] = allRatings
        userid += 1
        index += 1
    return testPrefs,prefs,users,books

def predict(prefs, userid, bookid, neighbours):
    sumSim = 0
    for sim, uid in neighbours:
        sumSim += sim
    weight = {}
    rating = 0
    for sim, uid in neighbours:
        weight[uid] = sim/sumSim
        if bookid in prefs[uid].keys():
            if prefs[uid][bookid] != -1:
                rating += prefs[uid][bookid] * weight[uid]
    return rating

def generateTrainPrefs(prefs, userid, items):
    for key in items.keys():
        prefs[userid][key] = 0
    return prefs

def rmse(predictRatings, realRatings):
    predictRatingList = []
    for userid, item in predictRatings.items():
        for itemid, value in item.items():
            predictRatingList.append(value)

    realRatingList = []
    for userid, item in realRatings.items():
        for itemid, value in item.items():
            realRatingList.append(value)
    print zip(predictRatingList, realRatingList)
    return sqrt(sum([(f - o) ** 2 for f, o in zip(predictRatingList, realRatingList)]) / len(predictRatingList))


if __name__ == '__main__':
    testPrefs,prefs,users,books = loadDataset("")
    rating = {}
    for userid in testPrefs.keys():
        trainPrefs = generateTrainPrefs(prefs, userid, testPrefs[userid])
        neighbours = getNeighbours(trainPrefs, userid, 20)
        rating.setdefault(userid, {})
        for bookid in testPrefs[userid].keys():
            rating[userid][bookid] = predict(trainPrefs, userid, bookid, neighbours)
    
    print rmse(rating, testPrefs)
    
    
