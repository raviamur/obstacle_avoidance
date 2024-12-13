from rplidar import RPLidar
import matplotlib.pyplot as plt

# Initialize LIDAR
PORT_NAME = '/dev/ttyUSB0'  # Replace with the correct port
lidar = RPLidar(PORT_NAME)

# Plot setup
plt.ion()
fig, ax = plt.subplots(figsize=(6, 6))
scan_plot, = ax.plot([], [], 'bo', markersize=2)
ax.set_xlim(0, 360)
ax.set_ylim(0, 5000)  # Adjust based on LIDAR range

def update_plot(angles, distances):
    """Update the scatter plot with LIDAR data."""
    scan_plot.set_xdata(angles)
    scan_plot.set_ydata(distances)
    ax.relim()
    ax.autoscale_view()
    plt.draw()  # Redraw the plot
    plt.pause(0.2)  # Brief pause for interactive mode

try:
    while True:

        if not plt.fignum_exists(fig.number):
            print("Plot window closed. Exiting...")
            break
        
        # Fetch a single scan
        scan = next(lidar.iter_scans())
        angles = [point[1] for point in scan]
        distances = [point[2] for point in scan]
        
        # Update the plot with the new data
        update_plot(angles, distances)
        lidar.stop()
        
        lidar.start_motor()   
        
except KeyboardInterrupt:
    print("Stopping LIDAR...")

finally:
    plt.close(fig)  # Close the plot properly
    lidar.stop()
    lidar.disconnect()