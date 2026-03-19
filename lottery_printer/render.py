"""RENDER MODULE - Draws tickets and numbers on the PDF

This module handles all visual rendering:
- Number dots/circles in the grid
- Registration marks for cutting/scanning
- Identifier boxes for distinguishing tickets
- Cash Ball placement
"""

from config import *
import datetime

from config import *

def draw_registration_marks(c, x_offset):
    """Joel: Black squares must be 2pt from edges for orientation."""
    c.setFillColorRGB(0, 0, 0)
    sq_size = 10
    # Top Left Square
    c.rect(x_offset + 2, PAGE_HEIGHT - sq_size - 2, sq_size, sq_size, fill=1)
    # Bottom Left Square
    c.rect(x_offset + 2, 2, sq_size, sq_size, fill=1)
    
    # Red Cut Lines
    c.setStrokeColorRGB(1, 0, 0)
    c.setLineWidth(0.5)
    c.rect(x_offset, 0, TICKET_WIDTH, PAGE_HEIGHT, stroke=1, fill=0)

def draw_scanner_registration_marks(c, x_offset, ticket_index):
    """Joel: 5 identifier boxes at bottom. Fill the correct one."""
    box_size = 7
    spacing = 4
    total_w = (5 * box_size) + (4 * spacing)
    start_x = x_offset + (TICKET_WIDTH - total_w) / 2
    id_y = 12
    
    c.setStrokeColorRGB(0, 0, 0)
    for i in range(1, 6):
        curr_x = start_x + (i-1) * (box_size + spacing)
        is_filled = 1 if i == (ticket_index + 1) else 0
        c.rect(curr_x, id_y, box_size, box_size, fill=is_filled, stroke=1)

def draw_selected_numbers_list(c, ticket_x, ticket_games):
    """Renders the 5 lines of readable text (e.g. 1> 07-16-26...)"""
    c.setFont("Helvetica", 9)
    center_x = ticket_x + TICKET_WIDTH / 2
    # Positioned high to stay clear of the Doubler Oval
    text_y_start = PAGE_HEIGHT - 80 
    
    for i, numbers in enumerate(ticket_games):
        if len(numbers) < 6: continue
        line_num = i + 1
        main_nums = sorted(numbers[:5])
        cash_ball = numbers[5]
        text = f"{line_num}> " + "-".join(f"{n:02d}" for n in main_nums) + f"={cash_ball}"
        c.drawCentredString(center_x, text_y_start - (i * NUMBERS_LINE_HEIGHT), text)

def draw_doubler_box(c, ticket_x, filled=True):
    """
    Dono Doubler marks ke beech gap add karta hai aur corners round karta hai.
    """
    DOUBLER_X_OFFSET = 60  # Right side shift
    
    center_x = ticket_x + (TICKET_WIDTH / 2)
    box_w, box_h = OVAL_WIDTH, OVAL_HEIGHT
    box_x = (center_x - (box_w / 2)) + DOUBLER_X_OFFSET

    dots_y_start = PAGE_HEIGHT - Y_TOP_ANCHOR
    
    c.setFillColorRGB(0, 0, 0) # Black Fill

    # 1. NEECHE wala mark (Fixed position)
    bottom_y = dots_y_start + DOUBLER_GAP_ABOVE_DOTS
    c.roundRect(box_x, bottom_y, box_w, box_h, OVAL_RADIUS, stroke=0, fill=1)

    # 2. OOPAR wala mark (Neeche wale se 'internal gap' ke fasle par)
    top_y = bottom_y + box_h + DOUBLER_INTERNAL_GAP
    c.roundRect(box_x, top_y, box_w, box_h, OVAL_RADIUS, stroke=0, fill=1)

def draw_game_dots(c, numbers, ticket_x, game_y_anchor, game_idx):
    """Draws the actual bubble grid for the scanner."""
    main_nums = numbers[:5]
    cash_ball = numbers[5]

    for num in range(1, 61):
        col = (num - 1) % 13
        row = (num - 1) // 13
        x = ticket_x + X_START + (col * COL_WIDTH)
        y = game_y_anchor - (row * ROW_HEIGHT)
        
        if num in main_nums: 
            c.setFillColorRGB(0, 0, 0)
            c.circle(x, y, CIRCLE_RADIUS, stroke=0, fill=1)

    # Cash Ball Row
    cash_y = game_y_anchor - (5 * ROW_HEIGHT) - 8
    cb_start_x = ticket_x + X_START + (CB_START_COL_INDEX * COL_WIDTH)
    
    for cb in range(1, 5):
        x = cb_start_x + ((cb - 1) * COL_WIDTH)
        if cb == cash_ball:
            c.setFillColorRGB(0, 0, 0)
            c.circle(x, cash_y, CIRCLE_RADIUS, stroke=0, fill=1)

def draw_scanner_essentials(c, x_offset):
    # Red Cut Lines - Ab naye TICKET_WIDTH aur PAGE_HEIGHT ko use karega
    c.setStrokeColorRGB(1, 0, 0)
    c.setLineWidth(0.8)
    c.rect(x_offset, 0, TICKET_WIDTH, PAGE_HEIGHT, stroke=1, fill=0)
    
    # Registration Marks
    c.setFillColorRGB(0, 0, 0)
    # Top-left square: PAGE_HEIGHT ab 8.5" hai, toh squares automatically naye top edge ke paas honge
    c.rect(x_offset + 2, PAGE_HEIGHT - 12, 8, 8, fill=1) 
    c.rect(x_offset + 2, 4, 8, 8, fill=1)
    
def draw_full_game_grid(c, numbers, start_x, game_top_y):
    main_nums = numbers[:5]
    cash_ball = numbers[5]
    c.setFont("Helvetica-Bold", 4.5) 
    
    # Main Numbers 1-60 (Rows 1-5)
    for num in range(1, 61):
        col = (num - 1) % 13
        row = (num - 1) // 13
        x = start_x + (col * COL_WIDTH)
        y = game_top_y - (row * ROW_HEIGHT)

        if num in main_nums:
            c.setFillColorRGB(0, 0, 0)
            c.circle(x, y, CIRCLE_RADIUS, stroke=0, fill=1)
            c.setFillColorRGB(1, 1, 1)
        else:
            c.setFillColorRGB(1, 1, 1)
            c.setStrokeColorRGB(0, 0, 0)
            c.circle(x, y, CIRCLE_RADIUS, stroke=1, fill=0)
            c.setFillColorRGB(0, 0, 0)
        c.drawCentredString(x, y - 1.5, str(num))

    # --- FIX: Cash Ball Row (Row 6) Alignment ---
    # Cash Ball 1 is placed at (CB_START_COL_INDEX + 0) * COL_WIDTH
    # This aligns 1 under 57, 2 under 58, 3 under 59, and 4 under 60 [cite: 121, 138]
    cash_y = game_top_y - (5 * ROW_HEIGHT) - 5 
    for cb in range(1, 5):
        # Calculate X so Cash Ball 'cb' aligns with the correct column
        x = start_x + ((CB_START_COL_INDEX + (cb - 1)) * COL_WIDTH)
        
        if cb == cash_ball:
            c.setFillColorRGB(0, 0, 0)
            c.circle(x, cash_y, CIRCLE_RADIUS, stroke=0, fill=1)
            c.setFillColorRGB(1, 1, 1)
        else:
            c.setStrokeColorRGB(0, 0, 0)
            c.circle(x, cash_y, CIRCLE_RADIUS, stroke=1, fill=0)
            c.setFillColorRGB(0, 0, 0)
        c.drawCentredString(x, cash_y - 1.5, str(cb))