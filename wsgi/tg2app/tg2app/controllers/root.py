# -*- coding: utf-8 -*-
"""Main Controller"""

from tg import expose, flash, require, url, request, redirect
from tg.i18n import ugettext as _, lazy_ugettext as l_
from tgext.admin.tgadminconfig import TGAdminConfig
from tgext.admin.controller import AdminController
from repoze.what import predicates

from tg2app.lib.base import BaseController
from tg2app.model import DBSession, metadata
from tg2app import model
from tg2app.controllers.secure import SecureController

from tg2app.controllers.error import ErrorController

import simplejson

import transaction

__all__ = ['RootController']


class RootController(BaseController):
    """
    The root controller for the tg2app application.

    All the other controllers and WSGI applications should be mounted on this
    controller. For example::

        panel = ControlPanelController()
        another_app = AnotherWSGIApplication()

    Keep in mind that WSGI applications shouldn't be mounted directly: They
    must be wrapped around with :class:`tg.controllers.WSGIAppController`.

    """
    secc = SecureController()

    admin = AdminController(model, DBSession, config_type=TGAdminConfig)

    error = ErrorController()

    @expose('tg2app.templates.index')
    def index(self):
        """Handle the front-page."""
        return dict(page='index')

    @expose('json')
    #@expose('')
    def game(self, game_id):
        game = model.DBSession.query(model.Game).filter_by(id=game_id).one()
  
        import pprint
        output = pprint.pformat(game.to_json())
        print output # for debugging on the console
        return output # for debugging in the browser
        #return game.to_json()
   

    @expose()
    def update_roll(self, roll, game_id):
        game = model.DBSession.query(model.Game).filter_by(id=game_id).one()

        game.current_roll = roll
        model.DBSession.flush()
        #model.DBSession.commit()
        transaction.commit()

    @expose()
    def update_game_state(self, turn_state, game_id):
        game = model.DBSession.query(model.Game).filter_by(id=game_id).one()
        game.game_state = state
        model.DBSession.flush()
        transaction.commit()
    
    @expose()
    def update_turn_state(self, turn_state, game_id):
        game = model.DBSession.query(model.Game).filter_by(id=game_id).one()
        game.game_turn = state
        model.DBSession.flush()
        transaction.commit() 

    @expose()
    def update_card_up(self, is_face_up, card_id):
        card = model.DBSession.query(model.Card).filter_by(card_id=card_id).one()
        card.is_up = is_face_up
        model.DBSession.flush()
        transaction.commit()

         
    @expose()
    def write_game_dummy(self, incoming_json_str):
        incoming_json = simplejson.loads(incoming_json_str)
        
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

    @expose('tg2app.templates.about')
    def about(self):
        """Handle the 'about' page."""
        return dict(page='about')

    @expose('tg2app.templates.environ')
    def environ(self):
        """This method showcases TG's access to the wsgi environment."""
        return dict(environment=request.environ)

    @expose('tg2app.templates.data')
    @expose('json')
    def data(self, **kw):
        """This method showcases how you can use the same controller for a data page and a display page"""
        return dict(params=kw)

    @expose('tg2app.templates.authentication')
    def auth(self):
        """Display some information about auth* on this application."""
        return dict(page='auth')

    @expose('tg2app.templates.index')
    @require(predicates.has_permission('manage', msg=l_('Only for managers')))
    def manage_permission_only(self, **kw):
        """Illustrate how a page for managers only works."""
        return dict(page='managers stuff')

    @expose('tg2app.templates.index')
    @require(predicates.is_user('editor', msg=l_('Only for the editor')))
    def editor_user_only(self, **kw):
        """Illustrate how a page exclusive for the editor works."""
        return dict(page='editor stuff')

    @expose('tg2app.templates.login')
    def login(self, came_from=url('/')):
        """Start the user login."""
        login_counter = request.environ['repoze.who.logins']
        if login_counter > 0:
            flash(_('Wrong credentials'), 'warning')
        return dict(page='login', login_counter=str(login_counter),
                    came_from=came_from)

    @expose()
    def post_login(self, came_from='/'):
        """
        Redirect the user to the initially requested page on successful
        authentication or redirect her back to the login page if login failed.

        """
        if not request.identity:
            login_counter = request.environ['repoze.who.logins'] + 1
            redirect('/login',
                params=dict(came_from=came_from, __logins=login_counter))
        userid = request.identity['repoze.who.userid']
        flash(_('Welcome back, %s!') % userid)
        redirect(came_from)

    @expose()
    def post_logout(self, came_from=url('/')):
        """
        Redirect the user to the initially requested page on logout and say
        goodbye as well.

        """
        flash(_('We hope to see you soon!'))
        redirect(came_from)
