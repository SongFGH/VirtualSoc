from Node import *
from DNA import *
from Socialiser import *
from PetriDish import *
from Networks import *


#
# listOfNodes = PetriDish.createSimpleNodes(PetriDish, numberOfNodes=10, nodeType=Node, DNA=DNA('random'))
#
#
# SocialiserObj = randomSocial(p=0.5)
#
#     # executor = concurrent.futures.ProcessPoolExecutor(10)
#
#
# SocialiserObj.simpleRandomSocialiser(listOfNodes)
# # if __name__ == '__main__':
# #
#
# adj = Node.adj(Node)

G1 = RandomGraph(4,0.5)

G2 = RandomGraph(4,0.8, undirected=False)


adj1 = G1.A()


adj2 = G2.A()


a = 2+ 3
