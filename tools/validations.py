#we want to write a simple tester to check various properties of a block diagrams
# are they closed loop?  Done
# does a model satisfy the requirements of block?
# what are their open ports? 
# are the wires typed correctly? Done
# do we have duplicate wires into the same port? 

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