from KafkaProducer import DataProducer
from KafkaConsumer import DataConsumer
from visualizer import RealTimeVisualizer
import threading

def start_producer():
    producer = DataProducer(topic='data_anamoly')  # topic to which data will be produced
    producer.produce_data()

def start_consumer_and_visualizer():
    consumer = DataConsumer(topic='data_anamoly')  # Passing the topic name to which consumer will consume the data
    visualizer = RealTimeVisualizer(consumer.consume_data())
    visualizer.start()

if __name__ == "__main__":
    # Starting the Kafka producer in a separate thread
    producer_thread = threading.Thread(target=start_producer)
    producer_thread.start()

    # Starting the Kafka consumer and visualizer in the main thread
    start_consumer_and_visualizer()
