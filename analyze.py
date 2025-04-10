import os
import logging
from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np
import scapy.all as scapy
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix

logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
scapy.conf.use_pcap = False

def create_images_directory():
    if not os.path.exists('images'):
        os.makedirs('images')


def analyze_pcap(filename):
    print(f"Analyzing {filename}...")
    try:
        packets = scapy.rdpcap(filename)
        packets = [p for p in packets if p.time is not None]
    except Exception as e:
        print(f"Error reading {filename}: {str(e)}")
        return None

    if not packets:
        print(f"No valid packets in {filename}")
        return None

    data = {
        'packet_sizes': [],
        'timestamps': [],
        'ip_ttl': [],
        'tcp_window': [],
        'inter_arrivals': [],
        'flows': defaultdict(lambda: {'size': 0, 'volume': 0})
    }

    prev_time = float(packets[0].time)
    for pkt in packets:
        try:
            current_time = float(pkt.time)
            size = int(len(pkt))
            data['packet_sizes'].append(size)
            data['timestamps'].append(current_time)

            if scapy.IP in pkt:
                data['ip_ttl'].append(int(pkt[scapy.IP].ttl))

                if scapy.TCP in pkt:
                    data['tcp_window'].append(int(pkt[scapy.TCP].window))

                    flow_id = (
                        pkt[scapy.IP].src,
                        pkt[scapy.IP].dst,
                        pkt[scapy.TCP].sport,
                        pkt[scapy.TCP].dport
                    )

                    data['flows'][flow_id]['size'] += 1
                    data['flows'][flow_id]['volume'] += size

            if prev_time is not None:
                data['inter_arrivals'].append(float(current_time - prev_time))
            prev_time = current_time

        except Exception as e:
            print(f"Packet processing error: {str(e)}")
            continue

    return data


def plot_comparison(app_data):
    create_images_directory()

    plt.figure(figsize=(15, 10))
    valid_apps = {k: v for k, v in app_data.items() if v and v['packet_sizes']}

    plt.subplot(1, 1, 1)
    for app, data in valid_apps.items():
        plt.hist(data['packet_sizes'], bins=50, alpha=0.5, label=app)
    plt.title('Packet Size Distribution')
    plt.xlabel('Bytes')
    plt.ylabel('Count')
    plt.legend()

    plt.savefig('images/packet_size_distribution.png')
    plt.clf()

    plt.subplot(1, 1, 1)
    for app, data in valid_apps.items():
        if data['inter_arrivals']:
            plt.hist(data['inter_arrivals'], bins=50, alpha=0.5, label=app, range=(0, 0.1))
    plt.title('Packet Inter-arrival Times')
    plt.xlabel('Seconds')
    plt.ylabel('Count')
    plt.legend()

    plt.savefig('images/inter_arrival_times.png')
    plt.clf()

    plt.subplot(1, 1, 1)
    for app, data in valid_apps.items():
        if data['tcp_window']:
            plt.hist(data['tcp_window'], bins=30, alpha=0.5, label=app)
    plt.title('TCP Window Size Distribution')
    plt.xlabel('Window Size')
    plt.ylabel('Count')
    plt.legend()

    plt.savefig('images/tcp_window_distribution.png')
    plt.clf()

    plt.subplot(1, 1, 1)
    for app, data in valid_apps.items():
        if data['ip_ttl']:
            plt.hist(data['ip_ttl'], bins=30, alpha=0.5, label=app)
    plt.title('IP TTL Distribution')
    plt.xlabel('TTL')
    plt.ylabel('Count')
    plt.legend()

    plt.savefig('images/ip_ttl_distribution.png')
    plt.clf()
    plt.tight_layout()
    plt.close()


