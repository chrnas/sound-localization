import numpy as np
import math
from scipy.optimize import minimize


# Multilateration class

class Multilateration:
    def __init__(self, v, delta_d, max_d):
        """
        Initialize the Multilateration object with the propagation speed,
        increments for radii, and the maximum distance.

        Args:
            v (int): Speed of transmission propagation.
            delta_d (int): Meter increments to radii of circles when generating locus of circle intersection.
            max_d (int): Max distance a transmission will be from the tower that first received the transmission.
        """
        self.v = v
        self.delta_d = delta_d
        self.max_d = max_d

    def get_locus(self, tower_1, tower_2, time_1, time_2):
        """
        Return a locus in x, y given two towers and their receive times.

        Args:
            tower_1 (tuple): (x, y) of one tower.
            tower_2 (tuple): (x, y) of the other tower.
            time_1 (float): Transmission receive time at tower_1.
            time_2 (float): Transmission receive time at tower_2.

        Returns:
            list of form [x, y], with x: list of x values of locus, y: list of y values of locus.
        """
        x0, x1, y0, y1 = [], [], [], []
        t_delta_d = abs(time_1 - time_2) * self.v
        if time_1 < time_2:
            circle1, circle2 = (
                tower_1[0], tower_1[1], 0), (tower_2[0], tower_2[1], t_delta_d)
        else:
            circle1, circle2 = (
                tower_2[0], tower_2[1], 0), (tower_1[0], tower_1[1], t_delta_d)

        for _ in range(int(self.max_d) // int(self.delta_d)):
            intersect = self.circle_intersection(circle1, circle2)
            if intersect is not None:
                x0.append(intersect[0][0])
                x1.append(intersect[1][0])
                y0.append(intersect[0][1])
                y1.append(intersect[1][1])

            circle1 = (circle1[0], circle1[1], circle1[2] + self.delta_d)
            circle2 = (circle2[0], circle2[1], circle2[2] + self.delta_d)

        x0.reverse()
        y0.reverse()
        x = x0 + x1
        y = y0 + y1

        return [x, y]

    def get_loci(self, rec_times, towers):
        """
        Return a set of loci on which a transmission may have occurred.

        Args:
            rec_times (np.array 1D): The times at which the towers received the transmission, in seconds.
            towers (np.array 2D): Locations of towers.

        Returns:
            list of tuples, where each tuple contains a list of x and a list of y elements.
        """
        if rec_times.shape[0] == 0:
            return []

        loci = []
        first_tower = int(np.argmin(rec_times))

        for j in [x for x in range(towers.shape[0]) if x != first_tower]:
            locus = self.get_locus(tower_1=(towers[first_tower][0], towers[first_tower][1]),
                                   tower_2=(towers[j][0], towers[j][1]),
                                   time_1=rec_times[first_tower],
                                   time_2=rec_times[j])
            if len(locus[0]) > 0:
                loci.append(locus)

        return loci

    @staticmethod
    def circle_intersection(circle1, circle2):
        """
        Calculate intersection points of two circles.

        Args:
            circle1: tuple(x, y, radius)
            circle2: tuple(x, y, radius)

        Returns:
            tuple of intersection points (which are (x, y) tuples)
        """
        x1, y1, r1 = circle1
        x2, y2, r2 = circle2
        dx, dy = x2 - x1, y2 - y1
        d = math.sqrt(dx ** 2 + dy ** 2)
        if d > r1 + r2 or d < abs(r1 - r2) or (d == 0 and r1 == r2):
            return None

        a = (r1 ** 2 - r2 ** 2 + d ** 2) / (2 * d)
        h = math.sqrt(r1 ** 2 - a ** 2)
        xm, ym = x1 + a * dx / d, y1 + a * dy / d
        xs1, xs2 = xm + h * dy / d, xm - h * dy / d
        ys1, ys2 = ym - h * dx / d, ym + h * dx / d

        return ((xs1, ys1), (xs2, ys2))

    def estimate_location(self, loci):
        """
        Estimate a single location from a set of loci using least squares optimization.
        """

        def objective_function(point, loci):
            # Check if point has exactly two elements; if not, raise an error
            if len(point) != 2:
                raise ValueError(
                    f"Expected point to have 2 elements, got {len(point)}")
            x, y = point  # Now safe to unpack
            total_distance = 0
            for locus in loci:
                locus_x, locus_y = locus
                distances = [(x - locus_x[i]) ** 2 + (y - locus_y[i])
                             ** 2 for i in range(len(locus_x))]
                min_distance = min(distances)
                total_distance += min_distance
            return total_distance

        # Flatten the loci into a list of points and ensure it's a 2D array
        points = np.array([(x, y) for locus in loci for x,
                          y in zip(locus[0], locus[1])])

        # Initial guess for the location is the mean of all points
        initial_guess = np.mean(points, axis=0)

        # Ensure initial_guess is explicitly shaped as a 2D array with one row and two columns
        # This should be a 1D array with two elements
        initial_guess = np.array(initial_guess)

        # Minimize the objective function to find the best estimate for the location
        result = minimize(objective_function, initial_guess,
                          args=(loci,), method='L-BFGS-B')

        if result.success:
            estimated_location = result.x
        else:
            raise Exception("Optimization failed")

        return tuple(estimated_location)
