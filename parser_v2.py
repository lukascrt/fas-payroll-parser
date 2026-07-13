days = {}
current_date = None

with open("sample_messages.txt") as file:
    lines = file.readlines()


def is_date_line(line):
    line = line.strip()
    if not line:
        return False
    return line[0].isdigit()

for line in lines:
    line = line.strip()
    if not line:
        continue
    elif is_date_line(line):
        current_date = line
        days[current_date] = []
    else:
        days[current_date].append(line)

for date in days:
    print(date, "→", days[date])
    print()


    

