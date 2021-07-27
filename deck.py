from kivy.uix.image import Image

deck_1 = []
deck_2 = []
suits = ['spades', 'clubs', 'diamonds', 'hearts']
ranks = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
high_card = 'Старшая карта'
one_pair = 'Пара'
two_pair = 'Две пары'
three = 'Тройка'
straight = 'Стрит'
flush = 'Флеш'
full_house = 'Фулл хаус'
four = 'Каре'
straight_flush = 'Стрит флеш'
royal_flush = 'Флеш рояль'

class Combination:
    def __init__(self, name, hand, power, comb_power):
        self.name = name
        self.hand = hand
        self.power = power
        self.comb_power = comb_power

def check_straight_or_royal_flush(cards):
    hand = []
    only_one_suit = []

    for suit in suits:
        if len(only_one_suit) >= 5:
            break
        only_one_suit.clear()
        for card in cards:
            if card.suit == suit:
                only_one_suit.append(card)

    if len(only_one_suit) < 5:
        return False

    for i in range(len(only_one_suit)):
        if len(hand) == 5:
            break
        if i == 0:
            hand.append(only_one_suit[i])
            continue
        if not only_one_suit[i].rank == only_one_suit[i - 1].rank - 1:
            break

        if len(hand) < 5:
            hand.append(only_one_suit[i])

    if len(hand) < 5:
        return False

    hand.sort(key=lambda x: x.rank, reverse=True)
    if hand[0].rank == 14:
        return Combination(royal_flush, hand, hand[0].rank, 10)
    else:
        return Combination(straight_flush, hand, hand[0].rank, 9)

def check_four(cards):
    hand = []

    '''for i in range(len(cards)):
        if i == 0:
            hand.append(cards[i])
            continue

        if cards[i].rank == cards[i-1].rank:
            hand.append(cards[i])
            if len(hand) == 4:
                break
        else:
            hand.clear()'''
    rank_count = {}
    for card in cards:
        proceed = True
        if len(rank_count) == 0:
            rank_count[card.rank] = 1
            continue
        for key in rank_count:
            if card.rank == key:
                rank_count[key] += 1
                proceed = False
                break
        if proceed:
            rank_count[card.rank] = 1

    for card in cards:
        if rank_count.get(card.rank) == 4:
            hand.append(card)
        if len(hand) == 5:
            break

    if len(hand) == 4:
        return Combination(four, hand, hand[0].rank, 8)
    else:
        return False

def check_full_house(cards):
    hand = []
    rank_count = {}
    for card in cards:
        proceed = True
        if len(rank_count) == 0:
            rank_count[card.rank] = 1
            continue
        for key in rank_count:
            if card.rank == key:
                rank_count[key] += 1
                proceed = False
                break
        if proceed:
            rank_count[card.rank] = 1

    for card in cards:
        if rank_count.get(card.rank) == 3:
            hand.append(card)

    if len(hand) == 3:
        for card in cards:
            if rank_count.get(card.rank) == 2:
                hand.append(card)
            if len(hand) == 5:
                break

    if len(hand) == 5:
        return Combination(full_house, hand, hand[0].rank, 7)
    else:
        return False

def check_flush(cards):
    hand = []
    for suit in suits:
        if len(hand) == 5:
            break
        hand.clear()
        for card in cards:
            if card.suit == suit:
                hand.append(card)
            if len(hand) == 5:
                break

    if len(hand) == 5:
        return Combination(flush, hand, hand[0].rank, 6)
    else:
        return False

def check_strait(cards):
    hand = []
    for i in range(len(cards)):
        if i == 0:
            continue
        if cards[i].rank == cards[i-1].rank - 1:
            if len(hand) == 0:
                hand.append(cards[i-1])
            hand.append(cards[i])
            if len(hand) == 5:
                break
        elif cards[i].rank == cards[i-1].rank:
            continue
        else:
            if len(hand) < 5:
                hand.clear()


    if len(hand) == 5:
        return Combination(straight, hand, hand[0].rank, 5)
    else:
        return False

