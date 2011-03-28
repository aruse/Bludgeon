# Copyright (c) 2011 Andy Ruse.
# See LICENSE for details.

import sys
import random

from const import *
from server import Server as S
from monster import *
from dlevel import *
from requesthandler import *

def monsters_take_turn():
    for m in S.monsters:
        if m.ai:
            m.ai.take_turn()


def handle_requests():
    """Handle requests coming in from the client."""
    while len(Network.requests):
        req, args = Network.requests.popleft()

        S.cmd_history.append((req, args))
        response = S.requests[req].do(args)
#        S.server_responses.append(response)


def init_server():
    """Initialize all of the server state."""
    S.map_rand = random.Random()
    S.rand = random.Random()

#    if options.save_file:
#        load_game(options.save_file)
#        S.map_rand.seed(S.random_seed)
#        S.rand.seed(S.random_seed)
#
#    else:
    if True:
        # We need to generate a random seed using the default-seeded random
        # number generator, and then save that to seed the game's generators.
        # This will allow us to use the same seed to duplicate games.
        S.random_seed = str(random.randrange(sys.maxint))
        S.map_rand.seed(S.random_seed)
        S.rand.seed(S.random_seed)

        S.u = Player(0, 0, 'wizard', fov_radius=10)
        S.dlevel = 1
        S.dlevel_dict['doom'] = []
        S.dlevel_dict['doom'].append(gen_connected_rooms())
        S.map = S.dlevel_dict['doom'][0]
    

    S.u.set_fov_map(S.map)
    S.u.fov_map.do_fov(S.u.x, S.u.y, S.u.fov_radius)
    attach_request_actions()
    message('Welcome, {0}!'.format("Whatever"), CLR['gold'])


def server_tick():
    """Main loop for the server."""
    handle_requests()

    if S.u_took_turn:
        S.u.fov_map.do_fov(S.u.x, S.u.y, S.u.fov_radius)
        monsters_take_turn()
        S.u_took_turn = False


    # Send responses to the client.
    response = {}

#    if True: # FIXME: should be if map is dirty
#        response['map'] = S.map


    # Tell the client which monsters to update.
    # FIXME: We currently send the whole monster object, but this needs to be
    # modified to only send the attributes which have changed since the last
    # update.
    for m in S.monsters:
        if m.dirty:
            if 'm' not in response:
                response['m'] = {}
            response['m'][m.oid] = m.client_serialize()
            m.dirty = False

    for m in S.monsters_to_delete:
        if 'm_del' not in response:
            response['m_del'] = []
        response['m_del'].append(m)
    del S.monsters_to_delete[:]


    # Tell the client which items to update.
    for i in S.items:
        if i.dirty:
            if 'i' not in response:
                response['i'] = {}
            response['i'][i.oid] = i.client_serialize()
            i.dirty = False

    for i in S.items_to_delete:
        if 'i_del' not in response:
            response['i_del'] = []
        response['i_del'].append(i)
    del S.items_to_delete[:]


    # Send the updated player to the client.
    if S.u.dirty:
        response['u'] = S.u.client_serialize()
        S.u.dirty = False

    if len(S.msgs):
        response['log'] = []
        for msg in S.msgs:
            response['log'].append(msg)
        S.msgs.clear()

    if response:
        Network.send_response(response)
