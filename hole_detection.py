'''
HOLE-DETECTION ALGORITHM for detecting holes on at least k vertices

Nikolopoulos, S., Palios, L. Detecting Holes and Antiholes in Graphs. Algorithmica 47, 119–138 (2007). https://doi.org/10.1007/s00453-006-1225-y

'''
import networkx as nx
import matplotlib.pyplot as plt

def integer_graph(G):
    '''
    This function constructs a graph, with integer nodes, which represents graph G (by mapping original vertices to integer indices and respecting adjacencies).
    
    '''
    n = nx.number_of_nodes(G)
    index = {v: i for i, v in enumerate(G.nodes())}
    
    H = nx.Graph()
    H.add_nodes_from(range(n))
    for u, v in G.edges():
        H.add_edge(index[u], index[v])
    return H

def find_hole(G, k): 
    '''
    This is the main function of the HOLE-DETECTION ALGORITHM.
   
    Purpose:    To determine if the graph G contains a hole of length k or more.
    
    Inputs:     G: The graph to be checked.
                k: The minimum length of the hole to be detected.
    
    Output:     True if the graph contains a hole of length k or more.
                False otherwise.
                
    The code uses a depth-first search approach to build paths in the graph and tries to detect if these paths can be extended to form a hole of length k. It efficiently tracks the paths and their extensions, using recursive calls and backtracking to explore possible cycles in the graph.
    
    As Nikolopoulos and Palios say: "We try to extend a P_k−2 u_0, u_1, ..., u_k−3 into P_k−1s of the form u_0, u_1, ..., u_k−3, u_k−2, then, for each such P_k−1, we proceed by extending the P_k−2 u_1, u_2, ..., u_k−2 into Pk−1s, and so on. In the above cases, the active-path is u_0, u_1, ..., u_k−3, it becomes u_0, u_1, ..., u_k−3, u_k−2, then u_0, u_1, ..., u_k−3, u_k−2, u_k-1, and so on (when we backtrack, the corresponding vertices are removed from the end of the current active-path); if ever we proceed to a P_k-2 such that the last vertex appears again in the current active-path, then the graph G contains a cycle and consequently a hole."
                
    '''
    def process(v, active_path, neighbors_in_pk_3, in_path): 
        '''
        Purpose:    To check if a given (long) path, called the "active-path", can be extended into a hole.

        Inputs:     v: The vertex to be added to extend the active-path.
                    
                    active_path: The given (long) path, ie. the active-path.
                    > active_path[-(k-3):] (ie. the list formed by the last k-3 elements of active_path) is a P_k-3, which we call "the current P_k-3".
                    > active_path[-(k-3):] + [v] is a P_k-2, which we call "the current P_k-2".
                    
                    neighbors_in_pk_3: A list of how many neighbors each vertex has in the current P_k-3.
                    
                    in_path: A list indicating which vertices are in the active-path. 
                    
        * Observe that active_path is equal to the current P_k-3 only when proccess is called from search_from.
        
        Logic:

        1. Add v to the path and update the neighborhood counts.
        2. For each neighbor w of v, check if w can complete a hole:
                > If w is already in the path, it completes the cycle.
                > Otherwise, update the path and neighborhood information and recursively call process.
        3. Backtrack if no hole is found.
        
        '''
        in_path[v] = 1
        active_path.append(v) # Now active_path[-(k-2):] is a P_k-2
        for w in neighborhood[v]:
            neighbors_in_pk_3[w] = neighbors_in_pk_3[w] + 1 # Now neighbors_in_pk_3 is a list of how many neighbors each vertex has in the current P_k-2.
        
        for w in neighborhood[v]: 
            if neighbors_in_pk_3[w]  == 1:
                # active_path[-(k-2):] + [w] is a P_k-1
                if in_path[w] == 1:
                    return True
                else:
                    source_pk_2 = active_path[-(k-2)]
                    for u in neighborhood[source_pk_2]:
                        neighbors_in_pk_3[u] = neighbors_in_pk_3[u] - 1
                    if process(w, active_path, neighbors_in_pk_3, in_path):
                        return True
                    for u in neighborhood[source_pk_2]:
                        neighbors_in_pk_3[u] = neighbors_in_pk_3[u] + 1
        
        for w in neighborhood[v]:
            neighbors_in_pk_3[w] = neighbors_in_pk_3[w] - 1            
        del active_path[-1]        
        in_path[v] = 0      
                    
        return False    

    def search_from(v, path, neighbors_in_path, in_path):
        '''
        Purpose:    To extend a path starting from vertex v into a P_k-3 and check if it can be extended to a hole of length k. 
        
        Inputs:     v: The current vertex being processed.
                    path: The current path being built.
                    neighbors_in_path: A list tracking how many neighbors each vertex has in the current path.
                    in_path: A list indicating which vertices are currently in the path.

        Logic:    
                      
        1. Add vertex v to the path.
        2. Update the count of how many times each neighbor of v is present in the path.
        3. If the path is a P_k−3: 
                > Try to extend the path by adding a neighbor w of v.
                > If w can be added to form a P_k-2, call process to check if this extension results in a hole. The function process is called with a copy of path and the vertex w allowing its extension (the path is extended into the corresponding P_k-2 inside process). 
           Else: Recursively attempt to extend the path by processing each neighbor of v.                    
    
        '''
        in_path[v] = 1 # This means that v belongs to the current active-path. Otherwise, in_path[v] = 0.
        path.append(v)        
        for w in neighborhood[v]:
            # neighbors_in_path[w] = number of neighbors of w in path
            neighbors_in_path[w] = neighbors_in_path[w] + 1       
        
        if len(path) == k-3:
            for w in neighborhood[v]:
                # Observe that if neighbors_in_path[w] == 1 then v is the only neighbor of w in path, so path + [w] is chordless.
                if in_path[w] == 0 and neighbors_in_path[w]  == 1 and process(w, path, neighbors_in_path, in_path):
                    return True
        else:      
            for w in neighborhood[v]:
                if in_path[w] == 0 and neighbors_in_path[w]  == 1 and search_from(w, path, neighbors_in_path, in_path):
                    return True
                
        in_path[v] = 0 
        del path[-1]            
        for w in neighborhood[v]:
            neighbors_in_path[w] = neighbors_in_path[w] - 1     
            
        return False                
          
    '''
    Main part of find_hole: 
    
    > Converts G into a format suitable for processing.
    > Creates the dictionary neighborhood where each key is a vertex, and the value is a list of its neighbors.
    > Iterates through each vertex v of G and uses the search_from function to try to build a path starting from v. If search_from finds a hole of length k or more, find_hole returns True. If no hole is found after all vertices are checked, it returns False.
    
    '''
    H = integer_graph(G) 
    n = nx.number_of_nodes(G)
    neighborhood = {v: list(H.neighbors(v)) for v in H} 
        
    for v in H:
        if search_from(v, [], [0]*n, [0]*n):     
            print(f"G contains a hole on at least {k} vertices.")   
            return   
    
    print(f"G does not contain a hole on at least {k} vertices.")    
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

# Examples

G = nx.cycle_graph(9) 
G.add_edge(1,3)
G.add_edge(7,4)
G.add_edge(1,6)
G.add_edge(3,6)
G.add_edge(5,7)
find_hole(G, 7)
show(G)

G = nx.cycle_graph(7) 
G.add_edge(1,6)
find_hole(G, 5)
show(G)