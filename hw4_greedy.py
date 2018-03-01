# Author: Akriti Sethi
# This class implements the TSP problem by the greedy approach. It basically takes the minimum distance from the current node to the
# next node. This keeps on going untill all the nodes are not visited, after which we add the start element at the end again.
# When this class is directly called from the wrapper, there are no changes to be made here and it would output the tour length and
# the time taken to complete the traversal. 
# When running the program independantly from this file, the user needs to uncomment the function call to this method and then 
# run the program since it would output the actual tour in addition to the time taken and cost of travelling.

try:   
    import re
    import time
    import sys, random
    random.seed(1024)
    from math import sqrt
except ImportError:
    print "Library missing! Please install the missing library and try again!!"
    pass
except:
    print "Error occured!!"
    pass

class Greedy_TSP: 
    
    def main_run(self, file_name, flag):
        
        global cm, coords, WIDTH, HEIGHT, CITIES
        try:         
            coords = self.read_from_file(file_name)
        except ImportError:
            print "Library missing! Please install the missing library and try again!!"
            return 
        except:
            print "Error occured!!"
            return 
        
        initial_time = time.time()
        CITIES = len(coords)
        visited_list = []
        
        if CITIES == 0:
            return 
        cm     = self.cartesian_matrix(coords)
        
        start_node = random.randint(0,CITIES)
        current_node = start_node
        visited_list.append(start_node)
        tour_length = 0
        
        
        while len(visited_list) != CITIES:
            min_dist = sys.maxint
            min_node = 0
            for j in range(0, CITIES):
                if current_node == j:
                    continue            
                if j in visited_list:
                    continue
                
                if min_dist>cm[(current_node,j)]:
                    min_dist = cm[(current_node,j)]
                    min_node = j
            
            
            tour_length = tour_length + cm[(current_node,min_node)]
            current_node = min_node
            visited_list.append(current_node)
                
        x = '('+str(current_node)+','+str(start_node)+')'
        y = eval(x)    
        tour_length = tour_length + cm[y]    
        final_time = time.time()
        
        visited_list.append(start_node)
        time_taken = final_time - initial_time
        if flag == True:
            print visited_list
        print tour_length 
        print str(time_taken) + " sec"
        
        return (tour_length, time_taken)
    
    # function to read a file of type EUC_2d
    def read_from_file(self, file_name):   
        output_list = []
        try:      
            with open(file_name, 'r') as f:
                for line in f:
                    try:
                        word_in_line = line.split()
                        if word_in_line[0].strip() == "EDGE_WEIGHT_TYPE" and not(word_in_line[2].strip() == "EUC_2D" or word_in_line[2].strip() == "ATT"):
                            return []
                        float(word_in_line[0])
                        output_list.append((float(word_in_line[1]),float(word_in_line[2]))) 

                    except:
                        continue

        except IOError:
            print "Oops!! The file does not exist in the location! Please add the file and try again!!"
            return []
        except EOFError:
            print "The end of file has been reached!!"
            return []
        except NameError:
            print "Oops!! The file does not exist in the location! Please add the file and try again!!"
            return []

        #except:
            #  print "Error occured!!"    

        return output_list    
    
    
    
    def cartesian_matrix(self, coords):
        """ A distance matrix """
        matrix={}
        for i,(x1,y1) in enumerate(coords):
            for j,(x2,y2) in enumerate(coords):
                
                dx, dy = x1-x2, y1-y2
                dist=sqrt(dx*dx + dy*dy)
                matrix[i,j] = dist
        
        return matrix


# Kindly uncomment this piece of code when the user wants to run only the greedy algorithm progran.

#obj = Greedy_TSP()
#obj.main_run("att48.tsp", True)
