"""PDF GENERATOR - Creates printable lottery ticket PDFs

This module generates the final PDF files with:
- Formatted lottery tickets ready to print
- Proper grid alignment for lottery machines
- Registration marks for cutting and scanning
- Optional debug versions with number labels
"""

import datetime
from reportlab.pdfgen import canvas
from config import *
from reader import read_numbers_file
from render import (
    draw_game_dots,
    draw_registration_marks,
    draw_scanner_registration_marks,
    draw_selected_numbers_list,
    draw_doubler_box,
    draw_full_game_grid,
)

def generate_lottery_pdf(games, output_filename, game_name="Cash4Life", date_str=None):
    """
    Generate the main lottery ticket PDF for printing.
    Joel's Requirements: 
    - 3 tickets per page (3.25" each)
    - Readable Header in Bold (Game Name, Date, No.)
    - Exact positioning for scanner accuracy.
    
    Scaling: Canvas is set to 72 DPI (standard for ReportLab), matching 1 inch = 72 points.
    This ensures the PDF renders at TRUE 100% scale when printed.
    """
    if not games:
        print("Error: No games found in the file!")
        return

    if date_str is None:
        date_str = datetime.datetime.now().strftime("%m/%d/%Y")

    print(f"Generating PDF: {output_filename} with {len(games)} games (Game: {game_name}, Date: {date_str})")

    # Page initialization (Letter Landscape 11x8.5")
    c = canvas.Canvas(output_filename, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    c.setPageCompression(0)
    
    # Add metadata to help with print driver scaling and document identification
    c.setTitle("Lottery Tickets")
    c.setAuthor("Lottery Printer")

    game_ptr = 0
    total_games = len(games)
    page_num = 1

    while game_ptr < total_games:
        print(f"--- Processing Page {page_num} ---")

        for t_idx in range(3): # 3 Tickets (Left, Middle, Right)
            if game_ptr >= total_games:
                break

            ticket_x = t_idx * TICKET_WIDTH
            display_ticket_num = (game_ptr // 5) + 1
            
            # Line data for the readable list below header
            ticket_games = games[game_ptr : game_ptr + 5]

            # ==========================================
            # HEADER DATA (Readable information for verification)
            # All header text must be clearly visible and machine-readable
            # ==========================================
            center_x = ticket_x + TICKET_WIDTH / 2
            c.setFillColorRGB(0, 0, 0)
            
            # Game Name (Uppercase and Large - primary identifier)
            c.setFont("Helvetica-Bold", 18) 
            c.drawCentredString(center_x, Y_HEADER_START, game_name.upper())

            # Game Date (secondary identifier)
            c.setFont("Helvetica-Bold", 13)
            c.drawCentredString(center_x, Y_HEADER_START - 20, f"Game Date {date_str}")
            
            # Game Number (ticket/batch identifier - formatted with leading zeros)
            c.setFont("Helvetica-Bold", 11)
            c.drawCentredString(center_x, Y_HEADER_START - 38, f"Game No. {display_ticket_num:03d}")

            # ==========================================
            # SCANNER MARKS & STRUCTURE
            # ==========================================
            draw_registration_marks(c, ticket_x)
            draw_scanner_registration_marks(c, ticket_x, t_idx)

            # Readable list of numbers (e.g., 1> 07-16-26...)
            draw_selected_numbers_list(c, ticket_x, ticket_games)
            
            # Doubler box (Rounded Oval)
            draw_doubler_box(c, ticket_x, filled=False)

            # ==========================================
            # DRAWING THE DOT GRID (5 games per ticket)
            # ==========================================
            for g_idx in range(5):
                if game_ptr < total_games:
                    current_game_data = games[game_ptr]
                    
                    # Console log for verification
                    print(f"Ticket {display_ticket_num}, Line {g_idx+1}: {current_game_data}")
                    
                    # Calculate vertical position based on Anchor and Spacing
                    game_y = (PAGE_HEIGHT - Y_TOP_ANCHOR) - (g_idx * GAME_SPACING)
                    
                    # Drawing the dots
                    draw_game_dots(c, current_game_data, ticket_x, game_y, g_idx)
                    
                    game_ptr += 1 

        c.showPage() # Finish current page
        page_num += 1

    c.save()
    print(f"\nSuccess! PDF saved as {output_filename}")

if __name__ == "__main__":
    data = read_numbers_file()
    generate_lottery_pdf(
        data["games"],
        "printed_slips.pdf",
        game_name=data.get("game_name", "Lottery"),
        date_str=data.get("date"),
    )

def generate_full_grid_pdf(games, output_filename, game_name="Lottery", date_str=None):
    """
    Generates a PDF with numbers inside circles (grid style) for reference.
    Same layout and style as the dot PDF: header, readable list, Doubler box,
    registration marks, identifier boxes. Full sheet 11" x 8.5" landscape.
    """
    if date_str is None:
        date_str = datetime.datetime.now().strftime("%m/%d/%Y")

    c = canvas.Canvas(output_filename, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    c.setPageCompression(0)

    for i in range(0, len(games), 15):
        page_games = games[i:i+15]
        for t_idx in range(3):
            ticket_x = t_idx * TICKET_WIDTH
            display_ticket_num = (i // 5) + t_idx + 1
            ticket_games = page_games[t_idx * 5 : (t_idx + 1) * 5]

            # Same header as dot PDF (Joel: readable area, all Helvetica-Bold)
            center_x = ticket_x + TICKET_WIDTH / 2
            c.setFillColorRGB(0, 0, 0)
            c.setFont("Helvetica-Bold", 12)
            c.drawCentredString(center_x, READABLE_TOP, game_name)
            c.setFont("Helvetica-Bold", 9)
            c.drawCentredString(center_x, READABLE_TOP - HEADER_LINE_HEIGHT, f"Game Date {date_str}")
            c.setFont("Helvetica-Bold", 10)
            c.drawCentredString(center_x, READABLE_TOP - 2 * HEADER_LINE_HEIGHT, f"Game No. {display_ticket_num:03d}")

            draw_registration_marks(c, ticket_x)
            draw_scanner_registration_marks(c, ticket_x, t_idx)
            draw_selected_numbers_list(c, ticket_x, ticket_games)
            draw_doubler_box(c, ticket_x, filled=False)

            for g_idx, g_data in enumerate(ticket_games):
                game_y = (PAGE_HEIGHT - Y_TOP_ANCHOR) - (g_idx * GAME_SPACING)
                draw_full_game_grid(c, g_data, ticket_x + X_START, game_y)

        c.showPage()
    c.save()