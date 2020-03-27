import random as ra
import math

class Node(object):
    def __init__(self,parent=None,amount=1,bet=1):
        self.child=[]
        self.amount=amount
        self.bet=bet
        self.visits=1
        self.wins=0
        self.isleaf=True
        self.parent=parent
        self.untried=futuremoves(amount,bet)
    def addchild(self):
        tem = ra.choice(self.untried)
        # print(self.untried)
        # print(tem)
        self.untried.remove(tem)
        self.isleaf=False
        # print(self.untried)
        self.child.append(Node(self,tem[0],tem[1]))
    def update(self, result):
        self.visits+=1
        self.wins+=result
    def selectc(self):
        s = sorted(self.child, key = lambda c: c.wins/c.visits + math.sqrt(2*math.log(self.visits)/c.visits))[-1]
        return s
# def rselection(node=Node()):
    # if(node.isleaf):
    # for i in range(5):
        # node.addchild()
        
def UCT(n,x,y,td,calls):
    rootnode = Node(None,x,y)
    node=Node(None,x,y)
    for i in range(n):
        node = rootnode
        print(node.amount,node.bet)
        print(node.untried)
        for no in node.child:
            print(no.amount,no.bet)
        while(node.untried == [] and node.child!=[]): #select
            node = node.selectc
        if(node.untried!=[]):   #expand
            node.addchild()
            node=ra.choice(node.child)
            # print(node)
            ##
        node2=node #rollover
        turn=1
        win=1
        while(chance(td,node2.bet,node2.amount,calls)>0.01):
            print(chance(td,node2.bet,node2.amount,calls))
            node2.addchild()
            node2=ra.choice(node2.child)
            turn=(turn+1)%2
            print(node2.amount,node2.bet)
        ##
        while(node != None): #update
            node.update(turn)
            node=node.parent
        print(i)
    return sorted(rootnode.child, key = lambda c: c.visits)[-1].amount,sorted(rootnode.child, key = lambda c: c.visits)[-1].bet
        
def deal(n):
    arr = []
    for j in range(n):
        arr.append(ra.randint(1,6))
    return arr

def futuremoves(x,y):
    mlist = []
    for i in range(y+1,7):
        mlist.append([x,i])
    for i in range(x+1,x+2):
        for j in range(1,7):
            mlist.append([i,j])
    return mlist

def chance(n,p,s,l):
    x=0
    t=1/3
    if(p==1):
        t=1/6
    for i in range(s,n+1):
        x += choose(n,i) * (t**i) * ((1-t)**(n-i))
    x+=0.1*l.count(p)
    return x    
    
def choose(x,y):
    if(y>x):
        return 0
    else:
        f = math.factorial
        try:
            return f(x)/f(y)/f(x-y)
        except:
            return 1

    
td = 10 
calls=[]
p = 3
s = 4 #4 3s 
    
print(UCT(10000,2,5,td,calls))
    
# print(chance(td,p,s,calls))
    
# root = Node(None, 2,3)
# for i in range(5):
    # root.addchild()
    # root.update(ra.randint(0,1))
    # print(root.child[i].amount,root.child[i].bet)
# print(root.untried,root.visits,root.wins)
# print(root.selectc().amount,root.selectc().bet)