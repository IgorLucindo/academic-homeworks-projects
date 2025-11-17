import numpy as np
import matplotlib.pyplot as plt


def main():
    # Create the figure
    _, ax = plt.subplots(figsize=(5, 5))

    # --- Proj_{R^2}(C_U): region where <1, x> > 0, x >= 0 ---
    # We'll shade the first quadrant except the origin
    x = np.linspace(0, 1.3, 100)
    y = np.linspace(0, 1.3, 100)
    X, Y = np.meshgrid(x, y)
    region = (X + Y > 0) & (X >= 0) & (Y >= 0)
    ax.contourf(X, Y, region, levels=[0.5, 1], colors=['#a0c4ff'], alpha=0.5)

    # --- U: line segment where <1, x> = 1 and x >= 0 ---
    x_u = np.linspace(0, 1, 100)
    y_u = 1 - x_u
    ax.plot(x_u, y_u, color='crimson', linewidth=2.5, label=r'$U:\ \langle 1, x \rangle = 1$')

    # --- Open circle at the origin (excluded point) ---
    ax.plot(0, 0, marker='o', markersize=8, markerfacecolor='white', 
            markeredgecolor='black', markeredgewidth=1.5, label='Excluded origin')

    # --- Axes and annotations ---
    ax.set_xlim(0, 1.3)
    ax.set_ylim(0, 1.3)
    ax.set_xlabel(r"$x_1$")
    ax.set_ylabel(r"$x_2$")
    ax.set_title(r"Visualization of $U$ and $\text{Proj}_{\mathbb{R}^2}(\mathcal{C}_U)$")

    # Labels
    ax.text(0.7, 0.6, r"$U$", color='crimson', fontsize=12)
    ax.text(0.9, 0.2, r"$\text{Proj}_{\mathbb{R}^2}(\mathcal{C}_U)$", color='#003366', fontsize=11)

    # Style
    ax.grid(True, linestyle='--', alpha=0.4)
    ax.set_aspect('equal')

    plt.show()


if __name__ == '__main__':
    main()