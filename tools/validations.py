#we want to write a simple tester to check various properties of a block diagrams
# are they closed loop?  Done
# does a model satisfy the requirements of block?
# what are their open ports? Done
# are the wires typed correctly? Done
# do we have duplicate wires into the same port? Done

import json
from collections import Counter

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

def get_ports_and_terminals(model, only_open_terminals=False, output_style="basic"):
    """
    Consolidated function that returns either a basic or an effective view of ports and terminals.

    Keyword Args:
        only_open_terminals (bool): If True (for basic output style) then only include terminals that
                                    are not used as the source for any wire.
                                    If False, include all terminals.
        output_style (str): Either "basic" or "effective".
           - "basic": returns a dictionary with keys:
               "open_ports": list of (processor_id, port) tuples for ports with no incoming wires.
               "available_terminals": list of (processor_id, terminal) tuples (filtered based on only_open_terminals).
           - "effective": returns a tuple:
               (effective_inputs, effective_outputs)
               effective_inputs: external input signals (deduced from open ports of processors that have no outgoing wires)
               effective_outputs: external output signals (terminals whose outgoing wires do not go to a different processor)
    
    Raises:
        ValueError: If an invalid output_style is provided.
    """
    # Build connection maps: incoming and outgoing.
    incoming = {}  # Map: processor_id -> list of (port_index, wire_space, source_processor)
    outgoing = {}  # Map: processor_id -> list of (wire_space, destination_processor)
    for wire in model.get("wires", []):
        src_proc, src_idx = wire["Source"]
        dst_proc, dst_idx = wire["Destination"]
        wire_space = wire["Parent"]
        incoming.setdefault(dst_proc, []).append((dst_idx, wire_space, src_proc))
        outgoing.setdefault(src_proc, []).append((wire_space, dst_proc))

    # --- Basic view computation ---
    open_ports = []
    available_terminals = []
    for proc in model.get("processors", []):
        proc_id = proc["ID"]
        ports = proc.get("Ports", [])
        terminals = proc.get("Terminals", [])
        # Determine open ports: for each port index, if there is no incoming wire for that index.
        for i, port in enumerate(ports):
            if not any(i == incoming_idx for (incoming_idx, _, _) in incoming.get(proc_id, [])):
                open_ports.append((proc_id, port))
        # Determine available terminals.
        for term in terminals:
            if only_open_terminals:
                # Only include this terminal if no outgoing connection from this processor uses it.
                if not any(wire_space == term for (wire_space, _) in outgoing.get(proc_id, [])):
                    available_terminals.append((proc_id, term))
            else:
                available_terminals.append((proc_id, term))

    if output_style == "basic":
        return {
            "open_ports": open_ports,
            "available_terminals": available_terminals,
        }
    elif output_style == "effective":
        # --- Effective view computation ---
        # First, determine the set of internally generated signals (all terminals)
        internally_generated = {
            term for proc in model.get("processors", [])
            for term in proc.get("Terminals", [])
        }
        effective_inputs = []
        # For effective inputs, we choose only those processors that have no outgoing wires
        # (i.e. signals truly coming from outside the system). This heuristic avoids counting
        # ports on processors that are part of an internal closed‐loop.
        for proc in model.get("processors", []):
            proc_id = proc["ID"]
            ports = proc.get("Ports", [])
            # Only consider a processor as a candidate for external input if it has no outgoing wires.
            if not outgoing.get(proc_id, []):
                for i, port in enumerate(ports):
                    if not any(i == incoming_idx for (incoming_idx, _, _) in incoming.get(proc_id, [])):
                        if port not in internally_generated:
                            effective_inputs.append(port)
        # Effective outputs: for each terminal in every processor, if that processor’s outgoing wires do
        # not include a connection (with a different destination) using that terminal, then consider it external.
        effective_outputs = []
        for proc in model.get("processors", []):
            proc_id = proc["ID"]
            terminals = proc.get("Terminals", [])
            for term in terminals:
                # Look up outgoing wires from this processor.
                out_conns = outgoing.get(proc_id, [])
                # If any outgoing connection uses this terminal and sends it to a different processor,
                # then we do not consider it an effective (external) output.
                if not any((wire_space == term and dest_proc != proc_id) for (wire_space, dest_proc) in out_conns):
                    effective_outputs.append(term)
        # Deduplicate outputs (and inputs) since we care only about the set of signals.
        effective_inputs = list(dict.fromkeys(effective_inputs))
        effective_outputs = list(dict.fromkeys(effective_outputs))
        return (effective_inputs, effective_outputs)
    else:
        raise ValueError("Invalid output_style. Use 'basic' or 'effective'.")


