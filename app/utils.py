


class NumberAnalyzer:
    def __init__(self, number):
        self.number = number
        self.result = self.analyze_number()

    @staticmethod
    def is_armstrong(n):
        """Check if the number is an Armstrong number."""
        num_str = str(n)
        power = len(num_str)
        return n == sum(int(digit) ** power for digit in num_str)

    @staticmethod
    def is_prime(n):
        """Check if the number is a prime number."""
        if n <= 1:
            return False
        for i in range(2, int(n ** 0.5) + 1):
            if n % i == 0:
                return False
        return True

    @staticmethod
    def is_perfect(n):
        """Check if the number is a perfect number."""
        return n == sum(i for i in range(1, n) if n % i == 0)

    @staticmethod
    def digit_sum(n):
        """Calculate the sum of the digits of the number."""
        return sum(int(digit) for digit in str(n))

    def analyze_number(self):
        """Return a dictionary with the analysis of the number."""
        result = {}

        # Check Armstrong
        armstrong_check = self.is_armstrong(self.number)
        result["armstrong"] = armstrong_check

        # Determine odd or even
        if armstrong_check:
            result["type"] = "even" if self.number % 2 == 0 else "odd"
        else:
            result["type"] = "even" if self.number % 2 == 0 else "odd"

            # Check prime
        result["prime"] = self.is_prime(self.number)

        # Check perfect
        result["perfect"] = self.is_perfect(self.number)

        # Calculate digit sum
        result["digit_sum"] = self.digit_sum(self.number)

        return result