# Copyright (c) 2011 Andy Ruse.
# See LICENSE for details.

"""
Setup of game objects and main game loop.
"""

import signal
import pygame
from pygame import Surface
import pygame.locals as pgl

import cfg
from common import impossible
from network import Network
from client_state import ClientState as CS
from client_map import ClientMap
from client_object import ClientObject
from client_item import ClientItem
from client_monster import ClientMonster
from client_player import ClientPlayer
from widgets import ScrollBar
import gui
import keys
import image
from client_util import client_message, quit_game


def client_init():
    """Initialiaze client state."""
    # Set up signal handlers
    signal.signal(signal.SIGINT, quit_game)
    signal.signal(signal.SIGTERM, quit_game)

    # Initializing these modules separately instead of calling
    # pygame.init() is WAY faster.
    pygame.display.init()
    pygame.font.init()

    # Wait 200 ms before repeating a key that's held down, and send them
    # as fast as possible.  The repeat delay is therefore limited by the
    # frame rate, not by set_repeat()
    pygame.key.set_repeat(200, 1)

    pygame.display.set_caption('{0} {1}'.format(cfg.GAME_NAME, cfg.VERSION))

    uname = 'Taimor'
    usex = 'Male'
    urace = 'Human'
    urole = 'Wizard'

    pygame.display.set_caption('{0} - {1} the {2} {3} {4}'.format(
            cfg.GAME_TITLE, uname, usex, urace, urole))

    CS.clock = pygame.time.Clock()

    CS.font = pygame.font.SysFont('Arial', cfg.FONT_SIZE)
    CS.font_h = CS.font.get_height()
    CS.font_w = CS.font.size('X')[0]

    # Size of the map surface
    CS.map_rect.w = (cfg.MAP_W + 2) * cfg.TILE_W
    CS.map_rect.h = (cfg.MAP_H + 2) * cfg.TILE_H

    # Size of the status panel
    CS.status_rect.w = cfg.STATUS_W * CS.font_w
    CS.status_rect.h = cfg.STATUS_H * CS.font_h

    # Size of the equipment panel
    CS.eq_rect.w = cfg.EQ_W * cfg.TILE_W
    CS.eq_rect.h = CS.status_rect.h

    # Size of the full game screen
    CS.screen_rect.w = CS.eq_rect.w + CS.status_rect.w + cfg.MIN_LOG_W
    if CS.screen_rect.w < cfg.INIT_SCREEN_W:
        CS.screen_rect.w = cfg.INIT_SCREEN_W

    CS.screen_rect.h = CS.status_rect.h + cfg.MIN_MAPVIEW_H
    if CS.screen_rect.h < cfg.INIT_SCREEN_H:
        CS.screen_rect.h = cfg.INIT_SCREEN_H

    # Size of the log surface
    CS.log_rect.w = CS.screen_rect.w - (
        CS.eq_rect.w + CS.status_rect.w) - cfg.SCROLLBAR_W - 50
    CS.log_rect.h = CS.status_rect.h
    CS.logview_rect.w, CS.logview_rect.h = CS.log_rect.w, CS.log_rect.h

    # The mapview size.  May be smaller or larger than the actual map size.
    # This is the location on the screen where the map or a piece thereof
    # is drawn.  It's not an actual surface, but a logical rectangle.
    CS.mapview_rect.w = CS.screen_rect.w - cfg.SCROLLBAR_W
    CS.mapview_rect.h = (
        CS.screen_rect.h - CS.status_rect.h - cfg.SCROLLBAR_W)

    # Locations to blit equipment on the equipment panel
    eq_cent = (int(CS.eq_rect.w / 2.0 - cfg.TILE_W / 2),
               int(CS.eq_rect.h / 2.0 - cfg.TILE_W / 2))
    CS.eq_hands = (eq_cent[0],
                   CS.eq_rect.y + cfg.TILE_H / 2 + 3 * cfg.TILE_H)
    CS.eq_rweap = (CS.eq_hands[0] - cfg.TILE_W,
                   CS.eq_hands[1])
    CS.eq_lweap = (CS.eq_hands[0] + cfg.TILE_W,
                   CS.eq_hands[1])
    CS.eq_rring = (CS.eq_hands[0] - cfg.TILE_W,
                   CS.eq_hands[1] + cfg.TILE_H)
    CS.eq_lring = (CS.eq_hands[0] + cfg.TILE_W,
                   CS.eq_hands[1] + cfg.TILE_H)
    CS.eq_boots = (CS.eq_hands[0],
                   CS.eq_hands[1] + cfg.TILE_H * 2)
    CS.eq_armor = (CS.eq_hands[0],
                   CS.eq_hands[1] - cfg.TILE_H)
    CS.eq_shirt = (CS.eq_hands[0] - cfg.TILE_W,
                   CS.eq_hands[1] - cfg.TILE_H)
    CS.eq_cloak = (CS.eq_hands[0] + cfg.TILE_W,
                   CS.eq_hands[1] - cfg.TILE_H)
    CS.eq_neck = (CS.eq_hands[0],
                  CS.eq_hands[1] - cfg.TILE_H * 2)
    CS.eq_eyes = (CS.eq_hands[0] - cfg.TILE_W,
                  CS.eq_hands[1] - cfg.TILE_H * 2)
    CS.eq_quiver = (CS.eq_hands[0] + cfg.TILE_W * 2,
                    CS.eq_hands[1] - cfg.TILE_H * 3)
    CS.eq_light = (CS.eq_hands[0] - cfg.TILE_W * 2,
                   CS.eq_hands[1] - cfg.TILE_H * 3)
    CS.eq_head = (CS.eq_hands[0],
                  CS.eq_hands[1] - cfg.TILE_H * 3)

    CS.screen = pygame.display.set_mode(
        (CS.screen_rect.w, CS.screen_rect.h), pygame.RESIZABLE)
    CS.eq_surf = Surface((CS.eq_rect.w, CS.eq_rect.h)).convert()
    CS.status_surf = Surface((CS.status_rect.w, CS.status_rect.h)).convert()
    CS.map_surf = Surface((CS.map_rect.w, CS.map_rect.h)).convert()

    # Set the system icon
    system_icon = image.load_image('icon.xpm')
    pygame.display.set_icon(system_icon)

    CS.tiles_img = image.load_image('tiles16.xpm')
    CS.gray_tiles_img = image.load_image('tiles16_gray.xpm')
    CS.menu_bg_img = image.load_image('parchment.jpg')

    CS.tile_dict = image.create_tile_dict()
    CS.blank_tile = CS.tile_dict['cmap, wall, dark']

    CS.x_scrollbar = ScrollBar(cfg.SCROLLBAR_W, 0, CS.map_rect,
                               CS.mapview_rect, always_show=False)
    CS.y_scrollbar = ScrollBar(cfg.SCROLLBAR_W, 1, CS.map_rect,
                               CS.mapview_rect, always_show=False)
    CS.log_scrollbar = ScrollBar(cfg.SCROLLBAR_W, 1, CS.log_rect,
                                 CS.logview_rect, always_show=False)

    # Process any initial setup data we've gotten from the server.  This
    # should include the first dungeon level and the Player object.
    handle_responses()

    # Set up keystroke actions
    keys.attach_key_actions()

    # Make sure everything is aligned correctly
    gui.center_map()
    gui.handle_resize(CS.screen_rect.w, CS.screen_rect.h)


