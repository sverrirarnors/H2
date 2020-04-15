# RADIUS = 0.01
RADIUS = 5
DIMENSIONS = {
    'height': 800,
    'width': 800,
}
NUMBER_OF_PEOPLE = 100
STATIC_PEOPLE_PERCENTAGE = 25
TIME_TO_RECOVER = 1300
TIME_TO_INFECT = 200
SPEED = 0.005

FRAMES_PER_SECOND = 30
TOTAL_TICKS = 50


def clamp(val, minimum=0, maximum=255):
    if val < minimum:
        return minimum
    if val > maximum:
        return maximum
    return val


def colorscale(hexstr, scalefactor):
    hexstr = hexstr.strip('#')

    if scalefactor < 0 or len(hexstr) != 6:
        return hexstr

    r, g, b = int(hexstr[:2], 16), int(hexstr[2:4], 16), int(hexstr[4:], 16)

    r = clamp(r * scalefactor)
    g = clamp(g * scalefactor)
    b = clamp(b * scalefactor)

    return "#%02x%02x%02x" % (r, g, b)
