import streamlit as st

# =========================
# Disaster knowledge base
# =========================

DISASTER_HAZARD_CATEGORIES = {
    "earthquake": {
        "safe": {
            "table": {
                "reason": "A sturdy table can protect you from falling debris.",
                "solution": "Take cover under a sturdy table or desk.",
                "how": "Get under the table, cover your head and neck, and hold on."
            },
            "desk": {
                "reason": "Desks can shield you from falling objects.",
                "solution": "Take cover under the desk.",
                "how": "Hold the desk legs and protect your head."
            },
            "open area": {
                "reason": "Open areas reduce the risk of falling debris.",
                "solution": "Move to an open area away from buildings.",
                "how": "Stay low and protect your head."
            }
        },
        "unsafe": {
            "tree": {
                "reason": "Trees may fall or drop branches during shaking.",
                "solution": "Move away from trees to an open area.",
                "how": "Cover your head and stay alert."
            },
            "road": {
                "reason": "Nearby buildings or poles may collapse.",
                "solution": "Move away from buildings to an open space.",
                "how": "Drop, Cover, and Hold On if debris starts falling."
            },
            "window": {
                "reason": "Glass can shatter and cause serious injuries.",
                "solution": "Move away from windows.",
                "how": "Take cover under sturdy furniture."
            },
            "roof": {
                "reason": "Upper levels experience stronger shaking.",
                "solution": "Stay inside and take cover immediately.",
                "how": "Get under sturdy furniture."
            }
        }
    },

    "flood": {
        "safe": {
            "roof": {
                "reason": "Roofs keep you above rising floodwater.",
                "solution": "Move to the roof if water is rising rapidly.",
                "how": "Avoid edges and signal for help."
            },
            "higher floor": {
                "reason": "Higher floors are safer than ground level.",
                "solution": "Move to higher floors inside your house.",
                "how": "Avoid basements and ground floors."
            }
        },
        "unsafe": {
            "road": {
                "reason": "Floodwater can sweep people away.",
                "solution": "Move to higher ground immediately.",
                "how": "Never walk or drive through floodwater."
            },
            "tree": {
                "reason": "Trees can collapse or be submerged.",
                "solution": "Move to a stable building or higher ground.",
                "how": "Avoid standing near trees in floods."
            },
            "basement": {
                "reason": "Basements fill quickly with water.",
                "solution": "Move to upper floors.",
                "how": "Evacuate early if possible."
            }
        }
    }
}

DISASTER_DEFINITIONS = {
    "earthquake": (
        "An earthquake is the sudden shaking of the ground caused by movement "
        "of tectonic plates beneath the Earth’s surface."
    ),
    "flood": (
        "A flood occurs when water overflows onto normally dry land, often due "
        "to heavy rain, river overflow, or dam failure."
    ),
    "cyclone": (
        "A cyclone is a large rotating storm system with strong winds and heavy rain. "
        "In India, cyclones usually form over warm oceans and cause wind damage, "
        "flooding, and storm surges."
    )
}

GENERAL_ACTIONS = {
    "earthquake": (
        "During an earthquake, **Drop, Cover, and Hold On**.\n\n"
        "What to do:\n"
        "- Get under sturdy furniture (table or desk)\n"
        "- Stay away from windows\n"
        "- Do not use elevators\n\n"
        "Why:\n"
        "Most injuries occur due to falling objects and glass."
    ),
    "flood": (
        "During a flood, move to **higher ground immediately**.\n\n"
        "What to do:\n"
        "- Avoid roads and floodwater\n"
        "- Move to higher floors or roofs\n"
        "- Follow evacuation orders\n\n"
        "Why:\n"
        "Floodwater can rise quickly and sweep people away."
    ),
    "cyclone": (
        "During a cyclone, stay **indoors in a strong building**.\n\n"
        "What to do:\n"
        "- Stay away from windows and doors\n"
        "- Keep emergency supplies ready\n"
        "- Follow official warnings\n\n"
        "Why:\n"
        "Cyclones cause strong winds, flying debris, and heavy rain."
    )
}

# =========================
# Streamlit setup
# =========================

st.set_page_config(
    page_title="Disaster Awareness Chatbot",
    page_icon="🌍",
    layout="wide"  # <-- use wide to allow side columns
)

st.title("🌍 Disaster Awareness Assistant")
st.write(
    "Ask about **earthquake, flood, or cyclone safety**.\n"
    "You will get clear answers with **what to do, why, and how**."
)

# Chat history + mascot
col1, col2 = st.columns([3, 1])  # 3:1 ratio, chat left, mascot right

with col2:
    st.image("robo.png", width=150, caption="Your friendly safety guide")  # Add your mascot here

with col1:
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display previous messages
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Chat input and response handling goes here (your existing code)


# =========================
# Helper functions
# =========================

def detect_disaster(text):
    text = text.lower()
    if "earthquake" in text or "quake" in text:
        return "earthquake"
    if "flood" in text:
        return "flood"
    if "cyclone" in text or "storm" in text:
        return "cyclone"
    return None

def get_last_disaster():
    for msg in reversed(st.session_state.messages):
        d = detect_disaster(msg["content"])
        if d:
            return d
    return None

def is_definition_question(text):
    return any(p in text.lower() for p in ["what is", "define", "meaning of", "explain"])

def is_general_action_question(text):
    return any(p in text.lower() for p in [
        "what should i do",
        "what to do",
        "during",
        "precautions",
        "safety measures"
    ])

def detect_location(text, disaster):
    text = text.lower()
    data = DISASTER_HAZARD_CATEGORIES.get(disaster, {})
    for cat in ["unsafe", "safe"]:
        for place in data.get(cat, {}):
            if place in text:
                return cat, place
    return None, None

def detect_place_only(text):
    places = [
        "window", "windows", "road", "tree", "roof",
        "table", "desk", "basement", "higher floor"
    ]
    for p in places:
        if p in text.lower():
            return p
    return None

def generate_answer(user_text):
    disaster = detect_disaster(user_text) or get_last_disaster()

    # Definition
    if is_definition_question(user_text) and disaster:
        return DISASTER_DEFINITIONS[disaster]

    # General actions
    if is_general_action_question(user_text) and disaster:
        return GENERAL_ACTIONS[disaster]

    # Location-based with disaster
    if disaster:
        cat, place = detect_location(user_text, disaster)
        if cat:
            info = DISASTER_HAZARD_CATEGORIES[disaster][cat][place]
            prefix = "Yes, safer." if cat == "safe" else "No, not safe."
            return (
                f"{prefix} {info['reason']}\n\n"
                f"What to do:\n{info['solution']}\n\n"
                f"How:\n{info['how']}"
            )

    # Place mentioned but no disaster
    place_only = detect_place_only(user_text)
    if place_only:
        return (
            "No, it is not safe.\n\n"
            "Why:\n"
            "Certain places like windows, roads, or trees can become dangerous during disasters.\n\n"
            "What to do:\n"
            "Move to a safer interior or open area depending on the situation.\n\n"
            "How:\n"
            "Stay calm, protect your head, and follow official safety instructions."
        )

    if not disaster:
        return "Please mention the disaster (earthquake, flood, or cyclone)."

    return GENERAL_ACTIONS[disaster]

# =========================
# User input
# =========================

user_input = st.chat_input("Ask about disaster safety...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    reply = generate_answer(user_input)
    st.session_state.messages.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.markdown(reply)

st.markdown("---")
st.caption("⚠️ This chatbot provides general safety guidance only. Always follow local authorities.")
