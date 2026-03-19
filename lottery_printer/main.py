"""LOTTERY TICKET PRINTER - Main Entry Point

This program reads lottery numbers from a .txt file and automatically:
1. Generates formatted PDF tickets
2. Prints them to the default printer
3. Displays confirmation messages

Usage: Double-click this executable to run (no manual steps needed)
"""

import os
import sys
import subprocess
from reader import read_numbers_file
from pdf_generator import generate_lottery_pdf

try:
    # Read all lottery numbers from the .txt file (stops at END)
    data = read_numbers_file()
    games = data["games"]

    if games:
        # Step 1: Generate the formatted PDF with all tickets
        pdf_filename = "printed_slips.pdf"
        generate_lottery_pdf(games, pdf_filename, game_name=data.get("game_name", "Lottery"), date_str=data.get("date"))
        print(f"✓ PDF generated successfully: {pdf_filename}")

        # Step 2: Auto-print the PDF to the default printer
        try:
            # Windows command: Use default PDF viewer to print
            print(f"→ Printing to default printer...")
            # Using 'print' verb in Windows explorer to use default printer
            os.startfile(pdf_filename, "print")
            print(f"✓ Print job sent successfully!")
            print(f"✓ Your {len(games)} tickets are printing now.")
        except Exception as print_error:
            print(f"⚠ Warning: Could not auto-print - {print_error}")
            print(f"  PDF saved as '{pdf_filename}' - you can print it manually.")
            
    else:
        print("❌ ERROR: No valid lottery numbers found in .txt file!")
        print("   Use format: 07,16,26,29,52,04 (one game per line). Use END to stop early.")
        
except Exception as e:
    print(f"❌ FATAL ERROR: {e}")
    sys.exit(1)

# Keep window open for a moment so user can see results
input("\nPress Enter to close...")
