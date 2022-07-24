from antlr4 import *
from mpl_toolkits.axisartist.axes_grid import ImageGrid

from cognilang.CogniLangParser import CogniLangParser
from cognilang.CogniLangLexer import CogniLangLexer
from cognilang.CogniLangListener import CogniLangListener
from cognilang.CogniLangVisitor import CogniLangVisitor
from cognitive.format.hypergraph.channels.tensor_channel import CognitiveArbiter, CognitiveChannel, TensorCognitiveIcon, \
    HypergraphTensorTransformation

from cognitive.format.hypergraph.lang.mapping.cogni_lang_mapping import load_from_description
from cognitive.format.hypergraph.lang.mapping.graphviz_mapping import create_graph_view

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

from cognitive.format.hypergraph.laplacian.graph_tensor_operations import graph_upper_bound_entropy_vector


def main():
    # TODO: ambient description (very-very important, by this point it would be awesome)
    sys, channel = load_from_description("examples/example_robotcar.cogni")
    create_graph_view(sys)
    arbiter = CognitiveArbiter(name="sys", timestamp=0)
    channel = CognitiveChannel("channel_01", 0, arbiter)
    view_icon = TensorCognitiveIcon("out", 0)
    ch = HypergraphTensorTransformation("dendrite1", 0, arbiter.domain, channel, view_icon)
    channel.add_connection(ch, 0, view_icon)
    tensor = ch.encode([sys])
    print(sys.subset_elements)
    print(graph_upper_bound_entropy_vector(tensor))

    fig = plt.figure()
    #ax = Axes3D(fig)
    #img = ax.scatter(tensor[:], tensor[:])
    grid = ImageGrid(fig, 111, nrows_ncols=(3,3))
    for ax, im in zip(grid, tensor):
        ax.imshow(im)
    plt.show()


if __name__ == "__main__":
    main()
