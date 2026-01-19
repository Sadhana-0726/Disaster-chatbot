import streamlit as st

st.error("RUNNING VERSION: v3-location-fix")

# =========================
# Page config
# =========================
st.set_page_config(
    page_title="Disaster Awareness Chatbot",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================
# FIXED SIDEBAR MASCOT
# =========================
st.markdown(
    """
    <style>
    section[data-testid="stSidebar"] {
        width: 420px !important;
        min-width: 420px !important;
    }

    .fixed-mascot {
        position: fixed;
        bottom: 40px;
        left: 40px;
        width: 340px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

with st.sidebar:
    st.markdown('<div class="fixed-mascot">', unsafe_allow_html=True)
    st.image("robo.png", use_container_width=True)
    st.markdown(
        """
        <p style="
            text-align:center;
            color:#cfd8e3;
            font-size:16px;
            line-height:1.4;
            margin-top:12px;
        ">
        Hi! I’m your little safety mascot<br>
        I’ll help you stay calm, informed, and prepared.
        </p>
        """,
        unsafe_allow_html=True
    )
    st.markdown("</div>", unsafe_allow_html=True)

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
            }
        },
        "unsafe": {
            "window": {
                "reason": "Glass can shatter and cause serious injuries.",
                "solution": "Move away from windows.",
                "how": "Take cover under sturdy furniture."
            },
            "tree": {
                "reason": "Trees may fall or drop branches.",
                "solution": "Move to an open area.",
                "how": "Protect your head."
            }
        }
    },
    "flood": {
        "safe": {
            "higher floor": {
                "reason": "Higher floors stay above floodwater.",
                "solution": "Move to higher floors.",
                "how": "Avoid basements."
            }
        },
        "unsafe": {
            "road": {
                "reason": "Floodwater can sweep you away.",
                "solution": "Move to higher ground.",
                "how": "Never walk or drive through floodwater."
            }
        }
    },
    "cyclone": {
        "safe": {
            "interior room": {
                "reason": "Interior rooms are protected from strong winds and flying debris.",
                "solution": "Stay in an interior room away from doors and windows.",
                "how": "Choose a small room on the lowest level of a strong building."
            }
        },
        "unsafe": {
            "window": {
                "reason": "Strong winds can shatter glass and turn debris into projectiles.",
                "solution": "Move away from windows immediately.",
                "how": "Go to an interior room and stay low."
            },
            "balcony": {
                "reason": "High winds can knock you over or throw debris.",
                "solution": "Go indoors to a safe shelter.",
                "how": "Close doors and stay inside."
            }
        }
    }
}

# =========================
# DEFINITIONS (UNCHANGED)
# =========================
DISASTER_DEFINITIONS = {
    "earthquake": (
        "An earthquake is a sudden shaking of the ground caused by movements "
        "within the Earth's crust. These movements release stored energy in the "
        "form of seismic waves, which can cause buildings to shake, crack, or collapse. "
        "Earthquakes often occur without warning and can lead to injuries, fires, "
        "and damage to infrastructure."
    ),
    "flood": (
        "A flood occurs when a large amount of water overflows onto normally dry land. "
        "Floods can be caused by heavy rainfall, overflowing rivers, dam failures, "
        "or storm surges. Floodwater can move very fast, carry debris, and contaminate "
        "water supplies, making it extremely dangerous to people and property."
    ),
    "cyclone": (
        "A cyclone is a powerful rotating storm system that forms over warm ocean waters. "
        "It is characterized by very strong winds, heavy rainfall, and sometimes storm surges. "
        "Cyclones can cause widespread damage to buildings, power lines, trees, and roads, "
        "and may also lead to flooding and loss of life."
    )
}

GENERAL_ACTIONS = {
    "earthquake": {
        "do": [
            "Drop, Cover, and Hold On.",
            "Take cover under sturdy furniture.",
            "Stay away from windows."
        ],
        "dont": [
            "Do not run outside during shaking.",
            "Do not use elevators."
        ],
        "why": (
            "Falling objects, broken glass, and structural collapse "
            "are the biggest causes of injury during earthquakes."
        )
    },
    "flood": {
        "do": [
            "Move to higher ground or higher floors immediately.",
            "Follow evacuation instructions issued by authorities.",
            "Keep emergency supplies and important documents ready."
        ],
        "dont": [
            "Do not walk, swim, or drive through floodwater.",
            "Do not touch electrical equipment if you are wet or standing in water."
        ],
        "why": (
            "Floodwater can be fast-moving, electrically charged, and contaminated."
        )
    },
    "cyclone": {
        "do": [
            "Stay indoors in a strong building.",
            "Secure loose objects.",
            "Keep emergency supplies ready."
        ],
        "dont": [
            "Do not go outside during strong winds.",
            "Do not ignore evacuation warnings."
        ],
        "why": (
            "Cyclones bring extreme winds and flooding that can cause serious harm."
        )
    }
}

# =========================
# Chat state
# =========================
if "messages" not in st.session_state:
    st.session_state.messages = []

if "last_disaster" not in st.session_state:
    st.session_state.last_disaster = None

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# =========================
# Helper functions
# =========================
def detect_disaster(text):
    if "earthquake" in text:
        return "earthquake"
    if "flood" in text:
        return "flood"
    if "cyclone" in text or "storm" in text:
        return "cyclone"
    return None


def generate_answer(user_text):
    text = user_text.lower()

    disaster = detect_disaster(text)
    if not disaster:
        disaster = st.session_state.last_disaster

    if not disaster:
        return "Please mention the disaster first."

    st.session_state.last_disaster = disaster

    # SAFE
    for place, info in DISASTER_HAZARD_CATEGORIES[disaster]["safe"].items():
        if place in text or "where is safe" in text or "safe place" in text:
            return (
                "YES — SAFE\n\n"
                f"Why: {info['reason']}\n\n"
                f"What to do: {info['solution']}\n\n"
                f"How: {info['how']}"
            )

    # UNSAFE
    for place, info in DISASTER_HAZARD_CATEGORIES[disaster]["unsafe"].items():
        if place in text:
            return (
                "NO — NOT SAFE\n\n"
                f"Why: {info['reason']}\n\n"
                f"What to do: {info['solution']}\n\n"
                f"How: {info['how']}"
            )

    # Definition
    if text.startswith("what is"):
        return DISASTER_DEFINITIONS[disaster]

    # Safety rules / precautions
    if "safety" in text or "rules" in text or "precaution" in text:
        return (
            f"Safety rules for {disaster}:\n\n"
            + "\n".join("- " + x for x in GENERAL_ACTIONS[disaster]["do"])
            + "\n\nAvoid:\n"
            + "\n".join("- " + x for x in GENERAL_ACTIONS[disaster]["dont"])
        )

    return f"You are asking about {disaster}."

# =========================
# Input
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
st.caption(" ⚠️ This chatbot provides general safety guidance only.")

