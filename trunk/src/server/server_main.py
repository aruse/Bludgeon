# Copyright (c) 2011 Andy Ruse.
# See LICENSE for details.

import sys
import random

from const import *
from network import Network
from server_state import ServerState as SS
from monster import *
from dlevel import *
from requesthandler import *

def monsters_take_turn():
    for m in SS.monsters:
        if m.ai:
            m.ai.take_turn()


def handle_requests():
    """Handle requests coming in from the client."""
    while len(Network.requests):
        req, args = Network.requests.popleft()

        SS.cmd_history.append((req, args))
        response = SS.requests[req].do(args)
#        SS.server_responses.append(response)


def init_server():
    """Initialize all of the server state."""
    SS.map_rand = random.Random()
    SS.rand = random.Random()

#    if options.save_file:
#        load_game(options.save_file)
#        SS.map_rand.seed(SS.random_seed)
#        SS.rand.seed(SS.random_seed)
#
#    else:
    if True:
        # We need to generate a random seed using the default-seeded random
        # number generator, and then save that to seed the game's generators.
        # This will allow us to use the same seed to duplicate games.
        SS.random_seed = str(random.randrange(sys.maxint))
        SS.map_rand.seed(SS.random_seed)
        SS.rand.seed(SS.random_seed)

        SS.u = Player(0, 0, 'wizard', fov_radius=10)
        SS.dlevel = 1
        SS.dlevel_dict['doom'] = []
        SS.dlevel_dict['doom'].append(gen_connected_rooms())
        SS.map = SS.dlevel_dict['doom'][0]
    

    SS.u.set_fov_map(SS.map)
    SS.u.fov_map.do_fov(SS.u.x, SS.u.y, SS.u.fov_radius)
    attach_request_actions()
    message('Welcome, {0}!'.format("Whatever"), CLR['gold'])


def server_tick():
    """Main loop for the server."""
    handle_requests()

    if SS.u_took_turn:
        SS.u.fov_map.do_fov(SS.u.x, SS.u.y, SS.u.fov_radius)
        monsters_take_turn()
        SS.u_took_turn = False


    # Send responses to the client.
    response = {}

#    if True: # FIXME: should be if map is dirty
#        response['map'] = SS.map


    # Tell the client which monsters to update.
    # FIXME: We currently send the whole monster object, but this needs to be
    # modified to only send the attributes which have changed since the last
    # update.
    for mon in SS.monsters:
        if mon.dirty:
            if 'm' not in response:
                response['m'] = {}
            response['m'][mon.oid] = mon.client_serialize()
            mon.dirty = False

    for mon in SS.monsters_to_delete:
        if 'm_del' not in response:
            response['m_del'] = []
        response['m_del'].append(mon)
    del SS.monsters_to_delete[:]


    # Tell the client which items to update.
    for item in SS.items:
        if item.dirty:
            if 'i' not in response:
                response['i'] = {}
            response['i'][item.oid] = item.client_serialize()
            item.dirty = False

    for item in SS.items_to_delete:
        if 'i_del' not in response:
            response['i_del'] = []
        response['i_del'].append(item)
    del SS.items_to_delete[:]


    # Send the updated player to the client.
    if SS.u.dirty:
        response['u'] = SS.u.client_serialize()
        SS.u.dirty = False

    if len(SS.msgs):
        response['log'] = []
        for msg in SS.msgs:
            response['log'].append(msg)
        SS.msgs.clear()

    if response:
        Network.send_response(response)
