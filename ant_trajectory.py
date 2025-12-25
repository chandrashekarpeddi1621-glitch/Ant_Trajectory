"""
Ant-Inspired Path Integration Navigation
========================================

This script demonstrates a simplified, bio-inspired navigation strategy
based on the behavior of desert ants observed in the BBC Earth video.

-------------------------------------------------------
WHAT IS BEING MODELED
-------------------------------------------------------
Desert ants are able to:
1. Explore their environment using irregular paths
2. Continuously track their displacement from the nest (path integration)
3. Periodically reorient using the Sun as a compass (scanning behavior)
4. Return to the nest along a nearly straight path

This simulation abstracts that behavior into a simple 2D model.

-------------------------------------------------------
INTERPRETATION OF THE PLANE
-------------------------------------------------------
• The X–Y plane represents the horizontal ground plane.
• X-axis and Y-axis are orthogonal spatial directions on the ground.
• All motion occurs in this flat, two-dimensional space.

-------------------------------------------------------
BIOLOGICAL INTERPRETATION OF VISUAL ELEMENTS
-------------------------------------------------------
• Blue path  : Actual exploratory path taken by the ant
• Green arrow: Internal displacement vector (ant's memory)
• Red path   : Direct returning path (inverse of the memory vector)
• Black dot  : Current ant position

IMPORTANT:
The ant does NOT remember the blue path.
It only remembers the green arrow.

-------------------------------------------------------
MODELING ASSUMPTIONS
-------------------------------------------------------
1. The environment is flat and two-dimensional.
2. The Sun provides a fixed global reference direction.
3. Distance is estimated via constant step length (idealized pedometer).
4. Directional error accumulates during movement.
5. Periodic scanning partially corrects this error.
6. No landmarks or pheromone trails are used.
7. Noise is minimal and symmetric.

These assumptions intentionally simplify real biology
to highlight the core navigation principle.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# =====================================================
# SIMULATION PARAMETERS
# =====================================================

np.random.seed(1)          # Ensures reproducibility

step_length = 0.5          # Distance traveled per step
num_explore_steps = 120    # Number of steps during exploration

scan_interval = 10         # How often the ant performs scanning
scan_gain = 0.1            # Strength of heading correction during scan

sun_direction = 0.0        # Global compass reference (radians)
                           # Defines the x-axis direction

# =====================================================
# STATE VARIABLES
# =====================================================

# True physical position of the ant
x, y = 0.0, 0.0

# Integrated displacement vector (ant's internal memory)
Dx, Dy = 0.0, 0.0

# Current heading of the ant (relative to Sun)
theta = 0.0

# History storage (used only for visualization)
explore_x = [x]
explore_y = [y]
Dx_hist = [Dx]
Dy_hist = [Dy]
theta_hist = [theta]

# =====================================================
# EXPLORATION PHASE (SEARCHING FOR FOOD)
# =====================================================

for step in range(num_explore_steps):

    # Random change in heading: exploratory behavior
    theta += np.random.uniform(-np.pi / 4, np.pi / 4)

    # Physical movement in the current direction
    dx = step_length * np.cos(theta)
    dy = step_length * np.sin(theta)

    x += dx
    y += dy

    # Path integration:
    # The ant updates its internal estimate of displacement
    Dx += dx
    Dy += dy

    # Periodic scanning:
    # Ant rechecks Sun direction to reduce compass drift
    if step % scan_interval == 0:
        theta -= scan_gain * (theta - sun_direction)

    # Store history for later visualization
    explore_x.append(x)
    explore_y.append(y)
    Dx_hist.append(Dx)
    Dy_hist.append(Dy)
    theta_hist.append(theta)

# Food location (end of exploration)
food_x, food_y = x, y

# =====================================================
# RETURNING TO NEST
# =====================================================

# Resultant displacement vector (from nest to food)
R_mag = np.sqrt(Dx**2 + Dy**2)      # Distance to nest
R_angle = np.arctan2(Dy, Dx)        # Direction of resultant vector

# To return home, the ant walks in the opposite direction
home_angle = R_angle + np.pi
num_home_steps = int(R_mag / step_length)

home_x = [food_x]
home_y = [food_y]

for _ in range(num_home_steps):
    food_x += step_length * np.cos(home_angle)
    food_y += step_length * np.sin(home_angle)
    home_x.append(food_x)
    home_y.append(food_y)

# =====================================================
# STATIC SUMMARY PLOT
# =====================================================

plt.figure(figsize=(6, 6))

# Actual paths
plt.plot(explore_x, explore_y, label="Exploration Path", color="blue")
plt.plot(home_x, home_y, label="Returning Path", color="red", linewidth=2)

# Resultant displacement vector (shown for understanding)
plt.arrow(
    0, 0, Dx, Dy,
    color="green",
    width=0.05,
    length_includes_head=True
)

# Key reference points
plt.scatter(0, 0, c="green", s=80, label="Nest")
plt.scatter(explore_x[-1], explore_y[-1], c="orange", s=80, label="Food")

plt.xlabel("X position (ground plane)")
plt.ylabel("Y position (ground plane)")
plt.title("Ant-Inspired Path Integration – Summary View")
plt.axis("equal")
plt.grid(True)
plt.legend()
plt.savefig("ant_navigation_plot.png", dpi=300)
plt.show()

# =====================================================
# ANIMATION (PROCESS VIEW)
# =====================================================

# Determine plot limits dynamically
all_x = explore_x + home_x
all_y = explore_y + home_y
margin = 2

fig, ax = plt.subplots(figsize=(6, 6))
ax.set_xlim(min(all_x) - margin, max(all_x) + margin)
ax.set_ylim(min(all_y) - margin, max(all_y) + margin)
ax.set_aspect("equal")
ax.grid(True)

# Visual elements
line_explore, = ax.plot([], [], "b-", label="Exploration Path")
line_home, = ax.plot([], [], "r-", linewidth=2, label="Returning Path")
ant_dot, = ax.plot([], [], "ko", markersize=6)

# Dummy line to show resultant vector in legend
vector_legend, = ax.plot([], [], color="green", linewidth=2,
                         label="Resultant Vector")

# Actual arrow representing the resultant vector
vector_arrow = ax.arrow(0, 0, 0, 0, color="green",
                        width=0.05, length_includes_head=True)

# Text box showing live computed values
info_text = ax.text(
    0.02, 0.98, "",
    transform=ax.transAxes,
    verticalalignment="top",
    fontsize=9,
    bbox=dict(boxstyle="round", facecolor="white", alpha=0.85)
)

ax.scatter(0, 0, c="green", s=80, label="Nest")
ax.scatter(explore_x[-1], explore_y[-1], c="orange", s=80, label="Food")
ax.legend(loc="lower left")

def update(frame):
    """
    Update function for animation.
    Shows how the displacement vector is accumulated during exploration
    and then directly used for Returning.
    """
    global vector_arrow
    vector_arrow.remove()

    if frame < len(explore_x):
        # Exploration phase
        line_explore.set_data(explore_x[:frame], explore_y[:frame])
        ant_dot.set_data([explore_x[frame]], [explore_y[frame]])

        Rx, Ry = Dx_hist[frame], Dy_hist[frame]
        Rm = np.sqrt(Rx**2 + Ry**2)
        th = theta_hist[frame]

        vector_arrow = ax.arrow(
            0, 0, Rx, Ry,
            color="green",
            width=0.05,
            length_includes_head=True
        )

        info_text.set_text(
            "Exploration Phase\n"
            f"x = {explore_x[frame]:.2f}, y = {explore_y[frame]:.2f}\n"
            f"Dx = {Rx:.2f}, Dy = {Ry:.2f}\n"
            f"|R| = {Rm:.2f}\n"
            f"θ = {np.degrees(th):.1f}°"
        )

    else:
        # Returing phase
        f = frame - len(explore_x)
        if f < len(home_x):
            line_home.set_data(home_x[:f], home_y[:f])
            ant_dot.set_data([home_x[f]], [home_y[f]])

            vector_arrow = ax.arrow(
                0, 0, Dx, Dy,
                color="green",
                width=0.05,
                length_includes_head=True
            )

            info_text.set_text(
                "Returning Phase\n"
                f"|R| = {R_mag:.2f}\n"
                f"θ_R = {np.degrees(R_angle):.1f}°\n"
                "Walking along −R"
            )

    return line_explore, line_home, ant_dot, vector_arrow, info_text

ani = animation.FuncAnimation(
    fig,
    update,
    frames=len(explore_x) + len(home_x),
    interval=100,
    blit=False
)

ani.save("ant_navigation.gif", writer="pillow")
plt.close()

print("Generated files:")
print("• ant_navigation_plot.png")
print("• ant_navigation.gif")
