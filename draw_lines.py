import random


def draw_diagonal(x, y, x2, y2, color='black', thickness=2):
    # format a line for svg
    return (
        f'<line x1="{x}" y1="{y}" x2="{x2}" y2="{y2}"'
        f' stroke="{color}" stroke-width="{thickness}" />'
            )


def make_maze(num, color="black", thickness=2, height=500):
    # num is the number of diagonals across and down
    # filename is the output file name
    width = height
    header = (
        f'<svg xmlns="http://www.w3.org/2000/svg"'
        f' viewBox="0 0 {width} {height}">'
        )

    step = height // num
    # write the header for the file
    output = header + '\n'
    # loop through
    for row in range(0, height, step):
        for col in range(0, width, step):
            # choose a random direction for the diagonal line
            if random.choice([0, 1]) == 0:
                # write the line
                output += draw_diagonal(
                    col, row, col + step, row + step,
                    color, thickness
                    ) + '\n'
            else:
                # write the line
                output += draw_diagonal(
                    col + step, row, col, row + step,
                    color, thickness
                    ) + '\n'
    # write the footer
    footer = f'</svg>'
    output += footer
    return output

if __name__ == "__main__":
    output = make_maze(10, color="darkviolet")
    with open("lines.svg", "w") as f:
        for line in output:
            f.writelines(line)
