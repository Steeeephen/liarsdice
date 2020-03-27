import random as ra
import math
import socket

def combet(enemyamount,enemynumber):
	enemynumber += ra.randint(1,10)
	if(enemynumber>12):
		enemyamount+=2
		enemynumber=enemynumber%6+1
	if(enemynumber>6):
		enemyamount+=1
		enemynumber = enemynumber%6+1
	return (enemyamount,enemynumber)
	
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
				amountt = ra.randint(2,3)
				numbert = ra.randint(2,6)
				botbet = (amountt,numbert)
				s.sendall(("%d %d" % botbet).encode())
			elif(ra.randint(1,100)>50):
				s.sendall("call".encode())
			else:
				botbet = combet(amount,number)
				s.sendall(("%d %d" % botbet).encode())