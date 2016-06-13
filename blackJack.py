# blackJack V1
# Dave Chang
# 2016/06/4

import random

class Card(object):
	
	suitList = ['Hearts','Spades','Diamonds','Clubs']
	rankList = ['A','2','3','4','5','6','7','8','9','10','J','Q','K']
	cardInfoDict = {'Hearts': rankList, 'Spades': rankList, 'Diamonds': rankList, 'Clubs': rankList}
	
	# take suit in string and rank in integer
	def __init__(self, suit, rank):
		self.suit = suit
		self.rank = rank
	
	# what's the card?
	def cardInfo(self):
		return (self.suit,Card.cardInfoDict[self.suit][self.rank-1])
		

class Deck(object):
	global random
	# create a list of Card object, 52 cards
	def __init__(self):
		self.card = []
		for suit in Card.suitList:
			for rank in range(1,14):
				self.card.append(Card(suit, rank))
	
	def deckInfo(self):
		return self.card
	
	# randomly shuffle the deck
	def shuffleTheDeck(self):
		shuffled_deck = random.shuffle(self.card)
		return shuffled_deck
	
	# pop the top card from the deck
	def popTheTopCard(self):
		return self.card.pop()
	
	# remaining cards in the deck
	def numberOfCards(self):
		return len(self.card)
		
		
class Player(object):
	# player with money & empty cards
	def __init__(self, money):
		self.money = money
		self.card = []
	
	# total money a player has
	def totalMoney(self, moneyAdjust):
		self.money += moneyAdjust
		return self.money
	
	# get a card and return a list with card info
	def getACard(self, card):
		self.card.append(card)
		return self.card
	
	# show a list of cards in hands
	def hands(self):
		return self.card	
	
	def countingPoints(self, aPoint):
		points = 0
		for card in self.card:
			if card[1] == 'A':
				points += aPoint
			elif card[1] == 'J' or card[1] == 'Q' or card[1] == 'K':
				points += 10
			else:
				points += int(card[1])
		return points
	
	def pointsInHands(self):
		points = 0
		aPoint = 11
		points = self.countingPoints(aPoint)
		if points > 21:
			aPoint = 1
			points = self.countingPoints(aPoint)
			
		return points
		

class Dealer(Player):
	global random
	def __init__(self):
		self.card = []
	
	# shuffle cards, pass in an instance of Deck object
	def shuffleCards(self, aDeck):
		return aDeck.shuffleTheDeck()
	
	# give out one card, pass in an instance of Deck object
	def giveOutACard(self, aDeck):
		return aDeck.popTheTopCard().cardInfo()
	

def askInfo():
	while True:
		try:
			moneyYouHave = int(raw_input('Please enter the money you have: '))
		except:
			print 'Please enter a valid number.'
			continue
		else:
			if moneyYouHave > 0:
				return moneyYouHave
				break

def askBetMoney():
	while True:
		try:
			moneyToBet = int(raw_input("Please enter the amount of money you want to bet: "))
		except:
			print 'Please enter a valid number.'
			continue
		else:
			if moneyToBet > 0:
				return moneyToBet
				break

def askHitOrStand():
	hitOrStand = raw_input("Hit or Stand (H/S)? ")
	while hitOrStand.lower() not in ['h','s','hit','stand']:
		hitOrStand = raw_input("Hit or Stand (H/S)? ")
	else:
		return hitOrStand

def displayPoints(Player, Dealer):
	print "Player's cards: %s" %Player.hands()
	print "Player points: %s" %Player.pointsInHands()
	print "Dealer's cards: %s" %Dealer.hands()
	print "Dealer points: %s" %Dealer.pointsInHands()
	print "------------------------------------------------------------------------"

