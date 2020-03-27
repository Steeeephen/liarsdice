import random as ra
import math
import socket
import time
import numpy

def deal(totaldice):
	playerdice = []
	alldice = []
	for i in totaldice:
		for j in i:
			playerdice.append(ra.randint(1,6))
		alldice.append(playerdice)
		playerdice = []
	return alldice

def check(alldice, bet):
	amount = bet[0]
	number = bet[1]
	count = 0
	for j in alldice:
		for i in j:
			if(i == number or (i == 1 and number != 1)):
				count+=1
	return count>=amount

start = time.time()
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	s.bind(('127.0.0.1', 65432))
	s.listen()
	players = []
	for i in range(2):
		connection, address = s.accept()
		players.append((connection,address))
numberofgames = int(input("Number of Games?\n"))
player1score=0
player1domination = []
player2score=0
player2domination = []
abcsv = []
playercalls = [[0,0],[0,0]]
for i in range(numberofgames):
	playerdice = [[1,1,1,1,1],[1,1,1,1,1]]
	playerdice = deal(playerdice)
	print(playerdice)
	turn = ra.randint(0,1)
	while(True):
		currentbet = [0,0]
		playerdice=deal(playerdice)
		for i in range(2):
			dicestring = "Player %d: %s" % (i+1,playerdice[i])
			players[i][0].sendall(dicestring.encode())
		while(True):
			print("-------------------------------------------------------------------------------------------------------")
			print(playerdice[turn])
			betstring = "Opponent's bet is %s" % currentbet
			print(betstring)
			players[turn][0].sendall(betstring.encode())
			print("Player %d" % (turn+1))
			input = players[turn][0].recv(1096).decode("utf-8")
			print(input)
			inp = input.lower()
			if(inp[:4]=='call'):
				playercalls[turn][1]+=1
				turnmod = (turn+1) % 2
				if(not check(playerdice, currentbet)):
					playerdice[turnmod] = playerdice[turnmod][1:]
					lossstring = "Player %d loses!\nDice count is: Player 1 (%d : %d) Player 2" % (turnmod+1,len(playerdice[0]),len(playerdice[1]))
					print(lossstring)
					players[0][0].sendall(lossstring.encode())
					players[1][0].sendall(lossstring.encode())
					try:
						abcsv.append([inp.split(" ")[1],1])
					except:
						pass
					time.sleep(0.015)
					playercalls[turn][0]+=1
					turn = turnmod
					break
				else:
					playerdice[turn] = playerdice[turn][1:]
					lossstring = "Player %d loses!\nDice count is: Player 1 (%d : %d) Player 2" % (turn+1,len(playerdice[0]),len(playerdice[1]))
					print(lossstring)
				
					players[0][0].sendall(lossstring.encode())
					players[1][0].sendall(lossstring.encode())
					try:
						abcsv.append([inp.split(" ")[1],0])
					except:
						pass
					time.sleep(0.015)
					break
			try:
				bet =list(map(int, input.split(" ")))
				if((bet[1]>0) & (bet[1]<7)) & (bet > currentbet):
					currentbet = bet
					turn = (turn+1)%2
				else:
					print("Invalid Input")
					players[turn][0].sendall("Invalid Input".encode())
			except:
				print("Invalid input (String)")
				players[turn][0].sendall("Invalid Input".encode())
		if(len(playerdice[0]) == 0):
			print("Player 1 loses!")
			player2score+=1
			player2domination.append(len(playerdice[1]))
			break
		elif(len(playerdice[1])==0) :
			print("Player 2 loses!")
			player1score+=1
			player1domination.append(len(playerdice[0]))
			break
print("Player 1 (%d : %d) Player 2" % (player1score,player2score))
print("Player 1 had an average of %.1f dice when winning, Player 2 had %.1f" % (numpy.mean(player1domination),numpy.mean(player2domination)))
print("Player 1 had a %.2f%% call accuracy, Player 2 had a %.2f%% call accuracy" % (100*playercalls[0][0]/playercalls[0][1],100*playercalls[1][0]/playercalls[1][1]))
end = time.time()
print("%d seconds" % (end-start))
import csv

with open('ab.csv', 'w') as csvfile:
	fieldnames = ['Percentage', 'Win']
	writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

	writer.writeheader()
	for i in abcsv:
		writer.writerow({'Percentage':i[0],'Win':i[1]})
