'''
    This file is part of Prolothar-Common (More Info: https://github.com/shs-it/prolothar-common).

    Prolothar-Common is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Prolothar-Common is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Prolothar-Common. If not, see <https://www.gnu.org/licenses/>.
'''
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
        display(SVG(graph._repr_image_svg_xml()))

    return graph.source