
import numpy as np
from tnbits.model.objects.glyph import getPoints

# http://iamtrask.github.io/2015/07/12/basic-python-network/

L = 10
D = {}

class NN:
    def __init__(self):
        self.X = None # Input data set
        self.y = None # Output data set

    # sigmoid function
    def nonlin(self, x,deriv=False):
        if(deriv==True):
            return x*(1-x)

        return 1/(1+np.exp(-x))

    def get(self, inputData): # Test output against
        # Feed forward through layers 0, 1, and 2
        l0 = inputData
        l1 = self.nonlin(np.dot(l0, self.syn0))
        l2 = self.nonlin(np.dot(l1, self.syn1))
        return l2

    def train(self, inputDataSet, outputDataSet):
        # X: Input data set.
        # y: Output data set.
        # X = np.array([[0,0,1], [0,1,1], [1,0,1], [1,1,1]])
        # y = np.array([[0], [1], [1], [0]])
        X = np.array(inputDataSet)
        y = np.array(outputDataSet)

        np.random.seed(1)

        # randomly initialize our weights with mean 0
        self.syn0 = 2*np.random.random((L,L*3)) - 1
        self.syn1 = 2*np.random.random((L*3,1)) - 1

        for j in range(60000):

            # Feed forward through layers 0, 1, and 2
            self.l0 = X
            self.l1 = self.nonlin(np.dot(self.l0, self.syn0))
            self.l2 = self.nonlin(np.dot(self.l1, self.syn1))

            # how much did we miss the target value?
            l2_error = y - self.l2

            if (j% 10000) == 0:
                print("Error:" + str(np.mean(np.abs(l2_error))))

            # in what direction is the target value?
            # were we really sure? if so, don't change too much.
            l2_delta = l2_error * self.nonlin(self.l2, deriv=True)

            # how much did each l1 value contribute to the l2 error (according to the weights)?
            l1_error = l2_delta.dot(self.syn1.T)

            # in what direction is the target l1?
            # were we really sure? if so, don't change too much.
            l1_delta = l1_error * self.nonlin(self.l1, deriv=True)

            self.syn1 += self.l1.T.dot(l2_delta)
            self.syn0 += self.l0.T.dot(l1_delta)

#print("Output After Training:")
#print(l1)

nn = NN()

f = CurrentFont()
FACTOR = 2 * f.info.unitsPerEm
XXX = [] # Collected point sets for every glyph
RSB = [] # Collected scaled right margins
for g in f:
    if 'cmb' in g.name:
        continue
    if not g.name in 'abcdef':
        continue
    xx = []
    for p in getPoints(g):
        xx.append(p.x / (2 * FACTOR) - FACTOR/2)
        #xx.append(p.y / (2 * FACTOR) - FACTOR/2)
    if not xx:
        continue
    maxx = max(xx)
    XX = []
    for x in sorted(xx, reverse=True)[:L]:
        XX.append(x - maxx)
    while len(XX) < L: XX.append(max(XX))
    print(g.name, g.rightMargin, XX, len(XX))
    w = g.rightMargin / FACTOR
    #if g.name == 'e':
    #D = g, XX
    #else:
    D[g.name] = XX
    XXX.append(XX)
    RSB.append([w])

#XXX = [ [0,0,1], [0,1,1], [1,0,1], [1,1,1] ]
#RSB = [0,0,1,1]
#print(len(XXX), len(RSB)  )
#print(XXX)
#print(RSB)
nn.train(XXX, RSB)
print(nn.l1       )

for name in 'abcdef':
    g = f[name]
    XX = D[name]
print(g, g.rightMargin, XX)
print(nn.get(XX)[0] * FACTOR, g.name, g.rightMargin)

