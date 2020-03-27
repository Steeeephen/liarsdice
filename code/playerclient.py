import socket

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	s.connect(('127.0.0.1', 65432))
	while True:
		dice = s.recv(256).decode("utf-8")
		print(dice)
		while True:
			bet = s.recv(512).decode("utf-8")
			print(bet)
			if(bet[0] == 'I'):
				data = s.recv(512).decode("utf-8")
				print(data)
			elif(bet[0] == 'P'):
				print("---------------------------------------------------------------------------------------")
				break
			inp = input("What is your bet?\n").encode()
			s.sendall(inp)