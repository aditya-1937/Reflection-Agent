# Daily Reflection Tree — DT Fellowship Assignment

## Overview

This project implements a **deterministic reflection system** designed to guide employees through an end-of-day self-reflection process.

The system is built as a **decision tree (Part A)** and a **deterministic CLI agent (Part B)** that walks users through structured questions across three psychological axes:

1. **Locus** — Victim vs Victor (Agency)
2. **Orientation** — Entitlement vs Contribution
3. **Radius** — Self-Centric vs Altrocentric (Perspective)

The key constraint:  
**No LLM is used at runtime.**  
All intelligence is encoded into the structure of the tree.

---

## Repository Structure
dt-reflection-agent/
│
├── tree/
│ └── reflection-tree.tsv # Part A: Deterministic decision tree
│
├── agent/
│ └── main.py # Part B: CLI agent
│
├── transcripts/
│ ├── persona1.md # Sample run (victim / entitlement / self-centric)
│ └── persona2.md # Sample run (victor / contribution / altrocentric)
│
└── README.md


---

## Part A: Reflection Tree Design

### Description

The reflection system is implemented as a **structured decision tree** stored in a TSV file.

Each node in the tree represents a step in the conversation:
- Questions (with fixed options)
- Decisions (routing logic)
- Reflections (insights)
- Bridges (axis transitions)
- Summary and End

### Key Properties

- Fully deterministic (same inputs → same outputs)
- No free-text input (fixed options only)
- Structured branching using decision rules
- Signal-based state tracking for each axis

### Node Schema

| Field | Description |
|------|------------|
| id | Unique node identifier |
| parentId | Parent node |
| type | Node type (question, decision, reflection, etc.) |
| text | Display text |
| options | Choices or decision rules |
| target | Jump target (for bridges) |
| signal | Axis signal (used for scoring) |

---

## Part B: Deterministic Agent

### Description

A **CLI-based agent** that:
- Loads the tree from `reflection-tree.tsv`
- Walks through nodes step-by-step
- Collects user responses
- Applies deterministic branching logic
- Tracks axis signals
- Generates a final reflection summary

### Features

- No AI/LLM usage
- Data-driven architecture (tree is external)
- State tracking (answers + axis scores)
- Text interpolation in summary
- Deterministic execution

---

## How to Run

### Requirements
- Python 3.x

### Steps

```bash
cd agent
python main.py
