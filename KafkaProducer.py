from kafka import KafkaProducer
import numpy as np
import json
import time
import random

class DataProducer:
    def __init__(self, topic='data_anamoly', bootstrap_servers='localhost:9092'):
        """
        Initializing the DataProducer class. It produces a continous stream of float-point data

        Args:
            1. topic (str): Kafka topic to which data will be produced. By Default it is 'data_anamoly'.
            bootstrap_servers (str): Address of the Kafka broker. By Default is 'localhost:9092'.
        """
        self.producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        self.topic = topic
        self.drift = 0  # Initialize the seasonal drift component to 0

    def generate_data_stream(self):
        """
        Generates a continuous stream of random floating-point numbers with seasonal drifts and occasional spikes.
        Yields:
            float: A generated value from the data stream.
        """
        t = 0  # Time step for updating the seasonal drift component
        
        while True:
            # Update the seasonal drift rate with a small random change
            drift_change = np.random.normal(0, 1.0)  # Normal distribution with mean 0 and std deviation 1
            self.drift += drift_change  # Accumulate drift change to the drift component

            # Generate a base value from a uniform distribution and add the drift component
            base_value = np.random.uniform(low=-100, high=100) + self.drift

            # Add Gaussian noise to the base value to simulate real-world variability
            noise = np.random.normal(0, 5)  # Normal distribution with mean 0 and std deviation 5
            value = base_value + noise

            # Occasionally introduce a random spike into the value
            if random.random() < 0.1:  # 10% chance to introduce a spike
                spike_magnitude = np.random.uniform(200, 500)  # Generate a random magnitude for the spike
                spike_direction = random.choice([-1, 1])  # Determine if the spike is positive or negative
                # Apply the spike to the value, also influenced by the current drift
                value += spike_direction * (spike_magnitude + abs(self.drift) * 2)  # Amplify spike with drift

            # Increment the time step (not used here but could be useful for future extensions)
            t += 1

            # Yield the generated value to be processed
            yield value

    def produce_data(self):
        """
        Continuously produces the generated data to the specified Kafka topic.
        
        Sends data to Kafka at a fixed interval to simulate real-time data streaming.
        """
        for value in self.generate_data_stream():
            # Send the generated value to the Kafka topic in a JSON-encoded format
            self.producer.send(self.topic, {'value': value})
            # Sleep for 0.1 seconds to simulate a delay between data points
            time.sleep(0.1)  # Adjust the sleep time as needed to match the desired data stream rate
