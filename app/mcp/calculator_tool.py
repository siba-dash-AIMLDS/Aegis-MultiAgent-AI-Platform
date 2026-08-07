class CalculatorTool:

    def calculate(self, expression):

        try:

            result = eval(expression)

            return str(result)

        except Exception:

            return "Invalid expression."