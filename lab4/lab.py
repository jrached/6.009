#!/usr/bin/env python3

from util import read_osm_data, great_circle_distance, to_local_kml_url

# NO ADDITIONAL IMPORTS!


ALLOWED_HIGHWAY_TYPES = {
    'motorway', 'trunk', 'primary', 'secondary', 'tertiary', 'unclassified',
    'residential', 'living_street', 'motorway_link', 'trunk_link',
    'primary_link', 'secondary_link', 'tertiary_link',
}


DEFAULT_SPEED_LIMIT_MPH = {
    'motorway': 60,
    'trunk': 45,
    'primary': 35,
    'secondary': 30,
    'residential': 25,
    'tertiary': 25,
    'unclassified': 25,
    'living_street': 10,
    'motorway_link': 30,
    'trunk_link': 30,
    'primary_link': 30,
    'secondary_link': 30,
    'tertiary_link': 25,
}



def build_auxiliary_structures(nodes_filename, ways_filename):
    """
    Create any auxiliary structures you are interested in, by reading the data
    from the given filenames (using read_osm_data)
    """
    
    nodes ={} 
    for way in read_osm_data(ways_filename):
        try: 
            if way['tags']['highway'] in ALLOWED_HIGHWAY_TYPES:
                try: 
                    if way['tags']['oneway'] == 'yes':
                        if way['nodes'][0] not in nodes.keys():
                            nodes[way['nodes'][0]] = [way['nodes'][1:]]
                        else:
                            nodes[way['nodes'][0]].append(way['nodes'][1:])    
                    else:
                        if way['nodes'][0] not in nodes.keys():
                            nodes[way['nodes'][0]] = [way['nodes'][1:]]
                        else:
                            nodes[way['nodes'][0]].append(way['nodes'][1:])
                        if way['nodes'][len(way['nodes'])-1] not in nodes.keys():
                            nodes[way['nodes'][len(way['nodes'])-1]] = [way['nodes'][len(way['nodes'])-2::-1]]
                        else:
                            nodes[way['nodes'][len(way['nodes'])-1]].append(way['nodes'][len(way['nodes'])-2::-1])
                except KeyError: 
                     if way['nodes'][0] not in nodes.keys():
                         nodes[way['nodes'][0]] = [way['nodes'][1:]]
                     else:
                         nodes[way['nodes'][0]].append(way['nodes'][1:])
                     if way['nodes'][len(way['nodes'])-1] not in nodes.keys():
                         nodes[way['nodes'][len(way['nodes'])-1]] = [way['nodes'][len(way['nodes'])-2::-1]]
                     else:
                         nodes[way['nodes'][len(way['nodes'])-1]].append(way['nodes'][len(way['nodes'])-2::-1])
        except: KeyError
        
    coords = {} 
    for node in read_osm_data(nodes_filename):
        coords[node['id']] = (node['lat'], node['lon'])
            
    
    # costs = {}
    # for way in read_osm_data(ways_filename):
    #     try: 
    #         if way['tags']['highway'] in ALLOWED_HIGHWAY_TYPES:
    #             prev = None
    #             for node in way['nodes']: 
    #                 if prev != None and (prev, node) not in costs.keys(): 
    #                     costs[(prev, node)] = compute_cost(prev, node)      
    #                 prev = node
    #     except: KeyError
        
    return (nodes, coords)



def search(successors, start_state, goal_test, costs_func):
    
    if goal_test(start_state):
        return [start_state]

    agenda = [((start_state,), 0)]
    visited = {start_state} 

    while agenda:
        costs = []
        for i in range(len(agenda)):
            costs.append(agenda[i][1]) 
        
        min_elem = min(costs)
        
        for i in range(len(agenda)):
            if agenda[i][1] == min_elem:
                index = i
                
        current_path = agenda.pop(index)  
        terminal_vertex = current_path[0][-1]
        try:

            for child in successors[terminal_vertex]:
                if child[0] in visited:
                    continue 
                add_path = []
                for node in child:
                    add_path.append(node)
                current_path.append(add_path)
                print("terminal vertex: " + str(terminal_vertex) + "child: " + str(child[-1]))
                added_cost = costs_func(terminal_vertex, child[-1])
                if goal_test(child[-1]):
                    return current_path 
                visited.add(child[0])
                agenda.append((current_path, added_cost))
        except: KeyError

