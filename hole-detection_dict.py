# Nikolopoulos, S., Palios, L. Detecting Holes and Antiholes in Graphs. Algorithmica 47, 119–138 (2007). https://doi.org/10.1007/s00453-006-1225-y

import networkx as nx

# Hole-Detection Algorithm

def twisted(edge):
    return (edge[1], edge[0])

def dict_visited(G):
    d1 = {(edge, vertex): 0 for edge in G.edges() for vertex in G}
    d2 = {(twisted(edge), vertex): 0 for edge in G.edges() for vertex in G}
    d1.update(d2)
    return d1

def find_hole(G):
    def process(a, b, c, visited, in_path):
        in_path[c] = 1
        visited[(a, b), c] = 1
        visited[(c, b), a] = 1
        for d in G.neighbors(c):
            if not (d in G.neighbors(a) or d in G.neighbors(b)):
                if in_path[d] == 1:
                    return True
                elif visited[(b, c), d] == 0:
                    if process(b, c, d, visited, in_path):
                        return True
        in_path[c] = 0
        return False
    
    visited = dict_visited(G)
    in_path = {vertex: 0 for vertex in G}
    
    for u in G:
        in_path[u] = 1
        for edge in G.edges():
            v, w = edge[0], edge[1]
            if u in G.neighbors(v) and not u in G.neighbors(w) and visited[(u, v), w] == 0:
                in_path[v] = 1
                if process(u, v, w, visited, in_path):
                    print("G has a hole.")
                    return 
                in_path[v] = 0
            if not u in G.neighbors(v) and u in G.neighbors(w) and visited[(u, w), v] == 0:
                in_path[w] = 1
                if process(u, w, v, visited, in_path):
                    print("G has a hole.")
                    return 
                in_path[w] = 0
        in_path[u] = 0
    
    print("G does not contain a hole.")
    return False

# Providing a certificate

def length(c, e): # c is a cycle, e is a chord
    return abs(c.index(e[1]) - c.index(e[0]))

def min_edge(c, chords):
    return min(chords, key=lambda e: length(c, e))

def path(c, e):
    i_min = c.index(e[0])
    i_max = c.index(e[1])
    if i_min < i_max:
        return c[i_min:i_max+1]
    else:
        return c[i_max:i_min+1]

def hole_certificate(G):
    def cycle(in_path):
        return sorted((key for key, value in in_path.items() if value != 0), key=in_path.get)
    
    def certificate(G, c):
        c_edges = set((c[i], c[i+1]) for i in range(len(c) - 1))
        c_edges.add((c[-1], c[0]))  
        chords = {(u, v) for u in c for v in G.neighbors(u) if v in c and not ((u, v) in c_edges or (v, u) in c_edges)}     
        if not chords: 
            return c
        else:
            return path(c, min_edge(c, chords))

    def process(a, b, c, visited, in_path, i):
        in_path[c] = i + 1
        visited[(a, b), c] = 1
        visited[(c, b), a] = 1
        # Extend the P_3 to a P_4
        for d in G.neighbors(c):
            if not (d in G.neighbors(a) or d in G.neighbors(b)):
                # abcd is a P_4 of G
                if in_path[d] != 0:
                    print("G has a hole:")
                    print(certificate(G, cycle(in_path)))
                    return True
                elif visited[(b, c), d] == 0:
                    if process(b, c, d, visited, in_path, in_path[c]):
                        return True
        in_path[c] = 0
        return False
    
    visited = dict_visited(G)
    in_path = {vertex: 0 for vertex in G}
    
    for u in G:
        in_path[u] = 1 # u is the first vertex in the active path
        for edge in G.edges():
            v, w = edge[0], edge[1]
            if u in G.neighbors(v) and not u in G.neighbors(w) and visited[(u, v), w] == 0:
                in_path[v] = 2
                if process(u, v, w, visited, in_path, 2):
                    #print("G has a hole.")
                    return 
                in_path[v] = 0
            if not u in G.neighbors(v) and u in G.neighbors(w) and visited[(u, w), v] == 0:
                in_path[w] = 2
                if process(u, w, v, visited, in_path, 2):
                    #print("G has a hole.")
                    return 
                in_path[w] = 0
        in_path[u] = 0
    
    print("G does not contain a hole.")
    return 

# Example
G = nx.cycle_graph(9) 
G.add_edge(2,7)
find_hole(G)
hole_certificate(G)