# fas-payroll-parser

A Python tool that parses real WhatsApp attendance messages from construction sites into structured payroll data (date → site → worker → hours).

## Why it exists

Built to automate manual data entry at FAS Construction LTD, where site managers and workers send daily attendance in a WhatsApp group chat across multiple jobs.

## The hard part

The messages are written by many different people, often in Romanian, with no fixed format. Real examples:

```
18,06,2026Roebuck Estates, Upperton Farm...   ← date and location glued together
o zi jumate                                   ← Romanian: "a day and a half"
+ 1 50 h                                      ← space instead of a decimal point
pana la 11:30                                 ← a clock time, not a duration
```

The parser's philosophy: parse what is certain, flag what isn't. It never crashes and never guesses silently.

## The review log

Anything ambiguous is stored, flagged, and written to `review.txt` with full context, so a human can resolve it in seconds:

```
Review: 16/07/2026 → SPITAL → VLAD V o zi jumate
Review: 14/07/2026 → Airbus → Cocă Viu pana la 11:30
Review: 06/07/2026 → Arbus → Bibiea FLIN + 1 50 h
```

## How to run


Requires `pip install openpyxl`

Put a WhatsApp chat export in `sample_messages_v2.txt`, run `parser_v2.py`, you get three outputs: structured data in the terminal, `payroll.xlsx`, and `review.txt` for flagged lines.

## Known limitations & roadmap

- Times like `4.30` (meaning 4h 30m) are currently read as the decimal 4.3
- Clock times such as `pana la 11:30` are flagged for review but stored as-is
- Romanian words like `numai` or `doar` can remain stuck inside worker names
- Locations starting with digits (postcodes) can be misread as date lines

Planned: V4 — overtime and pay-rate logic, a review column in the Excel output, plus worker search by date range.

## Versions

V1: proof of concept on clean, consistent messages. V2: real-world formats, nested date → site → worker structure, review log. V3: (current) — Excel export.