"""Routines for calculating field of view (FOV).
Based on Bjorn Bergstrom's recursive shadowcasting algorithm
(http://roguebasin.roguelikedevelopment.org/index.php?title=FOV_using_recursive_shadowcasting)"""

class FOVMap(object):
    # Multipliers for transforming coordinates to other octants:
    mult = [
                [1,  0,  0, -1, -1,  0,  0,  1],
                [0,  1, -1,  0,  0, -1,  1,  0],
                [0,  1,  1,  0,  0, -1, -1,  0],
                [1,  0,  0,  1, -1,  0,  0, -1]
            ]
    def __init__(self, map):
        self.data = map
        self.w, self.h = len(map), len(map[0])
        self.light = []
        for i in range(self.w):
            self.light.append([0] * self.h)
        self.flag = 1

    def square(self, x, y):
        return self.data[x][y]

    def blocked(self, x, y):
        return (x < 0 or y < 0
                or x >= self.w or y >= self.h
                or self.data[x][y].block_sight)

    def lit(self, x, y):
        return self.light[x][y] == self.flag

    def set_lit(self, x, y):
        if 0 <= x < self.w and 0 <= y < self.h:
            self.light[x][y] = self.flag

    def _cast_light(self, cx, cy, row, start, end, radius, xx, xy, yx, yy, id):
        """Recursive lightcasting function"""
        if start < end:
            return
        radius_squared = radius * radius

        for j in range(row, radius+1):
            dx, dy = -j - 1, -j
            blocked = False

            while dx <= 0:
                dx += 1
                # Translate the dx, dy coordinates into map coordinates:
                X, Y = cx + dx * xx + dy * xy, cy + dx * yx + dy * yy
                # l_slope and r_slope store the slopes of the left and right
                # extremities of the square we're considering:
                l_slope, r_slope = (dx - 0.5) / (dy + 0.5), (dx + 0.5) / (dy - 0.5)
                if start < r_slope:
                    continue
                elif end > l_slope:
                    break
                else:
                    # Our light beam is touching this square; light it:
                    if dx * dx + dy * dy < radius_squared:
                        self.set_lit(X, Y)
                    if blocked:
                        # we're scanning a row of blocked squares:
                        if self.blocked(X, Y):
                            new_start = r_slope
                            continue
                        else:
                            blocked = False
                            start = new_start
                    else:
                        if self.blocked(X, Y) and j < radius:
                            # This is a blocking square, start a child scan:
                            blocked = True
                            self._cast_light(cx, cy, j + 1, start, l_slope,
                                             radius, xx, xy, yx, yy, id + 1)
                            new_start = r_slope
            # Row is scanned; do next row unless last square was blocked:
            if blocked:
                break

    def do_fov(self, x, y, radius):
        """Calculate lit squares from the given location and radius"""
        self.flag += 1
        for oct in range(8):
            self._cast_light(x, y, 1, 1.0, 0.0, radius,
                             self.mult[0][oct], self.mult[1][oct],
                             self.mult[2][oct], self.mult[3][oct], 0)
        # This is necessary because the algorithm doesn't recognise the
        # starting square as being in the FOV.
        self.set_lit(x, y)
        
