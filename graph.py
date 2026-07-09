import tkinter as tk
from itertools import combinations
import math

#---------Coment Block
# his is a 
# some more coments
# more coments
# noch ein test

# ---- Configuration ----
START_SIZE     = 700   # initial window size in pixels
MARGIN         = 80    # distance from window edge to the shapes
POINTS_PER_SIDE = 10   # number of points on each side / around the circle
POINT_RADIUS   = 2     # radius of each drawn point


def build_square_points(width, height):
    """Return points distributed along the 4 sides of a square."""
    left   = MARGIN
    right  = width  - MARGIN
    top    = MARGIN
    bottom = height - MARGIN

    points = []
    for i in range(POINTS_PER_SIDE):
        t = i / POINTS_PER_SIDE
        points.append((left + t * (right - left), top))
        points.append((right, top + t * (bottom - top)))
        points.append((right - t * (right - left), bottom))
        points.append((left, bottom - t * (bottom - top)))
    return points


def build_circle_points(width, height):
    """Return points evenly distributed around a circle/ellipse."""
    cx = width  / 2
    cy = height / 2
    rx = (width  - 2 * MARGIN) / 2
    ry = (height - 2 * MARGIN) / 2

    total = POINTS_PER_SIDE * 4
    points = []
    for i in range(total):
        angle = 2 * math.pi * i / total
        points.append((cx + rx * math.cos(angle),
                        cy + ry * math.sin(angle)))
    return points


def redraw(canvas, width, height,
           show_square, show_circle, show_cross):
    """Clear and redraw based on current size and toggle states."""
    canvas.delete("all")

    if width <= 2 * MARGIN or height <= 2 * MARGIN:
        return

    square_points = build_square_points(width, height) if show_square.get() else []
    circle_points = build_circle_points(width, height) if show_circle.get() else []

    # ── Outlines ──────────────────────────────────────────────────────────────
    if show_square.get():
        canvas.create_rectangle(
            MARGIN, MARGIN, width - MARGIN, height - MARGIN,
            outline="black", width=2
        )

    if show_circle.get():
        canvas.create_oval(
            MARGIN, MARGIN, width - MARGIN, height - MARGIN,
            outline="black", width=2
        )

    # ── Square ↔ Square lines (blue) ──────────────────────────────────────────
    if show_square.get():
        color = "#7aa6ff"
        for (x1, y1), (x2, y2) in combinations(square_points, 2):
            canvas.create_line(x1, y1, x2, y2, fill=color, width=1)
            #color = color - 1

    # ── Circle ↔ Circle lines (green) ─────────────────────────────────────────
    if show_circle.get():
        for (x1, y1), (x2, y2) in combinations(circle_points, 2):
            canvas.create_line(x1, y1, x2, y2, fill="#7fffa6", width=1)

    # ── Square ↔ Circle cross lines (orange) ──────────────────────────────────
    if show_cross.get() and show_square.get() and show_circle.get():
        for (x1, y1) in square_points:
            for (x2, y2) in circle_points:
                canvas.create_line(x1, y1, x2, y2, fill="#ffb347", width=1)

    # ── Square points (red) ───────────────────────────────────────────────────
    if show_square.get():
        for (x, y) in square_points:
            canvas.create_oval(
                x - POINT_RADIUS, y - POINT_RADIUS,
                x + POINT_RADIUS, y + POINT_RADIUS,
                fill="red", outline="black"
            )

    # ── Circle points (blue) ──────────────────────────────────────────────────
    if show_circle.get():
        for (x, y) in circle_points:
            canvas.create_oval(
                x - POINT_RADIUS, y - POINT_RADIUS,
                x + POINT_RADIUS, y + POINT_RADIUS,
                fill="#0055ff", outline="black"
            )

def main():
    root = tk.Tk()
    root.title("Square & Circle — connected points")
    root.geometry(f"{START_SIZE}x{START_SIZE + 60}")

    # ── Toggle variables ──────────────────────────────────────────────────────
    show_square = tk.BooleanVar(value=True)
    show_circle = tk.BooleanVar(value=True)
    show_cross  = tk.BooleanVar(value=True)

    # ── Control panel ─────────────────────────────────────────────────────────
    panel = tk.Frame(root, bg="#f0f0f0", pady=6)
    panel.pack(fill="x")

    def make_cb(text, var, color):
        return tk.Checkbutton(
            panel, text=text, variable=var,
            font=("Arial", 10, "bold"),
            fg=color, bg="#f0f0f0", activebackground="#f0f0f0",
            command=lambda: redraw(canvas, canvas.winfo_width(),
                                   canvas.winfo_height(),
                                   show_square, show_circle, show_cross)
        )

    cb_square = make_cb("⬜  Square",        show_square, "#cc0000")
    cb_circle = make_cb("⭕  Circle",        show_circle, "#0055ff")
    cb_cross  = make_cb("🔀  Cross-lines",   show_cross,  "#cc7700")

    for cb in (cb_square, cb_circle, cb_cross):
        cb.pack(side="left", padx=18)

    # ── Canvas ────────────────────────────────────────────────────────────────
    canvas = tk.Canvas(root, bg="white", highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    # ── Resize handler ────────────────────────────────────────────────────────
    last_size = {"w": 0, "h": 0}

    def on_resize(event):
        if event.width != last_size["w"] or event.height != last_size["h"]:
            last_size["w"] = event.width
            last_size["h"] = event.height

            if event.width > event.height:
                event.height = event.width
            elif event.height > event.width:
                event.width =  event.height
                
            redraw(canvas, event.width, event.height,
                   show_square, show_circle, show_cross)

    canvas.bind("<Configure>", on_resize)

    root.mainloop()


if __name__ == "__main__":
    main()
