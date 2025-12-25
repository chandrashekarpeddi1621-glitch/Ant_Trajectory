# Ant-Inspired Path Integration Navigation

## Overview
This project implements a simplified bio-inspired navigation model based on the foraging behavior of desert ants. The agent explores a two-dimensional environment using random motion while continuously integrating displacement vectors relative to a fixed Sun-based compass. After exploration, it returns directly to the nest by following the inverse of the accumulated displacement vector.

## Inputs (Configurable Parameters)
The following parameters are defined in the script:
- `step_length` – distance moved per step  
- `num_explore_steps` – number of exploration steps  
- `scan_interval` – frequency of orientation scanning  
- `scan_gain` – strength of heading correction during scanning  
- `sun_direction` – global reference direction (Sun compass)

## Outputs
Running the script generates:
- **ant_navigation_plot.png** – static summary of exploration and homing paths  
- **ant_navigation.gif** – animated visualization showing step-by-step path integration and homing  

## How to Run

### Requirements
- Python 3.8 or later  
- NumPy  
- Matplotlib  
- Pillow  

### Installation
```bash
pip install numpy matplotlib pillow
```
### Execution
```bash
python ant_navigation.py
```
## Key Assumptions
- **Flat, two-dimensional environment**  
- **Constant step length** (idealized distance estimation)  
- **Fixed global compass reference** (Sun)  
- **Periodic orientation correction** (scanning behavior)  
- **No landmarks, maps, or pheromone cues**

## Notes
The agent does not store the full exploratory path. Only the resultant displacement vector is retained and used for homing, reflecting the biological strategy observed in desert ants.
