import pygame
from numpy import array
from math import radians, cos, sin

X, Y, Z = 0, 1, 2

def rotation_matrix(alpha, beta, gamma):
    """
    rotation matrix of alpha, beta, gamma degrees around x, y, z axes (respectively)
    """
    alpha_rad = radians(alpha)
    beta_rad = radians(beta)
    gamma_rad = radians(gamma)

    s_alpha, c_alpha = sin(alpha_rad), cos(alpha_rad)
    s_beta, c_beta = sin(beta_rad), cos(beta_rad)
    s_gamma, c_gamma = sin(gamma_rad), cos(gamma_rad)

    return (
        (c_beta * c_gamma, -c_beta * s_gamma, s_beta),
        (c_alpha * s_gamma + s_alpha * s_beta * c_gamma, c_alpha * c_gamma - s_gamma * s_alpha * s_beta, -c_beta * s_alpha),
        (s_gamma * s_alpha - c_alpha * s_beta * c_gamma, c_alpha * s_gamma * s_beta + s_alpha * c_gamma, c_alpha * c_beta)
    )

class Physical:
    def __init__(self, vertices, edges):
        """
        a 3D object that can rotate around the three axes
        :param vertices: a tuple of points (each has 3 coordinates)
        :param edges: a tuple of pairs (each pair is a set containing 2 vertices' indexes)
        """
        self.__vertices = array(vertices)
        self.__edges = tuple(edges)
        self.__rotation = [0, 0, 0]  # radians around each axis

    def rotate(self, axis, theta):
        self.__rotation[axis] += theta

    @property
    def lines(self):
        location = self.__vertices.dot(rotation_matrix(*self.__rotation))  # an index->location mapping
        return ((location[v1], location[v2]) for v1, v2 in self.__edges)

BLACK, RED = (0, 0, 0), (255, 128, 128)

class Paint:
    def __init__(self, shape, keys_handler):
        self.__shape = shape
        self.__keys_handler = keys_handler
        self.__size = 1000, 1000
        self.__clock = pygame.time.Clock()
        self.__screen = pygame.display.set_mode(self.__size)
        self.__mainloop()

    def __fit(self, vec):
        """
        ignore the z-element (creating a very cheap projection), and scale x, y to the coordinates of the screen
        """
        return [round(70 * coordinate + frame / 2) for coordinate, frame in zip(vec, self.__size)]

    def __handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
        self.__keys_handler(pygame.key.get_pressed())

    def __draw_shape(self, thickness=4):
        for start, end in self.__shape.lines:
            pygame.draw.line(self.__screen, RED, self.__fit(start), self.__fit(end), thickness)

    def __mainloop(self):
        while True:
            self.__handle_events()
            self.__screen.fill(BLACK)
            self.__draw_shape()
            pygame.display.flip()
            self.__clock.tick(40)

def main():
    from pygame import K_q, K_w, K_a, K_s, K_z, K_x

    cube_size = 0.2  # Fixed size of the cube

    cube_vertices = [((cube_size/2) * x, (cube_size/2) * y, (cube_size/2) * z) for x in (-1, 1) for y in (-1, 1) for z in (-1, 1)]

    cube_edges = ({0, 1}, {0, 2}, {2, 3}, {1, 3},
                  {4, 5}, {4, 6}, {6, 7}, {5, 7},
                  {0, 4}, {1, 5}, {2, 6}, {3, 7})

    cube = Physical(vertices=cube_vertices, edges=cube_edges)

    counter_clockwise = 5  # degrees
    clockwise = -counter_clockwise

    params = {
        K_q: (X, clockwise),
        K_w: (X, counter_clockwise),
        K_a: (Y, clockwise),
        K_s: (Y, counter_clockwise),
        K_z: (Z, clockwise),
        K_x: (Z, counter_clockwise),
    }

    def keys_handler(keys):
        for key in params:
            if keys[key]:
                cube.rotate(*params[key])

    pygame.init()
    pygame.display.set_caption('Control -   q,w : X    a,s : Y    z,x : Z')
    Paint(cube, keys_handler)

if __name__ == '__main__':
    main()
