# coding: shift_jis

import random

class Board():
	def __init__(self):
		self.state = "wait"
		self.height = 8
		self.width = 8
		
		self.icon1 = "(whew)"
		self.icon2 = "(emo)"
		
		self.player1 = False
		self.player2 = False
		
		self.cells = [[0 for j in range(self.width)] for i in range(self.height)]
		
		ch = (self.height/2) - 1
		cw = (self.width/2) - 1
		self.cells[ch][cw] = 1
		self.cells[ch][cw+1] = 2
		self.cells[ch+1][cw] = 2
		self.cells[ch+1][cw+1] = 1
		
		self.pairs = [
					{"keyX": 0, "keyY": -1},
					{"keyX": 1, "keyY": -1},
					{"keyX": 1, "keyY": 0},
					{"keyX": 1, "keyY": 1},
					{"keyX": 0, "keyY": 1},
					{"keyX": -1, "keyY": 1},
					{"keyX": -1, "keyY": 0},
					{"keyX": -1, "keyY": -1},
				]
	
	def start(self):
		self.state = "start"
		self.chat.SendMessage(u"ゲームを開始します。")
		self.turn = random.randint(1, 2)
		self.disp()
		self.dispTurn()
	
	def dispTurn(self):
		if self.turn == 1:
			self.chat.SendMessage(u"%sさんのターンです icon: %s" % (self.player1["name"], self.icon1))
		elif self.turn == 2:
			self.chat.SendMessage(u"%sさんのターンです icon: %s" % (self.player2["name"], self.icon2))
	
	def put(self, x, y):
		result = self.canput(self.turn, x, y)
		if result == True:
			self.chain(x, y)
			self.disp()
			if not self.change():
				self.endGame()
				return
		elif result == -1:
			self.chat.SendMessage(u"値が範囲外です。石は(1 <= x <= 8, 1 <= y <= 8)の範囲に置いてください。")
		elif result == -2:
			self.chat.SendMessage(u"既に石が置かれています。別の位置に置いてください。")
		elif result == -3:
			self.chat.SendMessage(u"石を裏返せません。別の位置に置いてください。")
		self.dispTurn()
	
	def canput(self, p, x, y):
		if not self.isValid(x, y):
			return -1
		elif self.isExists(x, y):
			return -2
		elif not self.canChain(p, x, y):
			return -3
		return True
	
	def isValid(self, x, y):
		if 0 <= x < self.width and 0 <= y < self.height:
			return True
		return False
	
	def isExists(self, x, y):
		if self.cells[y][x] != 0:
			return True
		return False
	
	def canChain(self, p, x, y):
		for pair in self.pairs:
			currentX = x
			currentY = y
			changed = False
			
			while True:
				currentX += pair["keyX"]
				currentY += pair["keyY"]
				
				if not self.isValid(currentX, currentY):
					break
				elif not self.isExists(currentX, currentY):
					break
				elif not changed and self.cells[currentY][currentX] == p:
					break
				elif self.cells[currentY][currentX] != p:
					changed = True
				elif self.cells[currentY][currentX] == p and changed:
					return True
		return False
	
	def chain(self, x, y):
		p = self.turn
		self.cells[y][x] = p
		
		for pair in self.pairs:
			currentX = x
			currentY = y
			changed = False
			
			while True:
				currentX += pair["keyX"]
				currentY += pair["keyY"]
				
				if not self.isValid(currentX, currentY):
					break
				elif not self.isExists(currentX, currentY):
					break
				elif not changed and self.cells[currentY][currentX] == p:
					break
				elif self.cells[currentY][currentX] != p:
					changed = True
				elif self.cells[currentY][currentX] == p and changed:
						while True:
							currentX -= pair["keyX"]
							currentY -= pair["keyY"]
							
							if self.cells[currentY][currentX] != p:
								self.cells[currentY][currentX] = p
							else:
								changed = False
								break
				else:
					break
	
	def change(self):
		if self.turn == 1:
			next = 2
			next2 = 1
		elif self.turn == 2:
			next = 1
			next2 = 2
		
		for i in range(self.height):
			for j in range(self.width):
				if self.canput(next, j, i) == True:
					self.turn = next
					return True
		for i in range(self.height):
			for j in range(self.width):
				if self.canput(next2, j, i) == True:
					self.turn = next2
					return True
		return False
	
	def endGame(self):
		self.chat.SendMessage(u"ゲーム終了")
		result1 = self.count(1)
		result2 = self.count(2)
		self.chat.SendMessage(u"集計結果　%s : %d, %s : %d" % (self.icon1, result1, self.icon2, result2))
		if result1 > result2:
			self.chat.SendMessage(u"%s さんの勝ち！" % (self.player1["name"]))
		elif result1 < result2:
			self.chat.SendMessage(u"%s さんの勝ち！" % (self.player2["name"]))
		else:
			self.chat.SendMessage(u"同点です！")
		self.__init__()
	
	def disp(self):
		for i in range(self.height):
			str = ""
			for j in range(self.width):
				if self.cells[i][j] == 0:
					str += "..... "
				elif self.cells[i][j] == 1:
					str += self.icon1 + " "
				elif self.cells[i][j] == 2:
					str += self.icon2 + " "
			self.chat.SendMessage(u"%s" % str)
	
	def getTurn(self):
		if self.turn == 1:
			return self.player1["id"]
		elif self.turn == 2:
			return self.player2["id"]
	
	def count(self, item):
		ans = 0
		
		for i in range(self.height):
			for j in range(self.width):
				if self.cells[i][j] == item:
					ans += 1
		return ans
