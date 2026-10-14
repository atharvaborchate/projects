import streamlit as st
from google import genai
from dotenv import load_dotenv
from PIL import Image
import urllib.parse

load_dotenv()

st.set_page_config(page_title="AI Travel Planner Pro", page_icon="✈️", layout="centered")

client = genai.Client()

# Header Styling
st.markdown(
    """
    <style>
    .travel-hero {
        background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%);
        padding: 2rem;
        border-radius: 16px;
        color: white;
        text-align: center;
        margin-bottom: 1.5rem;
    }
    .travel-title {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(to right, #ffffff, #a8ff78);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    </style>
    <div class="travel-hero">
        <div style="font-size: 3rem;">✈️ 🌍 🧳</div>
        <h1 class="travel-title">Gen-Z AI Travel Companion</h1>
        <p style="color: #d0d7de; margin-top: 8px;">Smart itineraries, interactive maps, and budget estimation</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# User Inputs
location = st.text_input("Destination", placeholder="e.g.,Goa,France,Tokyo,Mexico")

col1, col2 = st.columns(2)
with col1:
    days_nr = st.slider("Duration (Days)", min_value=1, max_value=15, value=3)
with col2:
    budget = st.selectbox("Budget Style", ["Budget-Friendly", "Moderate / Comfort", "Luxury"])

travel_type = st.radio("Traveling With", ["Solo", "Couple", "Friends", "Family"], horizontal=True)

uploaded_file = st.file_uploader(
    "Upload a ticket, itinerary screenshot, or destination photo (Optional)", 
    type=["png", "jpg", "jpeg","pdf"]
)

preview_image = None
if uploaded_file:
    preview_image = Image.open(uploaded_file)
    st.image(preview_image, caption="Uploaded Reference", use_container_width=True)

# Generate Itinerary
if st.button("Generate Smart Itinerary", type="primary"):
    if not location.strip():
        st.warning("Please enter a destination first.")
    else:
        # 1. Budget Breakdown Calculator
        st.subheader("💰 Estimated Budget Breakdown")
        
        # Base daily rates per person based on style
        daily_rates = {
            "Budget-Friendly": {"Stay": 1200, "Food": 800, "Transit & Activities": 600},
            "Moderate / Comfort": {"Stay": 3500, "Food": 2000, "Transit & Activities": 1500},
            "Luxury": {"Stay": 9000, "Food": 4500, "Transit & Activities": 4000},
        }
        
        rates = daily_rates[budget]
        stay_cost = rates["Stay"] * days_nr
        food_cost = rates["Food"] * days_nr
        transit_cost = rates["Transit & Activities"] * days_nr
        total_estimate = stay_cost + food_cost + transit_cost

        col_b1, col_b2, col_b3, col_b4 = st.columns(4)
        col_b1.metric("Stay / Hotel", f"₹{stay_cost:,}")
        col_b2.metric("Food & Drinks", f"₹{food_cost:,}")
        col_b3.metric("Activities & Transit", f"₹{transit_cost:,}")
        col_b4.metric("Est. Total / Person", f"₹{total_estimate:,}")

        st.markdown("---")

        # 2. Google Maps Direct Explorer
        st.subheader(f"📍 Explore {location} on Google Maps")
        encoded_location = urllib.parse.quote(location)
        col_m1, col_m2, col_m3 = st.columns(3)
        col_m1.link_button("🗺️ Open City Map", f"https://www.google.com/maps/search/?api=1&query={encoded_location}")
        col_m2.link_button("🏨 View Hotels", f"https://www.google.com/maps/search/?api=1&query=hotels+in+{encoded_location}")
        col_m3.link_button("🍽️ View Top Food", f"https://www.google.com/maps/search/?api=1&query=best+restaurants+in+{encoded_location}")

        st.markdown("---")

        # 3. AI Itinerary Generation
        st.subheader(f"🗺️ Day-by-Day Itinerary for {location}")

        system_prompt = f"""
        You are an elite travel concierge. 
        Create a detailed, exciting, and realistic itinerary for a trip to {location}.
        Details:
        - Duration: {days_nr} days
        - Budget Style: {budget}
        - Travel Group: {travel_type}

        Format Requirements:
        - Day-by-day morning, afternoon, and evening plan.
        - Must-try local cuisines and recommended places.
        - Important insider advice, dress codes, and local tips.
        Keep answers clean and formatted in Markdown with bullet points.
        """

        contents = [system_prompt]
        if preview_image:
            contents.append(preview_image)
            contents.append("Analyze this uploaded image and incorporate relevant details directly into the trip plan.")

        def generate_stream():
            try:
                # Updated primary model
                response = client.models.generate_content_stream(
                    model="gemini-3.5-flash-lite",
                    contents=contents,
                )
                for chunk in response:
                    yield chunk.text
            except Exception:
                # Fallback to gemini-3.8-flash if needed
                response = client.models.generate_content_stream(
                    model="gemini-3.8-flash",
                    contents=contents,
                )
                for chunk in response:
                    yield chunk.text

        with st.spinner("Crafting your itinerary..."):
            itinerary_text = st.write_stream(generate_stream())

        if itinerary_text:
            st.download_button(
                label="📥 Download Itinerary (.txt)",
                data=itinerary_text,
                file_name=f"{location}_trip_plan.txt",
                mime="text/plain",
            )