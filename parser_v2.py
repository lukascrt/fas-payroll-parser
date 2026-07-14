days = {}
current_date = None

with open("sample_messages.txt") as file:
    lines = file.readlines()



def is_date_line(line):
    line = line.strip()
    if not line:
        return False
    return line[0].isdigit()

def clean_date(raw):
    date_part = ""
    for char in raw:
        if char.isalpha():     # .isalpha() = is this a letter?
            break              # stop the loop instantly
        date_part += char      # otherwise keep building the date
    date_part = date_part.replace(".", "/").replace(",", "/")  # NOW replace . and , with / on date_part only

    parts = date_part.split("/")

    if len(parts[2]) == 2:
        parts[2] = "20" + parts[2]

    date_part = "/".join(parts)

    return date_part



for line in lines:
    line = line.strip()
    if not line:
        continue
    elif is_date_line(line):
        current_date = clean_date(line)
        
        if current_date not in days:
            days[current_date] = []
    else:
        days[current_date].append(line)

for date in days:
    print(date, "→", days[date])
    print()

