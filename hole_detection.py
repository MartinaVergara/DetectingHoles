# Nikolopoulos, S., Palios, L. Detecting Holes and Antiholes in Graphs. Algorithmica 47, 119–138 (2007). https://doi.org/10.1007/s00453-006-1225-y

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

####################################################################################

# Hole-Detection Algorithm 

def find_hole(G):
    
    # vertex: index (neccesary only if the vertices are not integers)
    inode = {u: i for i, u in enumerate(G.nodes)}
    # edge: index
    iedge = {e: i for i, e in enumerate(list(G.edges) + [(e[1], e[0]) for e in G.edges])}  
    visited_P3 = np.zeros((G.number_of_edges()*2, G.number_of_nodes()), dtype=int)
    in_path = [0 for u in G]
    
    def process(a, b, c, visited_P3, in_path):
        ic = inode[c]
        in_path[ic] = 1
        visited_P3[iedge[(a, b)], ic] = 1
        visited_P3[iedge[(c, b)], inode[a]] = 1
        for d in G.neighbors(c):
            id = inode[d]
            if d not in G.neighbors(a) and d not in G.neighbors(b):
                if in_path[id] == 1:
                    return True
                elif visited_P3[iedge[(b, c)], id] == 0:
                    if process(b, c, d, visited_P3, in_path):
                        return True
        in_path[ic] = 0
        return False
    
    for u in G:
        iu = inode[u]
        in_path[iu] = 1
        for e in G.edges():
            if u not in e:
                v, w = e[0], e[1]
                iv, iw = inode[v], inode[w]
                if u in G.neighbors(v) and u not in G.neighbors(w) and visited_P3[iedge[(u, v)], iw] == 0:
                    in_path[iv] = 1
                    if process(u, v, w, visited_P3, in_path):
                        print(f'{G} has a hole.')
                        return 
                    in_path[iv] = 0
                if u not in G.neighbors(v) and u in G.neighbors(w) and visited_P3[iedge[(u, w)], iv] == 0:
                    in_path[iw] = 1
                    if process(u, w, v, visited_P3, in_path):
                        print(f'{G} has a hole.')
                        return 
                    in_path[iw] = 0
        in_path[iu] = 0
    
    print(f'{G} does not contain a hole.')
    return False

####################################################################################

# Providing a certificate
    
def hole_certificate(G):
    
    nodes = list(G.nodes)
    # node: index (neccesary only if the nodes are not integers)
    inode = {u: i for i, u in enumerate(nodes)}
    # edge: index
    iedge = {e: i for i, e in enumerate(list(G.edges) + [(e[1], e[0]) for e in G.edges])}  
    visited_P3 = np.zeros((G.number_of_edges()*2, G.number_of_nodes()), dtype=int)
    in_path = [0 for u in G]
        
    def return_hole(G, in_path, c, d):
        
        def cycle(in_path, c, d):
            active_path = [i for i, x in sorted(enumerate(in_path), key=lambda x: x[1]) if x != 0]
            print(f'active path: {active_path}')
            start = active_path.index(inode[d])
            end = active_path.index(inode[c])
            if start <= end:
                icycle = active_path[start:end + 1]
            else:
                icycle = active_path[start:] + active_path[:end + 1]
            return [nodes[i] for i in icycle]
        
        def length(C, e): 
            return abs(C.index(e[1]) - C.index(e[0]))
        
        def hole(C, e):
            i = C.index(e[0])
            i_min = i
            i_max = C.index(e[1])
            if i_max < i_min:
                i_min = i_max
                i_max = i
            return C[i_min:i_max+1]
        
        C = cycle(in_path, c, d)
        print(f'cycle: {C}')
        chords = [(u,v) for u, v in G.edges if u in C and v in C and length(C, (u,v)) not in {1, len(C)-1}]   
        print(f'chords: {chords}')
        if not chords: 
            return C
        else:
            return hole(C, min(chords, key=lambda e: length(C, e)))
        
    def process(a, b, c, visited_P3, in_path, i):
        print(f'--- start process ---\na: {a}, b: {b}, c: {c}')
        ic = inode[c]
        in_path[ic] = i + 1
        visited_P3[iedge[(a, b)], ic] = 1
        visited_P3[iedge[(c, b)], inode[a]] = 1
        print(f'in path: {in_path}')
        print(f'visited_P3:\n {visited_P3}')
        for d in G.neighbors(c):
            id = inode[d]
            print(f'd: {d}')
            if d not in G.neighbors(a) and d not in G.neighbors(b):
                if in_path[id] != 0:
                    print(f'G has a hole: {return_hole(G, in_path, c, d)}')
                    return True
                elif visited_P3[iedge[(b, c)], id] == 0:
                    if process(b, c, d, visited_P3, in_path, in_path[ic]):
                        return True
        in_path[ic] = 0
        print(f'in path: {in_path}')
        print('--- end process ---')
        return False
    
    for u in G:
        iu = inode[u]
        in_path[iu] = 1 
        #print(f'u: {u}')
        #print(f'in path: {in_path}')
        for e in G.edges:
            #print('e in G: ' + str(e))
            if u not in e:
                v, w = e[0], e[1]
                iv, iw = inode[v], inode[w]
                #print(f'v: {v}, w: {w}')
                if u in G.neighbors(v) and u not in G.neighbors(w) and visited_P3[iedge[(u, v)], iw] == 0:
                    in_path[iv] = 2
                    if process(u, v, w, visited_P3, in_path, 2):
                        return 
                    in_path[iv] = 0
                if u not in G.neighbors(v) and u in G.neighbors(w) and visited_P3[iedge[(u, w)], iv] == 0:
                    in_path[iw] = 2
                    if process(u, w, v, visited_P3, in_path, 2):
                        return 
                    in_path[iw] = 0
            #print(f'in path: {in_path}')
        in_path[iu] = 0
        #print(f'in path: {in_path}')
    print("G does not contain a hole.")
    return 

####################################################################################

def show(G):
    fig, ax = plt.subplots(figsize=(7, 7))    
    pos = nx.shell_layout(G, rotate = 0)
    nx.draw_networkx_nodes(G, pos, node_color = "tab:blue", node_size = 350, alpha = 1)
    nx.draw_networkx_edges(G, pos)
    nx.draw_networkx_labels(G, pos, font_size = 14, font_color = "white")
    plt.show()
    plt.clf()
    return

####################################################################################

# Example

G = nx.cycle_graph(9) 
G.add_edge(1,3)
G.add_edge(8,4)
G.add_edge(1,6)
G.add_edge(3,6)
G.add_edge(5,7)
hole_certificate(G)
show(G)