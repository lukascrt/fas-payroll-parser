# --- Setup ---

days = {}                # Final result: {date: {location: {worker: hours}}}
current_date = None      # Pointer: which date block we are inside
current_location = None  # Pointer: which location block we are inside
expecting_location = False  # Flag: whether we are expecting a location line next
workers = None             # Pointer: which worker block we are inside

# --- Read the file ---

with open("sample_messages.txt") as file:
    lines = file.readlines()



def is_date_line(line):
    line = line.strip() # Removes white space and \n
    if not line:        # Crash Guard: if line is empty, return False
        return False
    return line[0].isdigit()  # Check if the first character is a digit, indicating a date line



def clean_date(raw): # Cleans the date string by removing any non-date characters and formatting it consistently
    date_part = ""
    rest = ""


    for char in raw:  # Iterate through each character in the raw date string
        if char.isalpha():     
            break               # Stop processing if an alphabetic character is encountered, as it indicates the end of the date part         
        date_part += char      
 
    date_length = len(date_part)  # Get the length of the date part to determine how many characters to skip for the location part

    rest = raw[date_length:].strip()  # Extract the location part by slicing the raw string and stripping any leading/trailing whitespace

    # Date Part Process
 
    date_part = date_part.replace(".", "/").replace(",", "/")   # Replace periods and commas with slashes to standardize the date format

    parts = date_part.split("/")    # Split the date part into components (day, month, year) using slashes as separators

    if len(parts[2]) == 2:
        parts[2] = "20" + parts[2] # If the year part has only two digits, prepend "20" to convert it to a four-digit year

    date_part = "/".join(parts) # Join the components back together with slashes to form the cleaned date string

    return date_part, rest  # Return the cleaned date and location as a tuple



for line in lines:
    line = line.strip()
    if not line:
        continue     # Skips everything below and goes to the next iteration of the loop
    elif is_date_line(line):
        current_date, rest = clean_date(line)    # Sets the current date to the cleaned date

        if current_date not in days:   # If the current date is not already a key in the days dictionary, create a new entry for it with an empty list 
            days[current_date] = {}
        if rest:
            current_location = rest  # If there is a location part in the line, set the current location to it
            if current_location not in days[current_date]:  # If the current location is not already a key in the list of messages for the current date, create a new entry for it with an empty list
                days[current_date][current_location] = {}
            expecting_location = False
        else:
            expecting_location = True  # If there is no location part in the line, set the flag to indicate that we are expecting a location line next
    elif expecting_location:
        current_location = line  # If we are expecting a location line, set the current location to the line
        if current_location not in days[current_date]:  # If the current location is not already a key in the list of messages for the current date, create a new entry for it with an empty list
            days[current_date][current_location] = {}
        expecting_location = False
    else:
        workers = line
        if workers not in days[current_date][current_location]:  # If the current worker is not already a key in the list of messages for the current date and location, create a new entry for it with an empty list
            days[current_date][current_location][workers] = None  # Initialize the worker's hours to None, indicating that we haven't recorded any hours for this worker yet


for date in days: # Iterates through each date in the days dictionary
    print(date, "→", days[date])
    print()