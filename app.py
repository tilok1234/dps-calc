import streamlit as st
import random

st.set_page_config(page_title="Fantasy Online 2 DPS Calculator")

st.title("⚔️ Fantasy Online 2 DPS Calculator")

# -----------------------
# AUTO ATTACK
# -----------------------
st.subheader("⚔️ Auto Attack")

min_damage = st.number_input("Auto Min Damage", value=1076.0)
max_damage = st.number_input("Auto Max Damage", value=1686.0)
attack_speed = st.number_input("Attack Speed (seconds per attack)", value=2.6)
crit_chance = st.number_input("Crit Chance (%)", value=142.0)

# -----------------------
# ENERGY
# -----------------------
st.subheader("⚡ Energy")

max_energy = st.number_input("Max Energy", value=1000.0)
starting_energy = st.number_input("Starting Energy", value=1000.0)
energy_regen = st.number_input("Energy Regen per second", value=50.0)

# -----------------------
# FIREBALL ICON TOGGLE
# -----------------------
st.subheader("🔥 Skills")

# Fireball constants
FIREBALL_MIN = 1250
FIREBALL_MAX = 2250
FIREBALL_COST = 750
FIREBALL_CD = 0
FIREBALL_CAST = 1.0

# Session state
if "fireball_enabled" not in st.session_state:
    st.session_state.fireball_enabled = False

col1, col2 = st.columns([1, 3])

with col1:
    # Show icon
    st.image("fireball.png", width=64)

    # Toggle button
    if st.button("Toggle Fireball"):
        st.session_state.fireball_enabled = not st.session_state.fireball_enabled

with col2:
    if st.session_state.fireball_enabled:
        st.markdown("### 🟢 Fireball ACTIVE")
    else:
        st.markdown("### 🔴 Fireball OFF")

# -----------------------
# SIMULATION
# -----------------------
simulation_time = st.number_input("Simulation Time (seconds)", value=60.0)


# -----------------------
# CRIT SYSTEM
# -----------------------
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


def roll_damage(min_dmg, max_dmg):
    return random.uniform(min_dmg, max_dmg)


# -----------------------
# SIMULATION
# -----------------------
if st.button("Calculate DPS"):

    time = 0
    dt = 0.01

    energy = min(starting_energy, max_energy)

    next_auto = 0
    next_skill = 0
    casting_until = 0

    total_damage = 0
    auto_damage = 0
    skill_damage = 0

    auto_hits = 0
    skill_casts = 0

    pending_hits = []

    while time < simulation_time:

        # Energy regen
        energy = min(max_energy, energy + energy_regen * dt)

        # ---------------- AUTO ATTACK ----------------
        while next_auto <= time:
            dmg = roll_damage(min_damage, max_damage)
            crit = roll_crit_multiplier(crit_chance)

            final = dmg * crit

            total_damage += final
            auto_damage += final
            auto_hits += 1

            next_auto += attack_speed

        # ---------------- APPLY SKILL DAMAGE ----------------
        for hit in pending_hits[:]:
            if time >= hit["time"]:
                total_damage += hit["damage"]
                skill_damage += hit["damage"]
                pending_hits.remove(hit)

        # ---------------- FIREBALL ----------------
        if st.session_state.fireball_enabled:

            if time >= casting_until:

                if time >= next_skill and energy >= FIREBALL_COST:

                    energy -= FIREBALL_COST
                    casting_until = time + FIREBALL_CAST
                    next_skill = time + FIREBALL_CD
                    skill_casts += 1

                    dmg = roll_damage(FIREBALL_MIN, FIREBALL_MAX)
                    crit = roll_crit_multiplier(crit_chance)

                    final = dmg * crit

                    pending_hits.append({
                        "time": casting_until,
                        "damage": final
                    })

        time += dt

    # ---------------- RESULTS ----------------
    total_dps = total_damage / simulation_time
    auto_dps = auto_damage / simulation_time
    skill_dps = skill_damage / simulation_time

    st.success(f"🔥 Total DPS: {total_dps:.2f}")

    st.write(f"⚔️ Auto DPS: {auto_dps:.2f}")
    st.write(f"🔥 Fireball DPS: {skill_dps:.2f}")

    st.write(f"Auto hits: {auto_hits}")
    st.write(f"Fireball casts: {skill_casts}")
    st.write(f"Ending Energy: {energy:.2f}")