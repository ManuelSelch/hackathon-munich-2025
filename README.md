# Hackathon Munich 2025

### Architecture
- `UI`: small webserver to trigger different modes -- **todo**
- `Record`: record raw data using Meta Quest VR
- `Robot`
    - `convert()`: migrate ros dataset to LeRobot dataset
    - `replay()`: replay episode 
    - `train()`: using recorded data to train policy
    - `deploy()`: deploy policy to execute a task
- `Workflow` -- **todo**
    - execute sequence of steps
    - detect if a step failed (e.g. by gripper state) -> retry
    - for simplicity transition to next step after a given duration

---

### Workflow
```mermaid
flowchart TD;

pickEcuHolder --> D1{"gripper fully closed?"}
    D1 -- Yes --> placeEcuHolder
    D1 -- No --> pickEcuHolder

placeEcuHolder 
    --> pickEcu
    --> placeEcu 
    --> pickNutA 
    --> placeNutA 
    --> pickNutB 
    --> placeNutB 
    --> done
```

