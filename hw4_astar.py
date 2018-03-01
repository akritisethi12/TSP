# Author: Akriti Sethi
# This implements the A* algorithm.
try:    
    import re
    import operator
    import collections
    import heapq
    from operator import itemgetter
    
    import sys, random
    random.seed(1024)
    from math import sqrt

except ImportError:
    print "Import Error occured!!"
    
except:
    print "Error occured!!"

cm     = []
coords = []
CITIES = 100
WIDTH   = 1024
HEIGHT  = 768
LAST_SCORE = -1

def main_run():
    global cm, coords, WIDTH, HEIGHT, CITIES
    file_name = ""
    try:
        # reading the folder name from the user
        file_name = raw_input("Please enter the file name for the A* algorithm!!\n")
    
    except NameError:
        print "Name error occured!!"
    except AttributeError:
        print "Attribue error occured!!"
    except:
        print "Error occured!!"    

    coords = read_from_file(file_name)
    
    g = 0
    CITIES = len(coords)
    
    if CITIES == 0:
        return
    
    visited_list = []
    unvisited_list = []
    
    cm     = cartesian_matrix(coords)
    
    for i in range(0,CITIES):
        unvisited_list.append(i)
    
    index = 0
    h_min_list = []
    start_index = 0
    
    # logic for pass 0
    for i in unvisited_list:
        
        h_3 = 0
        calc_kruskals = list((set(unvisited_list) - set([i])))    
        h_3 = kruskals_algo(calc_kruskals, file_name) 
        dist_start = []
        
        min_start = 0
        
        for j in unvisited_list:
            if i == j:
                continue
               
            y_start = (i,j)
            dist_start.append(cm[y_start])
            
                       
        min_start = min(dist_start)
        h = h_3 + min_start
        h_min_list.append((h,i))
        
        
    start_index = min(h_min_list)[1]   
    
    unvisited_list = []
    visited_list.append(start_index) 
    for x in range(0,len(coords)):
        if x == start_index:
            continue
        unvisited_list.append(x)
        
    heap_f_value = []
    
    temp_visited_list = []
    min_value_h1 = sys.maxint
    min_value_h2 = sys.maxint
    
    g = 0
    final_min = sys.maxint
   
    # main logic starts
    while True:
        
        f = 0
        final_min = sys.maxint
        
        # calculation of g(x)
        
        if len(visited_list) == 1:
            g = 0

        final_id = 0
        final_min = sys.maxint      
        
        for i in unvisited_list:
            min_value_h1 = sys.maxint
            min_value_h2 = sys.maxint
            h_3 = 0                        
            
            for m in unvisited_list:
                if int(m) == int(i):
                    continue
                else:
                    x1 = '('+str(i)+','+str(m)+')'
                    y1 = eval(x1) 
                    if min_value_h1>cm[y1]:
                        min_value_h1 = cm[y1]
                     
                   
                    if int(m) == int(start_index):
                        continue
                    else:                    
                   
                        x2 = '('+str(start_index)+','+str(m)+')'
                        y2 = eval(x2)
                        
                        if min_value_h2>cm[y2]:
                            min_value_h2 = cm[y2]
                        
            
            calc_kruskals = list((set(unvisited_list) - set([i])))    
            h_3 = kruskals_algo(calc_kruskals, file_name)
            h = min_value_h1 + min_value_h2 + h_3
           
            
            f = g + h
            temp_visited_list = list(visited_list)
            temp_visited_list.append(i)
            heapq.heappush(heap_f_value, (f, temp_visited_list))         
            # elements pushed into a priority queue
            
        
        popped_element = heapq.heappop(heap_f_value)
        
        pop_index = 0
        
        dist_list_popped = [popped_element]
        popped_element_f = popped_element[0]
        popped_element_dist = len(popped_element[1])
        min_popped = popped_element
        while True:
            temp_popped_element = heapq.heappop(heap_f_value)
            dist_list_popped.append(temp_popped_element)
            
            if (temp_popped_element[0] - popped_element_f) > 1.0:              
                break
                                  
            if len(temp_popped_element[1]) > popped_element_dist:
                min_popped = temp_popped_element
                popped_element_dist = len(temp_popped_element[1])
            
            
        dist_list_popped.remove(min_popped)
        for b in dist_list_popped:
            heapq.heappush(heap_f_value, b)
        popped_element = min_popped
        
        visited_list = []
        unvisited_list = []
        visited_list = popped_element[1]
        # print visited_list
        
        g = tour_length(cm, visited_list)
        for x in range(0,len(coords)):
            if x in popped_element[1]:
                continue
            unvisited_list.append(x)       
        
        if len(unvisited_list) == 1:
            break
        
    
    visited_list.append(unvisited_list[0])   
    visited_list.append(start_index)
    final_g = tour_length(cm, visited_list)
    print visited_list
    print final_g
    