def classify_applications(app_data):
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import classification_report, confusion_matrix

    features = []
    labels = []
    label_map = {}

    for i, (app, d) in enumerate(app_data.items()):
        label_map[i] = app
        if d and d['packet_sizes'] and d['inter_arrivals']:
            packet_sizes = np.array(d['packet_sizes'])
            inter_arrivals = np.array(d['inter_arrivals'])
            tcp_windows = np.array(d['tcp_window']) if d['tcp_window'] else np.zeros(len(packet_sizes))

            feature_vector = [
                np.mean(packet_sizes),
                np.std(packet_sizes),
                np.median(packet_sizes),
                np.mean(inter_arrivals),
                np.std(inter_arrivals),
                np.max(packet_sizes) / (np.min(packet_sizes) + 1),
                np.mean(tcp_windows) if len(tcp_windows) else 0,
            ]

            for _ in range(min(100, len(packet_sizes) // 5)):
                features.append(feature_vector)
                labels.append(i)

    if len(set(labels)) < 2:
        print("Insufficient class diversity for classification.")
        return

    X = np.array(features)
    y = np.array(labels)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    clf = RandomForestClassifier(n_estimators=200, random_state=42)
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)

    print("\n🌟 Classification Report:")
    print(classification_report(y_test, y_pred, target_names=[label_map[i] for i in sorted(label_map)]))

    cm = confusion_matrix(y_test, y_pred)

    print("\n🎯 Classification by Application:")
    for i in range(len(cm)):
        correct = cm[i, i]
        total = sum(cm[i, :])
        app_name = label_map[i]
        percentage = (correct / total) * 100 if total > 0 else 0
        print(f"{app_name}: {correct}/{total} correctly classified ({percentage:.1f}%)")


def summarize_flows(app_data):
    print("\n📦 Flow Summary Per App:")

    for app, d in app_data.items():
        flows = d.get('flows', {})
        if not flows:
            print(f"{app}: No flow data.")
            continue

        num_flows = len(flows)
        sizes = [f['size'] for f in flows.values()]
        volumes = [f['volume'] for f in flows.values()]

        print(f"\n🔹 {app}:")
        print(f"Total flows: {num_flows}")
        print(f"Average flow size (packets): {np.mean(sizes):.2f}")
        print(f"Max flow size: {np.max(sizes)} packets")
        print(f"Average flow volume (bytes): {np.mean(volumes):.2f}")
        print(f"Max flow volume: {np.max(volumes)} bytes")

def plot_flow_comparison(app_data):
    valid_apps = {k: v for k, v in app_data.items() if v and v.get('flows')}
    if not valid_apps:
        print("No flow data to plot.")
        return

    create_images_directory()

    app_names = []
    flow_counts = []
    avg_sizes = []
    avg_volumes = []

    for app, d in valid_apps.items():
        flows = d['flows']
        sizes = [f['size'] for f in flows.values()]
        volumes = [f['volume'] for f in flows.values()]
        app_names.append(app)
        flow_counts.append(len(flows))
        avg_sizes.append(np.mean(sizes))
        avg_volumes.append(np.mean(volumes))

    plt.figure(figsize=(15, 6))

    plt.subplot(1, 3, 1)
    plt.bar(app_names, flow_counts, color='skyblue')
    plt.title('Number of Flows per App')
    plt.ylabel('Flows')

    plt.subplot(1, 3, 2)
    plt.bar(app_names, avg_sizes, color='lightgreen')
    plt.title('Average Flow Size (packets)')
    plt.ylabel('Packets per Flow')

    plt.subplot(1, 3, 3)
    plt.bar(app_names, avg_volumes, color='salmon')
    plt.title('Average Flow Volume (bytes)')
    plt.ylabel('Bytes per Flow')

    plt.tight_layout()
    plt.savefig('images/flow_comparison.png')
    plt.close()




if __name__ == "__main__":
    apps = ['chrome_browsing', 'edge_browsing', 'spotify_streaming', 'youtube_streaming', 'zoom_meeting']
    app_data = {}

    for app in apps:
        pcap_file = f'{app}.pcap'
        print(f"\nProcessing {pcap_file}...")
        app_data[app] = analyze_pcap(pcap_file)

    app_data = {k: v for k, v in app_data.items() if v is not None}

    if app_data:

        plot_comparison(app_data)
        summarize_flows(app_data)
        plot_flow_comparison(app_data)
        classify_applications(app_data)
    else:
        print("\nNo valid data to analyze")