# ----------------- TESTS -----------------

def test_basic_mode_all_terminals():
    """
    Test basic output with all terminals included.
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
    result = get_ports_and_terminals(test_model, only_open_terminals=False, output_style="basic")
    expected = {
        "open_ports": [("f", "X"), ("s", "X")],
        "available_terminals": [("f", "X"), ("g", "U"), ("s", "Y")]
    }
    assert result == expected, f"Basic mode (all terminals) failed. Got: {result}"


def test_basic_mode_only_open_terminals():
    """
    Test basic output when filtering terminals to only those that are not used as a source.
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
    result = get_ports_and_terminals(test_model, only_open_terminals=True, output_style="basic")
    # In this model every terminal is used as a source (f uses "X", g uses "U", s uses "Y"),
    # so available_terminals should be empty.
    expected = {
        "open_ports": [("f", "X"), ("s", "X")],
        "available_terminals": []
    }
    assert result == expected, f"Basic mode (only open terminals) failed. Got: {result}"


def test_effective_mode_closed_loop():
    """
    Test effective view on a closed-loop system.
    Expect no effective inputs and effective outputs to include only 'X' (from the dynamics blocks).
    """
    closed_loop_model = {
        "processors": [
            {
                "ID": "alice_dynamics",
                "Parent": "F",
                "Ports": ["X", "U"],
                "Terminals": ["X"]
            },
            {
                "ID": "bob_dynamics",
                "Parent": "F",
                "Ports": ["X", "U"],
                "Terminals": ["X"]
            },
            {
                "ID": "alice_decision",
                "Parent": "Decision",
                "Ports": ["Theta"],
                "Terminals": ["U"]
            },
            {
                "ID": "bob_decision",
                "Parent": "Decision",
                "Ports": ["Theta"],
                "Terminals": ["U"]
            }
        ],
        "wires": [
            {
                "ID": "w_alice_action",
                "Parent": "U",
                "Source": ["alice_decision", 0],
                "Destination": ["alice_dynamics", 1]
            },
            {
                "ID": "w_bob_action",
                "Parent": "U",
                "Source": ["bob_decision", 0],
                "Destination": ["bob_dynamics", 1]
            },
            {
                "ID": "w_alice_feedback",
                "Parent": "X",
                "Source": ["alice_dynamics", 0],
                "Destination": ["alice_dynamics", 0]
            },
            {
                "ID": "w_bob_feedback",
                "Parent": "X",
                "Source": ["bob_dynamics", 0],
                "Destination": ["bob_dynamics", 0]
            }
        ]
    }
    effective_inputs, effective_outputs = get_ports_and_terminals(closed_loop_model, output_style="effective")
    # By our heuristic, every processor has an outgoing connection so none are considered external.
    expected_effective_inputs = []  
    # For effective outputs, we allow self-loops. Only the dynamics processors provide an output "X".
    # (Duplicates are removed in the function.)
    expected_effective_outputs = ["X"]
    assert effective_inputs == expected_effective_inputs, f"Effective mode closed-loop: expected effective_inputs {expected_effective_inputs}, got {effective_inputs}"
    assert set(effective_outputs) == set(expected_effective_outputs), f"Effective mode closed-loop: expected effective_outputs {expected_effective_outputs}, got {effective_outputs}"


