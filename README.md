# Visualization and Comparative Analysis of BFS and A* Search Algorithms

This project presents a **visual and empirical comparison** of two classical pathfinding algorithms — **Breadth-First Search (BFS)** and **A\*** — implemented on a grid-based maze environment using **Python and Pygame**.

The primary objective is to complement theoretical coursework with **practical observation**, enabling a clearer understanding of algorithmic behavior through visualization and measured performance metrics.

## Objectives
- Visualize the step-by-step execution of BFS and A\* on a 2D maze
- Compare the algorithms based on:
  - Number of nodes explored
  - Path length
  - Execution time
- Study how heuristic guidance influences search efficiency

## Methodology
- The maze is modeled as a discrete grid with blocked and free cells.
- **BFS** explores nodes in increasing order of depth, guaranteeing the shortest path in an unweighted graph.
- **A\*** incorporates a *Manhattan distance heuristic* to prioritize nodes closer to the goal.
- Parent tracking is used to reconstruct the final path once the goal is reached.
- Performance metrics are recorded during execution and displayed in real time.

## Implementation
- **Language:** Python  
- **Library:** Pygame  
- **Algorithms:** Breadth-First Search (BFS), A\* Search  

### Controls
- Press **B** → Run BFS  
- Press **A** → Run A\*

## Motivation
This work was motivated by an introduction to search algorithms during coursework in the previous semester.  
The project aims to bridge the gap between **theoretical understanding and empirical behavior**, reinforcing concepts such as completeness, optimality, and computational efficiency.

## Supplementary Write-up
A short **technical paper** accompanies this project, including a brief literature overview and an analysis of observed algorithmic behavior.

## How to Run
```bash
pip install pygame
python main.py
