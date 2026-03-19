"""FILE READER - Extracts lottery numbers from text files

Expected format in .txt file:
    Optional first line: GameName or GameName,MM/DD/YYYY
    07,16,26,29,52,04
    05,09,39,41,45,01
    END   (stops processing; current page is printed even if &lt;3 tickets)

Where:
    - First 5 numbers: main lottery numbers (1-60)
    - Last number: Cash Ball (1-4)
    - One game per line, separated by commas
"""

import glob
import os
import datetime


def _parse_header_line(line):
    """If line looks like 'GameName' or 'GameName,MM/DD/YYYY', return (name, date_str or None). Else return None."""
    line = line.strip()
    if not line:
        return None
    parts = [p.strip() for p in line.split(",", 1)]
    if len(parts) == 1:
        # Single token: use as game name only if it doesn't look like numbers
        if parts[0] and not all(c.isdigit() or c.isspace() for c in parts[0].replace(",", "")):
            return (parts[0], None)
        return None
    if len(parts) == 2 and parts[0]:
        return (parts[0], parts[1] if parts[1] else None)
    return None


def _parse_game_line(line):
    """Parse a line into a game list of 6 ints, or return None if not valid."""
    line = line.strip()
    if not line:
        return None
    try:
        nums = [int(x.strip()) for x in line.split(",") if x.strip()]
        if len(nums) != 6:
            return None
        if not (all(1 <= n <= 60 for n in nums[:5]) and 1 <= nums[5] <= 4):
            return None
        return nums
    except ValueError:
        return None


def read_numbers_file():
    """Read .txt file(s) and extract metadata + lottery games. Stops at 'END'.

    Returns:
        dict: {
            "games": list of [n1, n2, n3, n4, n5, cash_ball],
            "game_name": str from file or "Lottery",
            "date": str MM/DD/YYYY from file or today
        }
    """
    result = {"games": [], "game_name": "Lottery", "date": datetime.datetime.now().strftime("%m/%d/%Y")}
    games = result["games"]
    game_name = result["game_name"]
    date_str = result["date"]
    header_done = False

    # Prefer numbers.txt as the lottery input file; otherwise any .txt except requirements.txt
    if os.path.isfile("numbers.txt"):
        txt_files = ["numbers.txt"]
    else:
        txt_files = [f for f in sorted(glob.glob("*.txt")) if f.lower() != "requirements.txt"]
    if not txt_files:
        print("ERROR: No input file found. Use numbers.txt or add a .txt file.")
        return result

    print(f"Reading input: {txt_files[0]}")

    for filename in txt_files:
        print(f"Reading file: {filename}")
        with open(filename, "r", encoding="utf-8") as f:
            for line in f:
                raw = line.strip()
                if not raw:
                    continue
                if raw.upper() == "END":
                    print("Stopping at END.")
                    result["games"] = games
                    result["game_name"] = game_name
                    result["date"] = date_str
                    return result
                game = _parse_game_line(raw)
                if game:
                    games.append(game)
                    continue
                if not header_done:
                    header = _parse_header_line(raw)
                    if header:
                        game_name, date_from_file = header
                        if date_from_file:
                            date_str = date_from_file
                        header_done = True
                    else:
                        header_done = True

    result["games"] = games
    result["game_name"] = game_name
    result["date"] = date_str
    print("TOTAL GAMES LOADED:", len(games))
    return result