def test_basic_mode_no_wires_all_terminals():
    """
    Test basic view on a model with a single processor and no wires.
    With only_open_terminals False, all declared terminals should be returned.
    """
    model_no_wires = {
        "processors": [
            {"ID": "p1", "Ports": ["A", "B"], "Terminals": ["C", "D"]}
        ],
        "wires": []
    }
    result = get_ports_and_terminals(model_no_wires, only_open_terminals=False, output_style="basic")
    expected = {
        "open_ports": [("p1", "A"), ("p1", "B")],
        "available_terminals": [("p1", "C"), ("p1", "D")]
    }
    assert result == expected, f"Basic mode no wires (all terminals) failed. Got: {result}"


def test_basic_mode_no_wires_only_open_terminals():
    """
    Test basic view on a model with a single processor and no wires.
    With only_open_terminals True, all terminals are still returned (since there are no outgoing wires).
    """
    model_no_wires = {
        "processors": [
            {"ID": "p1", "Ports": ["A", "B"], "Terminals": ["C", "D"]}
        ],
        "wires": []
    }
    result = get_ports_and_terminals(model_no_wires, only_open_terminals=True, output_style="basic")
    expected = {
        "open_ports": [("p1", "A"), ("p1", "B")],
        "available_terminals": [("p1", "C"), ("p1", "D")]
    }
    assert result == expected, f"Basic mode no wires (only open terminals) failed. Got: {result}"


def test_effective_mode_no_wires():
    """
    Test effective view on a model with a single processor and no wires.
    In this case, the processor is external so its open ports and terminals become effective inputs and outputs.
    """
    model_no_wires = {
        "processors": [
            {"ID": "p1", "Ports": ["A", "B"], "Terminals": ["C", "D"]}
        ],
        "wires": []
    }
    effective_inputs, effective_outputs = get_ports_and_terminals(model_no_wires, output_style="effective")
    # For processor p1: both ports are open and p1 has no outgoing wires.
    expected_effective_inputs = ["A", "B"]
    expected_effective_outputs = ["C", "D"]
    assert set(effective_inputs) == set(expected_effective_inputs), f"Effective mode no wires: expected effective_inputs {expected_effective_inputs}, got {effective_inputs}"
    assert set(effective_outputs) == set(expected_effective_outputs), f"Effective mode no wires: expected effective_outputs {expected_effective_outputs}, got {effective_outputs}"


def test_effective_mode_mixed():
    """
    Test effective view on a model where one processor is external and one is internal.
    The external processor (with no outgoing wires) should provide an effective input.
    """
    model_mixed = {
        "processors": [
            {"ID": "ext_proc", "Ports": ["P1", "P2"], "Terminals": ["T1"]},
            {"ID": "int_proc", "Ports": ["X"], "Terminals": ["Y"]}
        ],
        "wires": [
            # int_proc sends a signal to ext_proc.
            {"ID": "w1", "Parent": "Y", "Source": ["int_proc", 0], "Destination": ["ext_proc", 1]}
        ]
    }
    effective_inputs, effective_outputs = get_ports_and_terminals(model_mixed, output_style="effective")
    # For ext_proc: outgoing is empty, and its open ports:
    #   Ports = ["P1", "P2"], but note: port index 1 receives a wire (so only "P1" is open).
    # For int_proc: outgoing exists so we ignore its ports.
    expected_effective_inputs = ["P1"]
    # For effective outputs:
    #   ext_proc's terminal "T1": no outgoing wires -> effective.
    #   int_proc's terminal "Y": outgoing wire goes to a different processor, so not effective.
    expected_effective_outputs = ["T1"]
    assert set(effective_inputs) == set(expected_effective_inputs), f"Effective mode mixed: expected effective_inputs {expected_effective_inputs}, got {effective_inputs}"
    assert set(effective_outputs) == set(expected_effective_outputs), f"Effective mode mixed: expected effective_outputs {expected_effective_outputs}, got {effective_outputs}"


