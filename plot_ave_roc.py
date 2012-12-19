'''
Created on 18 Dec 2012

@author: James McInerney
'''

#plots average roc curve for set of roc curves using linear interpolation
from matplotlib.pyplot import plot, show, figure, xlim, ylim, title, scatter
from numpy import array,random,arange,zeros
from random import choice

class Interpolation(object):
    def __init__(self,xs,ys):
        assert len(xs)==len(ys)
#        assert self._monotonically_increasing(xs)
#        assert self._monotonically_increasing(ys)
        xs1, ys1 = self._sort_xys(xs,ys) #throws error if xs,ys not monotonically increasing
        self.xs, self.ys = self._remove_dups(xs1,ys1) #remove duplicate x values (taking max of corresponding y values)
        self.min_x = self.xs[0]
        self.max_x = self.xs[-1] #get last element in list
    
    def _monotonically_increasing(self,vs):
        #returns True iff vs list is monotonically increasing (not necessarily strictly increasing)
        i = 0
        print 'vs',vs
        while vs[i]<=vs[i+1] and i<(len(vs)-1): i+=1
        return i==(len(vs)-1)
    
    def _sort_xys(self,xs,ys):
        xs_is = zip(xs, range(len(xs))) #zip indices with values
        xs1,is1 = zip(*sorted(xs_is))
        ys1 = []
        for i in is1: ys1.append(ys[i])
        return xs1,ys1

    def _remove_dups(self,xs,ys):
        #removes duplicate x values (taking max of corresponding y values)
        i = 0
        xs1,ys1 = [], []
        while i < len(xs):
            #search forwards for matching x values (could be more than 2)
            j = 1
            while (i+j) < len(xs) and xs[i]==xs[i+j]: j+=1
            y_max = max(ys[i:(i+j)])
            xs1.append(xs[i])
            ys1.append(y_max)
            i+=j
        return xs1,ys1
    
    def getY(self,x):
        #get y by direct value or linear interpolation
        assert x >= self.min_x and x <= self.max_x
        #find nearest x value
        i = 0
        while self.xs[i]<x: i+=1 #by previous assertion, we know that in worst case self.xs[N-1]==x
        if self.xs[i]==x:
            #just return direct value:
            return self.ys[i]
        else:
            #return linear interpolation:
            m = (self.ys[i]-self.ys[i-1])/(self.xs[i]-self.xs[i-1])
            return m*(x - self.xs[i-1]) + self.ys[i-1]
    
    def getAllY(self,xs):
        ys = []
        for x in xs:
            ys.append(self.getY(x))
        return ys

class RocSet(object):
    def __init__(self,xss,yss):
        assert len(xss)==len(yss)
        self.rocs = []
        for xs,ys in zip(xss,yss):
            self.rocs.append(Interpolation(xs,ys))
    
    def plot_values(self,N=100):
        interval = 1/float(N)
        xs = arange(0.,1.,interval)
        ys = zeros(N)
        assert len(xs)==len(ys)
        for roc in self.rocs:
            ys += array(roc.getAllY(xs))
        ys = ys/float(len(self.rocs)) #average
        return xs,ys
    
def plotAve(xss,yss):
    #plots single roc corresponding to average of unsorted set of xs,ys (FP,TP) 
    roc_ave = RocSet(xss,yss)
    xs,ys = roc_ave.plot_values(N=150)
    plot(xs,ys)
    title('Average ROC')
    for xs,ys in zip(xss,yss):
        #title('ROC %i'%i)
        scatter(xs,ys)
    xlim((0.,1.))
    ylim((0.,1.))
    i=1
    for xs,ys in zip(xss,yss):
        figure()
        title('ROC %i'%i)
        scatter(xs,ys)
        xlim((0.,1.))
        ylim((0.,1.))
        i+=1
    show()
    
def genRandom(size=3):
    #generate |size| random roc curves (xs=FP, ys=TP)
    xss,yss = [], []
    for _ in range(size):
        xs = [0.0,1.0]
        xprev = 0.0
        for _ in range(10):
            xs.append(xprev + choice([0.0,random.beta(1,10)*(1.-xprev)])) #put in some duplicate xs, as may happen from time to time
            xprev = xs[-1]
        xss.append(xs)
    for _ in range(size):
        ys = [0.0,1.0]
        yprev = 0.0
        for _ in range(10):
            ys.append(yprev + random.beta(1,5)*(1.-yprev))
            yprev = ys[-1]
        yss.append(ys)
    return xss,yss

def test():
    xss,yss = genRandom()
    plotAve(xss,yss)
    
test()