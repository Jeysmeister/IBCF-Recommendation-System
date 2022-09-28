import random

import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors
import recmetrics

ratings = pd.read_csv('ratinggames.csv', usecols=['userId','gameId','rating'])
movies = pd.read_csv('gamespc.csv', usecols=['gameId','title', 'genres'])
ratings2 = pd.merge(ratings, movies, how='inner', on='gameId')
df = ratings2.pivot_table(index='title',columns='userId',values='rating').fillna(0)
df1 = df.copy()
df2 = df.copy()
ratedgameIds = pd.read_csv('ratinggames.csv')
ratedgameIdsColumns = ratedgameIds.loc[:,'gameId'].unique()
gameIds = pd.read_csv('gamespc.csv', usecols=['gameId','genres','title'])
gameIdsColumns = gameIds.loc[:,'gameId']
gameIdsGenres = gameIds.loc[:,'genres']
gameIdsTitle = gameIds.loc[:,'title']
gameIdsTitleList = []
unratedmovies = []
unratedtitles = []
unratedgenres = []
list1 = []
list2 = []
listno = []
topratedgenres = []
final_new_menu = []
target_user = 0
target_user_ratings = []
target_user_timestamp = []
target_user_df = []
rating_df = pd.read_csv('ratinggames.csv')

def take_third(elem):
    return elem[2]

def get_timeweight(user):
    df_timeweight = pd.read_csv('ratinggames.csv')
    user_df = df_timeweight.loc[df_timeweight['userId'] == user]
    user_timestamps = user_df.loc[:, 'timestamp'].tolist()
    user_ratings = user_df.loc[:, 'rating'].tolist()
    user_gameId = user_df.loc[:, 'gameId'].tolist()
    user_list = zip(user_gameId, user_ratings, user_timestamps)
    user_list = list(user_list)
    user_list = sorted(user_list, key=take_third, reverse=True)
    movie_indexes = []
    for x in user_gameId:
        movie_indexes.append(gameIdsColumns.tolist().index(x))
    most_recent = 0
    list_of_diff = []
    sum_of_time_diff = 0
    time_weight_list = []
    for x in user_list:
        if most_recent == 0:
            most_recent = x[2]
            list_of_diff.append(0)
        else:
            list_of_diff.append(most_recent - x[2])
            sum_of_time_diff = sum_of_time_diff + (most_recent - x[2])
    for x in list_of_diff:
        time_weight_list.append(1 - (x / sum_of_time_diff))
    return time_weight_list, movie_indexes

def getTargetRatings(target_user):
    target_user_df = rating_df.loc[rating_df['userId'] == target_user]
    return target_user_df


for i in gameIdsTitle:
    gameIdsTitleList.append(i)

def getUnrated():
    for i in gameIdsColumns:
        if i in ratedgameIdsColumns:
            #print('MOVIE ID {} : MATCH FOUND'.format(i))
            pass
        else:
            unratedmovies.append(i)

getUnrated()

#print(unratedmovies)

unratedmoviecount = len(unratedmovies)
#print(unratedmoviecount)

for i in unratedmovies:
    unratedgenres.append(gameIdsGenres[i-1])
    unratedtitles.append(gameIdsTitle[i-1])
    #print('gameId {} : {} - {}'.format(i, gameIdsTitle[i-1],gameIdsGenres[i-1]))

#for i in gameIds:
#    if i in ratedgameIds:
#        print('MOVIE ID : {}, MATCH FOUND'.format(i))
#    else:
#        unratedmovies.append(i)


