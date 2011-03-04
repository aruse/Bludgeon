import math

import pygame
from pygame.locals import *


class ScrollBar():
    white = (255, 255, 255)
    black = (0, 0, 0)
    dark_gray = (63, 63, 63)
    gray = (128, 128, 128)
    medium_light_gray = (160, 160, 160)
    light_gray = (191, 191, 191)
    lighter_gray = (220, 220, 220)

    def __init__(self, thickness, axis, surf_rect, display_rect):
        """axis can be 0 for the x-axis or 1 for the y-axis"""

        self.thickness = thickness
        self.axis = axis
        self.surf_rect = surf_rect
        self.display_rect = display_rect

        # We may be resizing the display rect, so we need to keep track of 
        # the original dimensions in case we need to restore them.
        self.orig_display_rect = display_rect.copy()

        self.scrolling = False

        # Whether or not the slider is clicked
        self.clicked = False

        # Whether or not the mouse is hovering over the slider
        self.hover = False

        self.resize()

    def resize(self):
        if self.axis == 0:
            self.ratio = float(self.display_rect.w) / self.surf_rect.w
            self.track = pygame.Rect(self.display_rect.x,
                                     self.display_rect.bottom,
                                     self.display_rect.w,
                                     self.thickness)
            self.slider = pygame.Rect(self.track)
            self.slider.w = self.track.w * min(1, self.ratio)

        elif self.axis == 1:
            self.ratio = float(self.display_rect.h) / self.surf_rect.h
            self.track = pygame.Rect(self.display_rect.right,
                                     self.display_rect.y,
                                     self.thickness,
                                     self.display_rect.h)
            self.slider = pygame.Rect(self.track)
            self.slider.h = self.track.h * min(1, self.ratio)

    def update(self, event):
        """Called by user with mouse events."""
        if event is None:
            return

        a = self.axis
        
        if event.type == MOUSEBUTTONDOWN:
            if self.slider.collidepoint(event.pos):
                self.clicked = True

                if self.ratio < 1:
                    self.scrolling = True

            elif self.track.collidepoint(event.pos):
                if a == 0:
                    if event.pos[a] > self.slider.bottomright[a]:
                        move = self.slider.w
                    elif event.pos[a] < self.slider.topleft[a]:
                        move = -self.slider.w

                    move = max(move, self.track.topleft[a] \
                                   - self.slider.topleft[a])
                    move = min(move, self.track.bottomright[a] \
                                   - self.slider.bottomright[a])
                    self.slider.move_ip((move, 0))
                elif a == 1:
                    if event.pos[a] > self.slider.bottomright[a]:
                        move = self.slider.h
                    elif event.pos[a] < self.slider.topleft[a]:
                        move = -self.slider.h

                    move = max(move, self.track.topleft[a] \
                                   - self.slider.topleft[a])
                    move = min(move, self.track.bottomright[a] \
                                   - self.slider.bottomright[a])
                    self.slider.move_ip((0, move))

                self.move_surf()


        elif event.type == MOUSEBUTTONUP:
            self.clicked = False
            self.scrolling = False

        elif event.type == MOUSEMOTION:
            if self.scrolling and event.rel[a] != 0:
                move = max(event.rel[a], self.track.topleft[a] 
                           - self.slider.topleft[a])
                move = min(move, self.track.bottomright[a] 
                           - self.slider.bottomright[a])
                        
                if move != 0:
                    if a == 0:
                        self.slider.move_ip((move, 0))
                    elif a == 1:
                        self.slider.move_ip((0, move))

                self.move_surf()

            if self.slider.collidepoint(event.pos):
                self.hover = True
            else:
                self.hover = False


    def move_surf(self):
        """Align the surface location according to the position of the
        slider.
        """
        if self.axis == 0:
            self.surf_rect.x = (
                (self.slider.x - self.display_rect.x) / self.ratio) * -1 \
                + self.display_rect.x
        elif self.axis == 1:
            self.surf_rect.y = (
                (self.slider.y - self.display_rect.y) / self.ratio) * -1 \
                + self.display_rect.y


    def draw(self, surf):
        """Render the scrollbar, but only if it's needed."""
        # The track
        pygame.draw.rect(surf, ScrollBar.gray, self.track, 0)

        slider_color = None

        if self.hover:
            slider_color = ScrollBar.lighter_gray

        if self.clicked or self.scrolling:
            slider_color = ScrollBar.dark_gray

        if slider_color is None:
            slider_color = ScrollBar.light_gray

        # The slider
        pygame.draw.rect(surf, slider_color,
                         (self.slider.x + 2,
                          self.slider.y + 2,
                          self.slider.w - 4,
                          self.slider.h - 4), 0)

        # The top and left of the slider
        pygame.draw.lines(surf, ScrollBar.white, False,
                          ((self.slider.x + 1,
                            self.slider.y + self.slider.h - 2),
                           (self.slider.x + 1, self.slider.y + 1),
                           (self.slider.x + self.slider.w - 2,
                            self.slider.y + 1)
                           ), 1)

        # The bottom and right of the slider
        pygame.draw.lines(surf, ScrollBar.black, False,
                          ((self.slider.x + self.slider.w - 2,
                            self.slider.y + 1),
                           (self.slider.x + self.slider.w - 2,
                            self.slider.y + self.slider.h - 2),
                           (self.slider.x + 1,
                            self.slider.y + self.slider.h - 2)
                           ), 1)

    def align(self):
        """Place the slider where it should be, according to the location
        of the surf_rect.
        """
        # math.ceil() needed to compensate for rounding errors causing the
        # bars to be off by one pixel.
        if self.axis == 0:
            self.slider.x = math.ceil(
                self.ratio * (self.surf_rect.x - self.display_rect.x) * -1
                + self.display_rect.x)

            if self.slider.x < self.display_rect.x:
                self.slider.x = self.display_rect.x

        elif self.axis == 1:
            self.slider.y = math.ceil(
                self.ratio * (self.surf_rect.y - self.display_rect.y) * -1
                + self.display_rect.y)

            if self.slider.y < self.display_rect.y:
                self.slider.y = self.display_rect.y

class ScrollView():
    """Implements a scrollable area with scrollbars that appear if the
    surface is larger than the view.
    """
    pass
