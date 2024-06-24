# Nikolopoulos, S., Palios, L. Detecting Holes and Antiholes in Graphs. Algorithmica 47, 119–138 (2007). https://doi.org/10.1007/s00453-006-1225-y

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
####################################################################################

# Hole-Detection Algorithm for graphs whose vertices are integers

def find_hole_int(G):
    
    iedge = {e: i for i, e in enumerate(list(G.edges) + [(e[1], e[0]) for e in G.edges])} 
    visited_P3 = np.zeros((G.number_of_edges()*2, G.number_of_nodes()), dtype=int)
    in_path = [0 for u in G]
    
    def process(a, b, c, visited_P3, in_path):
        in_path[c] = 1
        visited_P3[iedge[(a, b)], c] = 1
        visited_P3[iedge[(c, b)], a] = 1
        for d in G.neighbors(c):
            if d not in G.neighbors(a) and d not in G.neighbors(b):
                if in_path[d] == 1:
                    return True
                elif visited_P3[iedge[(b, c)], d] == 0:
                    if process(b, c, d, visited_P3, in_path):
                        return True
        in_path[c] = 0
        return False
    
    for u in G:
        in_path[u] = 1
        for e in G.edges():
            if u not in e:
                v, w = e[0], e[1]
                if u in G.neighbors(v) and u not in G.neighbors(w) and visited_P3[iedge[(u, v)], w] == 0:
                    in_path[v] = 1
                    if process(u, v, w, visited_P3, in_path):
                        print(f'{G} has a hole.')
                        return 
                    in_path[v] = 0
                if u not in G.neighbors(v) and u in G.neighbors(w) and visited_P3[iedge[(u, w)], v] == 0:
                    in_path[w] = 1
                    if process(u, w, v, visited_P3, in_path):
                        print(f'{G} has a hole.')
                        return 
                    in_path[w] = 0
        in_path[u] = 0
    
    print(f'{G} does not contain a hole.')
    return False

####################################################################################

# Hole-Detection Algorithm for graphs whose vertices are not necessarily integers

def find_hole(G):
    
    ivertex = {u: i for i, u in enumerate(G.nodes)} 
    iedge = {e: i for i, e in enumerate(list(G.edges) + [(e[1], e[0]) for e in G.edges])}  
    visited_P3 = np.zeros((G.number_of_edges()*2, G.number_of_nodes()), dtype=int)
    in_path = [0 for u in G]
    
    def process(a, b, c, visited_P3, in_path):
        ic = ivertex[c]
        in_path[ic] = 1
        visited_P3[iedge[(a, b)], ic] = 1
        visited_P3[iedge[(c, b)], ivertex[a]] = 1
        for d in G.neighbors(c):
            id = ivertex[d]
            if d not in G.neighbors(a) and d not in G.neighbors(b):
                if in_path[id] == 1:
                    return True
                elif visited_P3[iedge[(b, c)], id] == 0:
                    if process(b, c, d, visited_P3, in_path):
                        return True
        in_path[ic] = 0
        return False
    
    for u in G:
        iu = ivertex[u]
        in_path[iu] = 1
        for e in G.edges():
            if u not in e:
                v, w = e[0], e[1]
                iv, iw = ivertex[v], ivertex[w]
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

# Providing a certificate (for graphs whose vertices are not necessarily integers)
    
def hole_certificate(G):
    
    vertices = list(G.nodes)
    ivertex = {u: i for i, u in enumerate(vertices)}
    iedge = {e: i for i, e in enumerate(list(G.edges) + [(e[1], e[0]) for e in G.edges])}  
    visited_P3 = np.zeros((G.number_of_edges()*2, G.number_of_nodes()), dtype=int)
    in_path = [0 for u in G]
        
    def return_hole(G, in_path, c, d):
        
        def cycle(in_path, c, d):
            active_path = [i for i, x in sorted(enumerate(in_path), key=lambda x: x[1]) if x != 0]
            print(f'active path: {active_path}')#
            start = active_path.index(ivertex[d])
            end = active_path.index(ivertex[c])
            if start <= end:
                icycle = active_path[start:end + 1]
            else:
                icycle = active_path[start:] + active_path[:end + 1]
            return [vertices[i] for i in icycle]
        
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
        print(f'cycle: {C}')#
        chords = [(u,v) for u, v in G.edges if u in C and v in C and length(C, (u,v)) not in {1, len(C)-1}]   
        print(f'chords: {chords}')#
        if not chords: 
            return C
        else:
            return hole(C, min(chords, key=lambda e: length(C, e)))
        
    def process(a, b, c, visited_P3, in_path, i):
        print(f'--- start process ---\na: {a}, b: {b}, c: {c}')#
        ic = ivertex[c]
        in_path[ic] = i + 1
        visited_P3[iedge[(a, b)], ic] = 1
        visited_P3[iedge[(c, b)], ivertex[a]] = 1
        print(f'in path: {in_path}\nvisited_P3:\n {visited_P3}')#
        for d in G.neighbors(c):
            id = ivertex[d]
            print(f'd: {d}')#
            if d not in G.neighbors(a) and d not in G.neighbors(b):
                if in_path[id] != 0:
                    print(f'{G} has a hole: {return_hole(G, in_path, c, d)}')
                    return True
                elif visited_P3[iedge[(b, c)], id] == 0:
                    if process(b, c, d, visited_P3, in_path, in_path[ic]):
                        return True
        in_path[ic] = 0
        print(f'in path: {in_path}\n--- end process ---')#
        return False
    
    for u in G:
        iu = ivertex[u]
        in_path[iu] = 1 
        print(f'u: {u}\nin path: {in_path}')#
        for e in G.edges:
            print(f'e in G: {e}')#
            if u not in e:
                v, w = e[0], e[1]
                iv, iw = ivertex[v], ivertex[w]
                print(f'v: {v}, w: {w}')#
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
            print(f'in path: {in_path}')#
        in_path[iu] = 0
        print(f'in path: {in_path}')#
    print(f'{G} does not contain a hole.')
    return 

