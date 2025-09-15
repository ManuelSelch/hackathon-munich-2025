# Hackathon Munich 2025
- `UI`: small webserver to trigger different modes
- `Record`: record raw data using Meta Quest VR
- `Train`: using recorded data to train policy
- `Deploy`: Workflow contains multiple steps 
    -> each step has its own policy 
    -> save policy checkpoint for each step
    -> decide based on state which policy to use next

---

- Error Handling: Retry current step