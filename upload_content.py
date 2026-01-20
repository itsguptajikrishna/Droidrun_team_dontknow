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

def run_phase_4_post_to_x_simple():
    """Commands DroidRun to post to X using the most recently downloaded images."""
    print("\n--- PHASE 4: POSTING TO X (RECENT MEDIA) ---")

    # 1. Load the body content and links
    if not os.path.exists("topic_content.txt") or not os.path.exists("topic_links.txt"):
        print("[!] Missing content files. Run Phase 3 first.")
        return

    with open("topic_content.txt", "r") as f:
        body_text = f.read().strip()
    
    with open("topic_links.txt", "r") as f:
        links = f.read().strip()

    full_post_content = f"{body_text}\n\nSources & More Info:\n{links}"

    # 2. Define the UI Task
    # We instruct the agent to look for the 'Recent' tab which is standard in mobile pickers
    post_prompt = f"""
    1. Open the X (Twitter) app on the mobile device.
    2. Tap the 'Compose' (+) button.
    3. Tap the 'Gallery' or 'Image' icon to attach media.
    4. Select the most recent images appearing at the top of the 'Recent' or 'Downloads' tab.
    5. Enter the following text into the post body and also limit the content to 250 characters  (250 character strictly needs to be followed for X.com so take care of it )
    ---
    {full_post_content}
    ---
    6. Click 'Post' on the top right corner to publish.
    """

    payload = {
        "task": post_prompt,
        "llmModel": "google/gemini-2.5-flash",
        "deviceId": DEVICE_ID,
        "vision": True 
    }

    # 3. Execution & Polling
    print("[*] Triggering X post task...")
    response = requests.post(
        f"{BASE_URL}/tasks/",
        headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
        json=payload
    ).json()

    task_id = response.get("id")

    while True:
        status_check = requests.get(
            f"{BASE_URL}/tasks/{task_id}/status", 
            headers={"Authorization": f"Bearer {API_KEY}"}
        ).json()
        status = status_check.get("status")
        print(f"    [Status]: {status}")
        
        if status in ["completed", "failed"]:
            break
        time.sleep(12)

    if status == "completed":
        print("\n[✔] Post successfully published to X.")
    else:
        print("\n[✘] Post failed. Please check the mobile device state.")
        
        
run_phase_4_post_to_x_simple()