####################################################################################

# Detecting holes on at least k vertices

def find_hole_k(G, k):
    
    ivertex = {u: i for i, u in enumerate(G.nodes)}
    visitedPk_2 = []
    in_path = [0 for u in G]
     
    # List of all induced paths of length l of G
    def induced_paths(G, l):
        paths = []
        
        def is_chordless(path, v):
            # Check if adding vertex to path creates a chord
            for i in range(len(path) - 1):
                if G.has_edge(path[i], v):
                    return False
            return True
        
        def dfs(u, path):
            if len(path) == l:
                paths.append(path.copy())
                return
            for v in G.neighbors(u):
                if v not in path and is_chordless(path, v):
                    path.append(v)
                    dfs(v, path)
                    path.pop()
        
        for u in G:
            dfs(u, [u])
        return paths
    
    def process(pk_2, visitedPk_2, in_path):    
        
        c = pk_2[-1]
        ic = ivertex[c] 
        in_path[ic] = 1    
        print(f'c: {c}\nin_path: {in_path}')#
        
        visitedPk_2.append(pk_2)
        visitedPk_2.append(pk_2[::-1])
        print(f'visitedPk_2: {visitedPk_2}')#
        
        for d in G.neighbors(c):
            print(f'd: {d}')#
            if all(d not in G.neighbors(pk_2[i]) for i in range(k-3)):
                # pk_2 + [d] is a P_k-1
                if in_path[ivertex[d]] == 1:
                    return True
                else:
                    new_pk_2 = pk_2[1:] + [d] 
                    print(f'new_pk_2: {new_pk_2}')#
                    if new_pk_2 not in visitedPk_2:
                        if process(new_pk_2, visitedPk_2, in_path):
                            return True
                        
        in_path[ic] = 0
        print(f'c: {c}\nin_path: {in_path}')#
        return False
        
    for u in G:
        
        iu = ivertex[u]
        in_path[iu] = 1
        print(f'u: {u}')#
        
        # Try to extend each P_k-3 of G into a P_k-2 by adding u  
        for pk_3 in [p for p in induced_paths(G, k-3) if u not in p]:
            
            source = pk_3[0]
            isource = ivertex[source]
            subpath = [pk_3[i] for i in range(1, k-4)] 
            isubpath = [ivertex[v] for v in subpath] 
            target = pk_3[k-4]
            itarget = ivertex[target]        
            print(f'pk_3: {pk_3}\nsource: {source}, subpath: {subpath}, target: {target}')#
                   
            if all(u not in G.neighbors(v) for v in subpath):
                if u in G.neighbors(source) and u not in G.neighbors(target):
                    pk_2 = [u] + pk_3
                    print(f'pk_2: {pk_2}')#
                    if pk_2 not in visitedPk_2:
                        # Try to extend the P_k-2 into a P_k-1
                        in_path[isource] = 1
                        for i in isubpath: 
                            in_path[i] = 1
                        print(f'in path: {in_path}')#
                        if process(pk_2, visitedPk_2, in_path): 
                            print(f'{G} has a hole on at least {k} vertices.')
                            return True
                        in_path[isource] = 0
                        for i in isubpath:
                            in_path[i] = 0
                        print(f'in path: {in_path}')#
                if u not in G.neighbors(source) and u in G.neighbors(target):
                    pk_2 = [u] + pk_3[::-1]
                    print(f'pk_2: {pk_2}')#
                    if pk_2 not in visitedPk_2:
                        # Try to extend the P_k-2 into a P_k-1
                        in_path[itarget] = 1
                        for i in isubpath:
                            in_path[i] = 1
                        print(f'in path: {in_path}')#
                        if process(pk_2, visitedPk_2, in_path): 
                            print(f'{G} has a hole on at least {k} vertices.')
                            return True
                        in_path[itarget] = 0
                        for i in isubpath:
                            in_path[i] = 0   
                        print(f'in path: {in_path}')#
                        
        in_path[iu] = 0
        print(f'in path: {in_path}')#
        
    print(f'{G} does not contain a hole on at least {k} vertices.')
    return False

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

# Examples

G = nx.cycle_graph(9) 
G.add_edge(1,3)
G.add_edge(7,4)
G.add_edge(1,6)
G.add_edge(3,6)
G.add_edge(5,7)
hole_certificate(G)
show(G)

G = nx.cycle_graph(7) 
G.add_edge(1,6)
find_hole_k(G, 7)
show(G)