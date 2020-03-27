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
	probability+=math.sqrt(0.1*calls.count(number)) 																					#parameter 1
	return probability


def combet(enemyamount,enemynumber,enemydice,dice,calls):
	if(ra.randint(1,100)>75):																								#parameter 2
		enemynumber += ra.randint(1,5)
		if(enemynumber>6):
			enemyamount+=1
			enemynumber = enemynumber%6+1
		return (enemyamount,enemynumber)
	else:
		count = 0
		for i in range(6):																									#parameter 3
			enemynumber+=1
			if(enemynumber>6):
				enemyamount+=1
				enemynumber=enemynumber%6
			if(enemynumber == 1):
				temp2 = enemyamount-dice.count(enemynumber)
			else:
				temp2 = enemyamount-dice.count(enemynumber)-dice.count(1)
			temp = chance(enemydice,enemynumber,temp2,calls)
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
		n = ra.randint(1,4)
		n/=10
		calls=[]
		while(True):
			bet = s.recv(512).decode("utf-8")
			print(bet)
			if(bet[0]=='P'):
				print("-----------------------------------------------------------------")
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
				print(*botbet, sep = ' ')
				s.sendall(("%d %d" % botbet).encode())
			elif(chance(enemydice,number,amount2,calls)<n):									#parameter 4
				sent="call %d" % (n*10)
				s.sendall(sent.encode())
			else:
				calls.append(number)
				if(len(calls)>50):
					s.sendall("call".encode())
				else:
					botbet = combet(amount,number,enemydice,dice,calls)
					print(*botbet, sep = ' ')
					s.sendall(("%d %d" % botbet).encode())