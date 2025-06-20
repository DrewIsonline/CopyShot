import streamlit as st
from openai import OpenAI

# --- SETUP ---
st.set_page_config(page_title="CopyShot - AI Ad Copy Generator", layout="centered")

# --- HEADER ---
st.image("app_icon.png", width=150)
st.markdown("### *AI-Powered Ad Copy by Drew Is*")
st.caption("From Drew Is: Tools to UpLevel the human experience. [v2]")

# --- API KEY HANDLING ---
if "OPENAI_API_KEY" in st.secrets:
    openai_api_key = st.secrets["OPENAI_API_KEY"]
    st.success("🔐 Using secure API key.")
else:
    openai_api_key = st.text_input("Enter your OpenAI API key", type="password")
    if not openai_api_key:
        st.warning("Please enter your API key to use the tool.")
        st.stop()

client = OpenAI(api_key=openai_api_key)

# --- SETTINGS ---
st.subheader("⚙️ Copy Settings")
gpt_model = st.selectbox("Choose GPT model", ["gpt-4", "gpt-3.5-turbo"])
add_emojis = st.checkbox("Add Emojis")
add_hashtags = st.checkbox("Add Hashtags")

# --- SESSION STATE ---
if "history" not in st.session_state:
    st.session_state.history = []

# --- FORM ---
with st.form("ad_form"):
    product_name = st.text_input("Product Name", placeholder="e.g. ShadowPoster 1.0")
    product_description = st.text_area("Product Description", placeholder="Tell us what it does and why it rocks...")
    audience = st.text_input("Target Audience", placeholder="e.g. Small business owners, Coaches, Tech lovers")
    tone = st.selectbox("Tone / Voice", ["Gritty", "Luxury", "Friendly", "Bold", "Spiritual", "Professional"])
    framework = st.selectbox("Copywriting Framework", [
        "AIDA", "PAS", "Hook & CTA", "Story",
        "Before–After–Bridge", "FAB", "4 Ps", "5 Cs", "Problem–Dream–Fix"
    ])
    email = st.text_input("📩 Want updates or to suggest a feature? Drop your email:")
    submitted = st.form_submit_button("🔥 Generate Copy")

# --- COPY GENERATION ---
if submitted:
    with st.spinner("Fueling your funnel... 🔥"):
        prompt = f"""
Write 3 variations of a marketing ad using the {framework} framework.
Product: {product_name}
Description: {product_description}
Audience: {audience}
Tone: {tone}
{"Add emojis." if add_emojis else ""}
{"Include hashtags relevant to the product and audience." if add_hashtags else ""}
Make it engaging and ready for Facebook or Instagram.
"""
        try:
            response = client.chat.completions.create(
                model=gpt_model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=600
            )
            output = response.choices[0].message.content
            st.subheader("📋 Your AI-Generated Ad Copy:")
            st.text_area("Copy Output", output, height=300)
            st.download_button("💾 Save as .txt", output, file_name="ad_copy.txt")
            st.session_state.history.insert(0, output)
            st.session_state.history = st.session_state.history[:3]
        except Exception as e:
            st.error(f"Error: {e}")

# --- COPY HISTORY ---
if st.session_state.history:
    st.markdown("---")
    st.subheader("📜 Your Last 3 Ad Copies")
    for i, entry in enumerate(st.session_state.history):
        st.text_area(f"Previous #{i+1}", entry, height=150)

# --- RESET ---
if st.button("🔄 Reset"):
    st.session_state.history = []
    st.rerun()

# --- FOOTER ---
st.markdown("---")
st.markdown("🔧 Powered by [Drew Is](https://DrewIs.online) – Tools to UpLevel the human experience.")
