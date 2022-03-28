from math import e, sin
from pickletools import int4
from tkinter import *
from Board import *
import neat
import os
import random
import visualize
import pickle
import copy
from neat.six_util import iteritems, itervalues

##CONFIGURE THE STARTING BOARD SETTINGS
board_config = [
[[],[],[],[],[],[],[],[]],
[[],[],[],[],[],[],[],[]],
[[],[],[],[],[],[],[],[]],
[[],[],[],[],[],[],[],[]],
[[],[],[],[],[],[],[],[]],
[[],[],[],[],[],[],[],[]],
[[],[],[],[],[],[],[],[]],
[[],[],[],[],[],[],[],[]]
]

blue = [
[1,1,1],[1,1,3],[1,1,5],[1,1,7],
[1,2,2],[1,2,4],[1,2,6],[1,2,8],
[1,3,1],[1,3,3],[1,3,5],[1,3,7]]

red = [
[1,6,2],[1,6,4],[1,6,6],[1,6,8],
[1,7,1],[1,7,3],[1,7,5],[1,7,7],
[1,8,2],[1,8,4],[1,8,6],[1,8,8]]


count = 0
fitnesses = [0]*10000
oneGame = type(None)



#Gets the size of the screen being used.
def get_display_size():
    root = Tk()
    root.update_idletasks()
    root.attributes('-fullscreen', True)
    root.state('iconic')
    height = root.winfo_screenheight()
    root.destroy()
    return height-250 #Arbitrary number to make height GUI smaller than screen


dp = get_display_size()

DispTXT=["Play as Blue!","Play as Red!","Play as Blue! (No GUI)","Play as Red! (No GUI)","Manually train NEAT","NEAT vs NEAT"]

button=[]
root=Tk()
root.title("What would you like to play as?")
root.geometry('350x200')
root.wm_attributes("-topmost", 1)


for i in range(6):
    b = Button(root, text=DispTXT[i], command= lambda i = i: multiFunky(i))
    b.pack()
    button.append(b)

def multiFunky(players):
    global gameType
    gameType = players
    for i in range(6):
        button[i].destroy()
    root.destroy()

    #strH=str(dp)+'x'+str(dp)  
    #root.geometry(strH)
    
root.mainloop()





def replay_genome(config_path, genome_path="winner.pkl"):
    # Load requried NEAT config
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

    # Unpickle saved winner
    with open(genome_path, "rb") as f:
        genome = pickle.load(f)


def single_genome():
    if(gameType == 0):
        oneHuman = Human("Blue", [red,blue],i)
        oneRobot = Robot("Red", [red,blue],i)
        oneGame = checkerboardClass(copy.deepcopy(board_config), copy.deepcopy(red), copy.deepcopy(blue), oneHuman, oneRobot)

    if(gameType == 1):
        oneRobot = Robot("Blue", [red,blue],i)
        oneHuman = Human("Red", [red,blue],i)
        oneGame = checkerboardClass(copy.deepcopy(board_config), copy.deepcopy(red), copy.deepcopy(blue), oneRobot, oneHuman)

    if(gameType == 2):
        oneHuman = Human("Blue", [red,blue],i)
        oneRobot = Robot("Red", [red,blue],i)
        oneGame = checkerboardClass(copy.deepcopy(board_config), copy.deepcopy(red), copy.deepcopy(blue), oneHuman, oneRobot)

    if(gameType == 3):
        oneRobot = Robot("Blue", [red,blue],i)
        oneHuman = Human("Red", [red,blue],i)
        oneGame = checkerboardClass(copy.deepcopy(board_config), copy.deepcopy(red), copy.deepcopy(blue), oneRobot, oneHuman)




