# Component-Based System Modeling

## Overview

This repository provides a structured approach to modeling component-based systems. It includes:
- A **Component Library** defining reusable "blocks" and "spaces".
- An **Example Model** demonstrating instantiation and wiring of components.

## Repository Structure

- **models/**
  - `simple_model.json`: A basic model demonstrating a single processor with a feedback loop.
  - `control_loop_model.json`: A model illustrating a closed-loop control system with a plant, controller, and sensor.
  - `game_model.json`: A model representing a two-player game with strategies and payoffs.

- **tools/**
  - `check_closed_loop.py`: A script to verify if a given block diagram model is fully closed-loop.
  - `visualize_model.py`: A script to generate visual representations of block diagram models.

## Table of Contents

- [Component-Based System Modeling](#component-based-system-modeling)
  - [Overview](#overview)
  - [Repository Structure](#repository-structure)
  - [Table of Contents](#table-of-contents)
  - [Conceptual Framework](#conceptual-framework)
  - [Component Library](#component-library)
    - [Library JSON Schemas](#library-json-schemas)
      - [Spaces Schema](#spaces-schema)
      - [Blocks Schema](#blocks-schema)
    - [Model JSON Schemas](#model-json-schemas)
      - [Processors Schema](#processors-schema)
      - [Wires Schema](#wires-schema)
  - [Example Records for the Library of Components](#example-records-for-the-library-of-components)
  - [Example Records for Building Models](#example-records-for-building-models)
    - [Example Model 1: Simple Dynamical System Plant](#example-model-1-simple-dynamical-system-plant)
      - [Model Concrete Components](#model-concrete-components)
      - [**JSON Representation**](#json-representation)
    - [**Step 2: Define the Concrete Example Model**](#step-2-define-the-concrete-example-model)
      - [**Example Model (`game_model.json`)**](#example-model-game_modeljson)
    - [**Explanation**](#explanation)


## Conceptual Framework

The conceptual framework distinguishes abstract patterns that we reuse from concrete components which satisfy those patterns. The abstract patterns tell us how things can be wired together but they cannot themselves be wired, only their concrete counterparts can be wired. By preserving these seperation we can identify and take advantage of stuctural similarities in the systems we're modeling.

The following table categorizes components into **abstract vs. concrete** and **structural vs. behavioral** dimensions:

|               | Abstract  | Concrete  |
|--------------|-----------|-----------|
| **Structure** | Space     | Wire      |
| **Behavior**  | Block     | Processor |

This classification provides a clear distinction between the elements of the system:

- **Abstract Structure (Space)**: Represents the conceptual spaces through which data, signals, or states flow.
- **Abstract Behavior (Block)**: Defines reusable templates describing how components behave in a system.
- **Concrete Structure (Wire)**: Connects instantiated components (processors) according to defined spaces.
- **Concrete Behavior (Processor)**: An instance of a block that interacts within the system based on its structure.

In summary, **spaces and blocks define the abstract model**, while **wires and processors bring it into concrete implementation** through instantiation and connectivity.

---

## Component Library

A component library is full of Abstract objects that can be thought of as reusable patterns or templates that the Concrete components satisfy.

The component library consists of:
- **Blocks**: Reusable templates for system components.
- **Spaces**: Define the types of inputs and outputs.

### Library JSON Schemas

These are the schemas for the components which exist within the component library. These are the Abstract Components.

#### Spaces Schema

```json
{
  "ID": "string (required)",
  "Name": "string (required)",
  "Description": "string (optional)"
}
```

#### Blocks Schema

```json
{
  "ID": "string (required)",
  "Name": "string (required)",
  "Description": "string (optional)",
  "Domain": "array[Space] (required, can be empty)",
  "Codomain": "array[Space] (required, can be empty)"
}
```

### Model JSON Schemas

These are the schemas for the components which exist within models. These are the Concrete Components.

#### Processors Schema

```json
{
  "ID": "string (required)",
  "Parent": "block_id (required)",
  "Name": "string (required)",
  "Description": "string (optional)",
  "Ports": "array[Space] (must match parent block Domain)",
  "Terminals": "array[Space] (must match parent block Codomain)"
}
```

#### Wires Schema

```json
{
  "ID": "string (required)",
  "Parent": "space_id (required)",
  "Name": "string (optional)",
  "Description": "string (optional)",
  "Source": "tuple(processor_id, int) (must be valid terminal)",
  "Destination": "tuple(processor_id, int) (must be valid port)"
}
```

---

## Example Records for the Library of Components

Examples of space records that may be found in a component library:

```json
{
  "spaces": [
    { "ID": "X", "Name": "state", "Description": "The state space of a dynamical system" },
    { "ID": "Y", "Name": "output", "Description": "The observable signals for a dynamical system" },
    { "ID": "U", "Name": "input", "Description": "The controllable signals for a dynamical system" }
  ]
}
```

Examples of block records that may be found in a component library:

```json
{
  "blocks": [
    { 
      "ID": "F", 
      "Name": "Function", 
      "Description": "The dynamics of a dynamical system", 
      "Domain": ["X", "U"], 
      "Codomain": ["X"] 
    },
    { 
      "ID": "G", 
      "Name": "Policy", 
      "Description": "The control policy used to decide what action to take given an observation", 
      "Domain": ["Y"], 
      "Codomain": ["U"] 
    },
    { 
      "ID": "S", 
      "Name": "Sensor", 
      "Description": "The sensor which emits observable signals based on state", 
      "Domain": ["X"], 
      "Codomain": ["Y"] 
    }
  ]
}
```

## Example Records for Building Models

### Example Model 1: Simple Dynamical System Plant

The first example represents a simple dynamical system:

\[
x^+ = f(x, u)
\]

#### Model Concrete Components

This system consists of:
- **One Processor ("f")**: Instantiated from the **Function Block ("F")**, representing the system dynamics.
- **One Wire ("wrefX")**: Connects the **state output (X) back to the state input (X)**, creating a feedback loop.
- **One Open Port ("U")**: The system has an **unconnected input port** of type `"U"`, meaning an external controller or policy could later provide an input signal.

#### **JSON Representation**

```json
{
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
```

### Example Model 2: Closing the Control Loop

## Example 2: Closing the Control Loop

The second example extends the first by introducing a **Controller ("g")** and a **Sensor ("s")**, forming a closed-loop system.

### **Mathematical Representation**

$$x^+ = f(x, u)$$
$$y = s(x)$$
$$u = g(y)$$

This system fully closes the control loop by:
1. **Observing the system state (\( s \to g \))**.
2. **Computing a control action (\( g \to f \))**.
3. **Executing system dynamics (\( f \to s \))**.

### **Conceptual Diagram**

#### Concrete Components
- **Processor "f" (Plant)**: Represents the system dynamics.
- **Processor "g" (Controller)**: Computes control input based on observed output.
- **Processor "s" (Sensor)**: Converts system state into an observable output.
- **Wires**:
  - `"wrefX1"`: Loops **State (X)** back into the **Plant (f)**.
  - `"wrefU1"`: Connects **Controller (g) output (U) to Plant (f) input (U)**.
  - `"wrefY1"`: Connects **Sensor (s) output (Y) to Controller (g) input (Y)**.

#### **JSON Representation**
```json
{
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

## Building Games

In this section we will create a new Block called "Game" then use the existing components to build a repeated game

---

### **Step 1: Add "Game" Block to the Component Library**
This is an **abstract block** that goes into **`component_library.json`**.

#### **Library Update (`component_library.json`)**
```json
{
  "ID": "Game",
  "Name": "Game",
  "Description": "This is a simple two-player game where each player takes an action in 'U' and receives a payoff in 'Y'.",
  "Domain": ["U", "U"],
  "Codomain": ["Y", "Y"]
}
```

This defines:
- **Two input spaces ("U", "U")** for player actions.
- **Two output spaces ("Y", "Y")** for player payoffs.

---

### **Step 2: Define the Concrete Example Model**
This **instantiates processors** and **connects them via wires** to form a **game interaction**.

#### **Example Model (`game_model.json`)**
```json
{
  "processors": [
    {
      "ID": "game",
      "Parent": "Game",
      "Name": "Two-Player Game",
      "Ports": ["U", "U"],
      "Terminals": ["Y", "Y"]
    },
    {
      "ID": "alice_policy",
      "Parent": "G",
      "Name": "Alice's Strategy",
      "Ports": ["Y"],
      "Terminals": ["U"]
    },
    {
      "ID": "bob_policy",
      "Parent": "G",
      "Name": "Bob's Strategy",
      "Ports": ["Y"],
      "Terminals": ["U"]
    },
    {
      "ID": "alice_payoff",
      "Parent": "S",
      "Name": "Alice's Payoff",
      "Ports": ["X"],
      "Terminals": ["Y"]
    },
    {
      "ID": "bob_payoff",
      "Parent": "S",
      "Name": "Bob's Payoff",
      "Ports": ["X"],
      "Terminals": ["Y"]
    }
  ],
  "wires": [
    {
      "ID": "w_alice_action",
      "Parent": "U",
      "Name": "Alice's Move",
      "Source": ["alice_policy", 0],
      "Destination": ["game", 0]
    },
    {
      "ID": "w_bob_action",
      "Parent": "U",
      "Name": "Bob's Move",
      "Source": ["bob_policy", 0],
      "Destination": ["game", 1]
    },
    {
      "ID": "w_alice_payoff",
      "Parent": "Y",
      "Name": "Alice's Reward",
      "Source": ["game", 0],
      "Destination": ["alice_payoff", 0]
    },
    {
      "ID": "w_bob_payoff",
      "Parent": "Y",
      "Name": "Bob's Reward",
      "Source": ["game", 1],
      "Destination": ["bob_payoff", 0]
    },
    {
      "ID": "w_alice_observe",
      "Parent": "Y",
      "Name": "Alice Observes Payoff",
      "Source": ["alice_payoff", 0],
      "Destination": ["alice_policy", 0]
    },
    {
      "ID": "w_bob_observe",
      "Parent": "Y",
      "Name": "Bob Observes Payoff",
      "Source": ["bob_payoff", 0],
      "Destination": ["bob_policy", 0]
    }
  ]
}
```

---

### **Explanation**
This forms a **closed-loop game** where:
- **The "Game" processor** takes **two inputs (U, U) → two outputs (Y, Y)**.
- **Alice and Bob each have**:
  - **A Strategy ("alice_policy", "bob_policy")**, computing an action (`U`) from the previous payoff (`Y`).
  - **A Payoff Sensor ("alice_payoff", "bob_payoff")**, measuring the received reward.
- **The system loops**:
  - Each player **observes their payoff** and **chooses their next action**.
  - The **game block updates** the payoffs based on the actions.
