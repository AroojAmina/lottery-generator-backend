# lottery_printer/config.py
from reportlab.lib.units import inch

# PAGE SETTINGS
PAGE_WIDTH = 11 * inch
PAGE_HEIGHT = 8.5 * inch

# TICKET SETTINGS
TICKETS_PER_PAGE = 3
TICKET_WIDTH = 3.25 * inch    # 3-1/4" width
TICKET_HEIGHT = 8.5 * inch    # 8.5" height

# HEADER & READABLE AREA
Y_HEADER_START = PAGE_HEIGHT - 25      # Main title "CASH4LIFE"
HEADER_LINE_HEIGHT = 18                # Space between title, date, and Game No.
NUMBERS_LINE_HEIGHT = 12               # Space between the 5 rows of text (1> ... 5>)
READABLE_TOP = Y_HEADER_START          # Alias used in some render functions

# DOUBLER OVAL SETTINGS
OVAL_WIDTH = 22                   # <--- THIS WAS MISSING
OVAL_HEIGHT = 8       
OVAL_RADIUS = 4.0                    # ~0.22 inches tall
DOUBLER_GAP_ABOVE_DOTS = 20   
DOUBLER_INTERNAL_GAP = 25

# GRID POSITIONING & MARGINS
X_START = 95.0   
Y_TOP_ANCHOR = 210.0                   # Distance from TOP edge to first dot

# DOT / CIRCLE SETTINGS
COL_WIDTH = 10.5   
ROW_HEIGHT = 10.2  
CIRCLE_RADIUS = 4.0   

# CASH BALL GRID OFFSET
CB_START_COL_INDEX = 4

# GAME SETTINGS
GAMES_PER_TICKET = 5
GAME_SPACING = 78.0  

# SCANNER MARKS
ID_BOX_SIZE = 7
ID_BOX_SPACING = 4