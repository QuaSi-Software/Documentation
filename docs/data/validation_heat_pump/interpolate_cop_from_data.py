"""
Interpolate field from data
"""
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
import pandas as pd
from scipy.interpolate import RBFInterpolator

def create_mesh(x_min, x_max, x_step, y_min, y_max, y_step):
    """Create mesh"""
    return np.meshgrid(np.linspace(x_min, x_max, int((x_max - x_min) / x_step) + 1),
                       np.linspace(y_min, y_max, int((y_max - y_min) / y_step) + 1))

def load_support_data(file_path):
    """Load support data"""
    data = pd.read_csv(file_path, delimiter=";", decimal=".")
    return data["x"], data["y"], data["z"]

def main():
    """Main script body"""
    scale = 1.0
    offset = 0.0

    # load support data
    input_file_path = "./support_points.csv"
    x_support, y_support, z_support = load_support_data(input_file_path)
    support_points = np.stack([x_support.to_numpy(), y_support.to_numpy()], -1)

    # create output mesh
    x_dense, y_dense = create_mesh(-20, 40, 5, 15, 70, 5)
    dense_points = np.stack([x_dense.ravel(), y_dense.ravel()], -1) # shape (N, 2) in 2d

    # inter- and extrapolate data based on support data to output mesh
    interpolator = RBFInterpolator(
        support_points, z_support.to_numpy(), smoothing=0, kernel='cubic'
    )
    z_dense = interpolator(dense_points).reshape(x_dense.shape)

    # plot interpolated mesh data and support points
    fig, ax = plt.subplots(subplot_kw={"projection": "3d", "computed_zorder": False})
    ax.plot_surface(x_dense, y_dense, z_dense, cmap=cm.cool)
    ax.plot(x_support, y_support, z_support, linestyle='None', markersize = 5.0, marker='o')

    # write interpolated results to file as points
    with open("./interpolated_points.csv", "w", encoding="utf-8") as file:
        file.write("x;y;z\n")
        for ix, x_val in enumerate(x_dense[0]):
            for iy, y_arr in enumerate(y_dense):
                y_val = y_arr[0]
                # note the switched index, for whatever reason
                z_val = z_dense[iy,ix]  * scale + offset
                file.write(f"{x_val:0.2f};")
                file.write(f"{y_val:0.2f};")
                file.write(f"{z_val:0.4f}\n")

    # write interpolated results to file as ReSiE input field data
    with open("./interpolated_field.csv", "w", encoding="utf-8") as file:
        # first line is zero followed by output temperatures (y values)
        file.write("0") # zero doesn't matter, could be anything
        for iy, y_arr in enumerate(y_dense):
            y_val = y_arr[0]
            file.write(f",{y_val:0.1f}")

        # each following line is for one input temperature and all output temperatures
        for ix, x_val in enumerate(x_dense[0]):
            file.write(";")
            file.write(f"{x_val:0.1f}")
            for iy, y_arr in enumerate(y_dense):
                y_val = y_arr[0]
                z_val = z_dense[iy,ix] * scale + offset
                file.write(f",{z_val:0.4f}")
        file.write("\n")

    # initialize view and register callback for updates
    elevation = 20 # degrees, not radians
    azimuth = 50

    def update_view(event):
        nonlocal azimuth
        if event.key == 'right':
            azimuth += 10 # rotate clockwise (around Z-axis)
        elif event.key == 'left':
            azimuth -= 10
        ax.view_init(elev=elevation, azim=azimuth)
        fig.canvas.draw()

    ax.view_init(elev=elevation, azim=azimuth)
    fig.canvas.mpl_connect('key_press_event', update_view)

    # start interactive plot window
    plt.show()

# entry point
main()
