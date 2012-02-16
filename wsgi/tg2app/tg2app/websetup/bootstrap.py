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
        # Add three lulzy users.
        player1 = model.Player(
            name="Lulzy Guy"
        )
        model.DBSession.add(player1)
        player2 = model.Player(
            name="Lulzy Lady"
        )
        model.DBSession.add(player2)

        player3 = model.Player(
            name="Foo Manchu"
        )
        model.DBSession.add(player3)

        # Make friends!
        player1.friends.append(player2)
        player2.friends.append(player1)

        # Make more friends!
        player1.friends.append(player3)
        player3.friends.append(player1)

        transaction.commit()

    except IntegrityError:
        print 'Warning, there was a problem adding your auth data, it may have already been added:'
        import traceback
        print traceback.format_exc()
        transaction.abort()
        print 'Continuing with bootstrapping...'
        

    # <websetup.bootstrap.after.auth>

def buildDeck():
    
    cards = []
    for i in range(4)
        for k in range(12)
            tempCard = model.Card(
                is_up = false,
                suit = i,
                kind = k
	     )
    return cards
