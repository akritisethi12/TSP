# Author: Akriti Sethi
# This class calculates the tour length and time taken to reach an optimal stage by applying genetic algorithm. We use the
# pyevolve library to do so.
# If this function is called from the wrapper nothing needs to be done. But if this file is to be executed independantly, 
# kindly uncomment the function call and execute the program!

try:   
    from pyevolve import G1DList, GAllele
    from pyevolve import GSimpleGA
    from pyevolve import Mutators
    from pyevolve import Crossovers
    from pyevolve import Consts

    import sys, random
    import time
    random.seed(1024)
    from math import sqrt

except ImportError:
    print "Some libraries are missing!!"

PIL_SUPPORT = None

try:
    from PIL import Image, ImageFont, ImageDraw

except:
    PIL_SUPPORT = False

class Genetic_algorithm:

    cm     = []
    coords = []
    CITIES = 100
    WIDTH   = 1024
    HEIGHT  = 768
    LAST_SCORE = -1


    def __init__(self):
        pass

    def cartesian_matrix(self, coords):
        """ A distance matrix """
        matrix={}
        for i,(x1,y1) in enumerate(coords):
            for j,(x2,y2) in enumerate(coords):
                dx, dy = x1-x2, y1-y2
                dist=sqrt(dx*dx + dy*dy)
                matrix[i,j] = dist
        return matrix

    def tour_length(self, matrix, tour):
        """ Returns the total length of the tour """
        total = 0
        t = tour.getInternalList()
        for i in range(CITIES):
            j      = (i+1)%CITIES
            total += matrix[t[i], t[j]]
        return total

    def write_tour_to_img(self, coords, tour, img_file):
        """ The function to plot the graph """
        padding=20
        coords=[(x+padding,y+padding) for (x,y) in coords]
        maxx,maxy=0,0
        for x,y in coords:
            maxx, maxy = max(x,maxx), max(y,maxy)
        maxx+=padding
        maxy+=padding
        img=Image.new("RGB",(int(maxx),int(maxy)),color=(255,255,255))
        font=ImageFont.load_default()
        d=ImageDraw.Draw(img);
        num_cities=len(tour)
        for i in range(num_cities):
            j=(i+1)%num_cities
            city_i=tour[i]
            city_j=tour[j]
            x1,y1=coords[city_i]
            x2,y2=coords[city_j]
            d.line((int(x1),int(y1),int(x2),int(y2)),fill=(0,0,0))
            d.text((int(x1)+7,int(y1)-5),str(i),font=font,fill=(32,32,32))

        for x,y in coords:
            x,y=int(x),int(y)
            d.ellipse((x-5,y-5,x+5,y+5),outline=(0,0,0),fill=(196,196,196))
        del d
        img.save(img_file, "PNG")
        print "The plot was saved into the %s file." % (img_file,)

    def G1DListTSPInitializator(self, genome, **args):
        """ The initializator for the TSP """
        lst = [i for i in xrange(genome.getListSize())]
        random.shuffle(lst)
        genome.setInternalList(lst)

    def main_run(self, PIL_SUPPORT, file_name):
        global cm, coords, WIDTH, HEIGHT, CITIES
        time_taken = 0
        start_time = time.time()

        flag = False
        if PIL_SUPPORT == True:
            flag = True
        else:
            flag = False

        try:
            coords = self.read_from_file(file_name)
        except NameError:
            print "Oops!! The file does not exist in the location! Please add the file and try again!!"
        except IOError:
            print "File error occured!!"

        CITIES = len(coords)

        if CITIES == 0:
            return
        cm     = self.cartesian_matrix(coords)
        genome = G1DList.G1DList(len(coords))

        genome.evaluator.set(lambda chromosome: self.tour_length(cm, chromosome))
        genome.crossover.set(Crossovers.G1DListCrossoverEdge)
        genome.initializator.set(self.G1DListTSPInitializator)

        ga = GSimpleGA.GSimpleGA(genome)
        ga.setGenerations(1000)
        ga.setMinimax(Consts.minimaxType["minimize"])
        ga.setCrossoverRate(1.0)
        ga.setMutationRate(0.02)
        ga.setPopulationSize(80)

        ga.evolve(freq_stats=500)
        best = ga.bestIndividual()

        tour_len = self.tour_length(cm, best)
        print tour_len

        if PIL_SUPPORT:
            self.write_tour_to_img(coords, best, "tsp_result.png")

        finish_time = time.time()
        if flag == True:
            self.write_to_output_file(best)
        if flag == False:
            time_taken = finish_time-start_time
            print "Tour length: ", tour_len
            print "Time taken: ", time_taken

        return (tour_len, time_taken)

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

    def write_to_output_file(self, best):
        output = open("output_file.txt", 'w')
        out_value = "TOUR_SECTION\n"
        for line in best.genomeList:
            out_value += str(line)+"\n"     

        output.write(out_value)
        output.close()

        print "The path was saved to the file: output_file.txt"



#obj = Genetic_algorithm()
#obj.main_run(True, "att48.tsp")
