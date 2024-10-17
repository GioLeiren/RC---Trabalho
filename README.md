# Adaptive Streaming Video Algorithm (BBA0) using PyDash

## Overview
This project is based on [PyDash](https://github.com/mfcaetano/pydash), a Python framework that simulates Dynamic Adaptive Streaming over HTTP (MPEG-DASH). The framework implements adaptive bitrate (ABR) algorithms, allowing clients to dynamically adjust video quality based on network conditions and buffer size. This repository extends the original PyDash project by implementing a new ABR algorithm, **BBA0 (Buffer-Based Adaptation version 0)**, which is designed to adjust video quality based on the size of the playback buffer.

## What is MPEG-DASH?
MPEG-DASH (Dynamic Adaptive Streaming over HTTP) is a streaming protocol that breaks video content into small segments. Each segment is encoded at multiple bitrates to accommodate different network conditions. The goal of an ABR algorithm in MPEG-DASH is to choose the highest possible bitrate that the network can handle without causing interruptions or buffering during playback​(Especificacao_pydash__2…).

## Original Project: PyDash
[PyDash](https://github.com/mfcaetano/pydash) is a functional client-side simulation platform for evaluating different ABR algorithms. The project allows users to implement new ABR algorithms in a modular way through an abstract class interface called `IR2A` (Interface of Rate Adaptation Algorithms)​(Especificacao_pydash__2…).

The basic components of the PyDash architecture include:

* **Player:** Manages the video buffer and playback, making decisions about which video segment to fetch next.
* **IR2A:** Abstract class for implementing new ABR algorithms.
* **ConnectionHandler:** Manages HTTP connections and controls network conditions (traffic shaping).
  
The main tasks of the client include fetching the MPD file (Media Presentation Description), which contains information about the available video qualities and segments, and then making decisions about which segment to download based on the current network conditions and buffer status.

For more details on the original project, visit the [PyDash repository](https://github.com/mfcaetano/pydash).

## BBA0 Algorithm
### Algorithm Overview
I implemented a new ABR algorithm called **BBA0** (Buffer-Based Adaptation version 0) by extending the `IR2A` interface. BBA0 adjusts video quality based on the size of the playback buffer, divided into two regions:
* **Reservoir:** The minimum buffer size (10% of the maximum) that should be filled before the algorithm increases the video quality.
* **Upper region:** The buffer above 90% capacity, where the highest quality is chosen.
The algorithm aims to minimize buffering while maximizing video quality when the buffer is sufficiently filled.

### Key Code Features
The main class for the BBA0 implementation is `R2A_BBA0`, which inherits from `IR2A`. Below are the key methods:
* `rate_function(self, b)`: This function calculates the recommended bitrate based on the buffer size. A linear function is used to transition between the minimum and maximum bitrates as the buffer fills from the reservoir to 90% of the buffer's capacity.
* `handle_segment_size_request(self, msg)`: This method decides which quality to request based on the buffer's state. It ensures that the lowest quality is chosen when the buffer is below the reservoir, and the highest quality is selected when the buffer is over 90%. In other cases, it uses the rate function to calculate the appropriate quality.

### How It Works
1. **Initialization:** The buffer's reservoir is set to 10% of the maximum buffer size.
2. **Rate Calculation:** As the buffer size grows beyond the reservoir, the requested quality gradually increases based on the linear rate function.
3. **Buffer Monitoring:** The algorithm constantly monitors the buffer size. When the buffer is below 10%, the minimum quality is requested to prevent buffering. If the buffer is above 90%, the highest quality is requested.

## Testing and Results
The BBA0 algorithm was tested using the **Big Buck Bunny** video, which is segmented into various qualities ranging from 46,980bps to 4,726,737bps​(Especificacao_pydash__2…). The algorithm successfully adapts to changes in buffer size, ensuring high-quality playback with minimal interruptions.

## How to Run
1. Clone the repository:
```
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
cd YOUR_REPOSITORY
```
2. Ensure all dependencies are installed (you can refer to the original PyDash repository for specific dependencies).

3. To run the simulation, use the following command:
```
python pydash.py --config dash_client.json
```
4. Modify the `dash_client.json` file to set the URL for the MPD file and configure any other parameters such as the buffer size or traffic shaping profile.

## Future Work
* Further tuning of the BBA0 algorithm to handle more complex network conditions.
* Adding support for additional metrics like smoothness and fairness in quality adaptation.
* Integrating more advanced traffic shaping profiles for dynamic bandwidth management.

## Resources
* PyDash GitHub Repository
* MPEG-DASH Overview​(Especificacao_pydash__2…).
