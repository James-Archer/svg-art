class Artist():

        def __init__(self):
                self.inputs = {}
                self.SVGoutput = ''

        def GetInputs(self):
                return None

        def ReturnSVG(self):
                return self.SVGoutput

        def RunInputs(self, **kwargs):
                # generate SVG stuff
                self.ReturnSVG()
