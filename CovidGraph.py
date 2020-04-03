"""
Created on Thu Apr  2 19:08:31 2020

@author: User
"""

from matplotlib import pyplot
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg

class CovidGraph:
    def __init__(self):
        self.fig=pyplot.Figure()
        self.canvas=FigureCanvasQTAgg(self.fig)
        self.bar=self.fig.add_subplot(111)
    def draw_bar_graph(self,x,y):
        self.bar.clear()
        self.bar.bar(x,y)
        self.canvas.draw()
    def return_cavas(self):
        return self.canvas
        

if __name__  == "__main__":
    graph=CovidGraph()
    graph.draw_bar_graph(range(0,10),range(0,10))
        