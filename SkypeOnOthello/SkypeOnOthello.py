# coding: shift_jis

import Skype4Py
import time
import Board

def handler(msg, event):
	global b
	
	if event == u"RECEIVED" or event == u"SENT":
		if b.state == "wait":
			if not b.player1:
				if  u"オセロ" in u"%s" % msg.Body:
					b.player1 = {"id": msg._GetSender().Handle, "name": msg._GetSender()._GetFullName()}
					msg.Chat.SendMessage(u"%s さんをプレイヤー1として登録しました。" % (b.player1["name"]))
			elif not b.player2:
				if u"オセロ" in u"%s" % msg.Body:
					b.player2 = {"id": msg._GetSender().Handle, "name": msg._GetSender()._GetFullName()}
					msg.Chat.SendMessage(u"%s さんをプレイヤー2として登録しました。" % (b.player2["name"]))
					b.chat = msg.Chat
					b.start()
		elif b.state == "start":
			if u"debug" in u"%s" % msg.Body:
				b.debug()
			elif b.getTurn() == msg._GetSender().Handle:
				keys = msg.Body.split(",")
				if 1 < len(keys):
					x = int(keys[0]) - 1
					y = int(keys[1]) - 1
					
					b.put(x, y)

def main():
	global b
	skype = Skype4Py.Skype()
	skype.OnMessageStatus = handler
	skype.Attach()
	
	while True:
		time.sleep(10)

if __name__ == '__main__':
	b = Board.Board()
	main()