def test_invalid_output_style():
    """
    Ensure that an invalid output_style raises a ValueError.
    """
    model_no_wires = {
        "processors": [
            {"ID": "p1", "Ports": ["A"], "Terminals": ["B"]}
        ],
        "wires": []
    }
    try:
        get_ports_and_terminals(model_no_wires, output_style="invalid")
    except ValueError:
        pass
    else:
        assert False, "Invalid output_style did not raise a ValueError"


# ----------------- RUN TESTS -----------------

if __name__ == "__main__":
    test_basic_mode_all_terminals()
    test_basic_mode_only_open_terminals()
    test_effective_mode_closed_loop()
    test_basic_mode_no_wires_all_terminals()
    test_basic_mode_no_wires_only_open_terminals()
    test_effective_mode_no_wires()
    test_effective_mode_mixed()
    test_invalid_output_style()
    print("✅ All tests passed!")

def validate_model_satisfies_block(model, block, require_open_terminals=False):
    """
    Checks whether a given model satisfies the requirements of a Block.

    Args:
        model (dict): The block diagram model (JSON).
        block (dict): The Block definition.
        require_open_terminals (bool): If True, expected terminals must be open (unused).

    Returns:
        bool: True if the model satisfies the Block requirements, False otherwise.
    """
    # Step 1: Check if the model is a single processor that directly implements the Block
    if len(model["processors"]) == 1:
        single_processor = model["processors"][0]
        if single_processor["Parent"] == block["ID"]:
            print(f"✅ Model directly implements the Block {block['ID']} as a single processor.")
            return True

    # Step 2: Get the model's inferred effective inputs and outputs
    model_inputs, model_outputs = get_effective_ports_and_terminals(model)

    block_inputs = block["Domain"]
    block_outputs = block["Codomain"]

    # Step 3: Compare counts of expected vs actual inputs/outputs
    model_input_counts = Counter(model_inputs)
    model_output_counts = Counter(model_outputs)

    block_input_counts = Counter(block_inputs)
    block_output_counts = Counter(block_outputs)

    missing_inputs = block_input_counts - model_input_counts
    missing_outputs = block_output_counts - model_output_counts

    # Debugging output
    print("\n--- Block Validation Debugging ---")
    print(f"Block Name: {block['ID']}")
    print(f"Block Inputs (Domain): {block_input_counts}")
    print(f"Model Effective Inputs: {model_input_counts}")
    print(f"Missing Inputs: {missing_inputs}")

    print(f"Block Outputs (Codomain): {block_output_counts}")
    print(f"Model Effective Outputs: {model_output_counts}")
    print(f"Missing Outputs: {missing_outputs}")
    print("--- End Debugging ---\n")

    # If there are any missing required inputs or outputs, return False
    if missing_inputs or missing_outputs:
        return False

    return True

from collections import Counter