def handle_events():
    """Handle input events."""
    for event in pygame.event.get():
        if event.type == pgl.QUIT:
            quit_game()
        elif event.type == pgl.KEYDOWN:
            CS.key = event
        elif event.type == pgl.KEYUP:
            CS.key = None
        elif event.type == pgl.MOUSEBUTTONDOWN:
            CS.button = event.button
        elif event.type == pgl.MOUSEBUTTONUP:
            CS.button = None
        elif event.type == pgl.MOUSEMOTION:
            pass
        elif event.type == pgl.VIDEORESIZE:
            gui.handle_resize(event.w, event.h)

        # Handle scrolling
        CS.x_scrollbar.handle_event(event)
        CS.y_scrollbar.handle_event(event)
        CS.log_scrollbar.handle_event(event)

    if CS.key:
        key_code, char, mod = CS.key.key, CS.key.unicode, CS.key.mod
        CS.key = None
    else:
        key_code, char, mod = None, None, None

    if CS.mode == cfg.ST_PLAYING:
        # Handle all keypresses
        if key_code:
            handled = False
            key_combo = ''

            if mod & pgl.KMOD_SHIFT:
                if char not in CS.pkeys[pgl.KMOD_NONE]:
                    key_combo = 'Shift + '

                if (key_code in CS.pkeys[pgl.KMOD_SHIFT] and
                    CS.pkeys[pgl.KMOD_SHIFT][key_code].action):
                    CS.pkeys[pgl.KMOD_SHIFT][key_code].perform_action()
                    handled = True

            elif mod & pgl.KMOD_CTRL:
                key_combo = 'Ctrl + '

                if (key_code in CS.pkeys[pgl.KMOD_CTRL] and
                    CS.pkeys[pgl.KMOD_CTRL][key_code].action):
                    CS.pkeys[pgl.KMOD_CTRL][key_code].perform_action()
                    handled = True

            elif mod & pgl.KMOD_ALT:
                key_combo = 'Alt + '

                if (key_code in CS.pkeys[pgl.KMOD_ALT] and
                    CS.pkeys[pgl.KMOD_ALT][key_code].action):
                    CS.pkeys[pgl.KMOD_ALT][key_code].perform_action()
                    handled = True

            if not handled:
                # First, look up by char.  If it's not found, then look up by
                # key_code.
                if (char in CS.pkeys[pgl.KMOD_NONE] and
                    CS.pkeys[pgl.KMOD_NONE][char].action):
                    CS.pkeys[pgl.KMOD_NONE][char].perform_action()
                    handled = True
                elif (key_code in CS.pkeys[pgl.KMOD_NONE] and
                      CS.pkeys[pgl.KMOD_NONE][key_code].action):
                    CS.pkeys[pgl.KMOD_NONE][key_code].perform_action()
                    handled = True

            if key_code not in CS.ignore_keys and handled is False:
                if char in CS.pkeys[pgl.KMOD_NONE]:
                    key_to_print = char
                else:
                    key_to_print = pygame.key.name(key_code)
                    client_message("Unknown command '{0}{1}'.".format(
                            key_combo, key_to_print))

    elif CS.mode == cfg.ST_MENU:
        if key_code:
            if len(char) == 1:
                index = ord(char) - ord('a')
                if index >= 0 and index < len(CS.menu_options):
                    if CS.menu == 'use':
                        CS.mode = cfg.ST_PLAYING  # Exit menu
                        if len(CS.u.inventory) > 0:
                            item = CS.u.inventory[index]
                            if item is not None:
                                Network.request('a', (item.oid,))

                    elif CS.menu == 'drop':
                        CS.mode = cfg.ST_PLAYING  # Exit menu
                        if len(CS.u.inventory) > 0:
                            item = CS.u.inventory[index]
                            if item is not None:
                                Network.request('d', (item.oid,))
                else:
                    CS.mode = cfg.ST_PLAYING  # Exit menu
            else:
                CS.mode = cfg.ST_PLAYING  # Exit menu

    elif CS.mode == cfg.ST_TARGETING:
        if CS.button:
            x, y = pygame.mouse.get_pos()
            x, y = gui.mouse2cell(x, y)

            # Accept the target if the player clicked in FOV, and in
            # case a range is specified, if it's in that range
            if CS.button == cfg.BUTTON_L and CS.u.fov_map.in_fov(x, y):
                targeting_function = CS.targeting_function.pop(0)
                success = targeting_function(CS.targeting_item, x, y)

                # If this targeting is the result of an item use,
                # destroy the item
                if CS.targeting_item and success:
                    CS.u.inventory.remove(CS.targeting_item)
                    del ClientObject.obj_dict[CS.targeting_item.oid]
                    CS.targeting_item = None

            CS.mode = cfg.ST_PLAYING
        elif key_code:
            client_message('Cancelled')
            CS.mode = cfg.ST_PLAYING
    elif CS.mode == cfg.ST_PLAYBACK:
        pass
    elif CS.mode == cfg.ST_QUIT:
        # Do nothing; let the main loop exit on its own.
        pass
    else:
        impossible('Unknown state: ' + CS.mode)


