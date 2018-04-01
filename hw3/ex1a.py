import pandas as pd

names = ['email', 'movie', 'date', 'rating']


def main():
    imdb = pd.read_csv("data/imdb-1.csv", names=names, quotechar='"', skipinitialspace=True)
    dedis = pd.read_csv("data/dedis-1.csv", names=names, quotechar='"', skipinitialspace=True)

    grouped_users_imdb = [imdb.iloc[v] for _, v in imdb.groupby(['email']).groups.items()]
    grouped_users_dedis = [dedis.iloc[v] for _, v in dedis.groupby(['email']).groups.items()]

    movies = {}
    me = ""

    for it, i in enumerate(grouped_users_imdb):
        print("Processing {} of {}".format(it, len(grouped_users_imdb)))
        for d in grouped_users_dedis:
            m = i.merge(d, on=['date', 'rating']).drop_duplicates()
            if len(m) == len(i.drop_duplicates()):
                if m.iloc[0].email_x == 'pau.argelaguet@epfl.ch':
                    print("My username is {}".format(m.iloc[0].email_y))
                    me = m.iloc[0].email_y
                for index, row in m.iterrows():
                    movies[row.movie_y] = row.movie_x
                break

    my_movies = dedis.loc[dedis['email'] == me]['movie']
    for i, m in my_movies.iteritems():
        my_movies.at[i] = movies[my_movies.at[i]]

    my_movies.to_csv("data/my-movies-1.csv", index=False)


if __name__ == '__main__':
    main()
