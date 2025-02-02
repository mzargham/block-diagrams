#we want to write a simple tester to check various properties of a block diagrams
# are they closed loop?  Done
# does a model satisfy the requirements of block?
# what are their open ports? 
# are the wires typed correctly? Done
# do we have duplicate wires into the same port? Done

import json

def is_closed_loop(model):
    """
    Checks whether a given block diagram model is fully closed-loop.
    A system is closed-loop if all input ports have at least one wire connection.
    """
    # Extract processors and wires
    processors = {p["ID"]: p for p in model["processors"]}
    wires = model["wires"]

    # Track which ports have at least one incoming connection
    connected_ports = set()

    for wire in wires:
        dest_proc, port_idx = wire["Destination"]
        
        if dest_proc in processors:
            num_ports = len(processors[dest_proc]["Ports"])
            if port_idx < num_ports:
                port_key = (dest_proc, port_idx)  # (Processor ID, Port index)
                connected_ports.add(port_key)

    # Debug: Print which ports have connections
    print("Connected Ports:", connected_ports)

    # Check if every processor's ports are fully wired
    for proc in processors.values():
        for port_idx in range(len(proc["Ports"])):  # Ensure all ports are connected
            if (proc["ID"], port_idx) not in connected_ports:
                print(f"Open Port Found: Processor '{proc['ID']}', Port Index {port_idx} ({proc['Ports'][port_idx]})")
                return False  # Found an open port, so it's not closed-loop

    return True  # If all ports are connected, it's fully closed-loop

def test_is_closed_loop():
    """
    Tests the is_closed_loop function using the simple and closed-loop models.
    """
    # Simple model (Not closed-loop)
    simple_model = {
        "processors": [
            {
                "ID": "f",
                "Parent": "F",
                "Name": "Dynamics",
                "Ports": ["X", "U"],
                "Terminals": ["X"]
            }
        ],
        "wires": [
            {
                "ID": "wrefX",
                "Parent": "X",
                "Name": "State Feedback",
                "Source": ["f", 0],
                "Destination": ["f", 0]
            }
        ]
    }

    # Control-loop model (Fully closed-loop)
    control_loop_model = {
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
            },
            {
                "ID": "wrefXSense",
                "Parent": "X",
                "Name": "State Measurement",
                "Source": ["f", 0],
                "Destination": ["s", 0]
            }
        ]
    }

    # Run tests
    assert is_closed_loop(simple_model) == False, "Test failed: Simple model should NOT be closed-loop."
    assert is_closed_loop(control_loop_model) == True, "Test failed: Control loop model SHOULD be closed-loop."

    print("All tests passed!")

if __name__ == "__main__":
    test_is_closed_loop()

def are_wires_typed_correctly(model):
    """
    Checks if all wires are properly typed.
    A wire is properly typed if the space type of its assigned Parent matches
    the space types of the associated port and terminal they connect.
    """
    processors = {p["ID"]: p for p in model["processors"]}
    
    for wire in model["wires"]:
        wire_parent = wire["Parent"]  # The space type of the wire
        
        src_proc, src_idx = wire["Source"]
        dest_proc, dest_idx = wire["Destination"]
        
        # Validate source processor (Terminal should match wire type)
        if src_proc in processors:
            src_terminals = processors[src_proc]["Terminals"]
            
            if src_idx < len(src_terminals) and src_terminals[src_idx] != wire_parent:
                print(f"Wire '{wire['ID']}' type mismatch: Source Terminal {src_terminals[src_idx]} != Wire Parent {wire_parent}")
                return False
        
        # Validate destination processor (Port should match wire type)
        if dest_proc in processors:
            dest_ports = processors[dest_proc]["Ports"]
            
            if dest_idx < len(dest_ports) and dest_ports[dest_idx] != wire_parent:
                print(f"Wire '{wire['ID']}' type mismatch: Destination Port {dest_ports[dest_idx]} != Wire Parent {wire_parent}")
                return False

    return True