# =====================================================
# Unified Function: get_ports_and_terminals
# =====================================================
def get_ports_and_terminals(model, only_open_terminals=False, output_style="basic"):
    """
    Returns information about ports and terminals from a model.
    
    Keyword Args:
        only_open_terminals (bool): (For basic output) If True, only include terminals
                                    that are not used as a source in any outgoing wire.
                                    If False, include all terminals.
        output_style (str): Either "basic" or "effective".
            - "basic": returns a dictionary:
                {
                    "open_ports": list of (processor_id, port) tuples (ports with no incoming wires),
                    "available_terminals": list of (processor_id, terminal) tuples
                        (either all terminals or only those that are open, depending on only_open_terminals)
                }
            - "effective": returns a tuple:
                (effective_inputs, effective_outputs)
                where effective_inputs are deduced external inputs and effective_outputs are
                deduced external outputs.
    
    Raises:
        ValueError: If an invalid output_style is provided.
    """
    # Build mapping dictionaries for incoming and outgoing connections.
    incoming = {}  # processor_id -> list of (port_index, wire_space, source_processor)
    outgoing = {}  # processor_id -> list of (wire_space, destination_processor)
    for wire in model.get("wires", []):
        src_proc, src_idx = wire["Source"]
        dst_proc, dst_idx = wire["Destination"]
        wire_space = wire["Parent"]
        incoming.setdefault(dst_proc, []).append((dst_idx, wire_space, src_proc))
        outgoing.setdefault(src_proc, []).append((wire_space, dst_proc))
    
    # --- BASIC VIEW ---
    open_ports = []
    available_terminals = []
    for proc in model.get("processors", []):
        proc_id = proc["ID"]
        ports = proc.get("Ports", [])
        terminals = proc.get("Terminals", [])
        # For each port, if there is no incoming wire for that index then it is open.
        for i, port in enumerate(ports):
            if not any(i == idx for (idx, _, _) in incoming.get(proc_id, [])):
                open_ports.append((proc_id, port))
        # For each terminal, include it (or only if it is not used as an outgoing signal).
        for term in terminals:
            if only_open_terminals:
                if not any(wire_space == term for (wire_space, _) in outgoing.get(proc_id, [])):
                    available_terminals.append((proc_id, term))
            else:
                available_terminals.append((proc_id, term))
    
    if output_style == "basic":
        return {"open_ports": open_ports, "available_terminals": available_terminals}
    elif output_style == "effective":
        # --- EFFECTIVE VIEW ---
        # Identify all internally generated signals (all terminals across processors).
        internally_generated = {
            term for proc in model.get("processors", []) for term in proc.get("Terminals", [])
        }
        effective_inputs = []
        # For effective inputs we consider ports that are open on processors with no outgoing wires.
        for proc in model.get("processors", []):
            proc_id = proc["ID"]
            ports = proc.get("Ports", [])
            # Only consider processors that do not drive any signal (i.e. no outgoing connections)
            if not outgoing.get(proc_id, []):
                for i, port in enumerate(ports):
                    if not any(i == idx for (idx, _, _) in incoming.get(proc_id, [])):
                        if port not in internally_generated:
                            effective_inputs.append(port)
        # For effective outputs, include a terminal if no outgoing wire from its processor
        # drives that terminal to a different processor.
        effective_outputs = []
        for proc in model.get("processors", []):
            proc_id = proc["ID"]
            terminals = proc.get("Terminals", [])
            for term in terminals:
                out_conns = outgoing.get(proc_id, [])
                if not any((wire_space == term and dest_proc != proc_id)
                           for (wire_space, dest_proc) in out_conns):
                    effective_outputs.append(term)
        # Remove duplicates while preserving order.
        effective_inputs = list(dict.fromkeys(effective_inputs))
        effective_outputs = list(dict.fromkeys(effective_outputs))
        return (effective_inputs, effective_outputs)
    else:
        raise ValueError("Invalid output_style. Use 'basic' or 'effective'.")


# =====================================================
# Block Validation Methods
# =====================================================
def validate_model_satisfies_block(model, block, require_open_terminals=False):
    """
    Checks whether a given model satisfies the requirements of a Block using its effective ports.
    
    Args:
        model (dict): The block diagram model.
        block (dict): The Block definition (with keys "ID", "Domain", "Codomain").
        require_open_terminals (bool): (Unused here, but included for interface compatibility.)
        
    Returns:
        bool: True if the model satisfies the Block requirements, False otherwise.
    """
    # Step 1: Direct implementation check.
    if len(model.get("processors", [])) == 1:
        proc = model["processors"][0]
        if proc.get("Parent") == block.get("ID"):
            print(f"✅ Model directly implements the Block {block['ID']} as a single processor.")
            return True
    
    # Step 2: Get the model's effective inputs and outputs.
    model_inputs, model_outputs = get_ports_and_terminals(model, output_style="effective")
    
    block_inputs = block.get("Domain", [])
    block_outputs = block.get("Codomain", [])
    
    # Compare counts using Counter.
    model_input_counts = Counter(model_inputs)
    model_output_counts = Counter(model_outputs)
    
    block_input_counts = Counter(block_inputs)
    block_output_counts = Counter(block_outputs)
    
    missing_inputs = block_input_counts - model_input_counts
    missing_outputs = block_output_counts - model_output_counts
    
    # Debugging output.
    print("\n--- Block Validation Debugging (Effective) ---")
    print(f"Block Name: {block['ID']}")
    print(f"Block Inputs (Domain): {block_input_counts}")
    print(f"Model Effective Inputs: {model_input_counts}")
    print(f"Missing Inputs: {missing_inputs}")
    print(f"Block Outputs (Codomain): {block_output_counts}")
    print(f"Model Effective Outputs: {model_output_counts}")
    print(f"Missing Outputs: {missing_outputs}")
    print("--- End Debugging ---\n")
    
    if missing_inputs or missing_outputs:
        return False
    return True


