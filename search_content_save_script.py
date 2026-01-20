import os
import json
import requests
import time
from datetime import datetime

# API Configuration
API_KEY = "dr_sk_fHOWhYeMjjpBSEGugyJBrGXuyswkbriuIVRSUtpybnqqWdLqqKIeSZEsZLWahbZM"
DEVICE_ID = "565198f9-a030-4331-b8fa-c5678ab6b3f6"
BASE_URL = "https://api.mobilerun.ai/v1"
STORAGE_FILE = "trending_headings.json"
GEMINI_API_KEY="AIzaSyAPTABHUvY__NaURkAQsb4bNY5MKa_hl1I"


def run_step_with_validation(task_desc, schema=None):
    """Executes a DroidRun task and polls for completion."""
    payload = {
        "task": task_desc,
        "llmModel": "google/gemini-2.5-flash",
        "deviceId": DEVICE_ID,
        "vision": True,
        "outputSchema": schema
    }
    
    response = requests.post(
        f"{BASE_URL}/tasks/",
        headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
        json=payload
    ).json()
    
    task_id = response.get("id")
    print(f"[*] Task Started: {task_id}")

    while True:
        status_data = requests.get(f"{BASE_URL}/tasks/{task_id}/status", 
                                   headers={"Authorization": f"Bearer {API_KEY}"}).json()
        status = status_data.get("status")
        if status in ["completed", "failed"]:
            break
        time.sleep(10)
    
    result = requests.get(f"{BASE_URL}/tasks/{task_id}", headers={"Authorization": f"Bearer {API_KEY}"}).json()
    return result["task"]["output"]

def run_phase_3_download_logic():
    # 1. Setup Naming Convention
    today_str = datetime.now().strftime("%Y-%m-%d")
    
    with open("selected_topic.txt", "r") as f:
        topic = f.read().strip()

    # STEP A: Image Download with Specific Naming
    # Instead of screenshots, we long-press/save or use download buttons
    image_task = f"""
    1. Search Google Images for '{topic}'.
    2. For the first 3 relevant images: 
       - Long-press or use the 'Download image' option.
       - Save them to the mobile storage folder named '{today_str}'.
       - Name the files sequentially: '{today_str}/image_1.jpg', '{today_str}/image_2.jpg', etc.
    """
    print(f"[*] Attempting to download images for: {topic}")
    run_step_with_validation(image_task)

    # STEP B: Link and Content Extraction
    content_task = f"""
    1. Go to the main Google Search results for '{topic}'.
    2. Extract 3 high-quality news links.
    3. Open the top result and extract a 3-paragraph factual summary.
    """
    content_schema = {
        "type": "object",
        "properties": {
            "links": {"type": "array", "items": {"type": "string"}},
            "summary": {"type": "string"}
        }
    }
    
    data = run_step_with_validation(content_task, content_schema)

    # 2. Local File Storage
    if data:
        with open("topic_links.txt", "w") as f:
            f.write("\n".join(data.get("links", [])))
        with open("topic_content.txt", "w") as f:
            f.write(data.get("summary", ""))
        
    print(f"\n[✔] Phase 3 Complete.")
    print(f"    Images saved on mobile as: {today_str}/image_N.jpg")
    print(f"    Links and Content stored in local .txt files.")


run_phase_3_download_logic()
