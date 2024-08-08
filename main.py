import argparse

import numpy_financial as npf

payments_dict = {
    1: 400,
    2: 0.1,
    3: 0.1,
    4: 0.1,
    5: 0.1,
    6: 0.1,
    7: 0.1,
    8: 0.1,
    9: 0.1,
    10: 0.1,
    11: 0.1,
    12: 0.1,
    13: 0.1,
    14: 0.1,
    15: 0.1,
    16: 0.1,
    17: 0.1,
    18: 0.1,
    19: 0.1,
    20: 0.1
}


def main():
    parser = argparse.ArgumentParser("years")
    parser.add_argument("years", help="Mortgage years", type=int)
    parser.add_argument("amount", help="Mortgage loan in pounds", type=int)
    parser.add_argument("rate", help="Mortgage interest rate", type=float)
    parser.add_argument("--overpay", help="Mortgage overpayments", action=argparse.BooleanOptionalAction)

    args = parser.parse_args()

    monthly = False

    amount = args.amount
    interest_rate = args.rate
    years = args.years
    overpay = args.overpay
    print(args.overpay)
    print(f'loan: £{amount}')
    print(f'years: {years}')
    print(f'interest rate: {interest_rate * 100:0.2f}%')

    interest_rate /= 1200
    payments = years * 12
    outstanding_yod = amount
    total_interest = 0
    total_principal = 0
    total_overpaid = 0

    monthly_payment = npf.pmt(interest_rate, payments, amount) * -1

    print(f'monthly payment: £{monthly_payment:0.2f}')

    print()

    for year in range(years):
        year += 1
        print(f"year {year}:")
        principal_yearly = 0
        overpayment = 0
        ended_month = 0
        interest_yearly = 0

        monthly_overpayment = payments_dict[year]
        if monthly_overpayment < 1:
            monthly_overpayment = outstanding_yod * monthly_overpayment / 12
        if monthly_overpayment - 1 > float(outstanding_yod) / 120:
            print(f"OVERPAYMENT TOO HIGH, reducing to {outstanding_yod / 120:0.2f}")
            monthly_overpayment = outstanding_yod / 120

        for month in range(12):
            monthly_interest = amount * interest_rate
            interest_yearly += monthly_interest
            if monthly_payment < amount:
                principal = monthly_payment - monthly_interest
                amount -= principal
                principal_yearly += principal
            else:
                principal = amount - monthly_interest
                principal_yearly += principal
                amount = 0

            if overpay:
                if monthly_overpayment < amount:
                    amount -= monthly_overpayment
                    overpayment += monthly_overpayment
                # else:
                #     # overpayment += monthly_overpayment
                #     amount = 0
                # if yearly_overpayment_percentage != 0:
                #     overpayment_percentage = outstanding_yod * yearly_overpayment_percentage / 12
                #     amount -= overpayment_percentage
                #     overpayment += overpayment_percentage
                # else:
                #     amount -= monthly_overpayment
                #     overpayment += monthly_overpayment
            if monthly:
                print(f'interest: {monthly_interest:0.2f}')
                print(f'principal: {principal + monthly_overpayment:0.2f}')
                print(f'balance: {amount:0.2f}')
            if amount <= 0:
                ended_month = month + 1
                break
        if not monthly:
            if ended_month > 0:
                months = ended_month
            else:
                months = 12
            interest = monthly_payment * months - principal_yearly
            total_interest += interest
            total_principal += principal_yearly
            print(f'interest: {interest_yearly:0.2f}')
            print(f'principal: {principal_yearly:0.2f}')
            print(f'balance: {amount:0.2f}')
            if overpayment > 0:
                total_overpaid += overpayment
                print(f'overpaid: {overpayment:0.2f}')
                print(f'monthly+overpay: {monthly_payment + overpayment / 12:0.2f}')

        if ended_month > 0:
            print(f"\nfinished after {year - 1} years {ended_month} months")

        outstanding_yod = amount
        if amount <= 0:
            break

        print()
    print(f"total interest: {total_interest:0.2f}")
    print(f"total principal: {total_principal:0.2f}")
    print(f"total overpaid: {total_overpaid:0.2f}")
    print(f"total: {total_interest + total_principal + total_overpaid:0.2f}")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
