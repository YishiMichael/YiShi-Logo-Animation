import re
import numpy as np


COMMAND_NUMBERS_COUNT = {
    "M": 2,  # moveto
    "L": 2,  # lineto
    "H": 1,  # horizontal lineto
    "V": 1,  # vertical lineto
    "C": 6,  # curveto
    "S": 4,  # smooth curveto
    "Q": 4,  # quadratic Bezier curve
    "T": 2,  # smooth quadratic Bezier curveto
    "A": 7,  # elliptical Arc
    "Z": 0,  # closepath
}
COMMAND_NUMBERS_FLAGS = {
    "M": "xy",
    "L": "xy",
    "H": "x",
    "V": "y",
    "C": "xyxyxy",
    "S": "xyxy",
    "Q": "xyxy",
    "T": "xy",
    "A": "-----xy",
    "Z": "",
}
    

def get_svg_path_components(path_string):
    pattern = r"[MLHVCSQTAZ][0-9-\. ]*"
    parts = re.findall(pattern, path_string)
    return [(part[0], [float(num_str) for num_str in part[1:].split(" ")] if part[1:] else []) for part in parts]


def assert_validity(components):
    for component in components:
        assert len(component[1]) == COMMAND_NUMBERS_COUNT[component[0]]


def shift(components, vector):
    new_components = []
    for command, numbers in components:
        new_numbers = []
        for index, number in enumerate(numbers):
            flag = COMMAND_NUMBERS_FLAGS[command][index]
            if flag == "x":
                number += vector[0]
            elif flag == "y":
                number += vector[1]
            new_numbers.append(number)
        new_components.append((command, new_numbers))
    return new_components


def convert_string_to_decimal(num, fix=2):
    temp_str = ("{0:." + str(fix) + "f}").format(num)
    while temp_str.endswith("0"):
        temp_str = temp_str[:-1]
    if temp_str[-1] == ".":
        temp_str = temp_str[:-1]
    return temp_str


def merge_svg_path_components(components):
    return "".join([component[0] + " ".join([convert_string_to_decimal(num) for num in component[1]]) for component in components])


def shift_path(path_string, vector):
    path_components = get_svg_path_components(path_string)
    assert_validity(path_components)
    return merge_svg_path_components(shift(path_components, vector))


def shift_whole_svg(svg_string, vector):
    svg_file_lines = svg_string.split("\n")
    new_svg_file_lines = []
    for line in svg_file_lines:
        if line.startswith("<path d='") and line.endswith("'/>"):
            path_string = line[9:-3]
            new_path_string = shift_path(path_string, vector)
            new_svg_file_lines.append("<path d='{0}'/>".format(new_path_string))
        else:
            new_svg_file_lines.append(line)
    return "\n".join(new_svg_file_lines)


def convert_relevant_to_absolute(path_string):
    upper_path_string = path_string.upper()
    path_components = get_svg_path_components(upper_path_string)
    assert_validity(path_components)
    curr_coordinate = [0, 0]
    new_components = []
    for command, numbers in path_components:
        new_numbers = []
        for index, number in enumerate(numbers):
            flag = COMMAND_NUMBERS_FLAGS[command][index]
            if flag == "x":
                number += curr_coordinate[0]
            elif flag == "y":
                number += curr_coordinate[1]
            new_numbers.append(number)
        new_components.append((command, new_numbers))
        if command != "Z":
            curr_coordinate[0] += numbers[-2]
            curr_coordinate[1] += numbers[-1]
    return merge_svg_path_components(new_components)


def d2r(degree):
    return degree / 180 * np.pi


def get_point_on_ellipse(cx, cy, rx, ry, phi, angle):
    return [
        cx + rx * np.cos(angle) * np.cos(phi) + ry * np.sin(angle) * np.sin(phi),
        cy + rx * np.cos(angle) * np.sin(phi) - ry * np.sin(angle) * np.cos(phi)
    ]


def convert_elliptical_arc_to_quadratic_bezier_curve(
    cx, cy, rx, ry, phi, start_angle, angle, n_components=8
):
    samples = np.zeros((2 * n_components + 1, 2))
    samples[::2] = np.array([
        get_point_on_ellipse(cx, cy, rx, ry, phi, a)
        for a in np.linspace(
            start_angle,
            start_angle + angle,
            n_components + 1,
        )
    ])
    theta = angle / n_components / 2
    samples[1::2] = np.array([
        get_point_on_ellipse(cx, cy, rx / np.cos(theta), ry / np.cos(theta), phi, a)
        for a in np.linspace(
            start_angle + theta,
            start_angle + angle - theta,
            n_components,
        )
    ])
    return samples


def get_elliptical_arc_path_string(
    cx, cy, rx, ry, phi, start_angle, angle, n_components=8
):
    samples = convert_elliptical_arc_to_quadratic_bezier_curve(
        cx, cy, rx, ry, phi, start_angle, angle, n_components
    )
    path_components = [("Q", samples[k : k + 2].flatten()) for k in range(1, 2 * n_components, 2)]
    return merge_svg_path_components(path_components)


if __name__ == "__main__":
    #with open("temp_input.txt", "r") as f:
    #    path_string = f.read()
    #result = shift_path(path_string, [-5.27546, 5.999995])
    #result = convert_relevant_to_absolute(path_string)
    #result = shift_path(convert_relevant_to_absolute(path_string), [-5, -5])
    #result = shift_whole_svg(path_string, [0, 0])
    #for x in np.linspace(323, 324, 101):
    #    print(x, get_point_on_ellipse(7.949, 7.886, 6.61, 6.9, d2r(-25), d2r(x)))
    #result = get_elliptical_arc_path_string(7.954, 7.886, 6.61, 6.9, d2r(-25), d2r(46.9), d2r(323.1 - 46.9))
    result = get_elliptical_arc_path_string(7.954, 7.886, 7.61, 7.28, d2r(-25), d2r(318.4), d2r(44.7 - 318.4))
    with open("temp_output.txt", "w") as f:
        f.write(result)
