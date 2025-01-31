#this is totally experimental gpt written code

def draw_block_diagram_improved():
    """Draws an improved structured block diagram with proper arrow direction and closed-loop indication."""
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.set_xlim(-1, 5)
    ax.set_ylim(-1, 3)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.axis("off")

    # Draw block (Processor "f")
    block = patches.Rectangle((2, 1), 2, 1, edgecolor="black", facecolor="lightblue", lw=2)
    ax.add_patch(block)
    ax.text(3, 1.5, "Dynamics (f)", ha="center", va="center", fontsize=12, fontweight="bold")

    # Draw ports and terminals
    # Ports (Inputs on left)
    ax.plot(1.8, 1.7, "ko", markersize=6)  # Input Port "U"
    ax.text(1.5, 1.7, "U", ha="right", va="center", fontsize=12)

    ax.plot(1.8, 1.3, "ko", markersize=6)  # Input Port "X"
    ax.text(1.5, 1.3, "X", ha="right", va="center", fontsize=12)

    # Terminals (Outputs on right)
    ax.plot(4.2, 1.5, "ro", markersize=6)  # Terminal "X"
    ax.text(4.4, 1.5, "X", ha="left", va="center", fontsize=12)

    # Draw wires with correct direction (Terminal → Port)
    ax.arrow(4.2, 1.5, 0.8, 0, head_width=0.1, head_length=0.2, fc="black", ec="black")  # Output X to feedback loop

    # Looping back the feedback wire with a curve to visually indicate a loop
    loop_x = [5.0, 5.2, 4.0, 1.0, 1.0, 1.8]
    loop_y = [1.5, 2.0, 2.5, 2.5, 1.3, 1.3]
    ax.plot(loop_x, loop_y, "k-", lw=1.5)  # Curved feedback wire

    # Indicate the open port (U)
    ax.text(1.5, 2.2, "Open Port (U)", ha="right", va="center", fontsize=10, color="red")

    plt.title("Block Diagram: Simple System (Closed-Loop Ready)", fontsize=14, fontweight="bold")
    plt.show()

# Draw the improved block diagram with clear closed-loop indication
draw_block_diagram_improved()
