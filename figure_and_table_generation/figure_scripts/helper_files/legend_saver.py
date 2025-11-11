import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.lines import Line2D


def save_legend_png(
    handles,
    filename,
    labels=None,
    ncol=1,
    title=None,
    frameon=False,
    dpi=200,
    label_fontsize=10,
    title_fontsize=None,
    pad_in=0.25,
):
    """
    Save a standalone legend as a PNG (transparent background).

    Parameters
    ----------
    handles : list[Artist]
        E.g., Patches or Line2D objects (proxy artists).
    labels : list[str] | None
        If None, uses handle labels.
    filename : str
        Output path.
    ncol : int
        Number of legend columns.
    title : str | None
        Optional legend title.
    frameon : bool
        Draw a frame around the legend.
    dpi : int
        Output DPI.
    label_fontsize : int | float
        Font size for legend labels.
    title_fontsize : int | float | None
        Font size for legend title (defaults to label_fontsize+1).
    pad_in : float
        Extra padding around the legend in inches.
    """
    # Create an empty figure just for the legend
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.axis("off")

    if labels is None:
        labels = [h.get_label() for h in handles]

    leg = fig.legend(
        handles=handles,
        labels=labels,
        loc="center",
        ncol=ncol,
        frameon=frameon,
        title=title,
        fontsize=label_fontsize,
    )
    if title and title_fontsize is None:
        title_fontsize = label_fontsize + 1
    if title and title_fontsize:
        leg.get_title().set_fontsize(title_fontsize)

    # Measure legend size and resize figure tightly around it
    fig.canvas.draw()
    bbox = leg.get_window_extent(fig.canvas.get_renderer())
    w_in, h_in = bbox.width / fig.dpi, bbox.height / fig.dpi
    fig.set_size_inches(w_in + pad_in, h_in + pad_in)

    # Transparent background
    fig.patch.set_alpha(0)

    fig.savefig(filename, dpi=dpi, bbox_inches="tight", transparent=True)
    plt.close(fig)


# --- Convenience helpers to build handles quickly ---


def box_handles(labels, colors, edgecolor="none"):
    """Square color boxes (categories)."""
    return [
        Patch(facecolor=c, edgecolor=edgecolor, label=l) for l, c in zip(labels, colors)
    ]


def marker_handles(labels, colors, markers=None, linestyle="none", linewidth=2):
    """Markers/lines for series."""
    return [
        Line2D(
            [0],
            [0],
            color=colors[i],
            linestyle=linestyle,
            linewidth=linewidth,
            label=labels[i],
        )
        for i in range(len(labels))
    ]
