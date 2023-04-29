import psutil
import time
import matplotlib.pyplot as plt
import speedtest
import matplotlib
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

matplotlib.use("TkAgg")
canvas = False

    
def get_bytes():
    return psutil.net_io_counters().bytes_sent + psutil.net_io_counters().bytes_recv

def record_bandwidth_traffic(x_bandwidth, y_bandwidth, x_traffic, y_traffic, duration=10):
    print("Recording data for", duration, "seconds...")
    bytes_start = get_bytes()
    start_time = time.time()
    while time.time() - start_time <= duration:
        bytes_end = get_bytes()
        bytes_diff = bytes_end - bytes_start
        now = time.time()
        x_bandwidth.append(now)
        y_bandwidth.append(bytes_diff)
        x_traffic.append(now)
        y_traffic.append(bytes_end)
        time.sleep(1)
        bytes_start = bytes_end

def plot_bandwidth_traffic(x_bandwidth, y_bandwidth, x_traffic, y_traffic):
    # delete all plots
    plt.clf()
    
    fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
    ax1.plot(x_bandwidth, y_bandwidth)
    ax1.set_title('Network Bandwidth')
    ax1.set_ylabel('Bandwidth (bytes/sec)')
    ax2.plot(x_traffic, y_traffic)
    ax2.set_title('Network Traffic')
    ax2.set_xlabel('Time (seconds)')
    ax2.set_ylabel('Bytes Transferred')

    # create a FigureCanvasTkAgg object with the plot figure
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()

    # embed the canvas into a Frame in the root window
    plot_frame = tk.Frame(root)
    plot_frame.pack(side=tk.BOTTOM)
    plot_frame.grid_rowconfigure(0, weight=1)
    plot_frame.grid_columnconfigure(0, weight=1)
    canvas.get_tk_widget().grid(row=0, column=0, sticky=tk.NSEW)

def run_speedtest():
    print("Running Speed Test...")
    st = speedtest.Speedtest()
    download_speeds = []
    upload_speeds = []
    timestamps = []
    for i in range(3):  # run the speedtest 3 times
        print("Test", i+1)
        download_speed = st.download() / 1000000  # Convert to Mbps
        upload_speed = st.upload() / 1000000  # Convert to Mbps
        print("Download Speed:", download_speed, "Mbps")
        print("Upload Speed:", upload_speed, "Mbps")
        download_speeds.append(download_speed)
        upload_speeds.append(upload_speed)
        timestamps.append(i+1)
        time.sleep(1)  # wait for 1 second before running the next test

    # plot the graph
    plt.clf()
    fig, ax = plt.subplots()
    ax.plot(timestamps, download_speeds, label='Download Speed')
    ax.plot(timestamps, upload_speeds, label='Upload Speed')
    ax.set_title('Speed Test Results')
    ax.set_xlabel('Test Number')
    ax.set_ylabel('Speed (Mbps)')
    ax.legend()

    # create a FigureCanvasTkAgg object with the plot figure
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()

    # embed the canvas into a Frame in the root window
    plot_frame = tk.Frame(root)
    plot_frame.pack(side=tk.BOTTOM)
    canvas.get_tk_widget().pack(side=tk.BOTTOM)

def main():
    def network_analysis():
        print("Starting Network Bandwidth Monitor...")
        x_bandwidth = [time.time()]
        y_bandwidth = [get_bytes()]
        x_traffic = [time.time()]
        y_traffic = [get_bytes()]
        record_bandwidth_traffic(x_bandwidth, y_bandwidth, x_traffic, y_traffic, duration=10)
        plot_fig = plt.Figure(figsize=(6, 6), dpi=100)
        plot_axis = plot_fig.add_subplot(211)
        plot_axis.plot(x_bandwidth, y_bandwidth)
        plot_axis.set_title('Network Bandwidth')
        plot_axis.set_ylabel('Bandwidth (bytes/sec)')
        plot_axis2 = plot_fig.add_subplot(212)
        plot_axis2.plot(x_traffic, y_traffic)
        plot_axis2.set_title('Network Traffic')
        plot_axis2.set_xlabel('Time (seconds)')
        plot_axis2.set_ylabel('Bytes Transferred')
        canvas = FigureCanvasTkAgg(plot_fig, master=root)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)



    # create the buttons in the root window
    button_test = tk.Button(root, text="Speed Test", command=run_speedtest)
    button_test.pack()

    button_net = tk.Button(root, text="Network Analysis", command=network_analysis)
    button_net.pack()
    
    root.mainloop()
    
if __name__ == '__main__':
    try:
        root = tk.Tk()
        main()
    except:
        print("CLOSE")
