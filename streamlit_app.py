import streamlit as st
import random
import pandas as pd

# Initialize the game
def initialize_game():
    return {
        "player_cash": 1000000,
        "computer_cash": 1000000,
        "rounds": 12,
        "oil_price": 85,
        "gasoil_price": 850,
        "player_positions": {"oil_contracts": 0, "gasoil_contracts": 0},
        "computer_positions": {"oil_contracts": 0, "gasoil_contracts": 0},
        "game_log": [],
        "news": ""
    }

# Game logic
def play_round(state, player_choice, quantity):
    # Random event
    events = [
        {"event": "OPEC cuts production", "oil_change": 5, "gasoil_change": 10},
        {"event": "Refinery strike", "oil_change": 0, "gasoil_change": 15},
        {"event": "Economic slowdown", "oil_change": -7, "gasoil_change": -10},
        {"event": "Pipeline disruption", "oil_change": 10, "gasoil_change": 5},
        {"event": "Mild winter demand drop", "oil_change": -5, "gasoil_change": -3},
    ]
    event = random.choice(events)
    state["oil_price"] += event["oil_change"]
    state["gasoil_price"] += event["gasoil_change"]
    state["news"] = event["event"]


    # Player action
    if player_choice == "buy_oil":
        cost = quantity * state["oil_price"] * 100
        if cost <= state["player_cash"]:
            state["player_positions"]["oil_contracts"] += quantity
            state["player_cash"] -= cost
    elif player_choice == "sell_oil":
        if state["player_positions"]["oil_contracts"] >= quantity:
            state["player_positions"]["oil_contracts"] -= quantity
            state["player_cash"] += quantity * state["oil_price"] * 100
    elif player_choice == "buy_gasoil":
        cost = quantity * state["gasoil_price"] * 10
        if cost <= state["player_cash"]:
            state["player_positions"]["gasoil_contracts"] += quantity
            state["player_cash"] -= cost
    elif player_choice == "sell_gasoil":
        if state["player_positions"]["gasoil_contracts"] >= quantity:
            state["player_positions"]["gasoil_contracts"] -= quantity
            state["player_cash"] += quantity * state["gasoil_price"] * 10

    # Computer action (randomized)
    computer_choice = random.choice(["buy_oil", "sell_oil", "buy_gasoil", "sell_gasoil", "hold"])
    comp_quantity = random.randint(1, 10)
    if computer_choice == "buy_oil":
        cost = comp_quantity * state["oil_price"] * 100
        if cost <= state["computer_cash"]:
            state["computer_positions"]["oil_contracts"] += comp_quantity
            state["computer_cash"] -= cost
    elif computer_choice == "sell_oil":
        if state["computer_positions"]["oil_contracts"] >= comp_quantity:
            state["computer_positions"]["oil_contracts"] -= comp_quantity
            state["computer_cash"] += comp_quantity * state["oil_price"] * 100
    elif computer_choice == "buy_gasoil":
        cost = comp_quantity * state["gasoil_price"] * 10
        if cost <= state["computer_cash"]:
            state["computer_positions"]["gasoil_contracts"] += comp_quantity
            state["computer_cash"] -= cost
    elif computer_choice == "sell_gasoil":
        if state["computer_positions"]["gasoil_contracts"] >= comp_quantity:
            state["computer_positions"]["gasoil_contracts"] -= comp_quantity
            state["computer_cash"] += comp_quantity * state["gasoil_price"] * 10

    # Log round
    state["game_log"].append({
        "Event": event["event"],
        "Oil Price": state["oil_price"],
        "Gasoil Price": state["gasoil_price"],
        "Player Cash": state["player_cash"],
        "Computer Cash": state["computer_cash"],
    })

# Streamlit interface
state = st.session_state

if "game_state" not in state:
    state.game_state = initialize_game()

st.title("Oil Trading Game")

if st.button("Reset Game"):
    state.game_state = initialize_game()

round_number = len(state.game_state["game_log"]) + 1
if round_number <= state.game_state["rounds"]:
    st.header(f"Round {round_number}")
    st.subheader("Market Conditions")
    st.write(f"Newsflash: {state.game_state['news']}")
    st.write(f"Oil Price: ${state.game_state['oil_price']}/barrel")
    st.write(f"Gasoil Price: ${state.game_state['gasoil_price']}/MT")
    st.write(f"Your Cash: ${state.game_state['player_cash']}")
    
    action = st.selectbox("Choose an action:", ["buy_oil", "sell_oil", "buy_gasoil", "sell_gasoil", "hold"])
    quantity = st.slider("Select quantity:", 1, 10, 1)

    if st.button("Submit Action"):
        play_round(state.game_state, action, quantity)

else:
    st.header("Game Over!")
    st.write(pd.DataFrame(state.game_state["game_log"]))