def handle_responses():
    """Read in server responses from the network and process."""

    res = Network.get_response()
    while res:
        # Load level map
        if 'map' in res:
            CS.map = ClientMap.unserialize(res['map'])
            new_dlevel = True
        else:
            new_dlevel = False

        # Update log messages
        if 'log' in res:
            for msg in res['log']:
                CS.msgs.append(msg)

            CS.log_updated = True

        # Update monsters
        if 'm' in res:
            for oid, m_str in res['m'].iteritems():
                if oid in ClientObject.obj_dict:
                    ClientObject.obj_dict[oid].update_from_string(m_str)
                else:
                    mon = ClientMonster.unserialize(m_str)
                    mon.place_on_map()

        # Delete monsters
        if 'm_del' in res:
            for oid, flags in res['m_del']:
                ClientObject.obj_dict[oid].delete(flags)

        # Update items
        if 'i' in res:
            for oid, i_str in res['i'].iteritems():
                if oid in ClientObject.obj_dict:
                    ClientObject.obj_dict[oid].update_from_string(i_str)
                else:
                    item = ClientItem.unserialize(i_str)
                    item.place_on_map()

        # Delete items
        if 'i_del' in res:
            for oid, flags in res['i_del']:
                ClientObject.obj_dict[oid].delete(flags)

        # Update the player object
        if 'u' in res:
            if CS.u is not None:
                CS.u.update_from_string(res['u'])
            else:
                CS.u = ClientPlayer.unserialize(res['u'])

            # If we're changing dungeon levels, the player needs a new FOV map
            if new_dlevel:
                CS.u.set_fov_map(CS.map.grid)

            CS.u.fov_map.do_fov(CS.u.x, CS.u.y, CS.u.fov_radius)
            gui.center_map()

        res = Network.get_response()


def client_tick():
    """
    Called from the main game loop to handle client functionality.
    Handle server responses, player input, and updating the client gui.
    """

    # If there are any server responses, handle them.
    handle_responses()

    if CS.mode != cfg.ST_PLAYBACK:
        CS.clock.tick(cfg.FRAME_RATE)
        handle_events()

    gui.update_gui()
