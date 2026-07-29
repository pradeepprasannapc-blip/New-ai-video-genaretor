import streamlit as st
from supabase import create_client, Client
import psycopg2
import google.generativeai as genai
import time

# --- 1. Secrets ලබා ගැනීම ---
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
GEMINI_KEY = st.secrets["GEMINI_KEY"]
DATABASE_URL = st.secrets["DATABASE_URL"]

# Gemini API සක්‍රීය කිරීම
genai.configure(api_key=GEMINI_KEY)

# Supabase Client එක සෑදීම
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- 2. Supabase Table එක Auto සෑදීම ---
def init_db():
    try:
        # Database URL එක හරහා කෙලින්ම සම්බන්ධ වී Table එක හදයි
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS generated_videos (
                id SERIAL PRIMARY KEY,
                prompt TEXT NOT NULL,
                video_url TEXT,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
            );
        """)
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        st.sidebar.error(f"Database Auto-Setup Error: {e}")

# පිටුව Load වන විටම Table එක හදන්න (තිබේ නම් මුකුත් නොකරයි)
init_db()


# --- 3. Streamlit අතුරුමුහුණත (UI) ---
st.set_page_config(page_title="AI Video Generator", page_icon="🎬", layout="centered")

st.title("🎥 Unlimited AI Video Generator")
st.write("වීඩියෝ එකක් සෑදීමට අවශ්‍ය විස්තර පහතින් ඇතුළත් කරන්න.")

# User ගෙන් Prompt එක ලබා ගැනීම
user_prompt = st.text_area("ඔබට අවශ්‍ය වීඩියෝව කුමක්ද?", placeholder="උදා: A futuristic city with flying cars in cyberpunk style...")

if st.button("වීඩියෝව නිර්මාණය කරන්න 🚀"):
    if user_prompt:
        with st.spinner("වීඩියෝව නිර්මාණය වෙමින් පවතී. කරුණාකර රැඳී සිටින්න..."):
            
            # (අමතර) Gemini හරහා Prompt එක තවත් ලස්සන කිරීම (Enhance prompt)
            try:
                model = genai.GenerativeModel('gemini-pro')
                response = model.generate_content(f"Make this prompt highly detailed and cinematic for an AI video generator: {user_prompt}")
                enhanced_prompt = response.text
                st.info(f"**Enhanced Prompt:** {enhanced_prompt}")
            except:
                enhanced_prompt = user_prompt

            # --- මෙතනින් ඔබේ api.py එකේ කේතය Run වේ ---
            try:
                # ඔබගේ repo එකේ ඇති api.py හි generate function එකක් ඇතැයි උපකල්පනය කර ඇත.
                # import api
                # video_url = api.generate_video(enhanced_prompt)
                
                time.sleep(3) # වීඩියෝව හැදෙන තුරු (simulation)
                
                # තාවකාලික Dummy URL එකක් (ඔබේ api.py එකෙන් එන URL එක මෙතැනට වැටිය යුතුය)
                video_url = "https://www.w3schools.com/html/mov_bbb.mp4" 

                st.success("වීඩියෝව සාර්ථකව නිර්මාණය විය!")
                st.video(video_url)

                # --- 4. සාදන ලද වීඩියෝව Supabase එකට Auto Save කිරීම ---
                try:
                    data = {"prompt": user_prompt, "video_url": video_url}
                    supabase.table("generated_videos").insert(data).execute()
                    st.toast("✅ වීඩියෝ විස්තර Supabase හි සුරක්ෂිතව ගබඩා විය!")
                except Exception as db_err:
                    st.warning(f"දත්ත ගබඩා කිරීමේ දෝෂයකි: {db_err}")

            except Exception as e:
                st.error(f"වීඩියෝව සෑදීමේදී දෝෂයක් මතු විය: {e}")
    else:
        st.warning("කරුණාකර වීඩියෝව සඳහා විස්තරයක් (Prompt) ඇතුළත් කරන්න.")

# Supabase හි දැනටමත් Save වී ඇති වීඩියෝ බැලීමට
with st.expander("📂 මින් පෙර සෑදූ වීඩියෝ බලන්න"):
    try:
        past_videos = supabase.table("generated_videos").select("*").order("created_at", desc=True).limit(5).execute()
        for vid in past_videos.data:
            st.write(f"**Prompt:** {vid['prompt']}")
            st.video(vid['video_url'])
            st.divider()
    except:
        st.write("තවමත් වීඩියෝ කිසිවක් ගබඩා කර නොමැත.")
