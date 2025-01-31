# Component-Based System Modeling

This repo demonstrates a technique for encoding Block Diagrams using json.

## Overview

This repository provides a structured approach to modeling component-based systems. It includes:
- A **Component Library** defining reusable "blocks" and "spaces".
- An **Example Model** demonstrating instantiation and wiring of components.

## Repository Structure

- **models/**
  - [x] `simple_model.json`: A basic model demonstrating a single processor with a feedback loop.
  - [x] `control_loop_model.json`: A model illustrating a closed-loop control system with a plant, controller, and sensor.
  - [x] `game_model.json`: A model representing a two-player game with strategies and payoffs.
  - [x] `adaptive_strategy.json`: A model representing a learning agent's decision process.
  - [x] `iterated_game_with_learning.json`: A model integrating learning agents into the two-payer game.

- **tools/**
  - [ ] `check_closed_loop.py`: A script to verify if a given block diagram model is fully closed-loop.
  - [ ] `visualize_model.py`: A script to generate visual representations of block diagram models.

## Quickstart
### Conceptual Framework

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


### Example Models

#### 1. Simple Dynamical System Plant
- **Description**: A basic model demonstrating a single processor with a feedback loop.
- **Model JSON**: [simple_model.json](models/simple_model.json)

#### 2. Closed-Loop Control System
- **Description**: A model illustrating a closed-loop control system with a plant, controller, and sensor.
- **Model JSON**: [control_loop_model.json](models/control_loop_model.json)

#### 3. Two-Player Game Model
- **Description**: A model representing a two-player game with strategies and payoffs.
- **Model JSON**: [game_model.json](models/game_model.json)

#### 4. Adaptive Strategy Model
- **Description**: This model introduces an adaptive strategy where the decision-making process incorporates learning from past experiences to refine the policy over time.
- **Model JSON**: [adaptive_strategy.json](models/adaptive_strategy.json)

#### 5. Iterated Game with Learning
- **Description**: An extension of the two-player game model where both players employ adaptive strategies, allowing them to learn and evolve their strategies over multiple iterations.
- **Model JSON**: [iterated_game_with_learning.json](models/iterated_game_with_learning.json)

## Table of Contents

- [Component-Based System Modeling](#component-based-system-modeling)
  - [Overview](#overview)
  - [Repository Structure](#repository-structure)
  - [Quickstart](#quickstart)
    - [Conceptual Framework](#conceptual-framework)
    - [Example Models](#example-models)
      - [1. Simple Dynamical System Plant](#1-simple-dynamical-system-plant)
      - [2. Closed-Loop Control System](#2-closed-loop-control-system)
      - [3. Two-Player Game Model](#3-two-player-game-model)
      - [4. Adaptive Strategy Model](#4-adaptive-strategy-model)
      - [5. Iterated Game with Learning](#5-iterated-game-with-learning)
  - [Table of Contents](#table-of-contents)
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
      - [Concrete Components](#concrete-components)
      - [JSON Representation](#json-representation)
    - [Example 2: Closing the Control Loop](#example-2-closing-the-control-loop)
      - [Mathematical Representation](#mathematical-representation)
      - [Concrete Components](#concrete-components-1)
      - [JSON Representation](#json-representation-1)
  - [Building Games](#building-games)
    - [Step 1: Add "Game" Block to the Component Library](#step-1-add-game-block-to-the-component-library)
      - [Library Update (`component_library.json`)](#library-update-component_libraryjson)
    - [Step 2: Define the Concrete Example Model](#step-2-define-the-concrete-example-model)
      - [Example Model (`game_model.json`)](#example-model-game_modeljson)
    - [Explanation](#explanation)
      - [Mathematical Representation](#mathematical-representation-1)
    - [Interpretation](#interpretation)
  - [Digging in to make more detailed models](#digging-in-to-make-more-detailed-models)
    - [Explanation](#explanation-1)
    - [Mathematical Representation](#mathematical-representation-2)
    - [How This Model Satisfies the "Policy" Block](#how-this-model-satisfies-the-policy-block)
    - [Summary](#summary)
  - [Iterated Game with Learning](#iterated-game-with-learning)
    - [Overview](#overview-1)
    - [Mathematical Representation](#mathematical-representation-3)
    - [Why This Model is Important](#why-this-model-is-important)
    - [Iterated Game with Learning Model JSON](#iterated-game-with-learning-model-json)



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

$$x^+ = f(x, u)$$

#### Concrete Components

This system consists of:
- **One Processor ("f")**: Instantiated from the **Function Block ("F")**, representing the system dynamics.
- **One Wire ("wrefX")**: Connects the **state output (X) back to the state input (X)**, creating a feedback loop.
- **One Open Port ("U")**: The system has an **unconnected input port** of type `"U"`, meaning an external controller or policy could later provide an input signal.

#### JSON Representation

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
### Example 2: Closing the Control Loop

The second example extends the first by introducing a **Controller ("g")** and a **Sensor ("s")**, forming a closed-loop system.

#### Mathematical Representation

$$x^+ = f(x, u)$$
$$y = s(x)$$
$$u = g(y)$$

This system fully closes the control loop by:
1. **Observing the system state (\( s \to g \))**.
2. **Computing a control action (\( g \to f \))**.
3. **Executing system dynamics (\( f \to s \))**.

#### Concrete Components
- **Processor "f" (Plant)**: Represents the system dynamics.
- **Processor "g" (Controller)**: Computes control input based on observed output.
- **Processor "s" (Sensor)**: Converts system state into an observable output.
- **Wires**:
  - `"wrefX1"`: Loops **State (X)** back into the **Plant (f)**.
  - `"wrefU1"`: Connects **Controller (g) output (U) to Plant (f) input (U)**.
  - `"wrefY1"`: Connects **Sensor (s) output (Y) to Controller (g) input (Y)**.

#### JSON Representation
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
```

## Building Games

In this section we will create a new Block called "Game" then use the existing components to build a repeated game. In addition to building the concrete model of the game, we will commit a new abstract component to the library, then use it along with previously defined abstract blocks and spaces.

---

### Step 1: Add "Game" Block to the Component Library
This is an **abstract block** that goes into **`component_library.json`**.

#### Library Update (`component_library.json`)
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

### Step 2: Define the Concrete Example Model
This **instantiates processors** and **connects them via wires** to form a **game interaction**.

#### Example Model (`game_model.json`)
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

### Explanation
Abstractly, this forms a **closed-loop game** where:
- **The "Game" processor** takes **two inputs (U, U) → two outputs (Y, Y)**.
- **Alice and Bob each have**:
  - **A Strategy ("alice_policy", "bob_policy")**, computing an action (`U`) from the previous payoff (`Y`).
  - Since we have not specified their details, we have not precluded strategies involving memory of past actions and payoffs.
- **The system loops**:
  - Each player **observes their payoff** and **chooses their next action**.
  - The **game block updates** the payoffs based on the actions.

Concretely, this example models a **repeated two-player game** where:

- **Alice and Bob** each choose an **action** $(u_A, u_B)$ from the action space \( U \).
- A **game function** $G(u_A, u_B)$ determines the **payoffs** $(y_A, y_B)$ for each player.
- Each player **observes their own payoff** $y_A$, and $y_B$ respectively
- The processors for Alice and Bob may be stateful, implying they may **update their strategy**.

#### Mathematical Representation
At each timestep \( t \):

1. **Players Choose Actions:**
$$u_A^t = g_A(y_A^{t-1})$$
$$u_B^t = g_B(y_B^{t-1})$$
where $g_A$ and $g_B$ are the **strategy functions** (policies) of Alice and Bob, respectively.

2. **Game Determines Payoffs:**
$$(y_A^t, y_B^t) = G(u_A^t, u_B^t)$$
where $G: U \times U \to Y \times Y$ is the **game function** mapping actions to payoffs.


### Interpretation
- Each **player observes their own payoff** and **chooses their next action** accordingly.
- The **game block computes the payoffs** based on the chosen actions.
- The system forms a **closed-loop interaction** where **strategies evolve dynamically** based on past outcomes.
- If we want to represent their strategy updates we could "zoom" in and define a more detailed model of how actions are chosen based on past actions and observations, including introducing endogenous state variables which can be thought of as memory, even if they are coded as the parameters of their strategy function.

Further equipping this model with mathematical or computation details would allow for further analysis of the **iterated game dynamics**, including:
- **Nash equilibrium convergence**
- **Reinforcement learning simulations**
- **Strategic decision-making analysis**

## Digging in to make more detailed models

Let's create a concrete model that satisfies the abstract Pattern "Policy". Recall the pattern:
```json
{ 
    "ID": "G", 
    "Name": "Policy", 
    "Description": "The control policy used to decide what action to take given an observation", 
    "Domain": ["Y"], 
    "Codomain": ["U"] 
}
```

We're going to build an "Adaptive Strategy" which has expectations and can adjust based on whether they are met. Here are our new abstract Blocks and spaces

```json
{
  "spaces": [
    { "ID": "Theta", "Name": "parameters", "Description": "The parameters of a learner" }
  ],
  "blocks": [
    { 
      "ID": "Learner", 
      "Name": "Learner", 
      "Description": "A model that learns from past actions and observations",
      "Domain": ["U", "Y", "Y"], 
      "Codomain": ["Theta"] 
    },
    { 
      "ID": "Decision", 
      "Name": "Decision", 
      "Description": "A decision-making model that generates actions based on learned parameters",
      "Domain": ["Theta"], 
      "Codomain": ["U", "Y"] 
    }
  ]
}
```
Keep in mind that we still have all of the other abstract components from our library. So we can build the following model

```json
{
  "processors": [
    {
      "ID": "learner",
      "Parent": "Learner",
      "Name": "Adaptive Learner",
      "Ports": ["U", "Y", "Y"],
      "Terminals": ["Theta"]
    },
    {
      "ID": "decision",
      "Parent": "Decision",
      "Name": "Decision Maker",
      "Ports": ["Theta"],
      "Terminals": ["U", "Y"]
    }
  ],
  "wires": [
    {
      "ID": "w_theta",
      "Parent": "Theta",
      "Name": "Updated Parameters",
      "Source": ["learner", 0],
      "Destination": ["decision", 0]
    },
    {
      "ID": "w_action",
      "Parent": "U",
      "Name": "Generated Action Feedback",
      "Source": ["decision", 0],
      "Destination": ["learner", 0]
    },
    {
      "ID": "w_expected_outcome",
      "Parent": "Y",
      "Name": "Expected Outcome Feedback",
      "Source": ["decision", 1],
      "Destination": ["learner", 2]
    }
  ]
}
```

This example extends the **Policy** block concept by incorporating **learning and adaptation**. 

### Explanation
- A **Policy** block is defined as a function **\( G: Y \to U \)** that maps an observation \( Y \) to an action \( U \).
- In this model, the **decision-making process** is **adaptive**: it incorporates **learning** from past experiences to refine the policy over time.

This is achieved by introducing two **new components**:
1. **Learner (`Learner`)**:
   - Updates parameters \( \theta \) based on past actions, expected outcomes, and realized outcomes.
2. **Decision Maker (`Decision`)**:
   - Uses learned parameters \( \theta \) to generate new actions and expected outcomes.

---

### Mathematical Representation
At each time step \( t \):

1. **The Decision Maker generates an action and an expected outcome**:
  $$(u^t, \hat{y}^t) = D(\theta^t)$$
   where:
   - $\theta^t$ represents the learned parameters at time $t$.
   - $u^t$ is the **chosen action**.
   - $\hat{y}^t$ is the **expected outcome**.

2. **The Learner updates its parameters** based on:
   - The action taken $u^t$.
   - The realized outcome $y^t$.
   - The predicted outcome $\hat{y}^t$.

   The learning update rule can be expressed as:
   $$\theta^{t+1} = L(\theta^t, u^t, \hat{y}^t, y^t)$$
   where $L$ is the **learning function**.

3. **The parameters are updated and fed back to the Decision Maker**:
   
   $$\theta^{t+1} \to D$$

This forms a **closed-loop system** where **observations dynamically shape future actions**.

---

### How This Model Satisfies the "Policy" Block
The abstract **"Policy" Block (G)** is defined by:

$$G: Y \to U$$

where the function $G$ determines an action $U$ based on an observation $Y$.

The **Adaptive Strategy Model** satisfies this definition because:
- The **Decision Maker (`Decision`)** computes an **action $U$** based on learned parameters $\theta$.
- The **Learner (`Learner`)** **adapts** those parameters based on the system's history.
- The overall system still functions as a **mapping from $Y$ to $U$** but **with an evolving internal state**.

Thus, this model can be seen as an **adaptive extension** of the **Policy Block**, where:
- The mapping from $Y$ to $U$ is **not static** but **evolves over time**.
- The system **self-adjusts** using feedback from prior experiences.

---

### Summary
- The **Adaptive Strategy Model** introduces **learning** into decision-making.
- It extends the **Policy** block by dynamically updating parameters **$ \theta$**.
- This model is useful for **reinforcement learning**, **adaptive control**, and **strategic decision-making**.

By implementing this structure, we move from a **static policy mapping** to a **self-improving decision process**, making it **suitable for environments with uncertainty and feedback-driven learning**.

## Iterated Game with Learning

This model extends the **two-player game** by introducing **adaptive learning**, replacing Alice's and Bob's strategies with **self-improving decision processes**.

### Overview
- Alice and Bob **initially make decisions** based on their current parameters.
- They **observe their actual payoffs** and **compare them to their expectations**.
- Their **learners update parameters** to improve future decisions.

This setup simulates **dynamic learning in strategic environments**, such as:
- **Game Theory**
- **Multi-Agent Reinforcement Learning**
- **Economic Decision-Making**

---

### Mathematical Representation

At each time step $t$:

1. **Alice and Bob make decisions** based on their current parameters:
   $$
   (u_A^t, \hat{y}_A^t) = D_A(\theta_A^t)
   $$
   $$
   (u_B^t, \hat{y}_B^t) = D_B(\theta_B^t)
   $$
   where:
   - $\theta_A^t, \theta_B^t$ are their current learning parameters.
   - $u_A^t, u_B^t$ are their chosen actions.
   - $\hat{y}_A^t, \hat{y}_B^t$ are their **expected payoffs**.

2. **The game computes actual payoffs**:
   $$
   (y_A^t, y_B^t) = G(u_A^t, u_B^t)
   $$
   where $G: U \times U \to Y \times Y$ is the game function.

3. **Alice and Bob update their learning parameters**:
   $$
   \theta_A^{t+1} = L_A(\theta_A^t, u_A^t, \hat{y}_A^t, y_A^t)
   $$
   $$
   \theta_B^{t+1} = L_B(\theta_B^t, u_B^t, \hat{y}_B^t, y_B^t)
   $$
   where:
   - $L_A, L_B$ are their **learning functions**.
   - They **adjust their parameters** based on:
     - The action taken $u$.
     - The expected outcome $\hat{y}$.
     - The actual payoff $y$.

---

### Why This Model is Important
- **It generalizes standard game-theoretic models** by incorporating **adaptive learning**.
- **Players improve over time**, instead of playing a static strategy.
- It allows us to **study equilibrium learning dynamics** and **strategic adaptation**.

---

### Iterated Game with Learning Model JSON
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
        "ID": "alice_learner",
        "Parent": "Learner",
        "Name": "Alice's Learner",
        "Ports": ["U", "Y", "Y"],
        "Terminals": ["Theta"]
      },
      {
        "ID": "alice_decision",
        "Parent": "Decision",
        "Name": "Alice's Decision",
        "Ports": ["Theta"],
        "Terminals": ["U", "Y"]
      },
      {
        "ID": "bob_learner",
        "Parent": "Learner",
        "Name": "Bob's Learner",
        "Ports": ["U", "Y", "Y"],
        "Terminals": ["Theta"]
      },
      {
        "ID": "bob_decision",
        "Parent": "Decision",
        "Name": "Bob's Decision",
        "Ports": ["Theta"],
        "Terminals": ["U", "Y"]
      }
    ],
    "wires": [
      {
        "ID": "w_alice_theta",
        "Parent": "Theta",
        "Name": "Alice's Updated Parameters",
        "Source": ["alice_learner", 0],
        "Destination": ["alice_decision", 0]
      },
      {
        "ID": "w_bob_theta",
        "Parent": "Theta",
        "Name": "Bob's Updated Parameters",
        "Source": ["bob_learner", 0],
        "Destination": ["bob_decision", 0]
      },
      {
        "ID": "w_alice_action",
        "Parent": "U",
        "Name": "Alice's Action",
        "Source": ["alice_decision", 0],
        "Destination": ["game", 0]
      },
      {
        "ID": "w_bob_action",
        "Parent": "U",
        "Name": "Bob's Action",
        "Source": ["bob_decision", 0],
        "Destination": ["game", 1]
      },
      {
        "ID": "w_alice_payoff",
        "Parent": "Y",
        "Name": "Alice's Realized Payoff",
        "Source": ["game", 0],
        "Destination": ["alice_learner", 2]
      },
      {
        "ID": "w_bob_payoff",
        "Parent": "Y",
        "Name": "Bob's Realized Payoff",
        "Source": ["game", 1],
        "Destination": ["bob_learner", 2]
      },
      {
        "ID": "w_alice_expected_payoff",
        "Parent": "Y",
        "Name": "Alice's Expected Payoff",
        "Source": ["alice_decision", 1],
        "Destination": ["alice_learner", 1]
      },
      {
        "ID": "w_bob_expected_payoff",
        "Parent": "Y",
        "Name": "Bob's Expected Payoff",
        "Source": ["bob_decision", 1],
        "Destination": ["bob_learner", 1]
      }
    ]
  }
```