def checkForWin(Player, Dealer):
	print "Final Result: "
	displayPoints(Player, Dealer)
	while Player.pointsInHands() <= 21 and Dealer.pointsInHands() <= 21:
		if Player.pointsInHands() > Dealer.pointsInHands():
			return 'Player Win!'
			break
		elif Player.pointsInHands() < Dealer.pointsInHands():
			return 'Player Lost!'
			break
		else:
			return "Push! It's a tied!"
			break
	else:
		if Player.pointsInHands() > 21:
			return 'Player got busted!'
		elif Dealer.pointsInHands() > 21:
			return 'Dealer got busted!'

def askIfPlayAgain():
	playAgain = raw_input("Play again (Y/N)? ")
	while playAgain.lower() not in ['y','n','yes','no']:
		playAgain = raw_input("Play again (Y/N)? ")
	else:
		return playAgain			
			
# main function
if __name__ == '__main__':
	# initialization
	print '----------Start the blackJack----------'
	gameOn = True
	gamePlay = True
	player_money = askInfo() 
	player1 = Player(money = player_money)
	
	while gameOn:
		
		while True:
			bet_money = askBetMoney()
			if player1.money >= bet_money:
				break
		
		print 'Total Money: %s' %player1.money
		print 'Money bet: %s' %bet_money
		dealer = Dealer()
		deck = Deck()
		dealer.shuffleCards(deck)
		
		# give out first two cards each to player & dealer
		for i in range(1,5):
			if i % 2 != 0:
				player1.getACard(dealer.giveOutACard(deck))
			else:
				dealer.getACard(dealer.giveOutACard(deck))
		print '----------Points after first 2 cards----------'
		displayPoints(player1, dealer)
		
		
		# game play after the first two cards
		turn = 1
		playerStand = False
		dealerStand = False
		
		while gamePlay:
			if turn % 2 != 0:
				if playerStand == False:
					# Player's turn
					print "Player's turn:"
					hitOrStand = askHitOrStand()
					if hitOrStand.lower() in ['h','hit']:
						print 'Player Hits!'
						player1.getACard(dealer.giveOutACard(deck))
						if player1.pointsInHands() > 21:
							#print 'Player got busted!'
							break
					else:
						print 'Player Stands!'
						playerStand = True
					print '---Points after move---'
					displayPoints(player1, dealer)
				turn += 1
			else:
				# dealer will hit until 17+ points and then stand
				if dealerStand == False and dealer.pointsInHands() < 17:
					print "Dealer's turn:"
					print 'Dealer has less than 17. Hit!'
					print '---Points after move---'
					dealer.getACard(dealer.giveOutACard(deck))
					if 17 <= dealer.pointsInHands() <= 21:
						dealerStand = True
						displayPoints(player1, dealer)
					elif dealer.pointsInHands() < 17:
						dealerStand = False
						displayPoints(player1, dealer)
					else: 
						#print 'Dealer got busted!'
						displayPoints(player1, dealer)
						break
				elif dealerStand == False and 17 <= dealer.pointsInHands() <= 21:
					print "Dealer's turn:"
					print 'Dealer has more than 17. Stand!'
					print '---Points after move---'
					displayPoints(player1, dealer)
					dealerStand = True	
				turn += 1
			gamePlay = not (playerStand and dealerStand)
		
		# Check result
		result = checkForWin(player1, dealer)
		print result
		
		# Calculate Player's money
		if result in ['Player Win!', 'Dealer got busted!']:
			player_money = player1.totalMoney(bet_money)
		elif result in ['Player Lost!', 'Player got busted!']:
			player_money = player1.totalMoney(-bet_money)
		else: 
			player_money = player1.totalMoney(0)
		print "Player's total money: ", player1.money
		
		# Ask if player want to keep playing
		playAgain = askIfPlayAgain()
		if playAgain.lower() in ['y', 'yes']:
			# re-initialization
			if player1.money <= 0:
				player1.money = askInfo()
			gameOn = True
			gamePlay = True
			player1.card = []
			print '----------Next Round----------'
			
		else:
			gameOn = False
	else:
		print 'Game is Over! Thanks for Playing!'
		print 'Total Money left: %s' %player1.money
