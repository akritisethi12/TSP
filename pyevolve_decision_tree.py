# The following class predicts the class for a given set of inputs by constructing a two category decision tree
try:
    
    from pyevolve import G1DList, GAllele
    from pyevolve import GSimpleGA
    from pyevolve import Mutators
    from pyevolve import Crossovers
    from pyevolve import Consts
    from pyevolve.G1DBinaryString import G1DBinaryString
    from pyevolve import Initializators
    
    import sys, random
    random.seed(1024)
    from math import sqrt
except ImportError:
    print "Library missing! Please install and try again!!"
except:
    print "Error occured!!"


class Decision_tree_pyevolve:
    
    def main_run(self):
        
        try:
            
            genome = G1DList.G1DList(48)    
            genome.evaluator.set(lambda chromosome: self.compute_accuracy(chromosome.getInternalList()))
            genome.crossover.set(Crossovers.G1DListCrossoverSinglePoint)
            genome.initializator.set(Initializators.G1DBinaryStringInitializator)
            ga = GSimpleGA.GSimpleGA(genome)
            ga.setGenerations(100)
            ga.setMinimax(Consts.minimaxType["maximize"])
            ga.setCrossoverRate(0.6)
            ga.setMutationRate(0.01)
            ga.setPopulationSize(15)
        
            ga.evolve(freq_stats=50)
            best = ga.bestIndividual()
            
            chromosome_best = best.genomeList
            # input for which we had to predict the class
            predict_list = [{'x1':-1, 'x2':4,'x3':1,'x4':1}, {'x1':-2, 'x2':4,'x3':-1,'x4':1},
                            {'x1':3, 'x2':3,'x3':0,'x4':1}]
            
            for element in predict_list:
                print "The predicted class for ",element, "is: ", self.predict_class(element, chromosome_best)
        except NameError:
            print "Name error occured!!"
        except ArithmeticError:
            print "Arithmetic error occured!!"
        except:
            print "Error occured!!"
            
    
    
    # predicts the accuracy of the system so as to maximize the value
    def compute_accuracy(self, chromosome):
        count = 0
        accuracy = 0
        input_list = [{'x1':1, 'x2':5,'x3':-1,'x4':3,'actual':'w1'}, {'x1':-1, 'x2':5,'x3':2,'x4':2,'actual':'w1'}, 
                      {'x1':2, 'x2':3,'x3':-1,'x4':0,'actual':'w1'}, {'x1':-3, 'x2':4,'x3':-2,'x4':-1,'actual':'w1'}, 
                      {'x1':-1, 'x2':-3,'x3':1,'x4':2,'actual':'w2'}, {'x1':-2, 'x2':4,'x3':-3,'x4':0,'actual':'w2'},
                      {'x1':-3, 'x2':5,'x3':1,'x4':1,'actual':'w2'}, {'x1':1, 'x2':-2,'x3':0,'x4':0,'actual':'w2'}]
        
        try:
            
            for item in input_list:
                if self.predict_class(item, chromosome) == 'w1' and item['actual'] == 'w1':
                    count = count + 1
                
                if self.predict_class(item, chromosome) == 'w2' and item['actual'] == 'w2':
                    count = count + 1
                    
            accuracy = float(count)/8
            
        except ArithmeticError:
            print "Arithmetic error occured!!"
        except AttributeError:
            print "Attribut error occured!!"
        except:
            print "Error occured!!"
            
        return accuracy
    
    
    # predicts the class of the input item
    def predict_class(self, input_item, chromosome):
        i = 0
        chromosome_list = []
        try:
            
            while i<42:
                temp_chromosome = chromosome[i:i+6]
                sign_bit = self.find_sign(temp_chromosome[0])
                attribute_value = self.find_attribute(temp_chromosome[1:3])
                chromosome_value = int(self.find_value(temp_chromosome[3:]))
                
                # splits the chromosome into the respective values according to the bits
                chromosome_list.append({'sign':sign_bit, 'attribute':attribute_value, 'value': chromosome_value})
                
                i = i + 6
            
            # checks the value of the input in the decision tree
            if input_item[chromosome_list[3]['attribute']] < (chromosome_list[3]['value'] * chromosome_list[3]['sign']):
                if input_item[chromosome_list[1]['attribute']] < (chromosome_list[1]['value'] * chromosome_list[1]['sign']):
                    if input_item[chromosome_list[0]['attribute']] < (chromosome_list[0]['value'] * chromosome_list[0]['sign']):
                        return 'w1'
                    else:
                        return 'w2'
                else:
                    if input_item[chromosome_list[2]['attribute']] < (chromosome_list[2]['value'] * chromosome_list[2]['sign']):
                        return 'w1'
                    else:
                        return 'w2'
                
            else:
                if input_item[chromosome_list[5]['attribute']] < (chromosome_list[5]['value'] * chromosome_list[5]['sign']):
                    if input_item[chromosome_list[4]['attribute']] < (chromosome_list[4]['value'] * chromosome_list[4]['sign']):
                        return 'w1'
                    else:
                        return 'w2'
                    
                else:
                    if input_item[chromosome_list[6]['attribute']] < (chromosome_list[6]['value'] * chromosome_list[6]['sign']):
                        return 'w1'
                    else:
                        return 'w2'
                    
        except AttributeError:
            print "Attribute error occured!!"
        except ArithmeticError:
            print "Arithmetic error occured!!"
        except:
            print "Error occured"
    
    # classifies the sign on the basis of the first index
    def find_sign(self, first_bit):
        try:        
            if int(first_bit) == 1:
                return 1
            else:
                return -1
            
        except NameError:
            print "Name Error occured!!"
        except:
            print "Error occured!!"
    
    # classifies the 2nd and 3rd bit as x1, x2, x3, x4
    def find_attribute(self, bits_input):
        try:            
            bits = str(bits_input[0])+""+str(bits_input[1])
            if bits == '00':
                return 'x1'
            elif bits == '01':
                return 'x2'
            elif bits == '10':
                return 'x3'
            else:
                return 'x4'
            
        except NameError:
            print "Name Error occured!!"
        except:
            print "Error occured!!"
    
    # converts a binary number to decimal value    
    def find_value(self, bits_input):
        try:            
            bits = str(bits_input[0])+""+str(bits_input[1])+""+str(bits_input[2])
            decimal_value = int(str(bits),2)
            
        except NameError:
            print "Name Error occured!!"
        except:
            print "Error occured!!"
            
        return decimal_value
    

obj_decision_tree = Decision_tree_pyevolve()
obj_decision_tree.main_run()
