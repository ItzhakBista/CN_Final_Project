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

## Directory Structure
*The project directory should look like this:*

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

## Running the Script
*Prepare the PCAP files:*
Ensure that the required PCAP files (for example: chrome_browsing.pcap, edge_browsing.pcap, etc.) are present in the project directory. These files contain the network traffic data to be analyzed.

*Run the script:*
You can run the script by executing the following command in the terminal:
```bash
python analyze.py
This will process the PCAP files, generate graphs for packet size distribution, TCP window sizes, inter-arrival times, and more. It will also simulate an attacker using clustering and generate a confusion matrix for classification.
