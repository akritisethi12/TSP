# Author: Akriti Sethi
# This class is a wrapper class which can be used to run the code for genetic algorithm and greedy algorithm. In this file, the
# input needs to be the folder name where the user has stored all the files for which they need to output the tour length 
# and time taken. Both the algorithms would run in sequence for one or multiple files depeneding on the number of files in the
# folder.

try:    
    import os
    import csv
    from pyevolve_ex12_tsp import Genetic_algorithm
    from hw4_greedy import Greedy_TSP
except ImportError:
    print "Library missing! Please install the missing library and try again!!"
    pass
except:
    print "Error occured!!"
    pass
    
class Wrapper_Class:
    def main(self):       
        file_names = ""
        try:
            # reading the folder name from the user
            folder_name = raw_input("Please enter the folder name from where the files have to be read!!\n")
            
            file_names = os.listdir(folder_name)
        except NameError:
            print "Name error occured!!"
        except AttributeError:
            print "Attribue error occured!!"
        except:
            print "Error occured!!"
        
        try:
            # creating an object of the class where genetic algorithm and greedy algorithm are implemented
            genetic_obj = Genetic_algorithm()
            greedy_obj = Greedy_TSP()
        except NameError:
            print "Name error occured!!"
        except AttributeError:
            print "Attribue error occured!!"
        except:
            print "Error occured!!"        
        
        for x in file_names:
            try:
                
                print "Output for Genetic for file:",x
                tour_len_genetic = genetic_obj.main_run(False, folder_name+"/"+x)
                print "Output for Greedy for file:",x
                tour_len_greedy = greedy_obj.main_run(folder_name+"/"+x, False)
                
                if len(tour_len_genetic) == 0 and len(tour_len_greedy) == 0:
                    print "Program terminates here!!"
            except NameError:
                print "Name error occured!!"
            except AttributeError:
                print "Attribue error occured!!"
            except:
                print "Error occured!!"            
        
        
        
obj_wrapper = Wrapper_Class()
obj_wrapper.main()
