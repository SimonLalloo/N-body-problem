import numpy as np
import scipy as sp
import matplotlib.pyplot as plt

# Returns a vector describing the distance between two bodies
def distance(i, j):
    x = (position_x[i] - position_x[j])
    y = (position_y[i] - position_y[j])
    return np.array([x, y])



# Returns the length of the distance vector
def r(distance):
    return np.sqrt(distance[0] ** 2 + distance[1] ** 2)



# Calculates the force between the given pair of particles using newton's law
# of universal gravity
def calc_force(i, j):
    dist = distance(i,j)
    forces[i][j] = -G * mass[i] * mass[j] * dist / (r(dist) + epsilon) ** 3



# Calculates the force between each pair of particles
def calc_forces():
    for i in range (0, particle_count - 1):
        for j in range (i + 1, particle_count):
            force = calc_force(i, j)



# Calculates the acceleration on a particle based on the force applied to it
def acceleration(i, force):
    return force / mass[i]



# Updates the velocity of a particle based on the force applied to it
def update_velocity(i, force):
    delta_v = timestep * acceleration(i, force)
    velocity_x[i] = velocity_x[i] + delta_v[0]
    velocity_y[i] = velocity_y[i] + delta_v[1]



# Updates the position of a particle based on its velocity
def update_position(i):
    position_x[i] = position_x[i] + timestep * velocity_x[i]
    position_y[i] = position_y[i] + timestep * velocity_y[i]



# Calculates the total forces on a particle, then updates velocity and position
def move_particles():
    # Loops over each particle
    for i in range (0, particle_count):
        total_force = 0

        # Sums the forces applied on that particle by each other particle
        for j in range (0, particle_count):
            if i == j:
                continue
            elif i < j:
                total_force += forces[i][j]
            else :
                total_force -= forces[j][i]

        update_velocity(i, total_force)
        update_position(i)



###############################################################################

# Hardcoded paths because we're lazy
path = "/home/simon/repos/N-body-problem/Nbody/Nbody/input_data/sun_and_planets_N_4.gal"
# Arvids path #
# path = "/home/arvid/Plugg/NumSim/N-body-problem/Nbody/Nbody/input_data/ellipse_N_00010.gal"

# Read input file
file = np.fromfile(path, dtype=float)

# Parse the inputs into arrays for each value
position_x  = file[0::6]
position_y  = file[1::6]
mass        = file[2::6]
velocity_x  = file[3::6]
velocity_y  = file[4::6]

# Define some numbers
steps = 200
particle_count = mass.shape[0];
epsilon = 10 ** -3
G = 100 / particle_count
timestep = 10 ** -5

# Make a 2D array that contains the forces between each pair of particles
forces = np.zeros((particle_count, particle_count, 2))

print("Step number 0")

# Make the plot
plot = plt.scatter(position_x, position_y)
plt.axis([0, 1, 0, 1])
plt.ion()

for step in range(1, steps + 1):
    print("Step number", step)

    # Calculate the forces between each pair of particles
    calc_forces()
    # Calculate the total force applied on each particle
    # Use that to calculate velocity, then move the particle
    move_particles()
    
    # Update the plot
    plot.set_offsets(np.c_[position_x, position_y])
    plt.pause(0.0001)

# Make output file
file.tofile("results.gal")

# Make the graph not disappear when the simulation ends
plt.show()
