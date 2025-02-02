# Wiring Validation Guide

This document provides a clear understanding of **valid and invalid wiring configurations** in the block diagram model. It also explains:

- **Open Ports** (ports with no incoming wires)
- **Available Terminals** (all terminals, since multiple wires can originate from them)
- **Open Terminals** (terminals with no outgoing wires)

---

## **1. Understanding Wiring in Block Diagrams**
Each **processor** has:
- **Ports (inputs)**: These receive signals from wires.
- **Terminals (outputs)**: These send signals to other processors via wires.

Each **wire**:
- **Has a source terminal** (output of one processor).
- **Has a destination port** (input of another processor).

---

## **2. Valid and Invalid Wiring**
### ✅ **Valid Wiring**
| **Wire ID** | **Source Processor (Terminal)** | **Destination Processor (Port)** | **Valid?** | **Reason** |
|------------|--------------------------------|---------------------------------|----------|----------|
| `w1` | `f.X` | `g.Y` | ✅ Yes | A wire **connects a terminal to a port** |
| `w2` | `g.U` | `f.U` | ✅ Yes | A wire **connects a terminal to a port** |
| `w3` | `s.Y` | `g.Y` | ✅ Yes | A wire **connects a terminal to a port** |

### ❌ **Invalid Wiring**
| **Wire ID** | **Source Processor (Terminal)** | **Destination Processor (Port)** | **Valid?** | **Reason** |
|------------|--------------------------------|---------------------------------|----------|----------|
| `w4` | `f.X` | `s.X` | ❌ No | Ports **cannot be sources** |
| `w5` | `g.Y` | `s.Y` | ❌ No | Ports **cannot connect to ports** |
| `w6` | `f.U` | `g.U` | ❌ No | Terminals **cannot be destinations** |

---

## **3. What Are Open Ports?**
**Open Ports** are ports **that do not have any incoming wire**.

| **Processor** | **Port** | **Incoming Wire?** | **Is Open?** |
|--------------|---------|-----------------|-----------|
| `f` | `X` | ❌ No | ✅ **Yes (Open)** |
| `f` | `U` | ✅ Yes (`w2`) | ❌ No |
| `g` | `Y` | ✅ Yes (`w1`, `w3`) | ❌ No |
| `s` | `X` | ❌ No | ✅ **Yes (Open)** |

### ✅ **Correct Open Ports**
```
[("f", "X"), ("s", "X")]
```

---

## **4. What Are Available Terminals?**
**Available Terminals** are **all terminals**, since multiple wires can originate from the same terminal.

| **Processor** | **Terminal** | **Outgoing Wire?** | **Always Available?** |
|--------------|------------|----------------|------------------|
| `f` | `X` | ✅ Yes (`w1`) | ✅ Yes |
| `g` | `U` | ✅ Yes (`w2`) | ✅ Yes |
| `s` | `Y` | ✅ Yes (`w3`) | ✅ Yes |

### ✅ **Correct Available Terminals**
```
[("f", "X"), ("g", "U"), ("s", "Y")]
```

---

## **5. What Are Open Terminals?**
**Open Terminals** are terminals **that do not have any outgoing wires**.

| **Processor** | **Terminal** | **Outgoing Wire?** | **Is Open?** |
|--------------|------------|----------------|-----------|
| `f` | `X` | ✅ Yes (`w1`) | ❌ No |
| `g` | `U` | ❌ No | ✅ **Yes (Open)** |
| `s` | `Y` | ✅ Yes (`w3`) | ❌ No |

### ✅ **Correct Open Terminals**
```
[("g", "U")]
```

---

## **6. Summary of Open and Available Elements**
| **Category** | **Definition** | **Correct Values** |
|-------------|--------------|------------------|
| **Open Ports** | Ports **with no incoming wires** | `[("f", "X"), ("s", "X")]` |
| **Available Terminals** | **All terminals** (multiple wires can originate) | `[("f", "X"), ("g", "U"), ("s", "Y")]` |
| **Open Terminals** | Terminals **with no outgoing wires** | `[("g", "U")]` |

---

## **7. Key Takeaways**
- **Ports (inputs) receive wires** → If a port has no incoming wire, it is **open**.
- **Terminals (outputs) send signals** → If a terminal has no outgoing wire, it is **open**.
- **Multiple wires can originate from the same terminal** → This is **always valid**.
- **Ports cannot be sources** and **terminals cannot be destinations**.

---

## **8. How This is Used in Code**
The `get_open_ports_and_terminals(model, only_open_terminals=False)` function correctly computes:
1. **Open Ports** (ports with no incoming wires).
2. **Available Terminals** (all terminals).
3. **Open Terminals** (terminals with no outgoing wires, if `only_open_terminals=True`).

```python
result = get_open_ports_and_terminals(model)
```
```python
result_only_open_terminals = get_open_ports_and_terminals(model, only_open_terminals=True)
```

---

## **9. Additional Notes**
- If an **expected test fails**, double-check the **expected values** before assuming the function is wrong.
- Open ports and terminals are **strictly defined by incoming/outgoing wires**.