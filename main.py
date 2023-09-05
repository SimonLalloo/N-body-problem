import numpy as np
import scipy as sp
import matplotlib.pyplot as plt

# This is a vector
# This is the 'thick' r from the pdf
def distance(i, j):
    # print("i and j are", i, j)
    x = (position_x[i] - position_x[j])
    y = (position_y[i] - position_y[j])
    return np.array([x, y])



# This is the 'thin' r from the pdf
def r(distance):
    return np.sqrt(distance[0] ** 2 + distance[1] ** 2)



def calc_force(i, j):
    dist = distance(i,j)
    forces[i][j] = -G * mass[i] * mass[j] * dist / (r(dist) + epsilon) ** 3



def calc_forces():
    for i in range (0, particle_count - 1):
        for j in range (i + 1, particle_count):
            force = calc_force(i, j)



def acceleration(i, force):
    return force / mass[i]



def update_velocity(i, force):
    delta_v = timestep * acceleration(i, force)
    velocity_x[i] = velocity_x[i] + delta_v[0]
    velocity_y[i] = velocity_y[i] + delta_v[0]



def update_position(i):
    position_x[i] = position_x[i] + timestep * velocity_x[i]
    position_y[i] = position_y[i] + timestep * velocity_y[i]



def move_particles():
    for i in range (0, particle_count):
        total_force = 0

        for j in range (0, particle_count):
            if i == j:
                continue
            elif i < j:
                total_force += forces[i][j]
            else :
                total_force -= forces[j][i]

        # print("Particle", i, "has total force", total_force)
        update_velocity(i, total_force)
        update_position(i)



###############################################################################

# Init stuff
# path = "/home/simon/repos/N-body-problem/Nbody/Nbody/input_data/circles_N_4.gal"
path = "/home/simon/repos/N-body-problem/Nbody/Nbody/input_data/ellipse_N_00010.gal"
# path = "/home/simon/repos/N-body-problem/Nbody/Nbody/input_data/sun_and_planets_N_3.gal"

file = np.fromfile(path, dtype=float)
steps = 20000000

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
forces = np.zeros((particle_count, particle_count, 2))

print("Step number 0")
print("X coords", position_x)
print("Y coords", position_y)

# plt.ion()
plot = plt.scatter(position_x, position_y)
plt.axis([0, 1, 0, 1])

for step in range(1, steps + 1):
    print("Step number", step)

    # Calculate the forces between each pair of particles
    calc_forces()
    # Calculate the total force & velocity, then move the particle
    move_particles()

    # print("forces ", forces)
    # print("X coords", position_x)
    # print("Y coords", position_y)
    
    plot.set_offsets(np.c_[position_x, position_y])
    plt.pause(0.001)

# Put stuff into file
file.tofile("sol_N_2.gal")

# Add graphics with MatPlotLib using eon? function
plt.show()
