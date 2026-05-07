"""Generate figures for final report."""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

OUT = os.path.join(os.path.dirname(__file__), "figures")
os.makedirs(OUT, exist_ok=True)

# Common style
plt.rcParams.update({
    "font.family": "serif",
    "font.size": 10,
    "axes.labelsize": 10,
    "axes.titlesize": 11,
    "legend.fontsize": 9,
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
    "figure.dpi": 200,
})

# ============================================================
# Figure 1: FPR vs Recall trade-off (the headline figure)
# ============================================================
methods = [
    ("YOLO-only",          2.44, 0.7272, "o", "#444444"),
    ("I1 zero-shot CLIP",  0.55, 0.5625, "s", "#1f77b4"),
    ("I2 probe v1",        1.25, 0.7029, "^", "#2ca02c"),
    ("I2 probe v2",        0.70, 0.6830, "D", "#d62728"),
    ("I2 ensemble",        0.30, 0.6063, "P", "#9467bd"),
]

fig, ax = plt.subplots(figsize=(4.8, 3.2))
for name, fpr, recall, marker, color in methods:
    ax.scatter(fpr, recall, s=110, marker=marker, color=color, edgecolor="black",
               linewidth=0.7, zorder=3, label=name)

# Annotate
offsets = {
    "YOLO-only":         (8, -2),
    "I1 zero-shot CLIP": (8, -2),
    "I2 probe v1":       (8, 4),
    "I2 probe v2":       (8, 4),
    "I2 ensemble":       (-86, 4),
}
for name, fpr, recall, _, _ in methods:
    dx, dy = offsets[name]
    ax.annotate(name, xy=(fpr, recall), xytext=(dx, dy),
                textcoords="offset points", fontsize=8.5)

# Connecting lines: probe variants form a frontier
front = [("I2 ensemble", 0.30, 0.6063),
         ("I2 probe v2", 0.70, 0.6830),
         ("I2 probe v1", 1.25, 0.7029)]
front_x = [m[1] for m in front]
front_y = [m[2] for m in front]
ax.plot(front_x, front_y, "--", color="#888", linewidth=0.9, zorder=2,
        label="I2 operating points")

# Reference: YOLO and I1 line (the "legacy frontier")
ax.plot([0.55, 2.44], [0.5625, 0.7272], ":", color="#bbb", linewidth=0.9, zorder=1)

ax.set_xlabel("Hard-negative FPR (%)")
ax.set_ylabel("Mean recall (full test set)")
ax.set_title("FPR vs. Recall: I2 dominates the I1-YOLO frontier")
ax.set_xlim(-0.15, 2.85)
ax.set_ylim(0.53, 0.76)
ax.grid(alpha=0.3, linewidth=0.4)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

plt.tight_layout()
plt.savefig(os.path.join(OUT, "fpr_recall_frontier.pdf"), bbox_inches="tight")
plt.savefig(os.path.join(OUT, "fpr_recall_frontier.png"), bbox_inches="tight", dpi=200)
print("wrote fpr_recall_frontier.{pdf,png}")
plt.close()

# ============================================================
# Figure 2: Tau_high ablation
# ============================================================
taus = [0.00, 0.30, 0.50, 0.60, 0.70, 0.80, 0.90, 1.00]
fpr_pct = [2.44, 2.24, 1.60, 1.25, 1.25, 1.20, 1.15, 1.15]
filtered = [0, 5, 21, 28, 28, 29, 30, 30]

fig, ax1 = plt.subplots(figsize=(4.6, 3.0))
ax1.plot(taus, fpr_pct, "-o", color="#d62728", linewidth=1.5, markersize=6,
         markeredgecolor="black", markeredgewidth=0.5, label="HN-FPR (%)")
ax1.set_xlabel(r"Auto-keep threshold $\tau_{\mathrm{high}}$")
ax1.set_ylabel("Hard-negative FPR (%)", color="#d62728")
ax1.tick_params(axis="y", labelcolor="#d62728")
ax1.grid(alpha=0.3, linewidth=0.4)
ax1.axhline(y=2.44, color="#999", linestyle=":", linewidth=0.8)
ax1.text(0.05, 2.50, "YOLO-only baseline", fontsize=8, color="#666")
ax1.set_ylim(0.9, 2.7)

ax2 = ax1.twinx()
ax2.plot(taus, filtered, "-s", color="#2ca02c", linewidth=1.0, markersize=5,
         alpha=0.7, label="boxes filtered")
ax2.set_ylabel("FP boxes filtered", color="#2ca02c")
ax2.tick_params(axis="y", labelcolor="#2ca02c")
ax2.set_ylim(-2, 35)

ax1.set_title(r"Cascade gating: $\tau_{\mathrm{high}}$ sweep (LR probe)")
plt.tight_layout()
plt.savefig(os.path.join(OUT, "tau_sweep.pdf"), bbox_inches="tight")
plt.savefig(os.path.join(OUT, "tau_sweep.png"), bbox_inches="tight", dpi=200)
print("wrote tau_sweep.{pdf,png}")
plt.close()

# ============================================================
# Figure 3: Per-class results bar chart (I2 v2 headline)
# ============================================================
classes = ["smoke", "fire"]
yolo_p = [0.807, 0.689]
yolo_r = [0.791, 0.663]
i1_p   = [0.876, 0.742]
i1_r   = [0.605, 0.520]
i2_p   = [0.845, 0.698]
i2_r   = [0.720, 0.646]

x = np.arange(len(classes))
width = 0.13

fig, ax = plt.subplots(figsize=(5.0, 3.2))
ax.bar(x - 2.5*width, yolo_p, width, label="YOLO-only P", color="#999", edgecolor="black", linewidth=0.4)
ax.bar(x - 1.5*width, i1_p,   width, label="I1 P",        color="#1f77b4", edgecolor="black", linewidth=0.4)
ax.bar(x - 0.5*width, i2_p,   width, label="I2 v2 P",     color="#d62728", edgecolor="black", linewidth=0.4)
ax.bar(x + 0.5*width, yolo_r, width, label="YOLO-only R", color="#999",    hatch="//", edgecolor="black", linewidth=0.4)
ax.bar(x + 1.5*width, i1_r,   width, label="I1 R",        color="#1f77b4", hatch="//", edgecolor="black", linewidth=0.4)
ax.bar(x + 2.5*width, i2_r,   width, label="I2 v2 R",     color="#d62728", hatch="//", edgecolor="black", linewidth=0.4)

ax.set_xticks(x)
ax.set_xticklabels(classes)
ax.set_ylabel("Score")
ax.set_title("Per-class precision (solid) / recall (hatched)")
ax.set_ylim(0, 1.0)
ax.legend(loc="upper right", ncol=2, fontsize=7.5, framealpha=0.9)
ax.grid(axis="y", alpha=0.3, linewidth=0.4)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

plt.tight_layout()
plt.savefig(os.path.join(OUT, "per_class.pdf"), bbox_inches="tight")
plt.savefig(os.path.join(OUT, "per_class.png"), bbox_inches="tight", dpi=200)
print("wrote per_class.{pdf,png}")
plt.close()

print("Done.")
