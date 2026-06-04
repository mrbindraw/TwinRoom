from fastapi import FastAPI
import random, time, math
from datetime import datetime
 
app = FastAPI()
start_time = time.time()
 
last_state = {"temp": None, "occupied": None}
 
def log_change(key, old_val, new_val):
    ts = datetime.now().strftime("%H:%M:%S")
    if key == "temp":
        print(f"[{ts}] Temperature: {old_val}°C -> {new_val}°C")
    elif key == "occupied":
        status = "Occupied" if new_val else "EMPTY"
        print(f"[{ts}] Room status: {status}")
 
@app.get("/room")
def get_room():
    global last_state
    
    t = time.time() - start_time
    # get random temp
    temp = round(22 + 2 * math.sin(t / 30) + random.uniform(-0.2, 0.2), 1)
    # get random is occupied
    occupied = (int(t / 10) % 2 == 0)
    
    # print room status
    if last_state["temp"] is not None and abs(temp - last_state["temp"]) > 0.2:
        log_change("temp", last_state["temp"], temp)
    
    if last_state["occupied"] is not None and occupied != last_state["occupied"]:
        log_change("occupied", last_state["occupied"], occupied)
    
    last_state["temp"] = temp
    last_state["occupied"] = occupied
    
    return {"temp": temp, "occupied": occupied}
 
if __name__ == "__main__":
    print("\n" + "="*50)
    print("  Mock IoT Server for Digital Twin Room")
    print("="*50)
    print("\nOpen terminal and execute command:")
    print("  uvicorn room_server:app --host 0.0.0.0 --port 8000")
    print("\nOpen in browser:")
    print("  http://localhost:8000/room")
    print("\n" + "="*50 + "\n")