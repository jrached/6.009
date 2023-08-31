#!/usr/bin/env python3

import pickle
# NO ADDITIONAL IMPORTS ALLOWED!

# Note that part of your checkoff grade for this lab will be based on the
# style/clarity of your code.  As you are working through the lab, be on the
# lookout for things that would be made clearer by comments/docstrings, and for
# opportunities to rearrange aspects of your code to avoid repetition (for
# example, by introducing helper functions).

###--------------------------HELPER FUNCTIONS-----------------------------

def actors_in_film(moviesdb, film):
    """ Returns an actors id for a particular film id
    """
    actors = list(moviesdb.keys())[list(moviesdb.values()).index(film)]
    return actors

def actor_to_movie_path(new_moviesdb, path):
    """ Takes in an actor id path and returns the equivalent movie id path"
    """
    movies_path = []
    for i in range(1, len(path)): 
        try:
            movies_path.append(new_moviesdb[(path[i-1], path[i])])
        except KeyError:
            movies_path.append(new_moviesdb[(path[i], path[i-1])])
    return movies_path

def connecting_movie(movie_actordb, actor_id_1, actor_id_2):
    """
    returns the film corresponding to two actors in the actor to movie databse

    """
    try:  
        return movie_actordb[(actor_id_1, actor_id_2)] 
    except KeyError:
        return movie_actordb[(actor_id_2, actor_id_1)]
    
def actor_to_id(db, actor):
    """
    Returns actors id
    """
    return db[actor]

def id_to_actor(db, actor_id):
    """
    Returns id's actor

    """
    return list(db.keys())[list(db.values()).index(actor_id)]


###-----------------------LAB FUNCTIONS------------------------------------
def transform_data(raw_data, movies = False):
    """
    If movies = False it just transforms the data into a graph using 
    a dictionary where each node is a key and its corresponding value is 
    a list of its children. If movies = True then it turns it into an actor to 
    movie database also using a dictionary where the keys are tuples of the actors
    who act in a film together and its respective value is the film itself.

    """
    graph = {}
    
    if movies:
         for tup in raw_data:
            graph[(tup[0], tup[1])] = tup[2]
    else:
        for tup in raw_data:
            if tup[0] in graph.keys():
                if tup[1] not in graph[tup[0]]:
                    graph[tup[0]].append(tup[1])
            else:
                graph[tup[0]] = [tup[1]] 
                
            if tup[1] in graph.keys():
                if tup[0] not in graph[tup[1]]:
                    graph[tup[1]].append(tup[0])
            else:
                graph[tup[1]] = [tup[0]] 
        
    return graph

def acted_together(data, actor_id_1, actor_id_2):
    """Returns True if the two actors provided have acted together according
       to the database, False otherwise.
    """
    if actor_id_2 != actor_id_1:
        return actor_id_2 in data[actor_id_1]
    else:
        return True


def actors_with_bacon_number(data, n):
    """
    Returns a list of actors with a bacon number of n.

    """
    bacon_id = 4724
    seen = set([bacon_id])
    paths = [(bacon_id,)]
    new_path = ()
    actors = set()
    while paths: 
        current_path = paths.pop(0)
        index = current_path[-1]
        
        if len(current_path) + 1> len(new_path) and 1 < len(new_path) < n + 1:
            actors = set()
        
        for child in data[index]:
            if child not in seen:
                new_path = current_path + (child,)
                if len(new_path) > n + 1:
                    break
                seen.add(child)
                actors.add(child)
                paths.append(new_path) 
    
    if len(list(actors)) == 0 and len(new_path) == 2:
        return set([bacon_id])
    else:
        return actors 
    


def bacon_path(data, actor_id):
    """ Returns the shortest path between any actor and kevin bacon using BFS.
    """
    return actor_to_actor_path(data, 4724, actor_id)


def actor_to_actor_path(data, actor_id_1, actor_id_2):
    """ Returns the shortest path between any two actors using BFS.
    """
    def goal_function(actor):
        return actor_id_2 == actor
    
    return actor_path(data, actor_id_1, goal_function) 

def actor_path(data, actor_id_1, goal_test_function):
    """ Returns the shortest path between any two actors according to 
        a condition provided by goal_test_function using BFS.
    """
    seen = {actor_id_1}
    paths = [(actor_id_1,)]
    while paths: 
        current_path = paths.pop(0)
        index = current_path[-1]        
        
        for child in data[index]:
            new_path = current_path + (child,)
            if goal_test_function(child):
                return new_path
            elif child not in seen:
                seen.add(child)
                paths.append(new_path) 
    return None



