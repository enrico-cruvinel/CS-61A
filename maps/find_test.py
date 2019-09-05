from abstractions import *
from data import ALL_RESTAURANTS, CATEGORIES, USER_FILES, load_user_file
from ucb import main, trace, interact
from utils import distance, mean, zip, enumerate, sample
from visualize import draw_map

user = make_user('Cheapskate', [
     make_review('A', 2),
     make_review('B', 5),
     make_review('C', 2),
     make_review('D', 5),
    ])
cluster = [
    make_restaurant('A', [5, 2], [], 4, [
    make_review('A', 5)
    ]),
    make_restaurant('B', [3, 2], [], 2, [
        make_review('B', 5)
    ]),
    make_restaurant('C', [-2, 6], [], 4, [
        make_review('C', 4)
    ]),
    make_restaurant('D', [4, 2], [], 2, [
    make_review('D', 3),
    make_review('D', 4)]),
    ]

fns = [restaurant_price, lambda r: mean(restaurant_ratings(r))]

def find_predictor(user, restaurants, feature_fn):
    """Return a rating predictor (a function from restaurants to ratings),
    for a user by performing least-squares linear regression using feature_fn
    on the items in restaurants. Also, return the R^2 value of this model.

    Arguments:
    user -- A user
    restaurants -- A sequence of restaurants
    feature_fn -- A function that takes a restaurant and returns a number
    """
    xs = [feature_fn(r) for r in restaurants]
    ys = [user_rating(user, restaurant_name(r)) for r in restaurants]

    # BEGIN Question 7
    "*** YOUR CODE HERE ***"
    s_xx = sum([(xi - mean(xs))**2 for xi in xs])
    s_yy = sum([(yj - mean(ys))**2 for yj in ys]) 

    t = zip([(xi - mean(xs)) for xi in xs], [(yj - mean(ys)) for yj in ys])
    
    s_xy = sum([i*j for i,j in t])
    
    b = s_xy/s_xx
    a = mean(ys) - b * mean(xs)
    r_squared = (s_xy**2)/(s_xx*s_yy) 
    # END Question 7

    def predictor(restaurant):
        return b * feature_fn(restaurant) + a

    return predictor, r_squared


def best_predictor(user, restaurants, feature_fns):
    """Find the feature within feature_fns that gives the highest R^2 value
    for predicting ratings by the user; return a predictor using that feature.

    Arguments:
    user -- A user
    restaurants -- A list of restaurants
    feature_fns -- A sequence of functions that each takes a restaurant
    """
    reviewed = user_reviewed_restaurants(user, restaurants)
    # BEGIN Question 8
    "*** YOUR CODE HERE ***"
    predictions = [find_predictor(user, reviewed, feature) for feature in feature_fns]
    return max(predictions, key = lambda x: x[1])[1]
    # END Question 8


pred = best_predictor(user, cluster, fns)
