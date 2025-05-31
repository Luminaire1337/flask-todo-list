import csv
import io
from typing import List
from sqlite3 import Row

def csv_encode(rows: List[Row]) -> str:
    """
    Convert a list of database rows to a CSV string.
    
    Args:
        rows: List of database Row objects to convert
        
    Returns:
        String containing CSV data
    """
    if not rows:
        return ""
        
    # Use the CSV module for proper escaping and formatting
    output = io.StringIO()
    writer = csv.writer(output, quoting=csv.QUOTE_MINIMAL)
    
    # Write the header row
    writer.writerow(rows[0].keys())
    
    # Write the data rows
    for row in rows:
        writer.writerow(row)
    
    return output.getvalue()