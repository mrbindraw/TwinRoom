# TwinRoom
This is a simple project to start my journey into UE Digital Twin.  
The mock server sends random data about the room's status: temperature and occupancy.  
On the project map, the cube changes color and displays the room's status as text above it.  

## Dependencies:
- [VaRest UE plugin from fab.com](https://www.fab.com/listings/5b751595-fe3e-4e85-b217-9b5496ab6d3f)
- Python 3+
- [Mosquitto, MQTT-broker](https://mosquitto.org/)

## How to launch:
1. Open a terminal and run the command:
```
pip install fastapi uvicorn
```

2. Switch to the `TwinRoom/MockServer` directory and run:
```
uvicorn room_server:app --host 0.0.0.0 --port 8000
```

Open `http://localhost:8000/room` in your browser to verify it works.

3. Launch the UE project

## Testing MQTT-broker:
1. Switch to the `TwinRoom/MockServer` directory and run in terminal:
```
sh make_certs.sh
```
Remark: If MinGW, POSIX-to-Windows path conversion, add `MSYS_NO_PATHCONV=1` sh make_certs.sh

2. Open new terminal and run:
```
mosquitto -c mosquitto.conf -v
```

3. Open new terminal and run:
```
python room_publisher.py
```

4. Open new terminal and run:
```
python room_subscriber.py
```

## Future Plans
I plan to update and add new features to the project.