def parse_lines(lines):
    result = []
    for number, line in enumerate(lines, 1):
        if not line.strip():
            continue
        label, raw = line.strip().split("=", 1)
        if not label:
            raise ValueError(f"line {number}: empty label")
        try:
            value = int(raw)
        except ValueError as error:
            raise ValueError(f"line {number}: invalid integer") from error
        result.append((label, value))
    return result
