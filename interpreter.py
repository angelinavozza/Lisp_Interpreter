from parser import Parser
from env import Environment

class Interpreter:
    def __init__(self):
        self.parser = Parser()
        self.environment = Environment()

    def loop(self):
        """
        Main interpreter loop that takes user input, parses it, evaluates the expression,
        and prints and writes the result to a file until the user quits.
        """
        print("> Welcome to the fancy new Prompt LISP INTERPRETER, type in LISP commands! >")

        try:
            # Open the result file in append mode to log the output
            with open("results.file", "a") as result_file:
                while True:
                    # Get user input (LISP expression)
                    tokens_str = input("> ")

                    # Skip empty input
                    if tokens_str.strip() == "":
                        continue

                    # Handle special case for empty list
                    if tokens_str == "()":
                        print(">", "NIL")
                        result_file.write("NIL\n")
                        continue

                    # Exit condition for the interpreter
                    if tokens_str == "(quit)":
                        print("> bye")
                        return

                    try:
                        # Parse and evaluate the expression, then format the result
                        parsed_expression = interpreter.parser.parse_expression(tokens_str)
                        result = interpreter.environment.evaluate_expression(parsed_expression)
                        formatted_result = self.conv_cell(result)
                        
                        # Print and write the result
                        print(">", formatted_result)
                        result_file.write(formatted_result + "\n")
                    except Exception as e:
                        print(f"Error: {e}")  # Print error but continue execution
                        result_file.write(f"Error: {e}\n")

        except Exception as e:
            # Handle any errors during evaluation or execution
            print(f"Fatal error: {e}")
        finally:
            # Write EOF to the result file when the loop terminates
            with open("results.file", "a") as result_file:
                result_file.write("EOF\n")
   
    def conv_cell(self, cell):
        """
        Converts the given cell (LISP expression result) to its string representation.
        Converts lists to the proper LISP format, and None/empty lists to "NIL".
        """
        if cell is None or cell is False or cell == []:
            return "NIL"
        if cell is True:
            return "T"
        if isinstance(cell, list):
            # Recursively convert each element in the list and join them
            return f"({' '.join(map(self.conv_cell, cell))})"
        
        # Return the string representation of the cell (number or symbol)
        return str(cell)


interpreter = Interpreter()
interpreter.loop()