def read_from_file(file_name):   
    output_list = []
    try:      
        with open(file_name, 'r') as f:
            for line in f:
                try:
                    word_in_line = line.split()
                    float(word_in_line[0])
                    output_list.append((float(word_in_line[1]),float(word_in_line[2]))) 
                except:
                    continue

    except IOError:
        print "The file does not exists!!"
    except EOFError:
        print "The end of file has been reached!!"
    #except:
        #  print "Error occured!!"    

    return output_list
       
    
def cartesian_matrix(coords):
    """ A distance matrix """
    matrix={}
    for i,(x1,y1) in enumerate(coords):
        for j,(x2,y2) in enumerate(coords):
            
            dx, dy = x1-x2, y1-y2
            dist=sqrt(dx*dx + dy*dy)
            matrix[i,j] = dist
    
    return matrix

def kruskals_algo(list_input, file_name):
    
    # logic for Kruskal's algorithm
    coords = read_from_file(file_name)
    CITIES = len(coords)      
    matrix     = cartesian_matrix(coords)
    
    h_value = 0.0
    
    sorted_matrix =sorted(matrix.items(), key=lambda matrix:matrix[1])
    visited = []
    subgraph = []
    
    for element in range(0, len(matrix)):
        
        item = sorted_matrix[element]
        item_split = item[0]
        dist = item[1]
        source = item_split[0]
        dest = item_split[1]
        
        if source not in list_input or dest not in list_input:
            continue       
        
        if source is dest:
            continue        
        
        if len(subgraph) == 0 and len(visited) == 0:
            temp_set = set([source,dest])
            subgraph.append(temp_set)
            h_value = h_value + dist
            continue

        
        source_index = -1
        dest_index = -1
        i = 0
        
        while(True):
            if len(subgraph) == 0:
                break
            if source in subgraph[i]:
                source_index = i
            
            if dest in subgraph[i]:
                dest_index = i
            
            i = i +1
            
            if i == len(subgraph):
                break        
        
        
        if source_index == -1 and dest_index == -1:
            temp_set = set([source,dest])
            subgraph.append(temp_set)            
            visited = subgraph[i].union(visited)
            h_value = h_value + dist
            
        elif source_index != -1 and dest_index == -1:
            subgraph[source_index].add(dest)           
            visited = subgraph[source_index].union(visited)
            h_value = h_value + dist
            
        elif source_index == -1 and dest_index != -1:
            subgraph[dest_index].add(source)
            visited = subgraph[dest_index].union(visited)
            h_value = h_value + dist
            
        elif source_index != -1 and dest_index != -1:
            if source_index == dest_index:
                continue
            else:
                if source_index > dest_index:
                    subgraph[dest_index] = subgraph[source_index].union(subgraph[dest_index])
                    del subgraph[source_index]
                    h_value = h_value + dist
                    
                else:
                    subgraph[source_index] = subgraph[source_index].union(subgraph[dest_index])
                    del subgraph[dest_index]
                    h_value = h_value + dist
                    
        
        if len(visited) == CITIES and len(subgraph) == 1:
            break
    
    return h_value 

def tour_length(matrix, t):
    """ Returns the total length of the tour """
    total = 0
    
    for i in range(len(t)):
        j      = (i+1)%len(t)
        total += matrix[(t[i], t[j])]
    return total
    
main_run()
