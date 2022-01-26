from calendar import monthrange
import datetime

def daysLeftInMonth() -> int:
    now = datetime.datetime.now()
    num_days = monthrange(now.year, now.month)
    last_day = datetime.datetime(now.year, now.month, num_days[1])
    days_left = last_day - now
    return days_left.days

def calculateSplitFromDaysLeft(days_left, assetsToInvestInto, totalAmount, interval=5):
    
    investment_days_left = days_left/interval
    amount_per_investment_day = float(totalAmount)/float(investment_days_left)
    investment_per_asset = amount_per_investment_day / assetsToInvestInto
    return investment_per_asset

    return None



if __name__ == "__main__":
    print(daysLeftInMonth())
    print(calculateSplitFromDaysLeft(daysLeftInMonth(), 3, 700))
