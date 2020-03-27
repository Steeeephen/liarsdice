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

def combet(enemyamount,enemynumber,enemydice,dice):
	count = 0
	possible = []
	for i in range(6):																									#parameter 3
		enemynumber+=1
		if(enemynumber>6):
			enemyamount+=1
			enemynumber=enemynumber%6
		if(enemynumber == 1):
			temp2 = enemyamount-dice.count(enemynumber)
		else:
			temp2 = enemyamount-dice.count(enemynumber)-dice.count(1)
		temp = chance(enemydice,enemynumber,temp2)
		possible.append([temp,enemyamount,enemynumber]) #maybe come back
	possible.sort(reverse=True)	
	choice = ra.randint(0,2)
	betamount=possible[choice][1]				
	betnumber=possible[choice][2]
	return (betamount,betnumber)

	
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	s.connect(('127.0.0.1', 65432))
	while True:
		diceinp = s.recv(25).decode("utf-8")
		print(diceinp)
		dice=[]
		for i in diceinp:
			try:
				dice.append(int(i))
			except:
				pass
		dice = dice[1:]
		enemydice = 5
		while(True):
			bet = s.recv(512).decode("utf-8")
			print(bet)
			if(bet[0]=='P'):
				print(bet[15])
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
				s.sendall("call".encode())
			else:
				botbet = combet(amount,number,enemydice,dice)
				print(*botbet, sep = ' ')
				s.sendall(("%d %d" % botbet).encode())