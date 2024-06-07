# Nikolopoulos, S., Palios, L. Detecting Holes and Antiholes in Graphs. Algorithmica 47, 119–138 (2007). https://doi.org/10.1007/s00453-006-1225-y

import networkx as nx
import numpy as np

########################################################################################################

# Hole-Detection Algorithm 

def find_hole(G):
    
    edges = list(G.edges()) + [(e[1], e[0]) for e in G.edges()]
    visited_P3 = np.zeros((G.number_of_edges()*2, G.number_of_nodes()), dtype=int)
    in_path = [0 for u in G]
        
    def process(a, b, c, visited_P3, in_path):
        in_path[c] = 1
        visited_P3[edges.index((a, b)), c] = 1
        visited_P3[edges.index((c, b)), a] = 1
        for d in G.neighbors(c):
            if not (d in G.neighbors(a) or d in G.neighbors(b)):
                if in_path[d] == 1:
                    return True
                elif visited_P3[edges.index((b, c)), d] == 0:
                    if process(b, c, d, visited_P3, in_path):
                        return True
        in_path[c] = 0
        return False
    
    for u in G:
        in_path[u] = 1
        for edge in G.edges():
            v, w = edge[0], edge[1]
            if u in G.neighbors(v) and not u in G.neighbors(w) and visited_P3[edges.index((u, v)), w] == 0:
                in_path[v] = 1
                if process(u, v, w, visited_P3, in_path):
                    print("G has a hole.")
                    return 
                in_path[v] = 0
            if not u in G.neighbors(v) and u in G.neighbors(w) and visited_P3[edges.index((u, w)), v] == 0:
                in_path[w] = 1
                if process(u, w, v, visited_P3, in_path):
                    print("G has a hole.")
                    return 
                in_path[w] = 0
        in_path[u] = 0
    
    print("G does not contain a hole.")
    return False

########################################################################################################

# Providing a certificate

def length(C, chord): 
    return abs(C.index(chord[1]) - C.index(chord[0]))

def min_edge(C, chords):
    return min(chords, key=lambda e: length(C, e))

def path(C, chord):
    i_min = C.index(chord[0])
    i_max = C.index(chord[1])
    if i_min < i_max:
        return C[i_min:i_max+1]
    else:
        return C[i_max:i_min+1]
    
def certificate(G, C):
    cycle_edges = [(C[i], C[i+1]) for i in range(len(C) - 1)] + [(C[-1], C[0])]
    chords = [(u, v) for u in C for v in G.neighbors(u) if v in C and not ((u, v) in cycle_edges or (v, u) in cycle_edges)]   
    if not chords: 
        return C
    else:
        return path(C, min_edge(C, chords))

def hole_certificate(G):
    
    edges = list(G.edges()) + [(e[1], e[0]) for e in G.edges()]
    visited_P3 = np.zeros((G.number_of_edges()*2, G.number_of_nodes()), dtype=int)
    in_path = [0 for u in G]
    
    def cycle(in_path):
        return [idx for idx, x in enumerate(in_path) if x != 0]

    def process(a, b, c, visited_P3, in_path, i):
        in_path[c] = i + 1
        visited_P3[edges.index((a, b)), c] = 1
        visited_P3[edges.index((c, b)), a] = 1
        # Extend the P_3 to a P_4
        for d in G.neighbors(c):
            if not (d in G.neighbors(a) or d in G.neighbors(b)):
                # abcd is a P_4 of G
                if in_path[d] != 0:
                    print("G has a hole:")
                    print(sorted(certificate(G, cycle(in_path))))
                    return True
                elif visited_P3[edges.index((b, c)), d] == 0:
                    if process(b, c, d, visited_P3, in_path, in_path[c]):
                        return True
        in_path[c] = 0
        return False
    
    for u in G:
        in_path[u] = 1 
        for e in G.edges():
            v, w = e[0], e[1]
            if u in G.neighbors(v) and not u in G.neighbors(w) and visited_P3[edges.index((u, v)), w] == 0:
                in_path[v] = 2
                if process(u, v, w, visited_P3, in_path, 2):
                    #print("G has a hole.")
                    return 
                in_path[v] = 0
            if not u in G.neighbors(v) and u in G.neighbors(w) and visited_P3[edges.index((u, w)), v] == 0:
                in_path[w] = 2
                if process(u, w, v, visited_P3, in_path, 2):
                    #print("G has a hole.")
                    return 
                in_path[w] = 0
        in_path[u] = 0
    
    print("G does not contain a hole.")
    return 

########################################################################################################

# Example

G = nx.cycle_graph(9) 
G.add_edge(2,7)
hole_certificate(G)