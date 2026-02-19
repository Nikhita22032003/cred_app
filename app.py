import streamlit as st
import pandas as pd
import time
import requests

st.set_page_config(page_title="CRED Rewards Optimizer", layout="wide")

# ==========================
# PREMIUM DARK THEME
# ==========================
st.markdown("""
<style>

/* Main Background */
.stApp {
    background-color: #0E1117;
    color: #FAFAFA;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #161B22;
}

/* Metric Cards */
div[data-testid="metric-container"] {
    background-color: #161B22;
    border: 1px solid #262730;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0px 4px 20px rgba(0,0,0,0.4);
}

/* Buttons */
.stButton>button {
    background-color: #3B82F6;
    color: white;
    border-radius: 10px;
    padding: 8px 20px;
    border: none;
    font-weight: 600;
}

.stButton>button:hover {
    background-color: #2563EB;
}

/* DataFrame Styling */
div[data-testid="stDataFrame"] {
    background-color: #161B22;
    border-radius: 10px;
    padding: 10px;
}

/* Headers */
h1, h2, h3 {
    color: #FFFFFF;
    font-weight: 600;
}

/* Info Box */
div[data-testid="stAlert"] {
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)


st.markdown("<h1 style='text-align: center;'>🪙 CRED Rewards Optimizer</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #9CA3AF;'>Simulate rewards, trust score & wallet growth</p>", unsafe_allow_html=True)


# ==========================
# SESSION STATE
# ==========================
if "history" not in st.session_state:
    st.session_state.history = []

if "wallet_balance" not in st.session_state:
    st.session_state.wallet_balance = 0

    # ==========================
# DEFAULT VARIABLES (PREVENT CRASH)
# ==========================
coins = 0.0
trust_score = 0
badge = "-"
trust_label = "-"


# ==========================
# SIDEBAR INPUTS
# ==========================
st.sidebar.header("🔧 Simulation Inputs")

username = st.sidebar.text_input(
    "👤 Enter your name",
    value="Nikhita"
)

amount = st.sidebar.number_input(
    "💳 Bill Amount",
    min_value=0,
    value=1000  # Default example bill
)

cibil = st.sidebar.slider(
    "📊 CIBIL Score",
    300,
    900,
    value=750  # Good credit score example
)

streak = st.sidebar.number_input(
    "🔥 Streak Days",
    min_value=0,
    value=5  # Example active user
)

fraud = st.sidebar.checkbox(
    "🚨 Fraud User?",
    value=False  # Default safe user
)

consent = st.sidebar.checkbox(
    "I confirm this is mock data",
    value=True  # Auto-enabled for demo
)

simulate = st.sidebar.button("🎯 Calculate Reward")
backend_btn = st.sidebar.button("🚀 Simulate via Backend")


# ==========================
# LOCAL SIMULATION
# ==========================
if simulate:

    if username == "":
        st.error("Please enter your name.")
        st.stop()

    if amount <= 0:
        st.error("Bill amount must be greater than 0.")
        st.stop()

    # Reward Logic
    coins = amount * 0.02 * (1 + streak * 0.1)

    if cibil >= 750:
        coins *= 1.2

    if fraud:
        coins *= 0.5

    coins = round(coins, 2)

    # Badge
    if coins < 5:
        badge = "🥉 Bronze"
    elif coins < 15:
        badge = "🥈 Silver"
    else:
        badge = "🥇 Gold"

    # Trust Score
    trust_score = 50

    if cibil >= 750:
        trust_score += 30
    elif cibil >= 650:
        trust_score += 15
    else:
        trust_score -= 10

    trust_score += min(streak * 2, 20)

    if fraud:
        trust_score -= 40

    trust_score = max(0, min(100, trust_score))

    if trust_score >= 70:
        trust_label = "🟢 High Trust"
    elif trust_score >= 40:
        trust_label = "🟡 Medium Trust"
    else:
        trust_label = "🔴 Low Trust"

   # ==========================
# DEFAULT GUIDE DISPLAY (ONLY ON FIRST LOAD)
# ==========================
if not st.session_state.history:

    st.subheader("📘 Example Simulation (Guide Preview)")

    # Default demo values
    demo_coins = 36.0
    demo_trust = 90
    demo_badge = "🥇 Gold"
    demo_label = "🟢 High Trust"

    col1, col2, col3 = st.columns(3)

    col1.metric("🪙 Coins Earned", demo_coins)
    col2.metric("🛡 Trust Score", f"{demo_trust}/100")
    col3.metric("🏅 Badge", demo_badge)

    st.info(f"Trust Level: {demo_label}")

    # Demo graph
    demo_days = list(range(1, 7))
    demo_coin_list = [24, 28, 30, 32, 34, 36]

    demo_df = pd.DataFrame({
        "Streak Days": demo_days,
        "Coins": demo_coin_list
    })

    st.line_chart(demo_df, x="Streak Days", y="Coins")

    st.caption("👆 This is a sample preview. Use the sidebar and click 'Calculate Reward' to simulate your own values.")


    

    # Save to history
    st.session_state.history.append({
        "User": username,
        "Amount": amount,
        "CIBIL": cibil,
        "Streak": streak,
        "Fraud": fraud,
        "Coins": coins,
        "Trust": trust_score
    })

    st.session_state.wallet_balance += coins

st.divider()

# ==========================
# WALLET SECTION
# ==========================
st.header("💼 Wallet Summary")

st.metric("🪙 Wallet Balance", round(st.session_state.wallet_balance, 2))

if st.session_state.history:

    history_df = pd.DataFrame(st.session_state.history)
    st.dataframe(history_df)

    csv = history_df.to_csv(index=False).encode("utf-8")
    st.download_button("⬇ Download Wallet CSV", csv, "cred_wallet.csv")

    if st.button("🗑 Clear Wallet"):
        st.session_state.history = []
        st.session_state.wallet_balance = 0
        st.success("Wallet cleared!")

st.divider()

# ==========================
# LEADERBOARD
# ==========================
if st.session_state.history:

    st.header("🏆 Leaderboard")

    df = pd.DataFrame(st.session_state.history)

    leaderboard = (
        df.groupby("User")["Coins"]
        .sum()
        .reset_index()
        .sort_values(by="Coins", ascending=False)
    )

    st.dataframe(leaderboard.head(5))

    top_user = leaderboard.iloc[0]["User"]
    top_coins = leaderboard.iloc[0]["Coins"]

    st.success(f"👑 Top User: {top_user} ({round(top_coins,2)} coins)")

st.divider()

# ==========================
# REDEEM SECTION
# ==========================
st.header("💳 Redeem Coins")

redeem = st.number_input("Enter coins to redeem", min_value=0.0)

if st.button("Redeem Now"):
    if redeem > st.session_state.wallet_balance:
        st.error("Not enough coins.")
    else:
        st.session_state.wallet_balance -= redeem
        st.success(f"Redeemed {redeem} coins 🎉")

st.divider()

# ==========================
# BACKEND SIMULATION
# ==========================
if backend_btn:

    if not consent:
        st.error("Please confirm mock data consent.")
        st.stop()

    try:
        response = requests.post(
            "http://127.0.0.1:8000/simulate",
            json={
                "amount": amount,
                "cibil": cibil,
                "streak": streak,
                "fraud": fraud
            }
        )

        if response.status_code != 200:
            st.error("Backend validation failed.")
            st.stop()

        data = response.json()

        st.success(f"Backend Coins: {data['coins']}")
        st.info(f"Risk Score: {data['risk_score']}")
        st.write(data["explanation"])

    except:
        st.error("Backend not running. Start FastAPI server.")
