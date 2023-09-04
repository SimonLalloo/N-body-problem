import numpy as np
import scipy as sp

# Test stuff
def print_values():
    print("file")
    print(file)

    print("x")
    print(position_x)

    print("y")
    print(position_y)

    print("mass")
    print(mass)

    print("v_x")
    print(velocity_x)

    print("v_y")
    print(velocity_y)

    print("f_x")
    print(forces_x)

    print("f_y")
    print(forces_y)



# This is a vector
# This is the 'thick' r from the pdf
def distance(i, j):
    x = (position_x[i] - position_x[j])
    y = (position_y[i] - position_y[j])
    return np.array([x, y])



# This is the 'thin' r from the pdf
def r(i, j):
    x = (position_x[i] - position_x[j])
    y = (position_y[i] - position_y[j])
    return np.sqrt(x ** 2 + y ** 2)



def calculate_force(i, j):
    return -G * mass[i] * mass[j] * distance(i, j) / (r(i, j) + epsilon) ** 3



def calc_forces():
    for i in range (0, particle_count - 1):
        for j in range (i, particle_count):
            # Calculate force
            (force_x, force_y) = calculate_force(i, j)
            forces_x[i][j] = force_x
            forces_y[i][j] = force_y



def move_particles():
    # Calculate total force on a particle
    # Calculate particle velocity
    # Update particle position



###############################################################################

# Init stuff
path = "/home/simon/repos/N-body-problem/Nbody/Nbody/input_data/circles_N_2.gal"
file = np.fromfile(path, dtype=float)
steps = 2

# TODO: look at (reshape array)

position_x  = file[0::6]
position_y  = file[1::6]
mass        = file[2::6]
velocity_x  = file[3::6]
velocity_y  = file[4::6]
brightness  = file[5::6]

# Numbers
particle_count = mass.shape[0];
epsilon = 10 ** -3
G = 100 / particle_count
timestep = 10 ** -5

# Array of all forces
forces_x    = np.zeros((particle_count, particle_count))
forces_y    = np.zeros((particle_count, particle_count))

for step in range(1, steps + 1):
    print("Step number:")
    print(step)

    # Calculate the forces between each particle pair
    calc_forces()
    # Calculate the total force & velocity, and move the particle
    move_particles()

    print(forces_x)
    # print_values()

# Put stuff into file
file.tofile("sol_N_2.gal")

# Add graphics with MatPlotLib using eon? function
