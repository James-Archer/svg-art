import random
from artist_class import Artist


class Quadrilateral:
    def __init__(self, x1, x2, y1, y2, col):
        '''
        Attributes:
        self.xTL x value of the top left
        self.xBL x value of the bottom left
        self.xTR x value of the top right
        self.xBR x value of the bottom right
        self.yTL y value of the top left
        self.yTR y value of the bottom left
        self.yBL y value of the top right
        self.yBR y value of the bottom right
        self.col color
        '''
        self.xTL = x1
        self.xBL = x1
        self.xTR = x2
        self.xBR = x2
        self.yTL = y1
        self.yTR = y1
        self.yBL = y2
        self.yBR = y2
        self.col = col


class RectangleArtist(Artist):

    def __init__(self):
        super().__init__()
        self.inputs["resolution"] = {
            "name": "Resolution",
            "type": "int",
            "min": 2,
            "max": 20,
            "default": 6
        }

    def draw_quad(self, quad):
    ##    M = moveto
    ##    L = lineto
        return f'<path d="M{quad.xTL} {quad.yTL} \
                L{quad.xTR} {quad.yTR} \
                L{quad.xBR} {quad.yBR} \
                L{quad.xBL} {quad.yBL}Z" stroke="black" fill="{quad.col}"/>'

    def RunInputs(self, size, **kwargs):
        
        resolution = int(kwargs["Resolution"])
        colors = ('#044BD9', '#0583F2', '#05AFF2', '#05DBF2', '#fa7f70')
        output = f'<svg viewBox="0 0 {size} {size}" xmlns="http://www.w3.org/2000/svg">\n'
        grid = {}
        quad_size = size/resolution
        for r in range(resolution):
            for c in range(resolution):
                q = None
                q = Quadrilateral(
                                c * quad_size, c * quad_size + quad_size, r * quad_size, 
                                r * quad_size + quad_size, random.choice(colors))
                grid[(r, c)] = q    

        #shifting stuff
        for r in range(1, resolution):
            for c in range(1, resolution):
                diffx = random.randint(0, quad_size // 2) - quad_size // 4                             
                diffy = random.randint(0, quad_size // 2) - quad_size // 4
                q = grid[(r, c)]
                qUpLeft = grid[(r - 1, c - 1)]
                qUp = grid[(r - 1, c)]
                qLeft = grid[(r, c - 1)]

                #update all 4 quads for the square I'm working with's top left
                q.xTL += diffx
                q.yTL += diffy
                qUpLeft.xBR += diffx
                qUpLeft.yBR += diffy
                qUp.xBL += diffx
                qUp.yBL += diffy
                qLeft.xTR += diffx
                qLeft.yTR += diffy
                output += self.draw_quad(qUpLeft)
            output += self.draw_quad(qUp)
            
        for c in range(resolution):
            q = grid[(r, c)]
            output += self.draw_quad(q)
        output += f'</svg>'
        self.SVGoutput = output
        return self.ReturnSVG()
