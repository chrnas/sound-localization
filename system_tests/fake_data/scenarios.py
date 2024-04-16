from generate_differences import (
    Point,
    Scenario,
    equilateral_triangle_center,
    equilateral_triangle_top
)

MICROPHONE_PLACEMENTS = (
    (Point(0, 0), Point(0, 15), equilateral_triangle_top(Point(0, 15))),
    (Point(0, 0), Point(0, 25), equilateral_triangle_top(Point(0, 25))),
    (Point(0, 0), Point(0, 35), equilateral_triangle_top(Point(0, 35))),
    (Point(0, 0, 0), Point(0, 30, 5.3), Point(30, 30, 0), Point(30, 0, 5.3))
)
SCENORIOS: tuple[Scenario, ...] = (
    # Scenarios equilateral triangle, side length 15m

    Scenario(
        Point(0, 0),
        MICROPHONE_PLACEMENTS[0],
        "[15m]: At microphone 1"
    ),
    Scenario(
        Point(0, 15),
        MICROPHONE_PLACEMENTS[0],
        "[15m]: At microphone 2"
    ),
    Scenario(
        equilateral_triangle_top(Point(0, 15)),
        MICROPHONE_PLACEMENTS[0],
        "[15m]: At microphone 3"
    ),
    Scenario(
        equilateral_triangle_center(Point(0, 15)),
        MICROPHONE_PLACEMENTS[0],
        "[15m]: Center of the triangle"
    ),
    Scenario(
        Point(10, 0),
        MICROPHONE_PLACEMENTS[0],
        "[15m]: Outside of the triangle"
    ),
    Scenario(
        Point(0, 7.5),
        MICROPHONE_PLACEMENTS[0],
        "[15m]: On the edge of the triangle"
    ),
    Scenario(
        Point(5, 5),
        MICROPHONE_PLACEMENTS[0],
        "[15m]: Inside of the triangle (1)"
    ),
    Scenario(
        Point(3, 10),
        MICROPHONE_PLACEMENTS[0],
        "[15m] Inside of the triangle (2)"
    ),

    # Scenarios equalateral triangle, side length 25m

    Scenario(
        Point(0, 0),
        MICROPHONE_PLACEMENTS[1],
        "[25m]: At microphone 1"
    ),
    Scenario(
        Point(0, 25),
        MICROPHONE_PLACEMENTS[1],
        "[25m]: At microphone 2"
    ),
    Scenario(
        equilateral_triangle_top(Point(0, 25)),
        MICROPHONE_PLACEMENTS[1],
        "[25m]: At microphone 3"
    ),
    Scenario(
        equilateral_triangle_center(Point(0, 25)),
        MICROPHONE_PLACEMENTS[1],
        "[25m]: Center of the triangle"
    ),
    Scenario(
        Point(10, 0),
        MICROPHONE_PLACEMENTS[1],
        "[25m]: Outside of the triangle"
    ),
    Scenario(
        Point(0, 10),
        MICROPHONE_PLACEMENTS[1],
        "[25m]: On the edge of the triangle"
    ),
    Scenario(
        Point(4, 11),
        MICROPHONE_PLACEMENTS[1],
        "[25m]: Inside of the triangle (1)"
    ),
    Scenario(
        Point(13, 13),
        MICROPHONE_PLACEMENTS[1],
        "[25m] Inside of the triangle (2)"
    ),

    # Scenarios equalateral triangle, side length 35m

    Scenario(
        Point(0, 0),
        MICROPHONE_PLACEMENTS[2],
        "[35m]: At microphone 1"
    ),
    Scenario(
        Point(0, 35),
        MICROPHONE_PLACEMENTS[2],
        "[35m]: At microphone 2"
    ),
    Scenario(
        equilateral_triangle_top(Point(0, 35)),
        MICROPHONE_PLACEMENTS[2],
        "[35m]: At microphone 3"
    ),
    Scenario(
        equilateral_triangle_center(Point(0, 35)),
        MICROPHONE_PLACEMENTS[2],
        "[35m]: Center of the triangle"
    ),
    Scenario(
        Point(10, 0),
        MICROPHONE_PLACEMENTS[2],
        "[35m]: Outside of the triangle"
    ),
    Scenario(
        Point(0, 10),
        MICROPHONE_PLACEMENTS[2],
        "[35m]: On the edge of the triangle"
    ),
    Scenario(
        Point(17.5, 17.5),
        MICROPHONE_PLACEMENTS[2],
        "[35m]: Inside of the triangle (1)"
    ),
    Scenario(
        Point(3, 27),
        MICROPHONE_PLACEMENTS[2],
        "[35m] Inside of the triangle (2)"
    ),

    # 3D scenarios

    Scenario(
        Point(15, 15, 0),
        MICROPHONE_PLACEMENTS[3],
        "[3D] Center of square"
    ),
    Scenario(
        Point(15, 15, 0),
        MICROPHONE_PLACEMENTS[3],
        "[3D] Center of square"
    ),
    Scenario(
        Point(15, 15, 0),
        MICROPHONE_PLACEMENTS[3],
        "[3D] Center of square"
    ),
    Scenario(
        Point(15, 15, 0),
        MICROPHONE_PLACEMENTS[3],
        "[3D] Center of square"
    ),
    Scenario(
        Point(15, 15, 0),
        MICROPHONE_PLACEMENTS[3],
        "[3D] Center of square"
    ),
    Scenario(
        Point(15, 15, 0),
        MICROPHONE_PLACEMENTS[3],
        "[3D] Center of square"
    ),
    Scenario(
        Point(15, 15, 0),
        MICROPHONE_PLACEMENTS[3],
        "[3D] Center of square"
    ),
    Scenario(
        Point(15, 15, 0),
        MICROPHONE_PLACEMENTS[3],
        "[3D] Center of square"
    ),
    Scenario(
        Point(15, 15, 0),
        MICROPHONE_PLACEMENTS[3],
        "[3D] Center of square"
    ),
    Scenario(
        Point(15, 15, 0),
        MICROPHONE_PLACEMENTS[3],
        "[35m] Inside of the triangle (2)"
    ),
    Scenario(
        Point(15, 15, 0),
        MICROPHONE_PLACEMENTS[3],
        "[35m] Inside of the triangle (2)"
    ),
    Scenario(
        Point(15, 15, 0),
        MICROPHONE_PLACEMENTS[3],
        "[35m] Inside of the triangle (2)"
    ),
)
