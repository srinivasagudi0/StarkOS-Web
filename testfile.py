import datetime

# Create a custom date (Year, Month, Day)
my_date = datetime.date(2026, 7, 14)

# Get the full day name
day_name = my_date.strftime("%a")
print(day_name)  # Output: Tuesday

# Optional: Use "%a" for the abbreviated name (e.g., "Tue")
