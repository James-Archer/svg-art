import random
from artist_class import Artist

rand_colors = [1,  0]
colors = {
    0: 'black',
    1: 'white'
    }


def draw_circle(x, y, width, height, color='black'):
    r = height / 2
    cx = x + r
    cy = y + r
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{color}" stroke-width="0"/>'


def make_circle_tiles(size, tiles, image_size):
    # size is number of sections per tile, tiles is number of tiles, image_size is
    # how big the image is in pixels
    header = f'<svg viewBox="0 0 {image_size} {image_size}" xmlns="http://www.w3.org/2000/svg">\n'
    print(header)


class SquaresArtist(Artist):

    def __init__(self):
        super().__init__()
        self.inputs["colour-single"] = {
            "name": "Colour",
            "type": "color",
            "default": "#000047"
        }
        self.inputs["dots"] = {
            "name": "Dots",
            "type": "int",
            "min": 3,
            "max": 25,
            "default": 17
        }
        self.inputs["tiles"] = {
            "name": "Tiles",
            "type": "int",
            "min": 1,
            "max": 7,
            "default": 3
        }

    def create_tile(self, size):
        mosaic = []
        # only do the first n//2 rows (treating the first n//2 cols first)
        for r in range(size // 2 + 1):
            temp_row = []
            # needed to flip black and white circles
            was_black = 0
            for c in range(size // 2 + 1):
                # if on the horizontal or vertical centre or on the diagonal
                # try not to make it too heavy on the black
                if was_black > 2:
                    temp_row.append(1)
                    was_black = 0
                    continue
                # otherwise
                if r == c or c == size // 2 + 1 or r == size // 2 + 1 or r < c:
                    col = random.choice(self.rand_colors)
                    temp_row.append(col)
                    if col == 0:
                        was_black += 1
                    else:
                        was_black = 0
                # bottom of diag
                elif r > c:
                    temp_row.append(mosaic[c][r])
            for c in range(size // 2, -1, -1):
                temp_row.append(temp_row[c])
            mosaic.append(temp_row)
        for r in range(size // 2, -1, -1):
            mosaic.append(mosaic[r])
        return mosaic

    def RunInputs(self, size, **kwargs):

        points = int(kwargs["Dots"])
        tiles = int(kwargs["Tiles"])
        colour = kwargs["Colour"]

        self.rand_colors = [1,  0]
        self.colors = {
            0: colour,
            1: 'white'
            }

        output = f'<svg viewBox="0 0 {size} {size}" xmlns="http://www.w3.org/2000/svg">\n'
        tile_size = size / tiles
        padding = 40
        for x in range(tiles):
            for y in range(tiles):
                top_left_x = x * tile_size + padding / 2
                top_left_y = y * tile_size + padding / 2
                bottom_right_x = top_left_x + tile_size - padding
                square_size = (bottom_right_x - top_left_x) / points
                tile = self.create_tile(points)
                for r in range(len(tile)):
                    for c in range(len(tile)):
                        col = tile[r][c]
                        top_left_x_tile = c * square_size + top_left_x
                        top_left_y_tile = r * square_size + top_left_y

                        line = draw_circle(
                            top_left_x_tile,
                            top_left_y_tile,
                            square_size,
                            square_size,
                            self.colors[col])

                        output += line
        output += f'</svg>'
        self.SVGoutput = output
        return self.ReturnSVG()
