import random as ra
import math
import socket

def choose(n,k):
	if(k>n):
		return 0
	else:
		f = math.factorial
		try:
			return f(n)/f(k)/f(n-k)
		except:
			return 1

def chance(opposingdice,number,amount):
	if(amount==0):
		return 1
	probability=0
	diceprob=1/3
	if(number==1):
		diceprob=1/6
	for i in range(amount,opposingdice+1):
		probability += choose(opposingdice,i) * (diceprob**i) * ((1-diceprob)**(opposingdice-i)) 																					#parameter 1
	return probability

def possibilities(branch, enemydice, dice,n):
	x = branch[1]
	x1=x
	y = branch[2]
	total = []
	for i in range(n):
		y += 1
		if(y > 6):
			x += 1
			y = (y%6)
		if(y!=1):
			x1 -= dice.count(1)
		else:
			x1 -= (dice.count(1)+dice.count(y))
		total.append([chance(enemydice,y,x1),x,y])
	return total

def combet(branch ,enemydice , dice,n):
	x = possibilities(branch,enemydice,dice,n)
	xs = [possibilities(i, enemydice,dice,n) for i in x]
	for i in xs:
		count=0
		for j in i:
			t = possibilities(j,enemydice,dice,n)
			t.sort(reverse=True)
			j[0]=t[0][0]
			i[count][0] = t[0][0]
			count+=1
		i.sort()
	count=0
	for i in xs:
		x[count][0]= i[0][0]
		count+=1
	x.sort(reverse=True)
	return (x[0][1],x[0][2])
	
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	s.connect(('127.0.0.1', 65432))
	while True:
		diceinp = s.recv(25).decode("utf-8")
		print(diceinp)
		dice=[]
		n=12
		for i in diceinp:
			try:
				dice.append(int(i))
			except:
				pass
		dice = dice[1:]
		enemydice = 5
		while(True):
			bet = s.recv(256).decode("utf-8")
			print(bet)
			if(bet[0]=='P'):
				print("-----------------------------------------------------------------")
				break
			try:
				amount = int(bet[19])
				number = int(bet[22])
			except:
				pass
			if(amount == 0):
				botbet=(ra.randint(2,3),max(set(dice),key=dice.count))
				print(*botbet, sep = ' ')
				s.sendall(("%d %d" % botbet).encode())
			elif(chance(enemydice,number,amount-dice.count(number)-dice.count(1))<0.35):									#parameter 4
				sent="call %d" % n
				s.sendall(sent.encode())
			else:
				botbet = combet([0,amount,number],enemydice,dice,n)
				print(*botbet, sep = ' ')
				s.sendall(("%d %d" % botbet).encode())