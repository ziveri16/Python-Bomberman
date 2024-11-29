import math
Point = tuple[float, float]


class Actor:
    """Interface to be implemented by each game character.
    """

    def move(self, arena: "Arena"):
        """Called by Arena, at the actor’s turn.
        """
        raise NotImplementedError("Abstract method")

    def pos(self) -> Point:
        """Return the position (x, y) of the actor (left-top corner).
        """
        raise NotImplementedError("Abstract method")

    def size(self) -> Point:
        """Return the size (w, h) of the actor.
        """
        raise NotImplementedError("Abstract method")

    def sprite(self) -> Point | None:
        """Return the position (x, y) of current sprite,
        if it is contained in a larger image, with other sprites;
        Otherwise, simply return None.
        """
        raise NotImplementedError("Abstract method")


def check_collision(a1: Actor, a2: Actor) -> bool:
    """Check two actors (args) for mutual collision or contact,
    according to bounding-box collision detection.
    Return True if actors collide or touch, False otherwise.
    """
    x1, y1, w1, h1 = a1.pos() + a1.size()
    x2, y2, w2, h2 = a2.pos() + a2.size()
    return (y2 <= y1 + h1 and y1 <= y2 + h2 and
            x2 <= x1 + w1 and x1 <= x2 + w2)


class Arena:
    """A generic 2D game, with a given size in pixels and a list of actors.
    """

    def __init__(self, full_size: Point, view_size: Point):
        """Create an arena with given full dimensions in pixels and view size for scrolling.
        """
        self._full_w, self._full_h = full_size  # Dimensioni totali della mappa
        self._view_w, self._view_h = view_size  # Dimensioni della finestra visibile
        self._count = 0
        self._turn = -1
        self._actors = []
        self._curr_keys = self._prev_keys = tuple()
        self._collisions = []
        self._offset_x = 0  # Offset per lo scrolling orizzontale

    def spawn(self, a: Actor):
        """Register an actor into this arena.
        Actors are blitted in their order of registration.
        """
        if a not in self._actors:
            self._actors.append(a)

    def kill(self, a: Actor):
        """Remove an actor from this arena.
        """
        if a in self._actors:
            self._actors.remove(a)

    def tick(self, keys=[]):
        """Move all actors (through their own move method).
        """
        actors = list(reversed(self._actors))
        self._detect_collisions(actors)
        self._prev_keys = self._curr_keys
        self._curr_keys = keys
        for self._turn, a in enumerate(actors):
            a.move(self)
        self._count += 1

    def scroll(self, bomberman_x):
        """Update the horizontal offset to keep Bomberman near the center of the visible window."""
        center_x = self._view_w // 2
        max_offset = self._full_w - self._view_w

        # Scorri solo se Bomberman non è troppo vicino ai bordi della mappa
        if bomberman_x > center_x and bomberman_x < self._full_w - center_x:
            self._offset_x = min(max(bomberman_x - center_x, 0), max_offset)

    def offset(self) -> int:
        """Return the current horizontal offset for scrolling."""
        return self._offset_x

    def _naive_collisions(self, actors):
        # Calcola le collisioni usando un semplice confronto di tutti con tutti
        self._collisions.clear()
        for a1 in actors:
            colls1 = []
            for a2 in actors:
                if a1 is not a2 and check_collision(a1, a2):
                    colls1.append(a2)
            self._collisions.append(colls1)

    def _detect_collisions(self, actors):
        self._collisions.clear()
        tile_size = 32  # Assuming a tile size of 32x32 pixels

        # Calculate the grid dimensions
        grid_width = math.ceil(self._full_w / tile_size)
        grid_height = math.ceil(self._full_h / tile_size)
        grid = [[[] for _ in range(grid_width)] for _ in range(grid_height)]

        # Populate the grid with actor indexes
        for i, actor in enumerate(actors):
            x, y, w, h = actor.pos() + actor.size()
            for tx in range(max(0, int(x // tile_size)), min(grid_width, int((x + w) // tile_size) + 1)):
                for ty in range(max(0, int(y // tile_size)), min(grid_height, int((y + h) // tile_size) + 1)):
                    grid[ty][tx].append(i)

        # Check for collisions within each grid cell and its neighbors
        for i, actor in enumerate(actors):
            collisions = set()
            x, y, w, h = actor.pos() + actor.size()
            for tx in range(max(0, int(x // tile_size)), min(grid_width, int((x + w) // tile_size) + 1)):
                for ty in range(max(0, int(y // tile_size)), min(grid_height, int((y + h) // tile_size) + 1)):
                    for j in grid[ty][tx]:
                        if i != j and check_collision(actor, actors[j]):
                            collisions.add(actors[j])
            self._collisions.append(list(collisions))

    def collisions(self) -> list[Actor]:
        """Get list of actors colliding with current actor
        """
        t, colls = self._turn, self._collisions
        return colls[t] if 0 <= t < len(colls) else []

    def actors(self) -> list:
        """Return a copy of the list of actors.
        """
        return list(self._actors)

    def size(self) -> Point:
        """Return the visible size (width, height) of the arena.
        """
        return (self._view_w, self._view_h)

    def full_size(self) -> Point:
        """Return the full size (width, height) of the arena."""
        return (self._full_w, self._full_h)

    def count(self) -> int:
        """Return the total count of ticks (or frames).
        """
        return self._count

    def current_keys(self) -> list[str]:
        """Return the currently pressed keys.
        """
        return self._curr_keys

    def previous_keys(self) -> list[str]:
        """Return the keys pressed at last tick.
        """
        return self._prev_keys