def check_three(cards):
    hand = []
    rank_count = {}
    for card in cards:
        proceed = True
        if len(rank_count) == 0:
            rank_count[card.rank] = 1
            continue
        for key in rank_count:
            if card.rank == key:
                rank_count[key] += 1
                proceed = False
                break
        if proceed:
            rank_count[card.rank] = 1

    for card in cards:
        if rank_count.get(card.rank) == 3:
            hand.append(card)
        if len(hand) == 5:
            break

    if len(hand) == 3:
        return Combination(three, hand, hand[0].rank, 4)
    else:
        return False

def check_two_pair(cards):
    hand = []
    rank_count = {}
    for card in cards:
        proceed = True
        if len(rank_count) == 0:
            rank_count[card.rank] = 1
            continue
        for key in rank_count:
            if card.rank == key:
                rank_count[key] += 1
                proceed = False
                break
        if proceed:
            rank_count[card.rank] = 1

    for card in cards:
        if rank_count.get(card.rank) == 2:
            hand.append(card)
        if len(hand) == 4:
            break

    if len(hand) == 4:
        return Combination(two_pair, hand, hand[0].rank, 3)
    else:
        return False

def check_one_pair(cards):
    hand = []
    rank_count = {}
    for card in cards:
        proceed = True
        if len(rank_count) == 0:
            rank_count[card.rank] = 1
            continue
        for key in rank_count:
            if card.rank == key:
                rank_count[key] += 1
                proceed = False
                break
        if proceed:
            rank_count[card.rank] = 1

    for card in cards:
        if rank_count.get(card.rank) == 2:
            hand.append(card)
        if len(hand) == 5:
            break
    if len(hand) == 2:
        return Combination(one_pair, hand, hand[0].rank, 2)
    else:
        return False

class Card:
    def __init__(self, id, suit, rank, image):
        self.id = id
        self.suit = suit
        self.rank = rank
        self.image = image

    def get_image(self):
        return Image(source=self.image)

def get_combination(cards):
    card9 = Card(0, "diamonds", 6, "cards/1_d6.png")
    card8 = Card(1, "clubs", 9, "cards/1_c9.png")
    card11 = Card(2, "clubs", 10, "cards/1_c10.png")
    card14 = Card(3, "hearts", 6, "cards/1_h6.png")
    card10 = Card(4, "clubs", 7, "cards/1_c7.png")
    card13 = Card(5, "clubs", 8, "cards/1_c8.png")
    card12 = Card(6, "diamonds", 8, "cards/1_d8.png")
    cards = [card9, card8, card11, card14, card10, card13, card12]
    #cards.sort(key=lambda x: x.rank, reverse=True)

    combination = check_straight_or_royal_flush(cards)
    if combination:
        return combination
    combination = check_four(cards)
    if combination:
        return combination
    combination = check_full_house(cards)
    if combination:
        return combination
    combination = check_flush(cards)
    if combination:
        return combination
    combination = check_strait(cards)
    if combination:
        return combination
    combination = check_three(cards)
    if combination:
        return combination
    combination = check_two_pair(cards)
    if combination:
        return combination
    combination = check_one_pair(cards)
    if combination:
        return combination
    hand = [cards[0]]
    return Combination(high_card, hand, hand[0].rank, 1)

id = 0
for suit in suits:
    for rank in ranks:
        imageStr = 'cards/1_' + suit[0] + str(rank) + '.png'
        card = Card(id, suit, rank, imageStr)
        deck_1.append(card)
        id += 1

for suit in suits:
    for rank in ranks:
        imageStr = 'cards/2_' + suit[0] + str(rank) + '.png'
        card = Card(id, suit, rank, imageStr)
        deck_2.append(card)
        id += 1

def get_deck(var):
    if var == 1:
        return deck_1
    elif var == 2:
        return deck_2

def get_shirt(var):
    if var == 1:
        return Image(source='cards/1_shirt.png')
    elif var == 2:
        return Image(source='cards/2_shirt.png')
    else:
        return None