def recommend_movies(user, num_recommended_movies):
    listno.append('\n')
    knn = NearestNeighbors(metric='cosine', algorithm='brute')
    knn.fit(df2.values)
    distances2, indices2 = knn.kneighbors(df2.values, n_neighbors=41)
    #print('The list of the Movies {} Has Watched \n'.format(user))
    #for m in df[df[user] > 0][user].index.tolist():
    #    print(m)

    #print('\n')

    recommended_movies = []
    recommended_list1 = []
    recommended_list2 = []
    movieonly1 = []
    movieonly2 = []

    for m in df[df[user] == 0].index.tolist():
        index_df = df.index.tolist().index(m)
        predicted_rating = df1.iloc[index_df, df1.columns.tolist().index(user)]
        recommended_movies.append((m, predicted_rating))

    sorted_rm = sorted(recommended_movies, key=lambda x: x[1], reverse=True)

    #print('The list of the Recommended Movies')
    for recommended_movie in sorted_rm[:num_recommended_movies]:
        #print('{} - predicted rating:{}'.format(recommended_movie[0], recommended_movie[1]))
        movie = str(recommended_movie[0])
        index = gameIdsTitleList.index(movie)
        genre = gameIdsGenres[index]
        topratedgenres.append(genre)
        recommended_list1.append(movie + ' -- ' + genre + ' || Predicted Rating : ' + str(recommended_movie[1]))
        #recommended_list1.append(recommended_movie[0])
        #movieonly1.append(recommended_movie[0])
        index_user_likes = df2.index.tolist().index(recommended_movie[0])  # get an index for a movie
        sim_movies = indices2[index_user_likes].tolist()  # make list for similar movies
        movie_distances = distances2[index_user_likes].tolist()  # the list for distances of similar movies
        id_movie = sim_movies.index(index_user_likes)  # get the position of the movie itself in indices and distances
        #print('Similar Movies to ' + str(df2.index[index_user_likes]) + ': \n')
        sim_movies.remove(index_user_likes)  # remove the movie itself in indices
        movie_distances.pop(id_movie)  # remove the movie itself in distances


        x = 1
        limit = len(sim_movies)/2
        if limit % 2 != 0:
            limit += .5
        start = limit/2
        if start % 2 != 0:
            start += .5
        for i in sim_movies:
            if x > int(start) and x < int(limit):
                recommended_list2.append(str(df2.index[i] + ' -- ' + str(genre) + '|| the distance with ' + str(df2.index[index_user_likes]) + ': ' + str(movie_distances[x - 1])))
                movie = str(df2.index[i])
                #print(movie)
                index = gameIdsTitleList.index(movie)
                genre = str(gameIdsGenres[index])
                #recommended_list2.append(str(df2.index[i]) + ' - ' + str(genre))
                #recommended_list2.append(movie + ' - ' + genre)
                #movieonly2.append(str(df2.index[i]))

            #print('\t' + str(df2.index[i]) + ' || the similarity with ' + str(df2.index[index_user_likes]) + ': ' + str(movie_distances[x - 1]))
            x += 1
    movieonly1.extend(movieonly2)
    if len(listno) == 1:
        list1.append(list(dict.fromkeys(movieonly1)))
    else:
        list2.append(list(dict.fromkeys(movieonly1)))


    print('\nTOP RECOMMENDED : ')
    for x in recommended_list1:
        print(x)
    print('\nNEAREST NEIGHBORS : ')
    for x in recommended_list2:
        print(x)
    recommended_list1.extend(recommended_list2)
    print('\nFINAL RECOMMENDED LIST : ')
    final_new_menu = list(dict.fromkeys(recommended_list1))

    randomUnratedIndex = 0
    topgenrematchunrated = False
    unratedgenreslist = []

    if unratedmoviecount != 0:
        randomUnratedIndex = random.randint(0, unratedmoviecount - 1)
        #print(str(unratedmoviecount) + ' = ' + str(randomUnratedIndex))
        if '|' in str(unratedgenres[randomUnratedIndex]):
            unratedgenreslist = unratedgenres[randomUnratedIndex].split('|')
            for x in unratedgenreslist:
                i = 0
                while i != 2:
                    if x in topratedgenres[i]:
                        topgenrematchunrated = True
                    i += 1
        else:
            randomUnratedGenre = unratedgenres[randomUnratedIndex]
            i = 0
            while i != 2:
                if randomUnratedGenre in topratedgenres[i]:
                    topgenrematchunrated = True
                i += 1

    if unratedmoviecount != 0:
        if topgenrematchunrated == True:
            final_new_menu.pop()
            final_new_menu.append(str(unratedtitles[randomUnratedIndex]) + ' -- ' + str(unratedgenres[randomUnratedIndex]))
            #print(str(unratedtitles[randomUnratedIndex]) + ' - ' + str(unratedgenres[randomUnratedIndex]) + ' : GENRE MATCHING')
        #else:
            #print(str(unratedtitles[randomUnratedIndex]) + ' - ' + str(unratedgenres[randomUnratedIndex]) + ' : GENRE NOT MATCHING')
    x = 1
    for fnm in final_new_menu:
        print(str(x) + ' : ' + fnm)
        x += 1
    return final_new_menu

