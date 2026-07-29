import streamlit as st
import google.generativeai as genai
import subprocess
import time

# --- 1. Secrets ලබා ගැනීම ---
# (දැනට Supabase අයින් කර ඇති නිසා GEMINI_KEY පමණක් ප්‍රමාණවත්)
GEMINI_KEY = st.secrets["GEMINI_KEY"]
genai.configure(api_key=GEMINI_KEY)

# --- 2. Streamlit අතුරුමුහුණත (UI) ---
st.set_page_config(page_title="AI Video Generator", page_icon="🎬", layout="centered")

st.title("🎥 Unlimited AI Video Generator")
st.write("වීඩියෝ එකක් සෑදීමට අවශ්‍ය විස්තර පහතින් ඇතුළත් කරන්න.")

user_prompt = st.text_area("ඔබට අවශ්‍ය වීඩියෝව කුමක්ද?", placeholder="උදා: බල්ලෙක් ගෙ සහ පූසෙක්ගේ ආදර කතාවක්...")

if st.button("වීඩියෝව නිර්මාණය කරන්න 🚀"):
    if user_prompt:
        with st.spinner("වීඩියෝව නිර්මාණය වෙමින් පවතී. කරුණාකර රැඳී සිටින්න..."):
            
            # Gemini හරහා Prompt එක Enhance කිරීම
            try:
                model = genai.GenerativeModel('gemini-pro')
                response = model.generate_content(f"Translate this prompt to English and make it highly detailed and cinematic for an AI video generator: {user_prompt}")
                enhanced_prompt = response.text
                st.info(f"**Enhanced Prompt (AI):** {enhanced_prompt}")
            except Exception as e:
                enhanced_prompt = user_prompt
                st.warning("Prompt enhancement අසාර්ථක විය.")

            # --- 3. ඔබේ ප්‍රධාන කේතය (Brain) Terminal එක හරහා ක්‍රියාත්මක කිරීම ---
            try:
                # මෙතන 'command_to_run' කියන එකට ඔබේ නියම කේතය run කරන විධානය දෙන්න ඕනේ.
                # මම දැනට උදාහරණයක් විදිහට 'python api.py' කියලා දීලා තියෙනවා.
                command_to_run = ["python", "api.py", enhanced_prompt]
                
                # Terminal command එක run කිරීම (මෙය ඔබේ brain එකට කිසිම හානියක් කරන්නේ නෑ)
                # result = subprocess.run(command_to_run, capture_output=True, text=True)
                
                # තාවකාලිකව තත්පර 3ක් රැඳී සිටීම (ඔබ නියම කේතය සෙට් කරනකම් පමණි)
                time.sleep(3)
                
                # --- ඔබේ නියම වීඩියෝ URL එක මෙතැනට ගත යුතුය ---
                # දැනට පරීක්ෂා කිරීමට පමණක් තාවකාලික ලින්ක් එකක් දී ඇත.
                video_url = "https://www.w3schools.com/html/mov_bbb.mp4"

                st.success("වීඩියෝව සාර්ථකව නිර්මාණය විය!")
                st.video(video_url)

            except Exception as e:
                st.error(f"වීඩියෝව සෑදීමේදී දෝෂයක් මතු විය: {e}")
    else:
        st.warning("කරුණාකර වීඩියෝව සඳහා විස්තරයක් (Prompt) ඇතුළත් කරන්න.")