def find_short_path_nodes(aux_structures, node1, node2):
    """
    Return the shortest path between the two nodes

    Parameters:
        aux_structures: the result of calling build_auxiliary_structures
        node1: node representing the start location
        node2: node representing the end location

    Returns:
        a list of node IDs representing the shortest path (in terms of
        distance) from node1 to node2
    """
    
    print(aux_structures[1])
    
    def compute_cost(node_id_1, node_id_2): 
        for node in aux_structures[1].keys():
            if node == node_id_1:
                coord1 = aux_structures[1][node]
            if node == node_id_2:
                coord2 = aux_structures[1][node]
                
        return great_circle_distance(coord1, coord2)
    
    def goal(inputn):
        return inputn == node2
    
    result = search(aux_structures[0], node1, goal, compute_cost)
    
    return result
    


def find_short_path(aux_structures, loc1, loc2):
    """
    Return the shortest path between the two locations

    Parameters:
        aux_structures: the result of calling build_auxiliary_structures
        loc1: tuple of 2 floats: (latitude, longitude), representing the start
              location
        loc2: tuple of 2 floats: (latitude, longitude), representing the end
              location

    Returns:
        a list of (latitude, longitude) tuples representing the shortest path
        (in terms of distance) from loc1 to loc2.
    """
    raise NotImplementedError


def find_fast_path(aux_structures, loc1, loc2):
    """
    Return the shortest path between the two locations, in terms of expected
    time (taking into account speed limits).

    Parameters:
        aux_structures: the result of calling build_auxiliary_structures
        loc1: tuple of 2 floats: (latitude, longitude), representing the start
              location
        loc2: tuple of 2 floats: (latitude, longitude), representing the end
              location

    Returns:
        a list of (latitude, longitude) tuples representing the shortest path
        (in terms of time) from loc1 to loc2.
    """
    raise NotImplementedError


if __name__ == '__main__':
    # additional code here will be run only when lab.py is invoked directly
    # (not when imported from test.py), so this is a good place to put code
    # used, for example, to generate the results for the online questions.
    # count = 0
    # for node in read_osm_data('resources/cambridge.ways'):
    #     try: 
    #         if node['tags']['oneway'] == 'yes':
    #                 count+=1
    #     except: KeyError
    # print(count)                                                             
    
    # miles = 0
    # for way in read_osm_data('resources/midwest.ways'):
    #     if way['id'] == 21705939:
    #         for i in range(1, len(way['nodes'])):
    #             for node in read_osm_data('resources/midwest.nodes'):
    #                 if node['id'] == way['nodes'][i-1]:
    #                     coord1 = (node['lat'], node['lon'])
    #                 if node['id'] == way['nodes'][i]:
    #                     coord2 = (node['lat'], node['lon'])
    #             miles += great_circle_distance(coord1, coord2)
            
    # print(miles)

    # print(great_circle_distance(coord1, coord2))
    ways_filename = 'resources/mit.ways'
    nodes_filename = 'resources/mit.nodes'
    
    # for node in read_osm_data(nodes_filename):
    #     print(node)
        
    
    for way in read_osm_data(ways_filename): 
        print(way)
        
    aux_structures = build_auxiliary_structures(nodes_filename, ways_filename)
    print(aux_structures)
    a = find_short_path_nodes(aux_structures, 2, 8)
    print(a)
    # for way in read_osm_data('resources/mit.ways'): 
    #     print(way)
    