def model_satisfies_block(model, block, require_open_terminals=False):
    """
    Checks whether a given model satisfies the requirements of a Block using its basic ports.
    
    Args:
        model (dict): The block diagram model.
        block (dict): The Block definition (with keys "ID", "Domain", "Codomain").
        require_open_terminals (bool): If True, available terminals are filtered to only those that are open.
    
    Returns:
        bool: True if the model satisfies the Block requirements, False otherwise.
    """
    # Step 1: Direct implementation check.
    if len(model.get("processors", [])) == 1:
        proc = model["processors"][0]
        if proc.get("Parent") == block.get("ID"):
            print(f"✅ Model directly implements the Block {block['ID']} as a single processor.")
            return True
    
    # Step 2: Get the model's open ports and available terminals (basic view).
    status = get_ports_and_terminals(model, only_open_terminals=require_open_terminals, output_style="basic")
    
    # Preserve duplicates if any.
    model_inputs = [port for (_, port) in status["open_ports"]]
    model_outputs = [terminal for (_, terminal) in status["available_terminals"]]
    
    block_inputs = block.get("Domain", [])
    block_outputs = block.get("Codomain", [])
    
    model_input_counts = Counter(model_inputs)
    model_output_counts = Counter(model_outputs)
    
    block_input_counts = Counter(block_inputs)
    block_output_counts = Counter(block_outputs)
    
    missing_inputs = block_input_counts - model_input_counts
    missing_outputs = block_output_counts - model_output_counts
    
    # Debugging output.
    print("\n--- Block Validation Debugging (Basic) ---")
    print(f"Block Name: {block['ID']}")
    print(f"Block Inputs (Domain): {block_input_counts}")
    print(f"Model Inputs: {model_input_counts}")
    print(f"Missing Inputs: {missing_inputs}")
    print(f"Block Outputs (Codomain): {block_output_counts}")
    print(f"Model Outputs: {model_output_counts}")
    print(f"Missing Outputs: {missing_outputs}")
    print("--- End Debugging ---\n")
    
    if missing_inputs or missing_outputs:
        return False
    return True


# =====================================================
# TESTS for Block Validation Functions
# =====================================================

def test_validate_model_direct_implementation():
    """
    If the model is a single processor whose Parent equals the Block ID,
    the validation should return True.
    """
    block = {"ID": "blockA", "Domain": ["A"], "Codomain": ["B"]}
    model = {
        "processors": [
            {"ID": "proc1", "Parent": "blockA", "Ports": ["A"], "Terminals": ["B"]}
        ],
        "wires": []
    }
    assert validate_model_satisfies_block(model, block) == True, "Direct implementation should pass."


def test_validate_model_missing_input():
    """
    If the Block expects more inputs than the model provides, validation should fail.
    """
    block = {"ID": "blockB", "Domain": ["A", "A"], "Codomain": ["B"]}
    # Model provides only one effective input "A" (from its only processor).
    model = {
        "processors": [
            {"ID": "proc1", "Parent": "F", "Ports": ["A"], "Terminals": ["B"]}
        ],
        "wires": []
    }
    assert validate_model_satisfies_block(model, block) == False, "Missing input should fail validation."


