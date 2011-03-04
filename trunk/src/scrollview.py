import pygame
from pygame.locals import *


class ScrollBar():
#class ScrollBar(pygame.sprite.DirtySprite):
#    """ Same interface as sprite.Group.
#    Get result of update() in pixels scrolled, from get_scrolled()
#    """

    white = (255, 255, 255)

    def __init__(self, thickness, axis, surf_rect, display_rect):
        """axis can be 0 for the x-axis or 1 for the y-axis"""

        self.thickness = thickness
        self.axis = axis
        self.surf_rect = surf_rect
        self.display_rect = display_rect
        self.scrolling = False

        self.resize()

    def resize(self):
        if self.axis == 0:
            self.scroll_ratio = float(self.display_rect.w) / self.surf_rect.w
            self.track = pygame.Rect(self.display_rect.x,
                                     self.display_rect.bottom - self.thickness,
                                     self.display_rect.w,
                                     self.thickness)
            self.slider = pygame.Rect(self.track)
            self.slider.w = self.track.w * self.scroll_ratio
        elif self.axis == 1:
            self.scroll_ratio = float(self.display_rect.h) / self.surf_rect.h
            self.track = pygame.Rect(self.display_rect.right - self.thickness,
                                     self.display_rect.y,
                                     self.thickness,
                                     self.display_rect.h)
            self.slider = pygame.Rect(self.track)
            self.slider.h = self.track.h * self.scroll_ratio

    def update(self, event):
        """Called by user with mouse events. Event must not be none."""
        a = self.axis
        
        if event.type == MOUSEBUTTONDOWN:
            if self.slider.collidepoint(event.pos):
                self.scrolling = True

        elif event.type == MOUSEBUTTONUP:
            if self.scrolling:
                self.scrolling = False

        elif (event.type == MOUSEMOTION and self.scrolling
              and event.rel[a] != 0):
            move = max(event.rel[a],
                       self.track.topleft[a] - self.slider.topleft[a])
            move = min(move,
                       self.track.bottomright[a] - self.slider.bottomright[a])
                        
            if a == 0:
                self.slider.move_ip((move, 0))
                self.surf_rect.x = (
                    self.slider.x / self.scroll_ratio) * -1
            elif a == 1:
                self.slider.move_ip((0, move))
                self.surf_rect.y = (
                    self.slider.y / self.scroll_ratio) * -1

    def draw(self, surf):
        pygame.draw.rect(surf, ScrollBar.white, self.track, 1)
        pygame.draw.rect(surf, ScrollBar.white, self.slider.inflate(-4,-4), 0)

    def align(self):
        if self.axis == 0:
            self.slider.x = self.surf_rect.x * self.scroll_ratio * -1
            print "aligning"
        elif self.axis == 1:
#            pass
            self.slider.y = self.surf_rect.y * self.scroll_ratio * -1 + 252*2


class ScrollView():
    """Implements a scrollable area with scrollbars that appear if the
    surface is larger than the view.
    """
    pass

