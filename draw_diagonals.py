import random
from artist_class import Artist


class DiagonalArtist(Artist):

    def __init__(self):
        super().__init__()
        self.inputs["resolution"] = {
            "name": "Resolution",
            "type": "int",
            "min": 5,
            "max": 100,
            "default": 10
        }
        self.inputs["thickness"] = {
            "name": "Thickness",
            "type": "int",
            "min": 1,
            "max": 10,
            "default": 2
        }
        self.inputs["colour-single"] = {
            "name": "Colour",
            "type": "color"
        }

    def RunInputs(self, size, **kwargs):

        resolution = int(kwargs["Resolution"])
        thickness = int(kwargs["Thickness"])
        colour_single = kwargs["Colour"]

        header = (
            f'<svg xmlns="http://www.w3.org/2000/svg"'
            f' viewBox="0 0 {size} {size}">'
            )

        step = size // resolution
        # write the header for the file
        output = header + '\n'
        # loop through
        for row in range(0, size, step):
            for col in range(0, size, step):
                # choose a random direction for the diagonal line
                if random.choice([0, 1]) == 0:
                    # write the line
                    output += self.draw_diagonal(
                        col, row, col + step, row + step,
                        colour_single, thickness
                        ) + '\n'
                else:
                    # write the line
                    output += self.draw_diagonal(
                        col + step, row, col, row + step,
                        colour_single, thickness
                        ) + '\n'
        # write the footer
        footer = f'</svg>'
        output += footer
        self.SVGoutput = output
        return self.ReturnSVG()

    def draw_diagonal(self, x, y, x2, y2, color, thickness):
        # format a line for svg
        return (
            f'<line x1="{x}" y1="{y}" x2="{x2}" y2="{y2}"'
            f' stroke="{color}" stroke-width="{thickness}" />'
                )


if __name__ == "__main__":
    artist = DiagonalArtist()
    artist.RunInputs(100, 50, 2, "red")
