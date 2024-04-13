import numpy
import PySimpleGUI as sg
from matplotlib import patches, pyplot
from matplotlib.collections import PatchCollection
from matplotlib.patches import PathPatch
from matplotlib.path import Path
from numpy import linspace, ndarray, pi, sin
from scipy.integrate import quad

a, b = -2, 3
area = 0
colours = ["lightcoral", "salmon", "coral"]
steps = [0.6000, 0.2500, 0.0500, 0.0020]
err_by_step = []


def integral(x):
    return 3**x


def prepare_integral_graph(ax, fig):

    x = linspace(a, b)
    y = integral(x)

    ax.plot(x, y, "r", linewidth=2)
    ax.set_ylim(bottom=0)

    ix = linspace(a, b)
    iy = integral(ix)
    verts = [(a, 0), *zip(ix, iy), (b, 0)]
    poly = patches.Polygon(verts, facecolor="0.9", edgecolor="0.5")
    ax.add_patch(poly)

    fig.text(0.9, 0.05, "$x$")
    fig.text(0.1, 0.9, "$y$")

    ax.spines[["top", "right"]].set_visible(False)


def rectangle_draw(lx, rx, h, colour) -> PathPatch:
    codes = []
    vertices = []

    codes = [Path.MOVETO] + [Path.LINETO] * 3 + [Path.CLOSEPOLY]
    vertices = [(lx, 0), (lx, h), (rx, h), (rx, 0), (0, 0)]

    path = Path(vertices, codes)

    return PathPatch(path, facecolor=colours[colour], edgecolor="none")


def numeric_integral_square_cover(ax, x_start, x_end, jump_length):
    current = x_start + jump_length
    rx, lx, area, current_colour = 0, 0, 0, 0
    patch_list = []

    while True:
        lx = current
        rx = current + jump_length if rx + jump_length <= x_end else x_end
        height = integral(rx)

        patch_list.append(rectangle_draw(lx, rx, height, current_colour))
        current = rx

        if current_colour < len(colours) - 1:
            current_colour += 1
        else:
            current_colour = 0

        area += height * jump_length

        if rx >= x_end:
            break

    patch_collection = PatchCollection(patch_list, match_original=True)
    ax.add_collection(patch_collection)
    ax.text(0, -2.7, f"P(n) n = {jump_length} : {area}")
    ax.text(0, -3.8, f"P: {quad(integral, a, b)[0]}")
    err_by_step.append([jump_length, area - quad(integral, a, b)[0]])


def prepare_err_graph(ax, step_sizes):
    errors = [err[1] for err in err_by_step]
    ax.plot(step_sizes, errors, "r", linewidth=2)
    ax.set_ylim(bottom=0)
    ax.set_xlabel("Step Size")
    ax.set_ylabel("Error")
    ax.spines[["top", "right"]].set_visible(False)


def do_me():
    for step in steps:
        fig, ax = pyplot.subplots()
        prepare_integral_graph(ax, fig)
        numeric_integral_square_cover(ax, a, b, step)
        pyplot.savefig(f"integral-step-{step}.svg")
    fic, bx = pyplot.subplots()
    prepare_err_graph(bx, steps)
    pyplot.savefig("Error graph.svg")


do_me()
