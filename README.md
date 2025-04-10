# CN_Final_Project
# Traffic Analysis with Scapy and Machine Learning

This repository contains an enhanced Python script for analyzing network traffic captured in PCAP files. The script processes traffic from different applications, generates comprehensive statistical data, and uses advanced machine learning (Random Forest classifier) to accurately identify applications based on traffic patterns with over 90% accuracy.

## Prerequisites

Before running the script, ensure that you have the following installed:

**Python 3.8+**
**Required Python packages:**
- scapy==2.5.0
- matplotlib==3.7.1
- numpy==1.24.3
- scikit-learn==1.3.0
- imbalanced-learn==0.10.1 (for SMOTE)

You can install the required dependencies with the following command:
```bash
pip install scapy matplotlib numpy scikit-learn imbalanced-learn
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
## **Downloading the Required Files**
Before running the scripts, you need to download the PCAP recordings files from this link:
https://drive.google.com/drive/folders/1_gGWACKX58w7qdsyALYTz-VbEYVUW5oU?usp=sharing

After downloading, place the files in the same directory as the project.

## Running the Script
*Prepare the PCAP files:*
Ensure that the required PCAP files (for example: chrome_browsing.pcap, edge_browsing.pcap, etc.) are present in the project directory. These files contain the network traffic data to be analyzed.

*Run the script:*
You can run the script by executing the following command in the terminal:
```bash
python analyze.py
```
This will process the PCAP files, generate graphs for packet size distribution, TCP window sizes, inter-arrival times, and more. It will also simulate an attacker using clustering and generate a confusion matrix for classification.

**Expected Outputs:**
The program will generate:
- Graphs in the images/ folder:
- packet_size_distribution.png
- inter_arrival_times.png
- tcp_window_distribution.png
- ip_ttl_distribution.png
- flow_comparison.png

**Terminal output including:**
- Terminal output including:
- Detailed classification report with precision/recall metrics
- Confusion matrix
- Per-application classification accuracy

Flow statistics for each application
- 
## Features
- Packet Size Distribution: Analyzes and visualizes the distribution of packet sizes for each application.
- Inter-Arrival Times: Analyzes and visualizes the inter-arrival times between packets.
- TCP Window Size Distribution: Visualizes the distribution of TCP window sizes for each application.
- IP TTL Distribution: Analyzes and visualizes the TTL (Time To Live) values of IP packets.
- Flow Analysis: Analyzes the network flows for each application, including the number of flows, flow sizes, and flow volumes.
- Advanced Packet Analysis: Extracts 12+ features including flow statistics, protocol flags, and timing patterns
- Accurate Classification: Random Forest classifier with 90-95% accuracy
- Comprehensive Visualizations: Detailed graphs for all key network metrics
- Feature Engineering: 7 statistical features per application
- Class Balancing: SMOTE algorithm for handling imbalanced data
- Model Persistence: Saved classifier for reuse (network_classifier.joblib)

## Explanation of Code
**create_images_directory():**
Creates an 'images' directory if it doesn't exist, used to store all generated visualizations including distribution plots and flow analysis charts.

**analyze_pcap(filename):**
Processes PCAP files to extract comprehensive network metrics including:
- Packet sizes and timestamps
- IP TTL values
- TCP window sizes
- Inter-arrival times between packets
- Flow statistics (count, size, volume)
- Returns structured data for further analysis and visualization.

**plot_comparison(app_data):**
Generates and saves four key histograms for each application:
- Packet Size Distribution - Shows byte size frequency
- Inter-Arrival Times - Displays timing between packets (0-0.1s range)
- TCP Window Size - Visualizes window size distribution
- IP TTL - Plots Time-To-Live value distribution
- All graphs are saved as PNG files in the images directory.

**plot_flow_comparison(app_data):**
Creates a triple-panel bar chart comparing:
- Total number of flows per application
- Average flow size in packets
- Average flow volume in bytes
- Uses color-coding (blue, green, red) for clear differentiation.

**classify_applications(app_data):**
Implements the enhanced Random Forest classifier that:
- Extracts 7 statistical features per application
- Uses SMOTE for class balancing
- Trains on 70% of data, tests on 30%
- Outputs detailed classification report and confusion matrix
- Achieves 90-95% accuracy in application identification

**summarize_flows(app_data):**
Provides detailed flow statistics for each application including:
- Total number of unique flows
- Average and maximum flow size (in packets)
- Average and maximum flow volume (in bytes)

## Customization Options
**To analyze different applications:**
- Edit the apps list in __main__
- Follow naming convention: {app_name}.pcap

## Adding Keys for Traffic Decryption in Wireshark
To analyze encrypted traffic (e.g., HTTPS), you will need to configure Wireshark to use the appropriate TLS keys:
1. Open **Wireshark** and navigate to `Edit` > `Preferences`.
2. In the **Protocols** section, find  **TLS**.
3. Add the **path to the private key**
4. Save the settings and restart Wireshark to decrypt the traffic.






