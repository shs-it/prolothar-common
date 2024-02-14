# -*- coding: utf-8 -*-

try:
    from IPython.display import SVG, display # type: ignore
    ipython_available = True
except ModuleNotFoundError:
    ipython_available = False

def plot_graph(graph, view=True, filepath=None, filetype='pdf',
               layout='dot') -> str:
    """plots the given gviz graph and returns the source of the graph
    
    Args:
        layout: default is dot. (dot, neato, circo)
    """
    graph.engine = layout
    if filepath is not None:
        graph.render(filepath, view=False, cleanup=True, format=filetype)
    if view:
        if not ipython_available:
            raise ModuleNotFoundError('IPython not available')
        display(SVG(graph._repr_svg_()))
    
    return graph.source    