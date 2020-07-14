from math import pi

import pandas as pd
from bokeh.embed import components
from bokeh.io import curdoc
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.palettes import Blues256, Category20c
from bokeh.plotting import figure
from bokeh.themes import built_in_themes
from bokeh.transform import cumsum, factor_cmap


def plot_bar_chart(x, y):
    curdoc().theme = "dark_minimal"

    source = ColumnDataSource(dict(y=y, right=x))
    # Add plot
    p = figure(
        title="Expense by categories",
        y_range=y,
        plot_width=800,
        x_axis_label="Amount",
        toolbar_location=None,
    )
    # Render glyph
    blues = []
    for i in range(15):
        blues.append(Blues256[i * 16])
    p.hbar(
        y="y",
        right="right",
        left=0,
        height=0.4,
        fill_color=factor_cmap("y", palette=blues, factors=y),
        source=source,
    )

    p.x_range.start = 0
    p.add_tools(HoverTool(tooltips=[("CATEGORY", "@y"), ("AMOUNT", "@right{1.11}")]))

    curdoc().add_root(p)
    script, div = components(p)

    return (script, div)


def plot_pie_chart(x):
    curdoc().theme = "dark_minimal"
    data = pd.Series(x).reset_index(name="value").rename(columns={"index": "category"})
    data["angle"] = data["value"] / data["value"].sum() * 2 * pi
    if len(x) > 2:
        data["color"] = Category20c[len(x)]
    elif len(x) > 1:
        data["color"] = ["#3182bd", "#e6550d"]
    else:
        data["color"] = ["#3182bd"]

    p = figure(
        plot_width=800,
        title="Expense by categories",
        toolbar_location=None,
        tools="hover",
        tooltips="@category: @value{1.11}",
        x_range=(-0.5, 1.0),
    )

    p.wedge(
        x=0,
        y=1,
        radius=0.4,
        start_angle=cumsum("angle", include_zero=True),
        end_angle=cumsum("angle"),
        line_color="white",
        fill_color="color",
        legend_field="category",
        source=data,
    )

    p.axis.axis_label = None
    p.axis.visible = False
    p.grid.grid_line_color = None

    curdoc().add_root(p)
    script, div = components(p)

    return (script, div)
