import random


class Universe(object):
    """Class representing a Game of Life universe."""
    def __init__(self, cells):
        self.cells = frozenset(cells)

    @classmethod
    def randomized(cls, width, height):
        """Returns a randomized Game of Life universe of the given dimensions"""
        seed = [(x, y)
                for x in xrange(width)
                for y in xrange(height)
                if random.choice([True, False])]

        return cls(seed)

    def next(self):
        """Evolves the universe one generation.

        Returns False if the new state is the same as the previous one.
        """

        next_generation = []

        interesting_cells = set([])  # Living cells and their neighbours

        for cell in self.cells:
            interesting_cells.add(cell)
            interesting_cells.update(self.neighbours(cell))

        for cell in interesting_cells:
            if self.outcome(cell) == True:
                next_generation.append(cell)

        next_generation = frozenset(next_generation)

        # Basic stability check
        if self.cells == next_generation:
            return False
        else:
            self.cells = next_generation
            return True

    @staticmethod
    def neighbours(cell):
        """Returns the coordinates of a cell's neighbours."""
        x, y = cell
        neighbours = [(x + dx, y + dy)
                      for dx in (-1, 0, 1)
                      for dy in (-1, 0, 1)
                      if not ((dx == 0) and (dy == 0))]

        return neighbours

    def living_neighbours(self, coord):
        """Returns the number of living cells surrounding a coordinate."""
        return len(set(self.neighbours(coord)) & self.cells)

    def outcome(self, cell):
        """Returns the state a cell should have in the next generation."""
        is_alive = cell in self.cells
        return self.rules(is_alive, self.living_neighbours(cell))

    @staticmethod
    def rules(is_alive, living_neighbours):
        """Applies the Game of Life rules.

        Returns the outcome for a cell based on its current state and the
        number of living cells that surround it.
        """
        if is_alive and living_neighbours in (2, 3):
            return True
        elif not is_alive and living_neighbours == 3:
            return True
        else:
            return False

    def __iter__(self):
        return self

    def __repr__(self):
        cells = self.cells
        margin = 10
        sorted_x, sorted_y = map(sorted, zip(*cells))
        min_x, max_x = sorted_x[0], sorted_x[-1]
        min_y, max_y = sorted_y[0], sorted_y[-1]
        rows = []
        for y in xrange(min_y - margin, max_y + margin + 1):
            row = ''
            for x in xrange(min_x - margin, max_x + margin + 1):
                row += 'x' if (x, y) in cells else '.'
            rows.append(row)
        return '\n'.join(rows) + '\n'
