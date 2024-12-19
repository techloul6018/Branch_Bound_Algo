import pandas as pd

class BranchAndBoundSolver:
    def __init__(self, revenues, days, max_days):
        self.revenues = revenues
        self.days = days
        self.max_days = max_days
        self.num_projects = len(revenues)
        self.best_solution = None
        self.best_value = 0

    def solve(self):
        self._branch_and_bound([], 0, 0, 0)

    def _branch_and_bound(self, current_solution, current_value, current_days, level):
        if current_days > self.max_days:
            return

        if level == self.num_projects:
            if current_value > self.best_value:
                self.best_value = current_value
                self.best_solution = current_solution
            return

        self._branch_and_bound(
            current_solution + [1],
            current_value + self.revenues[level],
            current_days + self.days[level],
            level + 1
        )

        self._branch_and_bound(
            current_solution + [0],
            current_value,
            current_days,
            level + 1
        )

    def get_solution(self):
        return self.best_solution, self.best_value

if __name__ == "__main__":
    try:
        file_path = input("Enter the path to the Excel file containing the project data: ")
        data = pd.read_excel(file_path)
        revenues = data['Revenue'].tolist()
        days = data['Days'].tolist()
    except Exception as e:
        print("Error reading the Excel file:", e)
        exit()

    try:
        max_days = int(input("Enter the maximum number of researcher days available: "))
    except ValueError:
        print("Invalid input. Using default value of 100 days.")
        max_days = 100

    solver = BranchAndBoundSolver(revenues, days, max_days)

    solver.solve()

    best_solution, best_value = solver.get_solution()

    print("Best solution:", best_solution)
    print("Maximum revenue:", best_value)
