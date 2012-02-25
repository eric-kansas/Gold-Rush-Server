# -*- coding: utf-8 -*-
"""Setup the tg2app application"""

import logging
from tg import config
from tg2app import model

import transaction


def bootstrap(command, conf, vars):
    """Place any commands to setup tg2app here"""

    # <websetup.bootstrap.before.auth
    from sqlalchemy.exc import IntegrityError
    try:
        #build game
        game = model.Game()

        #build cards
        cards = buildDeck()
        for card in cards:
            model.DBSession.add(card)

        for card in cards:
            game.cards.append(card)

        #make hand
        hand1 = model.Hand()

        #make cards in hand
        hand1.cards.append(cards[1])
        cards[1].hand_id = hand1
        model.DBSession.add(hand1)
        game.hands.append(hand1)

        # Add four lulzy users.
        players = []
        for i in range(4):
            players.append(model.Player(
                name="Lulzy Guy " + str(i)
            ))
            model.DBSession.add(players[i])
            game.players.append(players[i])
        
        game.whose_turn = players[0]

        # Make friends!
        #player1.friends.append(player2)
        #player2.friends.append(player1)

        # Make more friends!
        #player1.friends.append(player3)
        #player3.friends.append(player1)

        # Add four lulzy avatars.
        entities = []
        for i in range(4):
            entities.append(model.Entity(
            is_avatar=True,
            row=2,
            col=3,
            ))
            model.DBSession.add(entities[i])
            entities[i].player =  players[i]
            entities[i].game = game
            model.DBSession.add(entities[i])
        
        game.whose_turn = players[i]
        model.DBSession.add(game)
       
        transaction.commit()

    except IntegrityError:
        print 'Warning, there was a problem adding your auth data, it may have\
         already been added:'
        import traceback
        print traceback.format_exc()
        transaction.abort()
        print 'Continuing with bootstrapping...'

    # <websetup.bootstrap.after.auth>


def buildDeck():

    cards = []
    for i in range(4):
        for k in range(13):
            tempCard = model.Card(
                is_up=False,
                suit=i,
                kind=k
            )
            cards.append(tempCard)

    return cards
