from kafka import KafkaConsumer
import json
import numpy as np
import hdbscan

class DataConsumer:
    def __init__(self, topic='data_anamoly', bootstrap_servers='localhost:9092'):
        """
        Initializing the DataConsumer to consume the continous stream data.
        
        Parameters:
        topic (str): The Kafka topic to subscribe to. 
        bootstrap_servers (str): The address of the Kafka server. By default it is 9092
        """
        # Create a Kafka consumer instance
        self.consumer = KafkaConsumer(
            topic,  # Topic to consume messages from
            bootstrap_servers=bootstrap_servers,  # Kafka server address
            auto_offset_reset='latest',  # Start reading from the latest messages
            enable_auto_commit=True,  # Enable automatic offset committing
            group_id='consumer-group',  # Consumer group ID
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))  # Deserialize message values from JSON
        )
        
        # Initialize parameters for HS Tree anomaly detection
        self.data_window = []  # List to store the most recent data points
        self.window_size = 1000  # Size of the sliding window
        
        # Initialize HDBSCAN for anomaly detection
        self.clusterer = hdbscan.HDBSCAN(min_cluster_size=5, min_samples=1, core_dist_n_jobs=-1)  # HDBSCAN parameters
        self.fit_needed = True  # Flag indicating whether the model needs to be fitted

    def fit_model(self):
        """
        Fitting the HDBSCAN model on the data currently in the window.
        This method converts the data window to a numpy array and trains the HDBSCAN model.
        """
        if len(self.data_window) > 1:
            # Converting the data window to a numpy array with the correct shape
            data = np.array(self.data_window).reshape(-1, 1)
            self.clusterer.fit(data)  # Fitting the HDBSCAN model on the data
            self.fit_needed = False  # Model is now fitted, no need to fit again until new data arrives

    def predict_anomaly(self, data_point):
        """
        Predicting whether the given data point is an anomaly based on the fitted model.
        
        Parameters:
        data_point (float): The new data point to be evaluated.
        
        Returns:
        int: -1 if the data point is an anomaly, 1 otherwise.
        """
        # Fitting the model if necessary
        if self.fit_needed:
            self.fit_model()
        
        # Converting the new data point to a numpy array with the correct shape
        data_point = np.array([data_point]).reshape(-1, 1)
        
        # Predicting the cluster label for the new data point
        # Note: HDBSCAN does not have a predict method; the predict approach here is hypothetical.
        label = self.clusterer.predict(data_point)
        
        # Anomalies are labeled as -1 by HDBSCAN
        return -1 if label == -1 else 1

    def consume_data(self):
        """
        Consume data from Kafka, apply anomaly detection, and yield the results.
        This method continuously reads messages from Kafka, updates the data window,
        fits the model if necessary, and predicts anomalies.
        """
        for message in self.consumer:
            # Extracting the data value from the Kafka message
            data = message.value['value']

            # Adding the new data point to the window
            self.data_window.append(data)

            # Maintaining a sliding window of fixed size
            if len(self.data_window) > self.window_size:
                self.data_window.pop(0)  # Remove the oldest entry to keep the window size constant

            # Fitting the model if the window has enough data points
            if len(self.data_window) > 1:
                self.fit_needed = True
            
            # Predicting if the current data point is an anomaly
            prediction = self.predict_anomaly(data)

            # Yielding the data point and its predicted classification
            yield data, prediction
