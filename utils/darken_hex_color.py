import colorsys

def darken_hex_color(hex_color: str, factor: float = 0.85) -> str:
    """
    Darken a hex color by a given factor.

    Args:
        hex_color (str): The hex color to darken (e.g., "#RRGGBB").
        factor (float): The factor by which to darken the color (0 to 1).
                        Default is 0.85.

    Returns:
        str: The darkened hex color.
    """
    # Remove the '#' if present
    hex_color = hex_color.lstrip('#')

    # Convert hex to RGB
    rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    # Convert RGB to HSV
    h, s, v = colorsys.rgb_to_hsv(rgb[0]/255, rgb[1]/255, rgb[2]/255)

    # Reduce the value (brightness) by the factor
    v = max(0, min(v * factor, 1))

    # Convert back to RGB
    r, g, b = colorsys.hsv_to_rgb(h, s, v)

    # Convert RGB back to hex
    return f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}"
