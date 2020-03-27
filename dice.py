import random as ra
import math

def deal(n):
	arr = []
	n2 = []
	for i in range(len(n)):
		for j in range(len(n[i])):
			arr.append(ra.randint(1,6))
		n2.append(arr)
		arr = []
	return n2

def check(l, t, n):
	x = t[0]
	y = t[1]
	c = 0
	for j in l:
		for i in range(n):
			c += j[i].count(y)
			if(y!=1):
				c+=j[i].count(1)
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

def chance(n,p,s,l):
	x=0
	t=1/3
	if(p==1):
		t=1/6
	for i in range(s,n+1):
		x += choose(n,i) * (t**i) * ((1-t)**(n-i))
	x+=0.1*l.count(p)
	return x

def combet(x,y,n,l,ca):
	if(ra.randint(1,100)>65):
		y += ra.randint(1,5)
		if(y>6):
			x+=1
			y = (y+1)%6
		return [x,y]
	else:
		c = 0
		x1=x
		y1=y-1
		for i in range(5):
			y+=1
			if(y>6):
				x+=1
				y=(y+1)%6
			temp = chance(n,y,x-l.count(y)-l.count(1),ca) #maybe come back
			if(temp>c):
				c = temp
				x1=x				
				y1=y
		return [x1,y1]

print("Number of Games")
ng = int(input())
print("Number of Players")
np = int(input())		
cs=0
ps=0
pList = []
for i in range(ng):
	for i in range(np):
		pList.append([1,2,3,4,5])
	print(pList)
	print(deal(pList))
	pList = deal(pList)
	turn = ra.randint(0,np-1)
	# ct = turn==1
	while(True): #each game
		calls=[]	
		#pList = []
		cb = [0,0]
		print(pList[turn])
		if(turn == 0):
				if(ra.randint(1,100)>60):
					cbet = [ra.randint(2,3),ra.randint(1,6)]
				else:
					cbet=[ra.randint(1,3),max(set(pList[1]),key=pList.count)]
				cb = cbet
				print(*cbet, sep = ' ')
		while(True): #each bet
			inp = input()
			if(inp=='call'):
				if(not check(pList, cbet,2)):
					pList[0] = pList[0][1:]
					print("Computer loses!") 
					#Computer has "+str(cd)+ ", Player has "+str(pd))
					ct = True
					break
				else:
					pList[turn] = pList[turn][1:]
					print("Player loses!") 
					#Computer has "+str(cd)+ ", Player has "+str(pd))
					ct = False
					break
			bet =list(map(int, inp.split(" ")))
			calls.append(bet[1])
			if((bet[1]>0) & (bet[1]<7)):
				cb = bet
				if(chance(len(pList[turn]),cb[1],cb[0]-pList[turn].count(cb[1])-pList[turn].count(1),calls)<0.35):
					print("I call!")
					if(not check(pList, bet,2)):
						pd-=1
						print("Player loses! Computer has "+str(cd)+ ", Player has "+str(pd))
						ct = False
						break
					else:
						cd -=1
						print("Computer loses! Computer has "+str(cd)+ ", Player has "+str(pd))
						ct = True
						break
				cbet = combet(bet[0],bet[1],pd,pList[1],calls)
				cb = cbet
				print(*cbet, sep = ' ')
			else:
				print("Invalid Input")
		if(pd == 0):
			print("Player loses!")
			cs+=1
			break
		elif(cd==0):
			print("Computer loses!")
			ps+=1
			break
	print(calls)
print(ps,cs)
print(calls)