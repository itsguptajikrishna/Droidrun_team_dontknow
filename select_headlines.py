import requests
import time
import json
import os

# API Configuration
API_KEY = "dr_sk_fHOWhYeMjjpBSEGugyJBrGXuyswkbriuIVRSUtpybnqqWdLqqKIeSZEsZLWahbZM"
DEVICE_ID = "565198f9-a030-4331-b8fa-c5678ab6b3f6"
BASE_URL = "https://api.mobilerun.ai/v1"
STORAGE_FILE = "trending_headings.json"
GEMINI_API_KEY="AIzaSyAPTABHUvY__NaURkAQsb4bNY5MKa_hl1I"

def run_heading_task(source_name, url):
    """Commands DroidRun to grab only headlines from a specific URL."""
    print(f"\n[*] Accessing {source_name}...")
   
    # Ultra-simple prompt to keep the LLM processing fast and light
    prompt = f"Go to {url}. Scroll once. Extract only the top 5 trending news headlines as a list of strings. Do not include summaries or links."
   
    payload = {
        "task": prompt,
        "llmModel": "google/gemini-2.5-flash",
        "deviceId": DEVICE_ID,
        "outputSchema": {
            "type": "object",
            "properties": {
                "headlines": {"type": "array", "items": {"type": "string"}}
            }
        }
    }
   
    response = requests.post(
        f"{BASE_URL}/tasks/",
        headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
        json=payload
    ).json()
   
    task_id = response.get("id")
   
    # Polling Loop
    while True:
        status_data = requests.get(f"{BASE_URL}/tasks/{task_id}/status",
                                   headers={"Authorization": f"Bearer {API_KEY}"}).json()
        status = status_data.get("status")
        print(f"    [{source_name}] Status: {status}")
       
        if status in ["completed", "failed"]:
            break
        time.sleep(8) # Reduced frequency to save bandwidth
       
    result = requests.get(f"{BASE_URL}/tasks/{task_id}",
                          headers={"Authorization": f"Bearer {API_KEY}"}).json()
    return result["task"]["output"].get("headlines", [])

def save_headlines(source, headings):
    """Saves headings to local file immediately."""
    data = {}
    if os.path.exists(STORAGE_FILE):
        with open(STORAGE_FILE, "r") as f:
            data = json.load(f)
   
    data[source] = headings
    with open(STORAGE_FILE, "w") as f:
        json.dump(data, f, indent=4)
    print(f"[✔] {source} data cached locally.")

# --- EXECUTION FLOW ---

# Define individual sources to prevent bulk-loading the API
sources = {
    "The Hindu": "https://www.thehindu.com/latest-news/",
    "BBC_World": "https://www.bbc.com/news",
    "Reuters_Top": "https://www.reuters.com/"
}

print("--- PHASE 1: SEQUENTIAL HEADLINE COLLECTION ---")
for name, url in sources.items():
    try:
        headlines = run_heading_task(name, url)
        save_headlines(name, headlines)
    except Exception as e:
        print(f"[!] Failed to scrape {name}: {e}")

# --- PHASE 2: TERMINAL DISPLAY ---
print("\n" + "="*40)
print("   LOCAL TRENDING ANALYSIS (TERMINAL)")
print("="*40)


def run_phase_2_analysis():
    """Reads the stored headings and asks Gemini to pick the single most important topic."""
    print("\n--- PHASE 2: AI TREND ANALYSIS ---")
    
    # 1. Load the data from your local storage file
    if not os.path.exists(STORAGE_FILE):
        print("[!] No storage file found. Please run Phase 1 first.")
        return

    with open(STORAGE_FILE, "r") as f:
        all_headlines = json.load(f)

    # 2. Prepare the text for Gemini
    # We combine all sources into one string to find cross-source repetition
    combined_text = ""
    for source, titles in all_headlines.items():
        combined_text += f"\nSource {source}: " + " | ".join(titles)

    # 3. Create the prompt for the single most relevant topic
    analysis_prompt = f"""
    Analyze these headlines from different news sources:
    {combined_text}
    
    Identify the single most important or frequently occurring news topic.
    Return ONLY the headline of this topic as a single string. 
    No explanations, no intro.
    """

    # 4. Use DroidRun to get the Gemini response
    # We use a simple schema to ensure we get a single string back
    payload = {
        "task": analysis_prompt,
        "llmModel": "google/gemini-2.5-flash",
        "deviceId": DEVICE_ID,
        "outputSchema": {
            "type": "object",
            "properties": {
                "top_headline": {"type": "string"}
            }
        }
    }

    print("[*] Sending headlines to Gemini for trend identification...")
    response = requests.post(
        f"{BASE_URL}/tasks/",
        headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
        json=payload
    ).json()

    # Poll for the result
    task_id = response.get("id")
    while True:
        status_data = requests.get(f"{BASE_URL}/tasks/{task_id}/status", 
                                   headers={"Authorization": f"Bearer {API_KEY}"}).json()
        if status_data.get("status") in ["completed", "failed"]:
            break
        time.sleep(5)

    result_task = requests.get(f"{BASE_URL}/tasks/{task_id}", 
                               headers={"Authorization": f"Bearer {API_KEY}"}).json()
    
    final_topic = result_task["task"]["output"].get("top_headline", "No topic identified")

    # 5. Store the final single topic in a new file
    with open("selected_topic.txt", "w") as f:
        f.write(final_topic)

    print(f"\n[✔] Analysis Complete!")
    print(f"    Selected Topic: {final_topic}")
    print("    Stored in: selected_topic.txt")
    
    
if os.path.exists(STORAGE_FILE):
    run_phase_2_analysis()
    with open(STORAGE_FILE, "r") as f:
        final_data = json.load(f)
   
    for source, titles in final_data.items():
        print(f"\n{source.upper()}:")
        for i, title in enumerate(titles, 1):
            print(f"  {i}. {title}")
else:
    print("No data collected.")
    




