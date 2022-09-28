import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors

df = pd.DataFrame({'user_0':[0,3,0,5,0,0,4,5,0,2], 'user_1':[0,0,3,2,5,0,4,0,3,0], 'user_2':[3,1,0,3,5,0,0,4,0,0], 'user_3':[4,3,4,2,0,0,0,2,0,0],
                   'user_4':[2,0,0,0,0,4,4,3,5,0], 'user_5':[1,0,2,4,0,0,4,0,5,0], 'user_6':[2,0,0,3,0,4,3,3,0,0], 'user_7':[0,0,0,3,0,2,4,3,4,0],
                   'user_8':[5,0,0,0,5,3,0,3,0,4], 'user_9':[1,0,2,0,4,0,4,3,0,0]},
                  index=['movie_0','movie_1','movie_2','movie_3','movie_4','movie_5','movie_6','movie_7','movie_8','movie_9'])

# find the nearest neighbors using NearestNeighbors(n_neighbors=3)
number_neighbors = 9
knn = NearestNeighbors(metric='cosine', algorithm='brute')
knn.fit(df.values)
distances, indices = knn.kneighbors(df.values, number_neighbors)

# convert user_name to user_index
user_index = df.columns.tolist().index('user_9')
print(user_index)

# t: movie_title, m: the row number of t in df
for m,t in list(enumerate(df.index)):
    #print(m,t)
    sim_movies = []
    movie_distances = []
    if df.iloc[m, user_index] == 0:
        sim_movies = indices[m].tolist()
        print(sim_movies)
        movie_distances = distances[m].tolist()
        print(movie_distances)
    print(movie_distances)
    print('\n')