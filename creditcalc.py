import math, argparse
import sys


class LoanCalculator:
    def __init__(self):
        self.args = None
        self.payment = None
        self.principle = None
        self.periods = None
        self.annuity = None
        self.interest = None

    def initialize_argparser(self):
        parser = argparse.ArgumentParser(description="This program calculates loan annuity, or differentiated payments")
        parser.add_argument("--type", choices=["annuity", "diff"], help="Choose between 'annuity' for annuity "
                                                                        "payment or 'diff' for differentiated")
        parser.add_argument("--payment", help="Enter monthly payment")
        parser.add_argument("--principal", help="Enter loan principal")
        parser.add_argument("--periods", help="The number of months needed to repay the loan")
        parser.add_argument("--interest", help="Must always be provided. Specified without a percent sign")
        self.args = parser.parse_args()
        self.principle = int(self.args.principal if self.args.principal else False)
        self.periods = int(self.args.periods if self.args.periods else False)
        self.interest = float(self.args.interest if self.args.interest else False)
        self.payment = float(self.args.payment if self.args.payment else False)

    def invalid(self):
        print("Incorrect parameters")
        sys.exit()

    def validate_inputs(self):
        if len(sys.argv) < 5:
            self.invalid()
        if self.args.type is None or self.args.type != "annuity" and self.args.type != "diff":
            print(self.args.type == "annuity")
            self.invalid()
        elif not self.args.interest:
            self.invalid()
        elif self.args.type == "diff" and self.args.payment:
            self.invalid()

    def process_inputs(self):
        self.interest = float(self.args.interest) / 12 / 100
        if self.args.type == "annuity":
            if not self.principle:
                self.get_principal()
            elif not self.periods:
                self.number_of_payments()
            else:
                self.annuity_payment()
        elif self.args.type == "diff":
            self.differentiated_payment()

    def differentiated_payment(self):
        total = 0
        for m in range(1, self.periods + 1):
            diff = math.ceil(self.principle / self.periods + self.interest * (self.principle - ((self.principle * (m - 1)) / self.periods)))
            print(f"Month {m}: payment is {diff}")
            total += diff
        overpayment = int(total - self.principle)
        print()
        print(f"Overpayment = {overpayment}")

    def annuity_payment(self):
        self.annuity = math.ceil(self.principle * ((self.interest * (1 + self.interest) ** self.periods) / ((1 + self.interest) ** self.periods - 1)))
        print(f"Your annuity payment = {self.annuity}!")
        overpayment = int(self.annuity * self.periods - self.principle)
        print(f"Overpayment: {overpayment}")

    def number_of_payments(self):
        months = math.ceil(math.log((self.payment / (self.payment - self.interest * self.principle)), 1 + self.interest))
        years = None
        if months > 11:
            years, months = months // 12, months % 12
        suffix, m_plural, y_plural = ["", "s"], months > 1, years > 1
        is_years = f"{int(years)} year{suffix[y_plural]} "
        is_months = f"{math.ceil(months)} month{suffix[m_plural]} "
        print(f"It will take {is_years if years else ''}{'and ' if years and months else ''}{is_months if months else ''}to repay this loan!")
        overpayment = math.ceil(((years * 12 + months) * self.payment) - self.principle)
        print(f"Overpayment = {overpayment}")

    def get_principal(self):
        self.principle = math.floor(self.payment / ((self.interest * (1 + self.interest) ** self.periods) / ((1 + self.interest) ** self.periods - 1)))
        print(f"Your loan principal = {self.principle}!")
        print(f"Overpayment = {int(self.payment * self.periods - self.principle)}")

if __name__ == '__main__':
    l1 = LoanCalculator()
    l1.initialize_argparser()
    l1.validate_inputs()
    l1.process_inputs()
