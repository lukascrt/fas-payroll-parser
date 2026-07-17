# --- Setup ---
days = {}                   # Result: {date: {location: {worker: hours}}}
current_date = None         # Pointer: active date block
current_location = None     # Pointer: active location block
expecting_location = False  # Flag: next non-date line is a location

# --- Load file ---
with open("sample_messages.txt") as file:
    lines = file.readlines()


def is_date_line(line):
    """A line starts a new date block if its first character is a digit."""
    line = line.strip()
    if not line:            # guard: empty lines are not dates
        return False
    return line[0].isdigit()


def clean_date(raw):
    """Normalise a date line to DD/MM/YYYY.
    Returns (date, rest) — rest is any location text glued to the date."""
    date_part = ""
    for char in raw:
        if char.isalpha():  # first letter marks where a glued location begins
            break
        date_part += char

    rest = raw[len(date_part):].strip()

    date_part = date_part.replace(".", "/").replace(",", "/")
    parts = date_part.split("/")
    if len(parts[2]) == 2:  # expand 2-digit years: 26 → 2026
        parts[2] = "20" + parts[2]

    return "/".join(parts), rest

def split_worker(line):

    """ Split the worker line into (name, hours) — hours is None if not found or invalid. """

    position = None
    last = None

    # Find the first and last digit positions in the line.

    for i, char in enumerate(line):
        if char.isdigit():
            position = i
            break
    
    for i, char in enumerate(line):
        if char.isdigit():
            last = i

    # Guard: if no digits found, return the whole line as name and None for hours.

    if position is None:
        return line.strip(), None
    
    name = line[:position].rstrip("+ ")
    hours = line[position:last + 1].strip() 


    try:
        if ":" in hours:
            hour_parts = hours.split(":")

            hours = int(hour_parts[0]) + int(hour_parts[1]) / 60
        else:
            hours = float(hours)

        return name, hours

    except ValueError:
        return name, None


# --- Parse: group lines into days → locations → workers → hours ---
for line in lines:
    line = line.strip()
    if not line:
        continue
    elif is_date_line(line):
        current_date, rest = clean_date(line)
        if current_date not in days:            # guard: same date may appear in multiple messages
            days[current_date] = {}
        if rest:                                # date had a location glued to it
            current_location = rest
            if current_location not in days[current_date]:
                days[current_date][current_location] = {}
            expecting_location = False
        else:
            expecting_location = True           # location follows on the next line
    elif expecting_location:
        current_location = line
        if current_location not in days[current_date]:   # guard: same site may repeat (split carloads)
            days[current_date][current_location] = {}
        expecting_location = False
    else:
        name, hours = split_worker(line)
        if name not in days[current_date][current_location]:
            days[current_date][current_location][name] = hours

# --- Display ---
for date in days:
    print(date, "→", days[date])
    print()

# Test cases for split_worker function

print(split_worker("Florin + 3.50 h"))
print(split_worker("Augustin Romez +1:30 h"))
print(split_worker("Vali James + 3.50.h"))
print(split_worker("Vladimir + 3 ore"))
print(split_worker("Vladimir Vorsi doar 3 h"))
print(split_worker("Abel Nan"))