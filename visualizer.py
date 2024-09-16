import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class RealTimeVisualizer:
    def __init__(self, data_stream):
        self.data_stream = data_stream  # Data stream from Kafka consumer
        self.fig, self.ax = plt.subplots()
        self.x_data, self.y_data = [], []
        self.anomaly_x, self.anomaly_y = [], []  # To store anomaly points
        self.line, = self.ax.plot([], [], lw=2, label='Data Stream', color='blue')  # Blue line for data stream

        # Adding plot labels and title
        self.ax.set_xlabel('Time')  # X-axis label
        self.ax.set_ylabel('Value')  # Y-axis label
        self.ax.set_title('Data Stream with Anomaly Detection')  # Plot title

        # Creating a scatter for anomalies (red dots)
        self.anomaly_points, = self.ax.plot([], [], 'ro', label='Anomalies', marker='o', linestyle='None')  # Red dots for anomalies

    def update_plot(self, frame):
        # Fetching the latest data from Kafka
        data, prediction = next(self.data_stream)

        self.x_data.append(len(self.x_data))  # Simulating time axis
        self.y_data.append(data)

        # Updating the data stream line
        self.line.set_data(self.x_data, self.y_data)

        # Updating the anomaly points if prediction indicates an anomaly (-1)
        if prediction == -1:
            self.anomaly_x.append(len(self.x_data) - 1)
            self.anomaly_y.append(data)
            self.anomaly_points.set_data(self.anomaly_x, self.anomaly_y)  # Add red dot

        # Adjusting the plot limits dynamically
        self.ax.relim()
        self.ax.autoscale_view()

        return self.line, self.anomaly_points

    def start(self):
        # Creating the animation that updates the plot
        ani = FuncAnimation(self.fig, self.update_plot, interval=1000, cache_frame_data=False)

        # Adding legend with symbols
        self.ax.legend(
            loc='upper right',
            frameon=True
        )

        plt.show()
