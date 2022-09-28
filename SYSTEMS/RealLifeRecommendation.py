import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors
import recmetrics
import random

ratings = pd.read_csv('ratings.csv', usecols=['userId','movieId','rating'])
movies = pd.read_csv('movies.csv', usecols=['movieId','title'])
ratings2 = pd.merge(ratings, movies, how='inner', on='movieId')
    
print(ratings2)
df = ratings2.pivot_table(index='title',columns='userId',values='rating').fillna(0)
df1 = df.copy()

list1 = []
list2 = []
listno = []

def recommend_movies(user, num_recommended_movies):
    listno.append("\n")
    #print('The list of the Movies {} Has Watched \n'.format(user))
    #for m in df[df[user] > 0][user].index.tolist():
    #    print(m)

    #print('\n')

    recommended_movies = []

    for m in df[df[user] == 0].index.tolist():
        index_df = df.index.tolist().index(m)
        predicted_rating = df1.iloc[index_df, df1.columns.tolist().index(user)]
        recommended_movies.append((m, predicted_rating))

    sorted_rm = sorted(recommended_movies, key=lambda x: x[1], reverse=True)

    #print('The list of the Recommended Movies \n')
    rank = 1
    for recommended_movie in sorted_rm[:num_recommended_movies]:
        #print('{}: {} - predicted rating:{}'.format(rank, recommended_movie[0], recommended_movie[1]))
        if len(listno) == 1:
            list1.append(recommended_movie[0])
        else:
            list2.append(recommended_movie[0])
        rank = rank + 1
    #print('\n\n\n')

def movie_recommender(user1, user2, num_neighbors, num_recommendation):
    users = []
    users.append(user1)
    users.append(user2)
    for user in users:
        number_neighbors = num_neighbors

        knn = NearestNeighbors(metric='cosine', algorithm='brute')
        knn.fit(df.values)
        distances, indices = knn.kneighbors(df.values, n_neighbors=number_neighbors)

        user_index = df.columns.tolist().index(user)

        for m, t in list(enumerate(df.index)):
            if df.iloc[m, user_index] == 0:
                sim_movies = indices[m].tolist()
                movie_distances = distances[m].tolist()

                if m in sim_movies:
                    id_movie = sim_movies.index(m)
                    sim_movies.remove(m)
                    movie_distances.pop(id_movie)

                else:
                    sim_movies = sim_movies[:num_neighbors - 1]
                    movie_distances = movie_distances[:num_neighbors - 1]

                movie_similarity = [1 - x for x in movie_distances]
                movie_similarity_copy = movie_similarity.copy()
                nominator = 0

                for s in range(0, len(movie_similarity)):
                    if df.iloc[sim_movies[s], user_index] == 0:
                        if len(movie_similarity_copy) == (number_neighbors - 1):
                            movie_similarity_copy.pop(s)
                        else:
                            movie_similarity_copy.pop(s - (len(movie_similarity) - len(movie_similarity_copy)))
                    else:
                        nominator = nominator + movie_similarity[s] * df.iloc[sim_movies[s], user_index]

                if len(movie_similarity_copy) > 0:
                    if sum(movie_similarity_copy) > 0:
                        predicted_r = nominator / sum(movie_similarity_copy)
                    else:
                        predicted_r = 0
                else:
                    predicted_r = 0

                df1.iloc[m, user_index] = predicted_r
        recommend_movies(user, num_recommendation)

i = 0
list_of_personalize = []
while i != 10:
    m = [341, 151, 379, 212, 346, 42, 14, 381, 437, 94]
    n = [461, 11, 522, 459, 158, 326, 18, 182, 350, 55]
    x = random.randint(1,600),
    y = random.randint(1,600)
    while x == y:
        x = random.randint(1,600)
    print("comparison between : {} and {}".format(m[i], n[i]))
    movie_recommender(m[i], n[i], 15, 45)
    i += 1
    finallist = []
    finallist.append(list1)
    finallist.append(list2)

    #print(finallist)
    x = recmetrics.personalization(predicted=finallist)
    print(recmetrics.personalization(predicted=finallist))
    list_of_personalize.append(x)
    list1 = []
    list2 = []
    listno = []

sum = 0
ctr = 0
for x in list_of_personalize:
    ctr += 1
    sum = x + sum
    if ctr == len(list_of_personalize):
        print("Average : ")
        print(sum/len(list_of_personalize))

#print(list1)
#print(list2)
