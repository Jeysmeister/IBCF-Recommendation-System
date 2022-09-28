import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors

df = pd.DataFrame({'user_0':[0,3,0,5,0,0,4,5,0,2], 'user_1':[0,0,3,2,5,0,4,0,3,0], 'user_2':[3,1,0,3,5,0,0,4,0,0], 'user_3':[4,3,4,2,0,0,0,2,0,0],
                   'user_4':[2,0,0,0,0,4,4,3,5,0], 'user_5':[1,0,2,4,0,0,4,0,5,0], 'user_6':[2,0,0,3,0,4,3,3,0,0], 'user_7':[0,0,0,3,0,2,4,3,4,0],
                   'user_8':[5,0,0,0,5,3,0,3,0,4], 'user_9':[1,0,2,0,4,0,4,3,0,0]},
                  index=['movie_0','movie_1','movie_2','movie_3','movie_4','movie_5','movie_6','movie_7','movie_8','movie_9'])

knn = NearestNeighbors(metric='cosine', algorithm='brute')
knn.fit(df.values)
distances, indices = knn.kneighbors(df.values, n_neighbors=10)

#print(knn.kneighbors(df.values, n_neighbors=5))
#print(knn.kneighbors(df.values, n_neighbors=10))


for title in df.index:

    index_user_likes = df.index.tolist().index(title)  # get an index for a movie
    sim_movies = indices[index_user_likes].tolist()  # make list for similar movies
    movie_distances = distances[index_user_likes].tolist()  # the list for distances of similar movies
    id_movie = sim_movies.index(index_user_likes)  # get the position of the movie itself in indices and distances
    #print('Similar Movies to ' + str(df.index[index_user_likes]) + ': \n')

    sim_movies.remove(index_user_likes)  # remove the movie itself in indices
    movie_distances.pop(id_movie)  # remove the movie itself in distances

    j = 1

    for i in sim_movies:
        #print(
        #    str(j) + ': ' + str(df.index[i]) + ', the distance with ' + str(title) + ': ' + str(movie_distances[j - 1]))
        j = j + 1

    print('\n')

    dict = {}
    for x in sim_movies:
        for y in movie_distances:
            dict[x] = y
            movie_distances.remove(y)
            break

    i = 0
    for x, y in dict.items():
        if i == 0:
            y = y + 100000
            temp = x
            dict.pop(x)
            dict.update({x: y})
            break
        else:
            break
    new_dict = sorted(dict.items(), key=lambda item: item[1])
    print(new_dict)

def recommend_movie(title):
    index_user_likes = df.index.tolist().index(title)  # get an index for a movie
    sim_movies = indices[index_user_likes].tolist()  # make list for similar movies
    movie_distances = distances[index_user_likes].tolist()  # the list for distances of similar movies
    id_movie = sim_movies.index(index_user_likes)  # get the position of the movie itself in indices and distances

    print('Similar Movies to ' + str(df.index[index_user_likes]) + ': \n')

    sim_movies.remove(index_user_likes)  # remove the movie itself in indices
    movie_distances.pop(id_movie)  # remove the movie itself in distances

    j = 1

    for i in sim_movies:
        print(
            str(j) + ': ' + str(df.index[i]) + ', the distance with ' + str(title) + ': ' + str(movie_distances[j - 1]))
        j = j + 1

recommend_movie('movie_1')