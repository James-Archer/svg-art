import random
import math
from artist_class import Artist


class CircleArtist(Artist):

    def __init__(self):
        super().__init__()
        self.inputs["resolution"] = {
            "name": "Resolution",
            "type": "int",
            "min": 1,
            "max": 10,
            "default": 3
        }
        self.inputs["colour-circle"] = {
                "name": "Circle Colour",
                "type": "color",
                "default": "#8f005d"
        }
        self.inputs["colour-lines"] = {
                "name": "Line Colour",
                "type": "color",
                "default": "#000000"
        }

    def RunInputs(self, size, **kwargs):

        resolution = int(kwargs["Resolution"]) * 2 - 1

        circle_colour = "black"#kwargs["Circle Colour"]
        line_colour = kwargs["Line Colour"]

        header = (
            f'<svg xmlns="http://www.w3.org/2000/svg"'
            f' viewBox="0 0 {size} {size}">'
            )
        # write the header for the file
        output = header + '\n'

        _radii = random.choices(range(2, 8), k=resolution)
        radii = [_radii[0]]
        for r in _radii[1:]:
            if len(radii)%2 == 0:
                radii.append(radii[-1] + r)
            else:
                radii.append(radii[-1] + 2*r)
        radii = [size/2 * i/radii[-1] for i in radii]
        tot = 0
        #[print(i) for i in radii]
        for radius_outer, radius_inner in zip(radii[1::2], radii[:-1][::2]):
            #print(radius_inner, radius_outer)
            angles = random.choices(range(0, 360), k=int(radius_outer))
            angles = [ang/180 * math.pi for ang in angles]
            for angle in angles:
                #print(angle)
                x1 = radius_inner * math.sin(angle) + size/2
                y1 = radius_inner * math.cos(angle) + size/2
                x2 = radius_outer * math.sin(angle) + size/2
                y2 = radius_outer * math.cos(angle) + size/2
                output += f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{line_colour}" />\n'
        for radius in radii:
            output += f'<circle cx="{size/2}" cy="{size/2}" r="{radius}" stroke="{circle_colour}" stroke-width="5" fill="none" />\n'
        # write the footer
        footer = f'</svg>'
        output += footer
        self.SVGoutput = output
        return self.ReturnSVG()

if __name__ == "__main__":

    C = CircleArtist()
    print(C.RunInputs(500, Resolution=3))
