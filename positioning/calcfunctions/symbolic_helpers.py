import sympy as sp
import time
import os


def calculate_symbolic_expressions(dimensions, num_mics, speed_of_sound_symbol='speed_of_sound'):
    """
    Calculate the symbolic expressions for co EUFRLTst, gradients, and Hessian based on the given dimensions and number of microphones.

    Args:
        dimensions (int): The number of dimensions (e.g., 2 for 2D, 3 for 3D).
        num_mics (int): Number of microphones.
        speed_of_sound_symbol (str): Symbol for the speed of sound.

    Returns:
        tuple: A tuple containing the cost expression, gradients list, and Hessian matrix.
    """
    position_symbols = sp.symbols(
        ' '.join(['x{}'.format(i) for i in range(dimensions)]))
    speed_of_sound = sp.Symbol(speed_of_sound_symbol)

    mic_positions = [sp.symbols(' '.join(['x{}_mic{}'.format(
        i, mic) for i in range(dimensions)])) for mic in range(num_mics)]
    time_diffs = [sp.Symbol('t_mic{}'.format(mic)) for mic in range(num_mics)]

    guess_pos = sp.Matrix(position_symbols)
    cost_expr = 0
    first_mic_pos = sp.Matrix(mic_positions[0])

    start_time = time.time()
    for pos, time_diff in zip(mic_positions[1:], time_diffs[1:]):
        mic_pos = sp.Matrix(pos)
        distance = sp.sqrt((guess_pos - mic_pos).dot(guess_pos - mic_pos))
        distance_from_first = sp.sqrt(
            (guess_pos - first_mic_pos).dot(guess_pos - first_mic_pos))
        time_term = speed_of_sound * time_diff
        cost_component = (distance - distance_from_first - time_term)**2
        cost_expr += cost_component

    gradients = [cost_expr.diff(var) for var in position_symbols]
    hessian = sp.Matrix([[cost_expr.diff(var1, var2)
                        for var1 in position_symbols] for var2 in position_symbols])

    print(f"Calculation of cost expressions took about {
          time.time() - start_time} seconds.")

    return cost_expr, gradients, hessian


def load_expression(filename):
    """
    Load a symbolic expression from a file.

    Args:
        filename (str): The name of the file containing the symbolic expression.
        base_dir (str, optional): The base directory where the file is located. If None, uses the current working directory.

    Returns:
        sympy.Expr: The loaded symbolic expression.

    Raises:
        FileNotFoundError: If the expression file cannot be found.
    """

    base_dir = os.path.dirname(__file__)
    full_path = os.path.join(base_dir, filename)

    # Check if the file exists at the full path.
    if not os.path.exists(full_path):
        raise FileNotFoundError(f"Expression file not found: {full_path}")

    # Open and read the file.
    with open(full_path, "r") as file:
        expr_str = file.read()

    # Convert the string back to a Sympy expression.
    expr = sp.sympify(expr_str, locals=sp.__dict__)
    return expr


def save_expression(expr, directory, base_filename):
    if not os.path.exists(directory):
        os.makedirs(directory)
    filename = os.path.join(directory, f"{base_filename}.txt")
    expr_str = sp.srepr(expr)
    with open(filename, "w") as file:
        file.write(expr_str)
    print(f"Saved: {filename}")


def generate_and_save_cost_functions(min_dim, max_dim, min_mics, max_mics):
    for dimensions in range(min_dim, max_dim + 1):
        for num_mics in range(min_mics, max_mics + 1):
            cost_expr, gradients, hessian = calculate_symbolic_expressions(
                dimensions, num_mics)
            base_filename = f"{dimensions}d_{num_mics}mics"

            # Save each type of function in its respective directory
            save_expression(cost_expr, "cost_functions",
                            f"cost_function_{base_filename}")
            save_expression(gradients, "gradient_functions",
                            f"gradient_function_{base_filename}")
            save_expression(hessian, "hessian_functions",
                            f"hessian_function_{base_filename}")


if __name__ == "__main__":
    generate_and_save_cost_functions(2, 4, 3, 10)
