def scramble_jpeg_header(input_path, output_path):
    with open(input_path, "rb") as f:
        data = bytearray(f.read())

    # Replace only the first 4 bytes (header)
    if data[0:4] == bytearray([0xFF, 0xD8, 0xFF, 0xE0]):
        data[0:4] = bytearray([0xFF, 0xE0, 0xD8, 0xFF])  # scrambled
    else:
        print("Warning: Header doesn't match expected JPEG magic bytes.")

    with open(output_path, "wb") as f:
        f.write(data)

    print(f"Scrambled JPEG header written to {output_path}")

# Example usage
scramble_jpeg_header("flag.jpg", "fragment_43.dat")
