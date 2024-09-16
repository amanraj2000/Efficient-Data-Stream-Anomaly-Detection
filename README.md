Efficient Data Stream Anomaly Detection

Python Version Used - 3.11.0


Algorithm Chosen - Half-Space Tree (HS Tree)

Half-Space Tree: It is a data structure used for efficient anomaly detection, particularly in high-dimensional spaces. It is designed to identify outliers or unusual patterns by partitioning the data space into regions using hyperplanes.

Reasons for adopting this algorithm - 

1. High Dimensionality Handling: HS Tree is designed to handle high-dimensional data efficiently. In financial transactions and system metrics, data often involves multiple features (e.g., transaction amount, time of day, user behavior metrics), making it important to use a method that can manage such complexity.

2. Scalability: HS Tree is scalable and can handle large datasets effectively. It works well with large volumes of continuous data, such as financial transactions over time, by partitioning the data into smaller, manageable regions.

3. Efficient Anomaly Detection: The HS Tree method uses a geometric approach to partition the data space, which allows it to identify anomalies by finding regions of the space that do not conform to the majority of the data. This geometric partitioning can be particularly useful for detecting subtle deviations in continuous data streams.

4. Concept Drift Adaptation: HS Tree can adapt to changes in data distribution over time, known as concept drift. This is crucial in financial transactions and system metrics where patterns can evolve, and new types of anomalies can emerge.

5. Real-Time Application: The method is suitable for real-time anomaly detection because it can quickly update its tree structure as new data arrives. This is important for continuous monitoring of financial transactions or system metrics.

6. Versatility: HS Tree can be adapted to different anomaly detection scenarios, whether the anomalies are outliers, changes in distribution, or unusual patterns in the data.






Result Plots of Anamoly Detection :

1. Anomaly detection on slow Seasonal Drift data
![Anamoly_Detection](https://github.com/user-attachments/assets/0e984df5-7ed5-4e5c-a8f6-9df49d9f7a88)





2. Anomaly Detection on rapid Seasonal Drift data

![Anamoly_Detection_2](https://github.com/user-attachments/assets/3bb99c8f-067a-4bba-bb4b-d161de0ee770)