def test_are_wires_typed_correctly():
    """
    Tests the are_wires_typed_correctly function.
    """
    correct_model = {
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
            },
            {
                "ID": "wrefXSense",
                "Parent": "X",
                "Name": "State Measurement",
                "Source": ["f", 0],
                "Destination": ["s", 0]
            }
        ]
    }

    incorrect_model = {
        "processors": [
            {
                "ID": "f",
                "Parent": "F",
                "Name": "Plant",
                "Ports": ["X", "U"],
                "Terminals": ["X"]
            }
        ],
        "wires": [
            {
                "ID": "wrefX1",
                "Parent": "U",  # Incorrect type, should be "X"
                "Name": "State Feedback",
                "Source": ["f", 0],
                "Destination": ["f", 0]
            }
        ]
    }

    assert are_wires_typed_correctly(correct_model) == True, "Test failed: Correct model should pass."
    assert are_wires_typed_correctly(incorrect_model) == False, "Test failed: Incorrect model should fail."

    print("All wire type tests passed!")

if __name__ == "__main__":
    test_are_wires_typed_correctly()

def no_duplicate_wires_into_ports(model):
    """
    Checks if any two wires are plugged into the same destination port.
    It's valid for multiple wires to come from the same terminal,
    but each port should have at most one incoming wire.
    """
    occupied_ports = {}  # Tracks wires going into each port

    for wire in model["wires"]:
        dest_proc, dest_idx = wire["Destination"]
        port_key = (dest_proc, dest_idx)  # Unique identifier for a destination port

        if port_key in occupied_ports:
            print(f"Error: Multiple wires are connected to the same port {dest_idx} on processor '{dest_proc}'. "
                  f"Conflicting Wires: {occupied_ports[port_key]} and {wire['ID']}")
            return False  # Found a duplicate connection
        
        occupied_ports[port_key] = wire["ID"]  # Register this port as occupied

    return True  # No duplicate ports found


def test_no_duplicate_wires_into_ports():
    """
    Tests the no_duplicate_wires_into_ports function.
    """

    # ✅ Valid case: No duplicate wires into the same port
    valid_model = {
        "processors": [
            {"ID": "f", "Parent": "F", "Name": "Plant", "Ports": ["X", "U"], "Terminals": ["X"]},
            {"ID": "g", "Parent": "G", "Name": "Controller", "Ports": ["Y"], "Terminals": ["U"]},
            {"ID": "s", "Parent": "S", "Name": "Sensor", "Ports": ["X"], "Terminals": ["Y"]}
        ],
        "wires": [
            {"ID": "w1", "Parent": "X", "Name": "State Feedback", "Source": ["f", 0], "Destination": ["g", 0]},
            {"ID": "w2", "Parent": "U", "Name": "Action", "Source": ["g", 0], "Destination": ["f", 1]},
            {"ID": "w3", "Parent": "Y", "Name": "Observation", "Source": ["s", 0], "Destination": ["f", 0]},
            {"ID": "w4", "Parent": "X", "Name": "State Measurement", "Source": ["f", 0], "Destination": ["s", 0]}
        ]
    }

    # ❌ Invalid case: Two wires into the same port
    invalid_model = {
        "processors": [
            {"ID": "f", "Parent": "F", "Name": "Plant", "Ports": ["X", "U"], "Terminals": ["X"]},
            {"ID": "g", "Parent": "G", "Name": "Controller", "Ports": ["Y"], "Terminals": ["U"]},
        ],
        "wires": [
            {"ID": "w1", "Parent": "X", "Name": "State Feedback", "Source": ["f", 0], "Destination": ["g", 0]},
            {"ID": "w2", "Parent": "X", "Name": "Duplicate Connection", "Source": ["s", 0], "Destination": ["g", 0]}  # Duplicate
        ]
    }

    assert no_duplicate_wires_into_ports(valid_model) == True, "Test failed: Valid model should pass."
    assert no_duplicate_wires_into_ports(invalid_model) == False, "Test failed: Invalid model should fail."

    print("All duplicate wire tests passed!")

if __name__ == "__main__":
    test_no_duplicate_wires_into_ports()

