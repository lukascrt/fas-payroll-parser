messages = ["Monday: Lukas, Mike, David - 9hrs",
            "Tuesday: Mike, David - 8hrs",
            "Wednesday: Lukas, David, Ion - 10hrs"
            ]

def parse_line(line):

    after_colon = line.split(":")[1]
    before_colon = line.split(":")[0]
    before_dash = after_colon.split("-")[0]
    after_dash = after_colon.split("-")[1]
    hour = after_dash.replace("hrs", "")
    between_commas = before_dash.split(",")


    print(before_colon)
    for names in between_commas:
        
        print(names.strip() + " -" + hour)

for _ in messages:
    print()
    parse_line(_)


