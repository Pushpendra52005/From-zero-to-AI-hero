import os
import json
from groq import Groq
from dotenv import load_dotenv

# ✅ Load API Key
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("❌ Error: GROQ_API_KEY is missing. Check your .env file!")

client = Groq(api_key=GROQ_API_KEY)

# ✅ Correct model name
MODEL_NAME = "llama-3.3-70b-versatile"

# ✅ Output folder
OUTPUT_FOLDER = "generated_scripts"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)  # Ensure folder exists

def generate_custom_script(title, duration=30):
    print(f"🚀 Generating {duration}-minute movie script for: {title}")

    script = ""
    chunk_count = duration // 5  # ✅ Break script into 5-minute chunks

    for i in range(chunk_count):
        print(f"🔹 Generating Part {i+1}/{chunk_count}...")

        prompt = (
            f"You are an expert screenwriter. Write a {duration}-minute screenplay titled '{title}'.\n\n"
            "Follow this screenplay format with realistic dialogues and emotional depth:\n\n"
            "FADE IN:\n\n"
            "INT. PUSHPENDRA'S ROOM - EARLY MORNING\n\n"
            "*The alarm clock BUZZES. A hand slams it off. PUSHPA (Pushpendra) groggily sits up, rubs his eyes, and grabs his LAPTOP.*\n\n"
            "PUSHPENDRA\n"
            "(murmuring, determined)\n"
            "Yeh coding jitni tough dikhti hai, asal mein utni hoti nahi hai... ek time tha jab mujhe bilkul bhi nahi aati thi.\n\n"
            "*Screen light reflects on his face as he types. Flashback begins.*\n\n"
            "FADE TO:\n\n"
            "INT. MEDICAL SHOP - NIGHT (FLASHBACK - 2022)\n\n"
            "*Shelves filled with medicines. Pushpendra, in a white apron, hands a medicine packet to a customer. His eyes are tired, his hands move robotically.*\n\n"
            "CUSTOMER\n"
            "(empathetic)\n"
            "Beta, tum hamesha yahan rehte ho. Kabhi aaram bhi karte ho?\n\n"
            "PUSHPENDRA\n"
            "(forced smile)\n"
            "Jee uncle, bas duty ka hissa hai.\n\n"
            "*Clock strikes 11 PM. He exhales deeply, looking at the closed shutter, lost in thought.*\n\n"
            "PUSHPENDRA (V.O.)\n"
            "Yeh 8 AM to 11 PM ka routine... yeh life nahi hai.\n\n"
            "*He types his resignation letter on his phone. SEND.*\n\n"
            "FADE TO:\n\n"
            "[CONTINUE SCREENPLAY WITH REMAINING SCENES]"
        )

        try:
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[{"role": "system", "content": prompt}]
            )
        except Exception as e:
            print("❌ API Request Error:", e)
            return None

        if not response or not hasattr(response, "choices") or not response.choices:
            print("❌ API did not return a valid response. Exiting...")
            return None

        content = response.choices[0].message.content.strip()
        
        if not content:
            print("❌ API response is empty. Skipping part...")
            continue

        script += f"\n\n# Part {i+1}\n{content}"  # ✅ Append script parts

    if not script.strip():
        print("❌ No script generated. Exiting...")
        return None

    # ✅ Generate file path
    filename = os.path.join(OUTPUT_FOLDER, f"{title.replace(' ', '_')}.txt")

    # ✅ File me script save karein
    with open(filename, "w", encoding="utf-8") as f:
        f.write(script)

    print(f"📂 Script saved successfully at: {filename}")
    return script

# ✅ Test Run
generate_custom_script("From Zero to AI Hero", duration=30)
