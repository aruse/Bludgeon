import math

import pygame
from pygame.locals import *

# Mouse buttons
BUTTON_L = 1
BUTTON_M = 2
BUTTON_R = 3
BUTTON_SCROLL_U = 4
BUTTON_SCROLL_D = 5


class ScrollBar():
    # Colors
    white = [255] * 3
    black = [0] * 3

    track_bg = white
    track_fg = [205] * 3

    slider_normal = [64] * 3
    slider_hover = [127] * 3
    slider_clicked = [32] * 3

    arrow_inactive = track_fg
    arrow_active = slider_normal

    # The length in pixels of the area off the end of the track where
    # the arrows are drawn.
    arrow_size = 16

    # Pixels to scroll with each wheel movement
    wheel_scroll_amt = 10

    def __init__(self, thickness, axis,
                 surf_rect, display_rect, always_show=True):
        """axis can be 0 for the x-axis or 1 for the y-axis"""

        self.thickness = thickness
        self.axis = axis
        self.surf_rect = surf_rect
        self.display_rect = display_rect

        # Rect defining the track in which the slider moves
        self.track = None
        # Rect defining the slider
        self.slider = None
        # Two Rects defining the arrows
        self.arrows = [None] * 2

        self.arrow_scroll_amount = 0

        # We may be resizing the display rect, so we need to keep track of 
        # the original dimensions in case we need to restore them.
        self.orig_display_rect = display_rect.copy()

        self.scrolling = False

        # Whether or not the slider is clicked
        self.clicked = False

        # Whether or not the mouse is hovering over the slider
        self.hover = False

        self.always_show = always_show
        self.shown = always_show

        # Ratio of the display size over the surface size
        self.surf_ratio = None

        # Ratio of the track size over the display size
        self.track_ratio = None
        
        self.resize()

    def resize(self):
        if self.axis == 0:
            self.surf_ratio = float(self.display_rect.w) / self.surf_rect.w
            self.track = pygame.Rect(
                self.display_rect.x + ScrollBar.arrow_size,
                self.display_rect.bottom,
                self.display_rect.w - ScrollBar.arrow_size * 2,
                self.thickness)
            self.arrows[0] = pygame.Rect(
                self.track.x - ScrollBar.arrow_size,
                self.track.y,
                ScrollBar.arrow_size,
                self.track.h)
            self.arrows[1] = pygame.Rect(
                self.track.x + self.track.w,
                self.track.y,
                ScrollBar.arrow_size,
                self.track.h)
            self.slider = pygame.Rect(self.track)
            self.slider.w = self.track.w * min(1, self.surf_ratio)
            self.track_ratio = float(self.track.w) / self.display_rect.w

        elif self.axis == 1:
            self.surf_ratio = float(self.display_rect.h) / self.surf_rect.h
            self.track = pygame.Rect(
                self.display_rect.right,
                self.display_rect.y + ScrollBar.arrow_size,
                self.thickness,
                self.display_rect.h - ScrollBar.arrow_size * 2)
            self.arrows[0] = pygame.Rect(
                self.track.x,
                self.track.y - ScrollBar.arrow_size,
                self.track.w,
                ScrollBar.arrow_size)
            self.arrows[1] = pygame.Rect(
                self.track.x,
                self.track.y + self.track.h,
                self.track.w,
                ScrollBar.arrow_size)
            self.slider = pygame.Rect(self.track)
            self.slider.h = self.track.h * min(1, self.surf_ratio)
            self.track_ratio = float(self.track.h) / self.display_rect.h

        if self.always_show is False:
            if self.surf_ratio < 1:
                self.shown = True
            else:
                self.shown = False

    def handle_event(self, event):
        """Handle mouse events.  Called by invoking program."""
        if event is None:
            return

        a = self.axis
        
        if event.type == MOUSEBUTTONDOWN:
            if self.slider.collidepoint(event.pos):
                self.clicked = True

                if self.surf_ratio < 1:
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

            elif self.arrows[0].collidepoint(event.pos):
                self.arrow_scroll_amount = -1

            elif self.arrows[1].collidepoint(event.pos):
                self.arrow_scroll_amount = 1

            # Handle scroll wheel
            if (self.axis == 1
                and (self.track.collidepoint(event.pos)
                     or self.display_rect.collidepoint(event.pos))):
                if event.button == BUTTON_SCROLL_U:
                    self._move_slider(-ScrollBar.wheel_scroll_amt)
                elif event.button == BUTTON_SCROLL_D:
                    self._move_slider(ScrollBar.wheel_scroll_amt)
                
                self.move_surf()

        elif event.type == MOUSEBUTTONUP:
            self.clicked = False
            self.scrolling = False
            self.arrow_scroll_amount = 0

        elif event.type == MOUSEMOTION:
            if self.scrolling and event.rel[a] != 0:
                # This keeps the mouse from activating the slider if you 
                # click and then move outside of the display_rect.
                if (event.pos[a] > self.display_rect.topleft[a]
                    and event.pos[a] < self.display_rect.bottomright[a]):

                    self._move_slider(event.rel[a])
                    self.move_surf()

            if self.slider.collidepoint(event.pos):
                self.hover = True
            else:
                self.hover = False

                                
    def _move_slider(self, d):
        """Move the slider by d amount."""
        a = self.axis
        move = max(d, self.track.topleft[a] 
                   - self.slider.topleft[a])
        move = min(move, self.track.bottomright[a] 
                   - self.slider.bottomright[a])
                        
        if move != 0:
            if a == 0:
                self.slider.move_ip((move, 0))
            elif a == 1:
                self.slider.move_ip((0, move))

    def update(self, surf):
        """Handle arrow scrolling and then draw the scrollbar. Needs to be
        called once per game loop iteration.
        """
        self.arrow_scroll()
        self.draw(surf)

    def arrow_scroll(self):
        """Scrolls while the arrows are clicked."""
        if self.arrow_scroll_amount != 0:
            self._move_slider(self.arrow_scroll_amount)
            self.move_surf()

    def move_surf(self):
        """Align the surface location according to the position of the
        slider.
        """
        if self.axis == 0:
            self.surf_rect.x = (
                (self.track.x - self.slider.x)
                / self.surf_ratio) / self.track_ratio \
                + self.display_rect.x

            # Compensate for rounding errors
            if self.surf_rect.right < self.display_rect.right:
                self.surf_rect.right = self.display_rect.right

        elif self.axis == 1:
            self.surf_rect.y = (
                (self.track.y - self.slider.y)
                / self.surf_ratio) / self.track_ratio \
                + self.display_rect.y

            # Compensate for rounding errors
            if self.surf_rect.bottom < self.display_rect.bottom:
                self.surf_rect.bottom = self.display_rect.bottom


    def align(self):
        """Place the slider where it should be, according to the location
        of the surf_rect.
        """
        # math.ceil() needed to compensate for rounding errors causing the
        # bars to be off by one pixel.
        if self.axis == 0:
            self.slider.x = math.ceil(
                self.track_ratio * self.surf_ratio
                * (self.display_rect.x - self.surf_rect.x)
                + self.track.x)

            if self.slider.x < self.display_rect.x:
                self.slider.x = self.display_rect.x

        elif self.axis == 1:
            self.slider.y = math.ceil(
                self.track_ratio * self.surf_ratio
                * (self.display_rect.y - self.surf_rect.y)
                + self.track.y)

            if self.slider.y < self.display_rect.y:
                self.slider.y = self.display_rect.y

    def draw(self, surf):
        """Render the scrollbar."""
        if self.shown is False:
            return

        # Some abbreviateions so the code doesn't take up so much visual space.
        ar = ScrollBar.arrow_size
        th = self.thickness

        if self.axis == 0:
            # The horizontal track
            pygame.draw.rect(surf, ScrollBar.track_bg,
                             (self.track.x - ar * 0.5,
                              self.track.y,
                              self.track.w + ar,
                              self.track.h), 0)
            pygame.draw.rect(surf, ScrollBar.track_fg,
                             (self.track.x + ar * 0.5,
                              self.track.y + 2,
                              self.track.w - ar,
                              self.track.h - 4), 0)

            # The left arrow
            pygame.draw.circle(surf, ScrollBar.track_bg,
                               (self.track.x - int(ar * 0.5),
                                self.track.y + int(th * 0.5)),
                               int(th * 0.5), 0)
            pygame.draw.circle(surf, ScrollBar.track_fg,
                               (self.track.x + int(ar * 0.5),
                                self.track.y + int(th * 0.5)),
                               int(th * 0.4), 0)
            points = ((self.track.x - 4, self.track.y + 4),
                      (self.track.x - ar + 4,
                       self.track.y + self.track.h / 2),
                      (self.track.x - 4,
                       self.track.y + self.track.h - 4))
            if self.slider.x == self.track.x:
                arrow_color = ScrollBar.arrow_inactive
            else:
                arrow_color = ScrollBar.arrow_active

            pygame.draw.polygon(surf, arrow_color, points, 0)

            # The right arrow
            pygame.draw.circle(surf, ScrollBar.track_bg,
                               (self.track.x + self.track.w + int(ar * 0.5),
                                self.track.y + int(th * 0.5)),
                               int(th * 0.5), 0)
            pygame.draw.circle(surf, ScrollBar.track_fg,
                               (self.track.x + self.track.w - int(ar * 0.5),
                                self.track.y + int(th * 0.5)),
                               int(th * 0.4), 0)
            points = ((self.track.x + self.track.w + 4, self.track.y + 4),
                      (self.track.x + self.track.w + ar - 4,
                       self.track.y + self.track.h / 2),
                      (self.track.x + self.track.w + 4,
                       self.track.y + self.track.h - 4))
            if self.slider.right == self.track.right:
                arrow_color = ScrollBar.arrow_inactive
            else:
                arrow_color = ScrollBar.arrow_active

            pygame.draw.polygon(surf, arrow_color, points, 0)

        elif self.axis == 1:
            # The vertical track
            pygame.draw.rect(surf, ScrollBar.track_bg,
                             (self.track.x,
                              self.track.y - ar * 0.5,
                              self.track.w,
                              self.track.h + ar), 0)
            pygame.draw.rect(surf, ScrollBar.track_fg,
                             (self.track.x + 2,
                              self.track.y + ar * 0.5,
                              self.track.w - 4,
                              self.track.h - ar), 0)

            # The up arrow
            pygame.draw.circle(surf, ScrollBar.track_bg,
                               (self.track.x + int(th * 0.5),
                                self.track.y - int(ar * 0.5)),
                               int(th * 0.5), 0)
            pygame.draw.circle(surf, ScrollBar.track_fg,
                               (self.track.x + int(th * 0.5),
                                self.track.y + int(ar * 0.5)),
                               int(th * 0.4), 0)
            points = ((self.track.x + 4, self.track.y - 4),
                      (self.track.x + self.track.w / 2,
                       self.track.y - ar + 4),
                      (self.track.x + self.track.w - 4,
                       self.track.y - 4))
            if self.slider.y == self.track.y:
                arrow_color = ScrollBar.arrow_inactive
            else:
                arrow_color = ScrollBar.arrow_active

            pygame.draw.polygon(surf, arrow_color, points, 0)

            # The down arrow
            pygame.draw.circle(surf, ScrollBar.track_bg,
                               (self.track.x + int(th * 0.5),
                                self.track.y + self.track.h + int(ar * 0.5)),
                               int(th * 0.5), 0)
            pygame.draw.circle(surf, ScrollBar.track_fg,
                               (self.track.x + int(th * 0.5),
                                self.track.y + self.track.h - int(ar * 0.5)),
                               int(th * 0.4), 0)
            points = ((self.track.x + 4, self.track.y + self.track.h + 4),
                      (self.track.x + self.track.w - 4,
                       self.track.y + self.track.h  + 4),
                      (self.track.x + self.track.w / 2,
                       self.track.y + self.track.h + ar - 4))
            if self.slider.bottom == self.track.bottom:
                arrow_color = ScrollBar.arrow_inactive
            else:
                arrow_color = ScrollBar.arrow_active

            pygame.draw.polygon(surf, arrow_color, points, 0)

        slider_color = ScrollBar.slider_normal

        if self.hover:
            slider_color = ScrollBar.slider_hover

        if self.clicked or self.scrolling:
            slider_color = ScrollBar.slider_clicked

        # The slider
        if self.axis == 0:
            pygame.draw.rect(surf, slider_color,
                             (self.slider.x + int(th * 0.5),
                              self.slider.y + 2,
                              self.slider.w - th,
                              self.slider.h - 4), 0)
            pygame.draw.circle(surf, slider_color,
                               (self.slider.x + int(th * 0.5),
                                self.slider.y + int(th * 0.5)),
                               int(th * 0.4), 0)
            pygame.draw.circle(surf, slider_color,
                               (self.slider.x + self.slider.w - int(th * 0.5),
                                self.slider.y + int(th * 0.5)),
                               int(th * 0.4), 0)
        elif self.axis == 1:
            pygame.draw.rect(surf, slider_color,
                             (self.slider.x + 2,
                              self.slider.y + int(th * 0.5),
                              self.slider.w - 4,
                              self.slider.h - th), 0)
            pygame.draw.circle(surf, slider_color,
                               (self.slider.x + int(th * 0.5),
                                self.slider.y + int(th * 0.5)),
                               int(th * 0.4), 0)
            pygame.draw.circle(surf, slider_color,
                               (self.slider.x + int(th * 0.5),
                                self.slider.y + self.slider.h - int(th * 0.5)),
                               int(th * 0.4), 0)

        # The highlight on the top and left
#        pygame.draw.lines(surf, ScrollBar.white, False,
#                          ((self.slider.x + 1,
#                            self.slider.y + self.slider.h - 2),
#                           (self.slider.x + 1, self.slider.y + 1),
#                           (self.slider.x + self.slider.w - 2,
#                            self.slider.y + 1)
#                           ), 1)

        # The shadow on the bottom and right
#        pygame.draw.lines(surf, ScrollBar.black, False,
#                          ((self.slider.x + self.slider.w - 2,
#                            self.slider.y + 1),
#                           (self.slider.x + self.slider.w - 2,
#                            self.slider.y + self.slider.h - 2),
#                           (self.slider.x + 1,
#                            self.slider.y + self.slider.h - 2)
#                           ), 1)



class ScrollView():
    """Implements a scrollable area with scrollbars that appear if the
    surface is larger than the view.
    """
    pass