def movie_recommender(user1, user2, num_neighbors, num_recommendation):
    users = []
    users.append(user1)
    #users.append(user2)
    timeweights, movieindexes = get_timeweight(user1)
    user_ratings = getTargetRatings(user1)
    user_ratings = list(user_ratings.loc[:, 'rating'])
    #print(user_ratings)
    for user in users:
        number_neighbors = num_neighbors

        knn = NearestNeighbors(metric='cosine', algorithm='brute')
        knn.fit(df.values)
        distances, indices = knn.kneighbors(df.values, n_neighbors=number_neighbors)
        user_index = df.columns.tolist().index(user)
        #print(user_index)

        for m, t in list(enumerate(df.index)):
            if df.iloc[m, user_index] == 0:
                sim_movies = indices[m].tolist()
                movie_distances = distances[m].tolist()

                #if m in sim_movies and m in movieindexes:
                    #print('USER RATING TO MOVIE {}: {}'.format(m, user_ratings[movieindexes.index(m)]))

                if m in sim_movies:
                    id_movie = sim_movies.index(m)
                    sim_movies.remove(m)
                    movie_distances.pop(id_movie)
                else:
                    sim_movies = sim_movies[:num_neighbors - 1]
                    movie_distances = movie_distances[:num_neighbors - 1]

                movie_similarity = [1 - x for x in movie_distances]
                movie_similarity_copy = movie_similarity.copy()
                movie_similarity_copy2 = movie_similarity.copy()
                nominator = 0
                nominator2 = 0

                for x in movieindexes:
                    if x in sim_movies:
                        movie_similarity_copy[sim_movies.index(x)] = movie_similarity_copy[sim_movies.index(x)] * timeweights[movieindexes.index(x)]

                for s in range(0, len(movie_similarity)):
                    if df.iloc[sim_movies[s], user_index] == 0:
                        if len(movie_similarity_copy) == (number_neighbors - 1):
                            movie_similarity_copy.pop(s)
                        else:
                            movie_similarity_copy.pop(s - (len(movie_similarity) - len(movie_similarity_copy)))
                    else:
                        if m in movieindexes:
                            #print('S : {} , SIMILARITY TO : {} , SIMILARITY VALUE : {} , RATING VALUE : {} , TIMEWEIGHTS : {}'.format(df.iloc[sim_movies[s], user_index], m, movie_similarity[s], df.iloc[sim_movies[s], user_index],timeweights[movieindexes.index(m)]))
                            nominator = nominator + movie_similarity[s] * (df.iloc[sim_movies[s], user_index] * timeweights[movieindexes.index(m)])
                        else:
                            nominator = nominator + movie_similarity[s] * df.iloc[sim_movies[s], user_index]

                for s in range(0, len(movie_similarity)):
                    if df.iloc[sim_movies[s], user_index] == 0:
                        if len(movie_similarity_copy2) == (number_neighbors - 1):
                            movie_similarity_copy2.pop(s)
                        else:
                            movie_similarity_copy2.pop(s - (len(movie_similarity) - len(movie_similarity_copy2)))
                    else:
                        nominator2 = nominator2 + movie_similarity[s] * df.iloc[sim_movies[s], user_index]
                        #print(movie_similarity[s])

                #print(sim_movies)

                if len(movie_similarity_copy) > 0:
                    if sum(movie_similarity_copy) > 0:
                        ##print('MOVIE ID : {}'.format(m))
                        original_predicted_r = nominator2 / sum(movie_similarity_copy2)
                        #print('ORIGINAL PREDICTED RATING = {}'.format(original_predicted_r))
                        predicted_r = nominator / sum(movie_similarity_copy)
                        #print('PREDICTION RATING WITH TIME WEIGHT = {}'.format(predicted_r))
                        #print('\n')
                    else:
                        predicted_r = 0
                else:
                    predicted_r = 0

                df1.iloc[m, user_index] = predicted_r
        menu_for_system = recommend_movies(user, num_recommendation)
        return menu_for_system

def get_user_list():
    return df.columns.tolist()

'''
list_of_personalize = []
ctr = 0
while ctr != 1:
    m = [341, 151, 379, 212, 346, 42, 14, 381, 437, 94]
    n = [461, 11, 522, 459, 158, 326, 18, 182, 350, 55]
    i = random.randint(1,600)
    j = random.randint(1,600)
    while i == j:
        i = random.randint(1,600)

    #print('Comparing: User {} and User {}'.format(i, j))
    movie_recommender(m[ctr], n[ctr], 15, 3)
    ctr += 1
    #print(list1)
    #print(list2)
    innerlist1 = list1[0]
    innerlist2 = list2[0]
    #print(innerlist1)
    #print(innerlist2)
    
    x = 0
    while len(innerlist1) < len(innerlist2):
        innerlist1.append(str(x))
        x += 1
    if x != 0:
        x = 0
    while len(innerlist2) < len(innerlist1):
        innerlist2.append(str(x))
        x += 1

    finallist = []
    finallist.append(innerlist1)
    finallist.append(innerlist2)
    #print(finallist)
    x = recmetrics.personalization(predicted=finallist)
    list_of_personalize.append(x)
    #print(x)
    list1 = []
    list2 = []
    listno = []

sum = 0
ctr = 0
for x in list_of_personalize:
    ctr += 1
    sum = x + sum
    print(x)
    if ctr == len(list_of_personalize):
        print('Average : ')
        print(sum/len(list_of_personalize))'''