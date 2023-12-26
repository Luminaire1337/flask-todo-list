def csv_encode(rows: list) -> str:
    csv_string = ','.join(rows[0].keys()) + '\n'
    csv_string += '\n'.join([','.join(map(str, row)) for row in rows])
    return csv_string