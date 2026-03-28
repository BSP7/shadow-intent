# Shadow Intent: IoT Device Behavior Analysis

Shadow Intent is a real-time monitoring and analysis system designed to detect suspicious activities and malicious "intents" in IoT (Internet of Things) devices. The system sniffs network traffic, extracts behavioral features, calculates intent scores using machine learning techniques, and provides an interactive dashboard to view device risks and alerts.

## Current Progress & Status

* **Backend API**: Implemented FastAPI backend with MongoDB integration. Added endpoints for metrics, history, and actions.
* **Traffic Monitoring**: Scapy-based network sniffer is operational for capturing network traffic. Improved Device Identification with OUI Vendor checks.
* **Analysis & ML**: Implemented persistent behavior learning and an **Isolation Forest ML Model** (`scikit-learn`) for dynamic anomaly detection.
* **Explainable AI (XAI)**: Upgraded Alert Engine to provide descriptive reasoning and confidence scores for malicious activity.
* **Simulated Defense**: Added a mock response engine to log "Block/Drop" mitigations against hostile actors automatically.
* **Frontend UI**: React-based interactive dashboard is built and visualizing threat data in real-time.
* **Evaluation Metrics**: Added real-time tracking for True Positives, Recall, and Accuracy during attack simulations.

## Project Structure

The project is split into two main components:

- **Backend (Python)**: Handles network packet sniffing, feature extraction, intent scoring, and serves the data via a REST API.
- **Frontend (React)**: An interactive Web Dashboard to visualize connected devices, view risk scores over time, and display alerts for anomalous behaviors.

### Directory Layout

```text
📦 shadow-intent
 ┣ 📜 docker-compose.yml        # Docker composition for easy deployment
 ┣ 📜 monitor.py                # Simple root fallback monitor script
 ┣ 📜 simulate.py               # Traffic simulation script
 ┣ 📂 backend                   # Python FastAPI Backend
 ┃ ┣ 📜 app.py                  # Main FastAPI application
 ┃ ┣ 📜 real_sniffer.py         # Scapy network traffic sniffer
 ┃ ┣ 📜 feature_extractor.py    # Traffic feature extraction (Scapy/Pandas)
 ┃ ┣ 📜 intent_engine.py        # ML heuristics and intent calculations
 ┃ ┣ 📜 baseline_model.py       # Baseline behavior model
 ┃ ┣ 📜 models.py               # Data models/schemas (Pydantic)
 ┃ ┣ 📜 database.py             # MongoDB integration logic
 ┃ ┣ 📜 alert_engine.py         # Alerting and threat notification rules
 ┃ ┣ 📜 attack_simulator.py     # Simulates malicious network attacks
 ┃ ┣ 📜 device_identifier.py    # Identifies IoT devices
 ┃ ┣ 📜 cli_monitor.py          # CLI tool for monitoring the system
 ┃ ┣ 📜 response_engine.py      # Automated response simulator
 ┃ ┣ 📜 evaluation.py           # ML Model evaluation metrics
 ┃ ┣ 📜 Dockerfile              # Backend container configuration
 ┃ ┗ 📜 requirements.txt        # Python dependencies
 ┗ 📂 frontend                  # React Dashboard Frontend
   ┣ 📂 src                     # React source files
   ┣ 📂 public                  # Static assets
   ┗ 📜 package.json            # Node dependencies and scripts
```

## Getting Started

### Prerequisites

- [Python 3.8+](https://www.python.org/downloads/)
- [Node.js](https://nodejs.org/) (minimum v16+ recommended)
- [npcap](https://npcap.com/) (Windows) or libpcap (Linux/macOS) for Scapy to capture packets

### 1. Setting up the Backend

Navigate to the `backend/` directory, create a virtual environment, and install the dependencies:

```bash
cd backend
python -m venv .venv

# On Windows:
.venv\Scripts\activate
# On Linux / macOS:
source .venv/bin/activate

pip install -r requirements.txt
```

#### Run the Backend Server
Start the FastAPI server:
```bash
python app.py
```
*Note: The API runs on `http://localhost:8000`. You can visit `http://localhost:8000/docs` to see the interactive Swagger UI.*

#### Run the Network Sniffer
In a separate terminal (with the virtual environment activated), run the network sniffer. This tool requires administrator/root privileges to capture raw network traffic:
```bash
# Must be executed with Admin/Root permissions
python real_sniffer.py
```

### 1.1 Running with Docker

Alternatively, you can run the application using Docker Compose:

```bash
docker-compose up --build
```
This will automatically build and start the backend, frontend, and any required databases.

### 2. Setting up the Frontend

Navigate to the `frontend/` directory and install the Node modules:

```bash
cd frontend
npm install
```

#### Run the Dashboard
Start the React development server:
```bash
npm start
```
*The web dashboard should automatically open in your default browser at `http://localhost:3000`.*

---

## How it Works / Usage

Once the backend, frontend, and sniffer are running, the system passively monitors your network.

1. **Traffic Capture**: `real_sniffer.py` captures raw packets and sends them to the analysis engine.
2. **Analysis**: `feature_extractor.py` and `intent_engine.py` evaluate the traffic against the `baseline_model.py` to calculate risk/intent scores.
3. **Dashboard Monitoring**: Open the React Dashboard (`http://localhost:3000`) to view connected devices and their corresponding intent scores.
4. **Threat Simulation**: You can use `backend/attack_simulator.py` or the root `simulate.py` to generate synthetic malicious traffic on your network and observe how the system detects and flags it.
5. **CLI Monitoring**: For a terminal-based view of the system's status and alerts, run `backend/cli_monitor.py`.

---

## Features

* **Real-Time Traffic Sniffing:** Passively monitors packets going in and out of the network in real-time.
* **Behavioral Analysis:** Calculates "intent scores" based on packet sizes, frequencies, unusual ports, and protocols.
* **Risk Categorization:** Classifies IoT devices as "Safe," "Monitor," "Suspicious," or "High Risk."
* **Advanced Alerts:** Automatically flags devices crossing critical thresholds.
* **Live Dashboard:** Clean and intuitive UI to oversee everything at a glance.

## License

This project is licensed under the MIT License.