def eval_genomes(genomes, config):
    global geno, nets, fitnesses, currentGames, redRobots, blueRobots, allRobots, count, oneRobot
    blueRobots = []
    redRobots = []
    allRobots = []
    geno = []
    nets = []
    currentGames = []
    count += 1


    i = 0
    if(len(genomes) == 1):
        net = neat.nn.FeedForwardNetwork.create(genomes[0], config)

        while(oneGame.win == False): ##while nobody has won, continue to run. 
            if (oneGame.currentTurn == "Blue"):
                if(oneGame.p1.isRobot()):
                    output = net.activate(oneGame.refreshData()) 
                    oneGame.getSelection(oneGame.p1,output)  
                
                else:
                    if(gameType == 2 or gameType == 3):
                        oneGame.p1.requestSelection()
                    else:
                        pass #graphical input here.


                if(oneGame.win == False and oneGame.turnTimer < 125):
                    oneGame.turn(oneGame.p1)
                else:
                    oneGame.p2.changeFitness(15)
                    break

            
            else:
                if(oneGame.p2.isRobot()):
                    output = net.activate(oneGame.refreshData()) 
                    oneGame.getSelection(oneGame.p2,output)  
                
                else:
                    if(gameType == 2 or gameType == 3):
                        oneGame.p2.requestSelection()
                    else:
                        pass #graphical input here.


                if(oneGame.win == False and oneGame.turnTimer < 125):
                    oneGame.turn(oneGame.p2)
                else:
                    oneGame.p1.changeFitness(15)
                    break
                
        oneGame.prettyBoard()
        oneGame.p1.changeFitness((-0.01)*oneGame.getTurn())
        oneGame.p2.changeFitness((-0.01)*oneGame.getTurn())
        p1f = oneGame.p1.getFitness()
        p2f = oneGame.p2.getFitness()

        genomes[0].fitness += ((p1f/abs(p1f-p2f))+(p1f/3)) if (p1f-p2f) != 0 else (p1f/3)
        genomes[0].fitness += ((p2f/abs(p2f-p1f))+(p2f/3)) if (p2f-p1f) != 0 else (p2f/3)
        fitnesses[0] = genomes[0].fitness
        fitnesses[0] = genomes[0].fitness



    else:
        for id, genome in genomes:
            ##creates the robots
        
            if i % 2 == 0:
                r = Robot("Blue", [red,blue],i)
                blueRobots.append(r)
            else:
                r = Robot("Red" , [red,blue],i)
                redRobots.append(r)

            i+=1
            allRobots.append(r)

            geno.append(genome)
            net = neat.nn.FeedForwardNetwork.create(genome, config)
            nets.append(net)
            if(genome.fitness == None): 
                genome.fitness = 2

        


        for g in range(allRobots):
            geno[g].fitness += fitnesses[g-1]
        

        

        for r in range(len(allRobots)):  
            try:  
                currentGames.append(checkerboardClass(copy.deepcopy(board_config), copy.deepcopy(red), copy.deepcopy(blue), blueRobots[r],redRobots[r]))
            except:
                pass
                geno[g].fitness = 0
            r+=1


        
        #for each game, play through an entire game
        for g, game in enumerate(currentGames):
            while(game.win == False): ##while nobody has won, continue to run. 
                if (game.currentTurn == "Blue"):
                    
                    output = nets[g].activate(game.refreshData()) 
                    #print(output,(output[0] + output[1] + output[2] + output[3])/4, " Player 1")
                    game.getSelection(game.p1,output)  
                    
                    #print(game.p1.getOriginalChecker())
                    #print(game.p1.getFinalChecker())

                    if(game.win == False and game.turnTimer < 125):
                        game.turn(game.p1)
                    else:
                        game.p2.changeFitness(15)
                        break



                
                else:
                    output = nets[g].activate(game.refreshData()) ##Red checkers, blue checkers. BLUE CHECKER ROBOT
                    #print(output, " Player 2")
                    game.getSelection(game.p2,output)  
                    
                    #print(game.p2.getOriginalChecker())
                    #print(game.p2.getFinalChecker())

                    if(game.win == False and game.turnTimer < 125):
                        game.turn(game.p2)
                    else:
                        game.p1.changeFitness(15)
                        break
                    
                
                    
                
                #time.sleep(0.5)
            #game.prettyBoard()
            game.p1.changeFitness((-0.01)*game.getTurn())
            game.p2.changeFitness((-0.01)*game.getTurn())
            p1f = game.p1.getFitness()
            p2f = game.p2.getFitness()

            geno[(g*2)-1].fitness += ((p1f/abs(p1f-p2f))+(p1f/3)) if (p1f-p2f) != 0 else (p1f/3)
            geno[  g*2  ].fitness += ((p2f/abs(p2f-p1f))+(p2f/3)) if (p2f-p1f) != 0 else (p2f/3)
            fitnesses[(g*2)-1] = geno[(g*2)-1].fitness
            fitnesses[  g*2  ] = geno[  g*2  ].fitness
            
            # if (p1f/abs(p1f-p2f)) < 0:
            #     raise ValueError("ERROR: fitness for p1 is negative (" + (p1f/abs(p1f-p2f)) + ")")
            # if (p2f/abs(p2f-p1f)) < 0:
            #     raise ValueError("ERROR: fitness for p2 is negative (" + (p2f/abs(p2f-p1f)) + ")")     
            
            #int((geno[  g*2  ].fitness)/count)
            

        random.shuffle(genomes)





def mod_sigmoid(x):
        if x == 0:
            return 0
        elif x == 1:
            return 1
        else:
            return (1/(1+((e)**(5-(10*x)))))
        

def run_neat(config_path):
    # Load configuration.
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path
    )
    

    config.genome_config.add_activation('modified_sigmoid', mod_sigmoid)   



    # Create the population, which is the top-level object for a NEAT run.
    #pop = neat.Checkpointer.restore_checkpoint('LaptopCheckpointV2-11934')
    pop = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    pop.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    pop.add_reporter(stats)
    pop.add_reporter(neat.Checkpointer(100))


    runs = 100000
    # Run for up to R(100,000) generations.
    winner = pop.run(eval_genomes, runs) #number of runs
    with open("best genome %d runs.pkl"%runs, "wb") as f:
        pickle.dump(winner, f)
        f.close()

    # Display the winning genome.
    #print('\nBest genome:\n
    # {!s}'.format(winner))
    
    # Show output of the most fit genome against training data.
    node_names = {}
    visualize.draw_net(config, winner, True, node_names=node_names)
    visualize.plot_stats(stats, ylog=False, view=True)
    visualize.plot_species(stats, view=True)


    #how to load from an old training file.
    
    #p.run(eval_genomes, 10)
    ##wat? how the fuck am i supposed to use created genome? look how to use w o having to train.



if (__name__ == '__main__'):
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'neat_config')
    if(gameType == 5):
        run_neat(config_path)

    if(gameType != 5):
        p = neat.Checkpointer.restore_checkpoint('LaptopCheckpointV2-11934')
        #for g in itervalues(p.population):
        #    print(g.fitness)
        print("Bestc: " + str(p.best_genome))

        
        single_genome()
 

    


