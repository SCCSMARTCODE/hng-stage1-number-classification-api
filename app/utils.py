class NumberAnalyzer:
    def __init__(self, number: int):
        self.number = number
        self.result = self.analyze_number()

    @staticmethod
    def is_armstrong(n: int) -> bool:
        """Check if the number is an Armstrong number."""
        num_str = str(n)
        power = len(num_str)
        return n == sum(int(digit) ** power for digit in num_str)

    @staticmethod
    def is_prime(n: int) -> bool:
        """Check if the number is a prime number."""
        if n <= 1:
            return False
        for i in range(2, int(n ** 0.5) + 1):
            if n % i == 0:
                return False
        return True

    @staticmethod
    def is_perfect(n: int) -> bool:
        """Check if the number is a perfect number."""
        return n == sum(i for i in range(1, n) if n % i == 0)

    @staticmethod
    def digit_sum(n: int) -> int:
        """Calculate the sum of the digits of the number."""
        return sum(int(digit) for digit in str(n))

    def analyze_number(self) -> dict:
        """Return a dictionary with the analysis of the number."""
        return {
            "armstrong": self.is_armstrong(self.number),
            "prime": self.is_prime(self.number),
            "perfect": self.is_perfect(self.number),
            "digit_sum": self.digit_sum(self.number)
        }
