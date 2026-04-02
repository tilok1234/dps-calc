import streamlit as st
import random

st.set_page_config(page_title="DPS Calculator")

st.title("⚔️ DPS Calculator (Fantasy Online 2 Accurate)")

# Inputs
min_damage = st.number_input("Min Damage", value=1076.0)
max_damage = st.number_input("Max Damage", value=1686.0)
attack_speed = st.number_input("Attack Speed (seconds per attack)", value=2.6)
crit_chance = st.number_input("Crit Chance (%)", value=142.0)
simulations = st.number_input("Number of Hits to Simulate", value=10000, step=1000)


# --- Crit system (your exact logic) ---
def roll_crit_multiplier(crit_chance):
    multiplier = 1
    remaining = crit_chance

    while remaining > 0:
        roll_chance = min(remaining, 90)
        if random.random() * 100 <= roll_chance:
            multiplier += 1
            remaining -= 90
        else:
            break

    return multiplier


# --- Simulation ---
if st.button("Calculate DPS"):

    total_damage = 0
    multiplier_counts = {}

    for _ in range(int(simulations)):

        # Random damage roll
        dmg = random.uniform(min_damage, max_damage)

        # Crit system
        multi = roll_crit_multiplier(crit_chance)

        # Track distribution
        multiplier_counts[multi] = multiplier_counts.get(multi, 0) + 1

        total_damage += dmg * multi

    # Average damage per hit
    avg_damage = total_damage / simulations

    # Convert attack speed (seconds → attacks/sec)
    attacks_per_second = 1 / attack_speed

    # Final DPS
    dps = avg_damage * attacks_per_second

    st.success(f"🔥 Estimated DPS: {dps:.2f}")

    # --- Show crit distribution ---
    st.subheader("📊 Crit Distribution")

    for multi in sorted(multiplier_counts):
        chance = (multiplier_counts[multi] / simulations) * 100
        st.write(f"{multi}x damage: {chance:.2f}%")