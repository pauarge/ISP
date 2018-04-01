import pandas as pd

names = ['email', 'movie', 'date', 'rating']


def main():
    imdb = pd.read_csv("data/imdb-2.csv", names=names, quotechar='"', skipinitialspace=True)
    dedis = pd.read_csv("data/dedis-2.csv", names=names, quotechar='"', skipinitialspace=True)

    grouped_movies_imdb = [imdb.iloc[v] for _, v in imdb.groupby(['movie']).groups.items()]
    grouped_movies_dedis = [dedis.iloc[v] for _, v in dedis.groupby(['movie']).groups.items()]

    grouped_movies_imdb.sort(key=lambda x: len(x), reverse=True)
    grouped_movies_dedis.sort(key=lambda x: len(x), reverse=True)

    movies = {}
    me = ""

    for x, y in zip(grouped_movies_imdb, grouped_movies_dedis):
        movies[y.iloc[0].movie] = x.iloc[0].movie

    for i, m in dedis.iterrows():
        dedis.at[i, 'movie'] = movies[dedis.at[i, 'movie']]

    grouped_users_imdb = [imdb.iloc[v] for _, v in imdb.groupby(['email']).groups.items()]
    grouped_users_dedis = [dedis.iloc[v] for _, v in dedis.groupby(['email']).groups.items()]

    for it, i in enumerate(grouped_users_imdb):
        print("Processing {} of {}".format(it, len(grouped_users_imdb)))
        for d in grouped_users_dedis:
            m = i.merge(d, on=['movie']).drop_duplicates()
            if len(m) == len(i.drop_duplicates()):
                if m.iloc[0].email_x == 'pau.argelaguet@epfl.ch':
                    print("My username is {}".format(m.iloc[0].email_y))
                    me = m.iloc[0].email_y
                break

    my_movies = dedis.loc[dedis['email'] == me]['movie']
    my_movies.to_csv("data/my-movies-2.csv", index=False)


if __name__ == '__main__':
    main()
