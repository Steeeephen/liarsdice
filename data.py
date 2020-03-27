import random as ra
import math
import csv

def deal(n):
	arr = []
	for j in range(n):
		arr.append(ra.randint(1,6))
	return arr

def check(l, t, n):
	x = t[0]
	y = t[1]
	c = 0
	for i in range(n):
		c += l[i].count(y)
		if(y!=1):
			c+=l[i].count(1)
	return c>=x

def choose(x,y):
	if(y>x):
		return 0
	else:
		f = math.factorial
		try:
			return f(x)/f(y)/f(x-y)
		except:
			return 1
def chance(n,p,s):
	# print(choose(n,s))
	# print(p**s)
	# print((1-p)**(n-s))
	x=0
	t=1/3
	if(p==1):
		t=1/6
	for i in range(s,n+1):
		x += choose(n,i) * (t**i) * ((1-t)**(n-i))
		# print(x)
	return x
	
def combet(x,y,n,l):
	if(ra.randint(1,100)>70):
		y += ra.randint(1,5)
		if(y>6):
			x+=1
			y = y%6+1
		return [x,y]
	else:
		c = 0
		x1=x
		y1=y
		# print("x1,y1 = " + str([x1,y1]))
		for i in range(5):
			y+=1
			if(y>6):
				x+=1
				y=(y+1)%6
			temp = chance(n,y,x-l.count(y)-l.count(1))
			# print(x1,y1)
			if(temp>c):
				c = temp
				x1=x				
				y1=y
			# print("combet returns "+str([x1,y1]))
		
		return [x1,y1]
# test=[2,3,3,4,5]
# while(True):
	# inpu=list(map(int,input().split()))
	# print(chance(5,inpu[1],int(inpu[0]-test.count(inpu[1]))))

# print(combet(3,4,5,[3,3,3,3,3]))		
ps=0
cs=0
diceT=[]
for i in range(10000):
	pd = 5
	cd = 5
	ct=ra.randint(1,10)>5
	while(True): #each game	
		pList = []
		pList.append(deal(pd))
		pList.append(deal(cd))
		cb = [0,0]
		if(ra.randint(1,100)>60):
			cbet = [ra.randint(2,3),ra.randint(1,6)]
		else:
			cbet=[ra.randint(2,3),max(set(pList[1]),key=pList.count)]
			cb = cbet
		# print("Comp:")
		# print(*cbet, sep = ' ')
		if(not ct):
				cbet=[1,6]
			
		while(True):
			bet = combet(cbet[0],cbet[1],cd,pList[0])
			# print("Player")
			# print(*bet,sep=' ')
			if(chance(pd,bet[1],bet[0]-pList[1].count(bet[1])-pList[1].count(1))<0.3):
				# print("Computer calls")
				if(not check(pList, bet,2)):
					pd-=1
					# print("Player loses! Computer has "+str(cd)+ ", Player has "+str(pd))
					# print(*pList,sep=' ')
					# print(len(pList[0])+len(pList[1]))
					# print("highest number "+str(bet[0]))
					diceT.append([len(pList[0])+len(pList[1]),bet[0]])
					ct = False
					break
				else:
					cd -=1
					# print("Computer loses! Computer has "+str(cd)+ ", Player has "+str(pd))
					# print(*pList,sep=' ')
					# print(len(pList[0])+len(pList[1]))
					# print("highest number "+str(bet[0]))
					diceT.append([len(pList[0])+len(pList[1]),bet[0]])
					ct = True
					break
			cbet = combet(bet[0],bet[1],pd,pList[1])
			# cb = cbet
			# print("Comp:")
			# print(*cbet, sep = ' ')
			# print(pList[0],pList[1])
			if(chance(cd,cbet[1],cbet[0]-pList[0].count(cbet[1])-pList[0].count(1))<0.3):
				# print("Player calls")
				if(not check(pList, cbet,2)):
					cd-=1
					# print("Computer loses! Computer has "+str(cd)+ ", Player has "+str(pd))
					# print(*(map(len,pList)),sep=' ')
					# print(len(pList[0])+len(pList[1]))
					# print("highest number "+str(cbet[0]))
					diceT.append([len(pList[0])+len(pList[1]),bet[0]])
					ct = True
					break
				else:
					pd -=1
					# print("Player loses! Computer has "+str(cd)+ ", Player has "+str(pd))
					# print(*pList,sep=' ')
					# print(len(pList[0])+len(pList[1]))
					# print("highest number "+str(cbet[0]))
					diceT.append([len(pList[0])+len(pList[1]),bet[0]])
					ct = False
					break
		if(pd == 0):
			# print("Player loses!")
			cs+=1
			break
		elif(cd==0):
			# print("Computer loses!")
			ps+=1
			break
# print(diceT)
import csv

with open('rolls.csv', 'w') as csvfile:
	fieldnames = ['Total_Amount', 'Highest_Bet']
	writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

	writer.writeheader()
	for i in range(len(diceT)):
		writer.writerow({'Total_Amount':diceT[i][0],'Highest_Bet':diceT[i][1]})
# print("Player score: "+str(ps)+"\nComputer Score: "+str(cs))