def actors_connecting_films(data, film1, film2):
    """ Returns shortest path between two films by finding the shortest path
        between one of the actors in the first film and any of the actors in the 
        second. Uses actor_path() and a goal_test_function to achieve this.
    """
    with open('resources/movies.pickle', 'rb') as f:
        movienamesdb = pickle.load(f)
    with open('resources/large.pickle', 'rb') as f: 
        largedb = pickle.load(f)
    moviesdb = transform_data(largedb, True)   
    actors = actors_in_film(moviesdb, film2)
            
    def goal_test_function(child):
        return child in actors
    
    start_actor= actors_in_film(moviesdb, film1)[0]
    
    return actor_path(data, start_actor, goal_test_function)
    
    # movie_id_path = actor_to_movie_path(moviesdb, path)
    
    # if film1 not in movie_id_path:
    #     movie_id_path.insert(0, film1)
    # if film2 not in movie_id_path:
    #     movie_id_path.append(film2)
    
    # return movie_id_path


if __name__ == '__main__':
    ##-----------------OPENING DATABASES------------------------------
    # with open('resources/small.pickle', 'rb') as f:
    #     smalldb = pickle.load(f)
    # with open('resources/names.pickle', 'rb') as f:
    #     namesdb = pickle.load(f)
    # with open('resources/movies.pickle', 'rb') as f:
    #     moviesdb = pickle.load(f)
    # with open('resources/small.pickle', 'rb') as f:
    #     smalldb = pickle.load(f)
    #     # print(tinydb)
    # with open('resources/large.pickle', 'rb') as f:
    #     largedb = pickle.load(f)
    # additional code here will be run only when lab.py is invoked directly
    # (not when imported from test.py), so this is a good place to put code
    # used, for example, to generate the results for the online questions.
    
    
    
    ##------------------TESTING ACTED TOGETHER-------------------
    # actor1 = "Noureddine El Ati"
    # actor2 = "Helene Lapiower" 
    
    # new_data = transform_data(smalldb)
    # print(acted_together(new_data, actor_to_id(actor1), actor_to_id(actor2)))
    
    
    ##-------------------TESTING MAP FUNCTIONS---------------------------
    # actor = "Eduardo Yanez"
    
    # actor_id = actor_to_id(namesdb, actor)
    # print(actor_id)
    # my_actor = id_to_actor(namesdb, actor_id)
    # print(my_actor)
    
    ##-------------TESTING ACTORS WITH BACON NUMBER----------------------
    # new_data = transform_data(largedb)
    # # print(new_data)
    # actors = actors_with_bacon_number(new_data, 6)
    # print(actors)                        
    
    # lista = [1367972, 1338716, 1345461, 1345462]
    # new_lista = []
    # for ele in lista: 
    #     new_lista.append(id_to_actor(namesdb, ele))
    
    # print(new_lista)
    
    ##------------------TESTING BACON PATH-------------------------------
    # actor = "Angela Molina"
    
    # data = transform_data(largedb)
    # path = bacon_path(data, actor_to_id(namesdb, actor))
    
    # new_path = []
    # for ele in path:
    #     new_path.append(id_to_actor(namesdb, ele))
        
    # print(new_path)
    
    ##----------------TESTING ARBITRARY PATH---------------------
    # actor1 = "Mikijiro Hira" 
    # actor2 = "Walt Gorney"
    # data = transform_data(largedb)
    
    # path = actor_to_actor_path(data, actor_to_id(namesdb, actor1), actor_to_id(namesdb, actor2))
    
    # new_path = []
    # for ele in path:
    #     new_path.append(id_to_actor(namesdb, ele))
    
    # print(new_path)
        
    # actor1 = "Ashley C. Coombs" 
    # actor2 = "Iva Ilakovac"
    
    # new_largedb = transform_data(largedb)
    # new_moviesdb = transform_data(largedb, True)
    # print(new_moviesdb)
    # path = actor_to_actor_path(new_largedb, actor_to_id(namesdb, actor1), actor_to_id(namesdb, actor2))
    
    # movies_path = []
    # for i in range(1, len(path)):
    #     try:
    #         movies_path.append(new_moviesdb[(path[i-1], path[i])])
    #     except KeyError:
    #         movies_path.append(new_moviesdb[(path[i], path[i-1])])
    # print(movies_path)
    
    # movie_path = [] 
    # for i in [9692, 1493, 30817, 29938, 256690, 283406]:
    #     movie_path.append(list(moviesdb.keys())[list(moviesdb.values()).index(i)])
        
    # print(movie_path)
        
    
    ###-------------------------TESTING CONNECTING FILMS------------------
    
    # print(moviesdb)
    # film1 = 53021
    # film2 = 229828
    # data = transform_data(largedb)
    # movie_path = actors_connecting_films(data, film1, film2)
    
    # print(actor_to_id(namesdb, 'Conrad Brooks'))
    pass