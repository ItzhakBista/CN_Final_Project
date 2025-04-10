# CN_Final_Project
# Traffic Analysis with Scapy and Machine Learning

This repository contains a Python script for analyzing network traffic captured in PCAP files. The script processes traffic from different applications, generates statistical data, and uses machine learning (K-Means clustering) to simulate an attacker trying to identify applications based on traffic patterns.

## Prerequisites

Before running the script, ensure that you have the following installed:

- **Python 3.x**
- **Required Python packages**:
  - `scapy` – for processing and analyzing PCAP files.
  - `matplotlib` – for plotting graphs.
  - `numpy` – for numerical operations.
  - `sklearn` – for machine learning clustering and preprocessing.

You can install the required dependencies with the following command:
```bash
pip install scapy matplotlib numpy scikit-learn
```
## Directory Structure
*The project directory should look like this:*
```bash
/project-directory
│
├── /images/                     # Directory for saving plots and graphs
│
├── chrome_browsing.pcap          
├── edge_browsing.pcap
├── spotify_streaming.pcap
├── youtube_streaming.pcap
├── zoom_meeting.pcap
│
├── analyze.py                     # Main Python script
└── README.md                     # This README file
```
## Running the Script
*Prepare the PCAP files:*
Ensure that the required PCAP files (for example: chrome_browsing.pcap, edge_browsing.pcap, etc.) are present in the project directory. These files contain the network traffic data to be analyzed.

*Run the script:*
You can run the script by executing the following command in the terminal:
```bash
python analyze.py
```
This will process the PCAP files, generate graphs for packet size distribution, TCP window sizes, inter-arrival times, and more. It will also simulate an attacker using clustering and generate a confusion matrix for classification.

*Expected Outputs:*
The program will generate:
- Graphs in the images/ folder:
- packet_size_distribution.png
- inter_arrival_times.png
- tcp_window_distribution.png
- ip_ttl_distribution.png
- flow_comparison.png

**Terminal output including:**
- Statistical analysis of traffic patterns
- Flow summaries for each application
- Clustering results and classification accuracy
- 
## Features
- Packet Size Distribution: Analyzes and visualizes the distribution of packet sizes for each application.
- Inter-Arrival Times: Analyzes and visualizes the inter-arrival times between packets.
- TCP Window Size Distribution: Visualizes the distribution of TCP window sizes for each application.
- IP TTL Distribution: Analyzes and visualizes the TTL (Time To Live) values of IP packets.
- Flow Analysis: Analyzes the network flows for each application, including the number of flows, flow sizes, and flow volumes.
- Machine Learning (Clustering): Simulates an attacker trying to identify applications based on packet sizes and inter-arrival times, using K-Means clustering.

## Explanation of Code
- create_images_directory(): Creates a directory named images if it doesn't exist, where all plots and graphs are saved.
- analyze_pcap(filename): Reads and processes a PCAP file. It extracts the packet size, timestamp, IP TTL, TCP window size, inter-arrival times, and flow information.
- plot_comparison(app_data): Plots histograms for packet size distribution, inter-arrival times, TCP window sizes, and IP TTL values for each application.
- simulate_attacker(data): Simulates an attacker trying to classify applications based on network traffic features (packet sizes and inter-arrival times). It uses K-Means clustering and prints a confusion matrix with classification results.
- summarize_flows(app_data): Prints statistics about network flows for each application, including the total number of flows, average flow size, and volume.
- plot_flow_comparison(app_data): Plots the number of flows, average flow size, and average flow volume for each application.

## Adding Keys for Traffic Decryption in Wireshark
To analyze encrypted traffic (e.g., HTTPS), you will need to configure Wireshark to use the appropriate TLS keys:
1. Open **Wireshark** and navigate to `Edit` > `Preferences`.
2. In the **Protocols** section, find  **TLS**.
3. Add the **path to the private key**
4. Save the settings and restart Wireshark to decrypt the traffic.






