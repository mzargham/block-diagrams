import json
import graphviz

# Example block diagram JSON
block_diagram = {
    "processors": [
        {
            "ID": "f",
            "Parent": "F",
            "Name": "Plant",
            "Ports": ["X", "U"],
            "Terminals": ["X"]
        },
        {
            "ID": "g",
            "Parent": "G",
            "Name": "Controller",
            "Ports": ["Y"],
            "Terminals": ["U"]
        },
        {
            "ID": "s",
            "Parent": "S",
            "Name": "Sensor",
            "Ports": ["X"],
            "Terminals": ["Y"]
        }
    ],
    "wires": [
        {
            "ID": "wrefX1",
            "Parent": "X",
            "Name": "State Feedback",
            "Source": ["f", 0],
            "Destination": ["f", 0]
        },
        {
            "ID": "wrefU1",
            "Parent": "U",
            "Name": "Action",
            "Source": ["g", 0],
            "Destination": ["f", 1]
        },
        {
            "ID": "wrefY1",
            "Parent": "Y",
            "Name": "Observation",
            "Source": ["s", 0],
            "Destination": ["g", 0]
        }
    ]
}

def generate_block_diagram(block_diagram, output_filename="block_diagram"):
    """Generates a Graphviz block diagram from a JSON block diagram model."""
    
    # Create Graphviz Digraph
    dot = graphviz.Digraph(format="png")
    dot.attr(rankdir="LR")  # Left to Right Layout

    # Define colors for different spaces (optional for clarity)
    space_colors = {
        "F": "lightblue",  # Plant
        "G": "lightcoral",  # Controller
        "S": "yellow",  # Sensor
    }

    # Add processors (blocks) with improved layout
    for processor in block_diagram["processors"]:
        block_id = processor["ID"]
        name = processor["Name"]
        ports = " | ".join(processor["Ports"]) if processor["Ports"] else "No Ports"
        terminals = " | ".join(processor["Terminals"]) if processor["Terminals"] else "No Terminals"

        # Define block label with ports at the top, name in the middle, and terminals at the bottom
        label = f"{{ {{ {ports} }} | {name} | {{ {terminals} }} }}"
        fillcolor = space_colors.get(processor["Parent"], "lightgray")  # Default color

        # Add processor node
        dot.node(block_id, label=label, shape="Mrecord", style="filled", fillcolor=fillcolor)

    # Add wires (connections)
    for wire in block_diagram["wires"]:
        src_block, _ = wire["Source"]
        dst_block, _ = wire["Destination"]
        label = wire["Name"]
        style = "dashed" if "Feedback" in label else "solid"  # Dashed lines for feedback

        # Draw the connection
        dot.edge(src_block, dst_block, label=label, style=style)

    # Render and save the diagram
    dot.render(output_filename)
    print(f"Block diagram saved as {output_filename}.png")

# Generate the block diagram
generate_block_diagram(block_diagram, "block_diagram_improved")
