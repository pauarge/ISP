#!/usr/bin/env python3
import random, datetime, sys, csv
from random import randrange, randint

date_start = datetime.date(2000, 1, 1)
date_period = 365 * 17

# Reads in emails.txt and movies.txt and creates 'nbr_movies' entries for each
# email.
# Returns the database, the emails and the movies in the following format:
# [ [ user, movie, date, grade ], ... ]
def create_db(nbr_movies):
    with open("emails.txt") as f:
        emails = f.read().split("\n");
    while "" in emails:
        emails.remove("")

    with open("movies.txt") as f:
        movies = f.read().split("\n");
    while "" in movies:
        movies.remove("")

    db = []

    for email in emails:
        movies_index = list(range(0, len(movies)))
        random.shuffle(movies_index)
        for i, f in enumerate(movies_index[0:nbr_movies]):
            dat = date_start + datetime.timedelta(randint(1, date_period))
            db.append(
                [email, movies[f], dat.strftime("%Y/%m/%d"), randint(1, 5)])

    return db, emails, movies


# Anonymize the given database, but still let the get_movies_with_rating
# function give the right answers.
def anonymize_1(db):
    return db


# For a given anonymized-database and a rating, this function should return
# the films with the given rating.
def get_movies_with_rating(anon, rating):
    return [anon[0][1], anon[1][1]]


# A bit lesser anonymization than anonymize_1, but still no date. The returned
# database should have enough information to be used by get_top_rated. If you
# use a too simple hashing-function like sha-256, the result will be rejected.
def anonymize_2(db):
    return db


# get_top_rated searches for all users having rated a movie and searches their
# top-rated movie(s). It returns a list of all found movies, also doubles!
def get_top_rated(anon, movie):
    return [anon[0][1]]


# This is called when you start the script on localhost, and when the
# checker wants to run your functions.
if __name__ == "__main__":
    # This part can be modified at your convenience.
    if len(sys.argv) == 1:
        print("Testing mode")
        db, emails, movies = create_db(20)

        anon_db1 = anonymize_1(db)
        print(get_movies_with_rating(anon_db1, 1))

        anon_db2 = anonymize_2(db)
        print(get_top_rated(anon_db2, movies[0]))

    # If you modify this part, don't complain if it doesn't work anymore!
    # This part is used to communicate with the verification-script. So you
    # should not touch it (unless you're looking for a bug to exploit the
    # verification script - but we didn't plan to put one in there).
    if len(sys.argv) >= 3:
        db_file, ex = sys.argv[1:3]
        with open(db_file) as f:
            db = list(csv.reader(f, skipinitialspace=True))
        # Get nice ints for comparisons
        for i, line in enumerate(db):
            db[i][3] = int(line[3])

        result = []
        if ex == "ex1aa":
            result = anonymize_1(db)
        elif ex == "ex1ag":
            rating = int(sys.argv[3])
            result = [get_movies_with_rating(db, rating)]
        elif ex == "ex1ba":
            result = anonymize_2(db)
        elif ex == "ex1bg":
            movie = sys.argv[3]
            result = [get_top_rated(db, movie)]

        with open("/tmp/student.csv", "w") as f:
            writer = csv.writer(f)
            writer.writerows(iter(result))