def get_open_ports_and_terminals(model, only_open_terminals=False):
    """
    Computes all open ports and available terminals in a block diagram model.
    
    Open ports: Ports that do not have an incoming wire.
    Available terminals: Terminals available for connection.
    
    If only_open_terminals=True, returns only terminals that have no outgoing wires.
    
    Args:
        model (dict): Block diagram model.
        only_open_terminals (bool): Whether to return only terminals that have no outgoing wires.
    
    Returns:
        dict: { 
            "open_ports": [(processor_id, port_name)], 
            "available_terminals": [(processor_id, terminal_name)] 
        }
    """
    processors = {p["ID"]: p for p in model["processors"]}
    occupied_ports = set()  # Tracks ports that have an incoming wire
    used_terminals = set()  # Tracks terminals that have outgoing wires

    # Step 1: Identify occupied ports (having at least one incoming wire) and used terminals
    for wire in model["wires"]:
        dest_proc, dest_idx = wire["Destination"]  # Destination is always a port
        src_proc, src_idx = wire["Source"]  # Source is always a terminal

        # Mark destination ports as occupied
        if dest_proc in processors and 0 <= dest_idx < len(processors[dest_proc]["Ports"]):
            occupied_ports.add((dest_proc, dest_idx))

        # Mark source terminals as used (since wires originate from terminals)
        if src_proc in processors and 0 <= src_idx < len(processors[src_proc]["Terminals"]):
            used_terminals.add((src_proc, src_idx))

    # Step 2: Identify open ports (ports without incoming wires)
    open_ports = []
    for proc in processors.values():
        for idx, port_name in enumerate(proc["Ports"]):
            if (proc["ID"], idx) not in occupied_ports:  # Open ports have no incoming wires
                open_ports.append((proc["ID"], port_name))

    # Step 3: Identify available terminals
    available_terminals = []
    for proc in processors.values():
        for idx, terminal_name in enumerate(proc["Terminals"]):
            if not only_open_terminals or (proc["ID"], idx) not in used_terminals:
                available_terminals.append((proc["ID"], terminal_name))

    return {
        "open_ports": open_ports,
        "available_terminals": available_terminals
    }

def test_get_open_ports_and_terminals():
    """
    Tests the get_open_ports_and_terminals function using a validated test model.
    """

    test_model = {
        "processors": [
            {"ID": "f", "Parent": "F", "Name": "Plant", "Ports": ["X", "U"], "Terminals": ["X"]},
            {"ID": "g", "Parent": "G", "Name": "Controller", "Ports": ["Y"], "Terminals": ["U"]},
            {"ID": "s", "Parent": "S", "Name": "Sensor", "Ports": ["X"], "Terminals": ["Y"]}
        ],
        "wires": [
            {"ID": "w1", "Parent": "X", "Source": ["f", 0], "Destination": ["g", 0]},
            {"ID": "w2", "Parent": "U", "Source": ["g", 0], "Destination": ["f", 1]},
            {"ID": "w3", "Parent": "Y", "Source": ["s", 0], "Destination": ["g", 0]}
        ]
    }

    # ✅ Corrected Expected Results
    expected_open_ports = [("f", "X"), ("s", "X")]  # Ports with no incoming wires
    expected_available_terminals = [("f", "X"), ("g", "U"), ("s", "Y")]  # All terminals
    expected_open_terminals = []  # Only terminals with no outgoing wires (none in this case)

    # Compute results
    result_all_terminals = get_open_ports_and_terminals(test_model)
    result_open_terminals = get_open_ports_and_terminals(test_model, only_open_terminals=True)

    # Debugging output
    print("\n--- Debugging Output ---")
    print("Computed Open Ports:", result_all_terminals["open_ports"])
    print("Expected Open Ports:", expected_open_ports)

    print("Computed Available Terminals:", result_all_terminals["available_terminals"])
    print("Expected Available Terminals:", expected_available_terminals)

    print("Computed Open Terminals:", result_open_terminals["available_terminals"])
    print("Expected Open Terminals:", expected_open_terminals)
    print("--- End Debugging ---\n")

    # Assertions to validate function correctness
    assert result_all_terminals["open_ports"] == expected_open_ports, "Test failed: Open ports incorrect."
    assert result_all_terminals["available_terminals"] == expected_available_terminals, "Test failed: Available terminals incorrect."
    assert result_open_terminals["available_terminals"] == expected_open_terminals, "Test failed: Open terminals incorrect."

    print("✅ All open port and terminal tests passed!")

# Run the test
if __name__ == "__main__":
    test_get_open_ports_and_terminals()