def test_validate_model_missing_output():
    """
    If the Block expects more outputs than the model provides, validation should fail.
    """
    block = {"ID": "blockC", "Domain": ["A"], "Codomain": ["B", "B"]}
    # Model provides only one effective output "B".
    model = {
        "processors": [
            {"ID": "proc1", "Parent": "F", "Ports": ["A"], "Terminals": ["B"]}
        ],
        "wires": []
    }
    assert validate_model_satisfies_block(model, block) == False, "Missing output should fail validation."


def test_validate_model_satisfied():
    """
    A model that yields the effective inputs and outputs required by the Block should pass.
    In this test we construct a model where two processors (with no outgoing wires)
    yield the necessary inputs and one processor provides the required output.
    """
    block = {"ID": "blockD", "Domain": ["A", "C"], "Codomain": ["B"]}
    model = {
        "processors": [
            {"ID": "procA", "Parent": "F", "Ports": ["A"], "Terminals": []},
            {"ID": "procC", "Parent": "F", "Ports": ["C"], "Terminals": []},
            {"ID": "procB", "Parent": "F", "Ports": [], "Terminals": ["B"]}
        ],
        "wires": []
    }
    # Processors procA and procC have no outgoing wires so they yield effective inputs "A" and "C".
    # Processor procB has no outgoing wires so its terminal "B" is effective.
    assert validate_model_satisfies_block(model, block) == True, "Satisfied block should pass validation."


def test_model_satisfies_block_basic():
    """
    Test the basic validation (using open ports and available terminals).
    This test uses a multi-processor model with wires.
    """
    block = {"ID": "blockE", "Domain": ["X"], "Codomain": ["Y"]}
    model = {
        "processors": [
            {"ID": "dynamics", "Parent": "F", "Ports": ["X", "U"], "Terminals": ["X"]},
            {"ID": "sensor", "Parent": "S", "Ports": ["X"], "Terminals": ["Y"]}
        ],
        "wires": [
            {"ID": "w1", "Parent": "U", "Source": ["dynamics", 1], "Destination": ["sensor", 0]},
            {"ID": "w2", "Parent": "X", "Source": ["dynamics", 0], "Destination": ["sensor", 0]}
        ]
    }
    # Using basic mode (open_ports and available_terminals) and not requiring open terminals,
    # we expect that the sensor's terminal "Y" is available.
    assert model_satisfies_block(model, block, require_open_terminals=False) == True, \
        "Basic mode: model should satisfy block E."


def test_model_satisfies_block_fail():
    """
    If the Block expects more signals than provided by the model,
    the basic validation should return False.
    """
    block = {"ID": "blockF", "Domain": ["X", "Z"], "Codomain": ["Y"]}
    model = {
        "processors": [
            {"ID": "proc1", "Parent": "F", "Ports": ["X"], "Terminals": ["Y"]}
        ],
        "wires": []
    }
    # The model only provides "X" as an open port but the block requires both "X" and "Z".
    assert model_satisfies_block(model, block) == False, \
        "Basic mode: model missing an input should fail block satisfaction."


# =====================================================
# Run All Tests
# =====================================================
def run_all_tests():
    print("Running tests for validate_model_satisfies_block (effective view)...")
    test_validate_model_direct_implementation()
    test_validate_model_missing_input()
    test_validate_model_missing_output()
    test_validate_model_satisfied()
    print("✅ validate_model_satisfies_block tests passed.\n")
    
    print("Running tests for model_satisfies_block (basic view)...")
    test_model_satisfies_block_basic()
    test_model_satisfies_block_fail()
    print("✅ model_satisfies_block tests passed.\n")
    
    print("✅ All block validation tests passed!")


if __name__ == "__main__":
    run_all_tests()
