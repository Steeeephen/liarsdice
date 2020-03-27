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

def chance(opposingdice,number,amount,calls):
	if(amount==0):
		return 1
	probability=0
	diceprob=1/3
	if(number==1):
		diceprob=1/6
	for i in range(amount,opposingdice+1):
		probability += choose(opposingdice,i) * (diceprob**i) * ((1-diceprob)**(opposingdice-i))
	probability+=math.sqrt(0.5*calls.count(number)) 																					#parameter 1
	return probability


def possibilities(branch, enemydice, dice,calls):
	x = branch[1]
	xnew=x
	y = branch[2]
	total = []
	for i in range(6):
		y += 1
		if(y > 6):
			x += 1
			y = (y%6)
		if(y!=1):
			xnew -= dice.count(1)
		else:
			xnew -= (dice.count(1)+dice.count(y))
		total.append([chance(enemydice,y,xnew,calls),x,y])
	return total

def combet(branch,enemydice,dice,calls):
	if(ra.randint(1,100)>75):		
		enemynumber = branch[2] + ra.randint(1,5)
		enemyamount = branch[1]
		if(enemynumber>6):
			enemyamount += 1
			enemynumber = enemynumber%6+1
		return (enemyamount,enemynumber)
	x = possibilities(branch,enemydice,dice,calls)
	xs = [possibilities(i, enemydice,dice,calls) for i in x]
	for i in xs:
		count=0
		for j in i:
			t = possibilities(j,enemydice,dice,calls)
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
	xn = 0#ra.randint(0,3)
	return (x[xn][1],x[xn][2])

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	s.connect(('127.0.0.1', 65432))
	while True:
		diceinp = s.recv(25).decode("utf-8")
		# print(diceinp)
		dice=[]
		for i in diceinp:
			try:
				dice.append(int(i))
			except:
				pass
		dice = dice[1:]
		enemydice = 5
		n = ra.randint(1,4)
		n/=10
		calls=[]
		while(True):
			bet = s.recv(512).decode("utf-8")
			# print(bet)
			if(bet[0]=='P'):
				# print("-----------------------------------------------------------------")
				break
			try:
				amount = int(bet[19])
				number = int(bet[22])
			except:
				pass
			if(number != 1):
				amount2 =amount - dice.count(1)
			else:
				amount2 = amount-(dice.count(number)+dice.count(1))
			if(amount == 0):
				if(ra.randint(1,100)>75):																						#parameter 2
					amountt = ra.randint(2,3)
					numbert = ra.randint(2,6)
					calls.append(numbert)
					botbet = (amountt,numbert)
				else:
						botbet=(ra.randint(2,3),max(set(dice),key=dice.count))
				# print(*botbet, sep = ' ')
				s.sendall(("%d %d" % botbet).encode())
			elif(chance(enemydice,number,amount2,calls)<0.35):									
				sent="call %d" % (n*10)
				s.sendall(sent.encode())
			else:
				calls.append(number)
				if(len(calls)>50):
					s.sendall("call".encode())
				else:
					botbet = combet([0,amount,number],enemydice,dice,calls)
				# print(*botbet, sep = ' ')
					s.sendall(("%d %d" % botbet).encode())