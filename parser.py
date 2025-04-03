import re

class Parser:
    # Parses the given expression and returns its evaluated representation.
    def parse_expression(self, expression):
        expression = expression.strip()  # Remove leading/trailing spaces

        # Check for quotation
        if expression.startswith("'"):
            return ['quote', self.parse_expression(expression[1:].strip())]

        # Check for numbers (positive or negative)
        if self.is_number(expression):
            return int(expression)  # Convert valid number string to integer

        # Check for list expressions (parenthesis)
        if self.is_list(expression):
            tokens = self.tokenize(expression)
            return self.parse_list(tokens[1:-1])  # Parse the list content excluding parentheses

        # Return the symbol itself if not a number or list (variable or function)
        return expression

    # Checks if the given expression is a valid number (positive or negative).
    def is_number(self, expression):
        return expression[0] == '-' and expression[1:].isdigit() or expression.isdigit()

    # Checks if the given expression is a list (enclosed in parentheses).
    def is_list(self, expression):
        return expression.startswith('(') and expression.endswith(')')

    # Parses a list of tokens and returns the corresponding nested expressions.
    def parse_list(self, tokens):
        parsed_tokens = []
        while tokens:
            token = tokens.pop(0)  # Get the first token

            if token == '(':
                # Nested list, handle recursively
                sub_expr = self.extract_sublist(tokens)
                parsed_tokens.append(self.parse_list(sub_expr))
            elif token == ')':
                raise SyntaxError("Unexpected closing parenthesis")
            elif token == "'":
                # Handle quotation (only applies to the next expression)
                self.handle_quotation(tokens, parsed_tokens)
            else:
                # Regular token (either number, symbol, or function)
                parsed_tokens.append(self.parse_expression(token))

        return parsed_tokens

    # Handles the processing of quoted expressions (those starting with ').
    def handle_quotation(self, tokens, parsed_tokens):
        if not tokens:
            raise SyntaxError("Unexpected end after quote")
        next_token = tokens.pop(0)  # Get the token after the quote

        # Check if the quoted expression is a list
        if next_token == '(':
            # If it's a list, extract the entire sublist and parse it recursively
            sub_expr = self.extract_sublist(tokens)
            quoted_expr = self.parse_list(sub_expr) # Recursively parse the sublist
        else:
            # If it's not a list, just parse the token as an expression
            quoted_expr = self.parse_expression(next_token)

        # Append the quoted expression to the list of parsed tokens
        parsed_tokens.append(['quote', quoted_expr])

    # Tokenizes the input string into a list of symbols and parentheses.
    def tokenize(self, tokens_str):
        return re.findall(r'\(|\)|[^\s()]+', tokens_str)

    # Extracts a sublist of tokens from a nested parenthesis expression.
    def extract_sublist(self, tokens):
        sub_expr = []
        depth = 1  # Track nested parentheses
        while tokens:
            token = tokens.pop(0)
            if token == '(':
                depth += 1  # Deeper level of nesting
            elif token == ')':
                depth -= 1
                if depth == 0:
                    return sub_expr  # Return the token list when depth is 0 (matching parentheses)
            sub_expr.append(token)
        raise SyntaxError("Unmatched opening parenthesis")