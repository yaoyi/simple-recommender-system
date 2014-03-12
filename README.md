simple-recommender-system
=========================

This simple recommender system is implemented to evaluate the 
user-based collaborative filtering with Pearson correlation coefficient.

the dataset we use

books: http://nifty.stanford.edu/2011/craig-book-recommendations/books.txt

ratings: http://nifty.stanford.edu/2011/craig-book-recommendations/ratings.txt

For each user in the data set, first two books will be used as test set. TWO types of predictions will be generated:

* Use the mean rating of that book as the predicted rating
* Use the scripts according to the instructions above to generate a predicted rating, with the size of neighbourhood equals to 5
* Repeat above, except that the size of the neighbourhood is 10

In the end, the RMSE (root mean squared error) for these three types of predictions will be the output to evaluate the algorithm.
