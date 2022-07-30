from mpl_toolkits.axisartist.axes_grid import ImageGrid

from rei.cognitive.channels.channel_base_definitions import CognitiveArbiter, CognitiveChannel
from rei.cognitive.channels.cognitive_dendrite import HypergraphTensorTransformation
from rei.cognitive.channels.cognitive_icons import TensorCognitiveIcon
from rei.presentation.graphviz.graphviz_mapping import create_graph_view

import matplotlib.pyplot as plt

from rei.cognitive.format.hypergraph.laplacian.graph_tensor_operations import graph_upper_bound_entropy_vector
from rei.simulation.sdf.sdf_generator import load_from_description


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
    grid = ImageGrid(fig, 111, nrows_ncols=(3,3))
    for ax, im in zip(grid, tensor):
        ax.imshow(im)
    plt.show()


if __name__ == "__main__":
    main()
