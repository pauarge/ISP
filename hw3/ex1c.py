import pandas as pd
import datetime

names = ['email', 'movie', 'date', 'rating']
date_format = "%d/%m/%y"
threshold = 13


def get_dates(date, days):
    before = datetime.datetime.fromtimestamp(date) - datetime.timedelta(days=days)
    after = datetime.datetime.fromtimestamp(date) + datetime.timedelta(days=days)
    return int(before.timestamp()), int(after.timestamp())


def main():
    imdb = pd.read_csv("data/imdb-3.csv", names=names, quotechar='"', skipinitialspace=True)
    imdb['date'] = imdb['date'].apply(lambda r: int(datetime.datetime.strptime(r, date_format).timestamp()))

    dedis = pd.read_csv("data/dedis-3.csv", names=names, quotechar='"', skipinitialspace=True)
    dedis['date'] = dedis['date'].apply(lambda r: int(datetime.datetime.strptime(r, date_format).timestamp()))

    myimdb = imdb.loc[imdb['email'] == "pau.argelaguet@epfl.ch"]
    users = pd.DataFrame({'count': dedis.groupby('email').size()}).reset_index()['email']
    for row in myimdb.itertuples():
        beforedate, afterdate = get_dates(row.date, threshold)
        rated_in_time = dedis[(dedis['date'] >= beforedate) & (dedis['date'] <= afterdate)]['email']
        users = pd.Series(list(set(users) & set(rated_in_time)))

    movies = pd.DataFrame({'count': imdb.groupby('movie').size()}).reset_index()['movie']
    possible_movies = pd.DataFrame({'count': dedis.groupby('movie').size()}).reset_index()['movie']

    movie_dict = {}
    for movie in movies:
        intersect = possible_movies.copy()
        for row in imdb.loc[imdb['movie'] == movie].itertuples():
            beforedate, afterdate = get_dates(row.date, threshold)
            rated_in_time = dedis[(dedis['date'] >= beforedate) & (dedis['date'] <= afterdate)]['movie']
            intersect = pd.Series(list(set(intersect) & set(rated_in_time)))
        movie_dict[intersect[0]] = movie

    my_movies = dedis.loc[dedis['email'] == users[0]]['movie']
    for i, m in my_movies.iteritems():
        my_movies.at[i] = movie_dict[my_movies.at[i]]
    my_movies.to_csv("data/my-movies-3.csv", index=False)


if __name__ == '__main__':
    main()
