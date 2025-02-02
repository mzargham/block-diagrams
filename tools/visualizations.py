import graphviz

def generate_block_diagram(block_diagram, output_filename=None):
    """
    Generates a Graphviz block diagram from a JSON block diagram model.
    
    Processors are drawn as rectangles, with their input ports (circles) on the left
    and output terminals (triangles) on the right. Wires are drawn as orthogonal
    (right-angle) straight lines. Colors are applied based on the parent spaces.
    
    Args:
        block_diagram (dict): The block diagram model.
        output_filename (str): Base name for the output file (PNG). If None,
                               the diagram is not rendered to file.
    
    Returns:
        graphviz.Digraph: The generated graph.
    """
    
    # --- Define Color Mappings ---
    processor_colors = {
        "F": "lightblue",    # e.g., Plant
        "G": "lightcoral",   # e.g., Controller
        "S": "lightyellow"   # e.g., Sensor
    }
    # For signals (ports/terminals) by their name
    signal_colors = {
        "X": "blue",
        "Y": "red",
        "U": "green"
    }
    # For wires: use the wire's Parent attribute (e.g., "X", "U", "Y")
    wire_colors = {
        "X": "blue",
        "Y": "red",
        "U": "green"
    }
    
    # --- Create the Graphviz Digraph ---
    dot = graphviz.Digraph(format="png")
    dot.attr(rankdir="LR", splines="ortho")  # left-to-right, orthogonal (right-angle) edges

    # --- Create Processor, Port, and Terminal Nodes ---
    for proc in block_diagram.get("processors", []):
        proc_id = proc["ID"]
        proc_name = proc.get("Name", proc_id)
        # Use the processor's Parent to choose a fillcolor (default to lightgray)
        fillcolor = processor_colors.get(proc.get("Parent"), "lightgray")
        
        # Create the central processor node (rectangle)
        dot.node(proc_id, label=proc_name, shape="box", style="filled", fillcolor=fillcolor)
        
        # Create input port nodes (assume Ports are inputs and will be on the left)
        for i, port in enumerate(proc.get("Ports", [])):
            port_id = f"{proc_id}_port_{i}"
            port_color = signal_colors.get(port, "white")
            dot.node(port_id, label=port, shape="circle", style="filled", fillcolor=port_color,
                     width="0.3", fixedsize="true")
            # Add an invisible edge from the port to the processor to force left alignment.
            dot.edge(port_id, proc_id, style="invis", weight="10")
            
        # Create output terminal nodes (assume Terminals are outputs and will be on the right)
        for i, term in enumerate(proc.get("Terminals", [])):
            term_id = f"{proc_id}_term_{i}"
            term_color = signal_colors.get(term, "white")
            # Using 'invtriangle' to draw a triangle.
            dot.node(term_id, label=term, shape="invtriangle", style="filled", fillcolor=term_color,
                     width="0.3", fixedsize="true")
            # Add an invisible edge from the processor to the terminal to force right alignment.
            dot.edge(proc_id, term_id, style="invis", weight="10")
    
    # --- Group Ports and Terminals in Subgraphs (to prevent overlapping) ---
    for proc in block_diagram.get("processors", []):
        proc_id = proc["ID"]
        # Group all port nodes for this processor on the same rank.
        with dot.subgraph() as s:
            s.attr(rank="same")
            for i, _ in enumerate(proc.get("Ports", [])):
                port_id = f"{proc_id}_port_{i}"
                s.node(port_id)
        # Similarly, group terminal nodes.
        with dot.subgraph() as s:
            s.attr(rank="same")
            for i, _ in enumerate(proc.get("Terminals", [])):
                term_id = f"{proc_id}_term_{i}"
                s.node(term_id)
    
    # --- Create Wire Edges ---
    # For this diagram, we assume that wires connect from a processor's terminal (output) to another processor's port (input).
    for wire in block_diagram.get("wires", []):
        # Interpret the JSON: Source refers to a processor's terminal index,
        # Destination refers to a processor's port index.
        src_proc, src_index = wire["Source"]
        dst_proc, dst_index = wire["Destination"]
        src_node = f"{src_proc}_term_{src_index}"
        dst_node = f"{dst_proc}_port_{dst_index}"
        label = wire.get("Name", "")
        style = "dashed" if "Feedback" in label else "solid"
        edge_color = wire_colors.get(wire.get("Parent"), "black")
        dot.edge(src_node, dst_node, label=label, style=style, color=edge_color)
    
    # --- Render (if a filename is provided) and Return the Graph ---
    if output_filename is not None:
        dot.render(output_filename, cleanup=True)
        print(f"Block diagram saved as {output_filename}.png")
    
    return dot


# =====================================================
# Example Usage (can be run in a Jupyter Notebook)
# =====================================================

# Example block diagram JSON. Note that for this new drawing we assume:
#   - "Ports" are inputs (left side) and "Terminals" are outputs (right side).
#   - In each wire, "Source" is given as [processor_id, terminal_index]
#     and "Destination" is given as [processor_id, port_index].
block_diagram = {
    "processors": [
        {
            "ID": "f",
            "Parent": "F",
            "Name": "Plant",
            "Ports": ["X", "U"],      # input ports
            "Terminals": ["X"]        # output terminals
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
        # Feedback: from Plant's output ("X") to its input ("X")
        {"ID": "wrefX1", "Parent": "X", "Name": "State Feedback", "Source": ["f", 0], "Destination": ["f", 0]},
        # Action: from Controller's output ("U") to Plant's input ("U")
        {"ID": "wrefU1", "Parent": "U", "Name": "Action",         "Source": ["g", 0], "Destination": ["f", 1]},
        # Observation: from Sensor's output ("Y") to Controller's input ("Y")
        {"ID": "wrefY1", "Parent": "Y", "Name": "Observation",    "Source": ["s", 0], "Destination": ["g", 0]}
    ]
}

# In a Jupyter Notebook you can simply display the returned Digraph:
diagram = generate_block_diagram(block_diagram)
diagram  # This will display the diagram inline
