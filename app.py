import random
from pathlib import Path

import streamlit as st

st.set_page_config(page_title="Fantasy Online 2 DPS Calculator", layout="wide")

# -----------------------
# CONSTANTS
# -----------------------
FIREBALL_MIN = 1250.0
FIREBALL_MAX = 2250.0
FIREBALL_COST = 750.0
FIREBALL_CD = 0.0
FIREBALL_CAST = 1.0

BASE_DIR = Path(__file__).parent

BUFFS = [
    {
        "key": "self_motivated_r6",
        "name": "Self-motivated Rank 6",
        "regen": 60.0,
        "icon": BASE_DIR / "self_motivated_r6.png",
    },
    {
        "key": "self_motivated_r5",
        "name": "Self-motivated Rank 5",
        "regen": 40.0,
        "icon": BASE_DIR / "self_motivated_r5.png",
    },
    {
        "key": "pet_owl_r3",
        "name": "Pet Owl Rank 3",
        "regen": 60.0,
        "icon": BASE_DIR / "pet_owl_r3.png",
    },
    {
        "key": "trade_off_r1",
        "name": "Trade Off Rank 1",
        "regen": 68.0,
        "icon": BASE_DIR / "trade_off_r1.png",
    },
    {
        "key": "manhole_manifest_r1",
        "name": "Manhole manifest Rank 1",
        "regen": 40.0,
        "icon": BASE_DIR / "manhole_manifest_r1.png",
    },
    {
        "key": "pet_ice_fairy",
        "name": "Pet Ice Fairy",
        "regen": 63.0,
        "icon": BASE_DIR / "pet_ice_fairy.png",
    },
]

# -----------------------
# SESSION STATE DEFAULTS
# -----------------------
if "fireball_enabled" not in st.session_state:
    st.session_state.fireball_enabled = False

for buff in BUFFS:
    if buff["key"] not in st.session_state:
        st.session_state[buff["key"]] = False

# -----------------------
# HELPERS
# -----------------------
def roll_crit_multiplier(crit_chance: float) -> int:
    crit_multiplier = 1
    remaining_crit = crit_chance

    while remaining_crit > 0:
        roll_chance = min(remaining_crit, 90)
        if random.random() * 100 <= roll_chance:
            crit_multiplier += 1
            remaining_crit -= 90
        else:
            break

    return crit_multiplier


def roll_damage(min_dmg: float, max_dmg: float) -> float:
    return random.uniform(min_dmg, max_dmg)


def icon_toggle(buff_key: str, icon_path: Path, label: str, active: bool, unique_key: str):
    border_color = "#32cd32" if active else "#444444"
    bg_color = "#162016" if active else "#111111"

    if icon_path.exists():
        st.markdown(
            f"""
            <div style="
                border: 3px solid {border_color};
                border-radius: 10px;
                padding: 4px;
                width: 74px;
                background: {bg_color};
                margin-bottom: 6px;
            ">
            """,
            unsafe_allow_html=True,
        )
        st.image(str(icon_path), width=64)
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.markdown(
            f"""
            <div style="
                border: 3px solid {border_color};
                border-radius: 10px;
                width: 74px;
                height: 74px;
                display: flex;
                align-items: center;
                justify-content: center;
                background: {bg_color};
                font-size: 11px;
                text-align: center;
                padding: 4px;
                margin-bottom: 6px;
            ">
                Missing icon
            </div>
            """,
            unsafe_allow_html=True,
        )

    button_text = "ON" if active else "OFF"
    if st.button(button_text, key=unique_key, use_container_width=True):
        st.session_state[buff_key] = not st.session_state[buff_key]
        st.rerun()

    st.caption(label)


def get_buff_regen_total() -> float:
    total = 0.0
    for buff in BUFFS:
        if st.session_state[buff["key"]]:
            total += buff["regen"]
    return total


# -----------------------
# TITLE
# -----------------------
st.title("⚔️ Fantasy Online 2 DPS Calculator")

# -----------------------
# BASE STATS
# -----------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("⚔️ Auto Attack")
    min_damage = st.number_input("Auto Min Damage", min_value=0.0, value=1076.0)
    max_damage = st.number_input("Auto Max Damage", min_value=0.0, value=1686.0)
    attack_speed = st.number_input(
        "Attack Speed (seconds per attack)",
        min_value=0.0001,
        value=2.6,
        step=0.1,
    )
    crit_chance = st.number_input("Crit Chance (%)", min_value=0.0, value=142.0)

with col2:
    st.subheader("⚡ Energy")
    max_energy = st.number_input("Max Energy", min_value=0.0, value=1000.0)
    starting_energy = st.number_input("Starting Energy", min_value=0.0, value=1000.0)

    use_manual_regen = st.checkbox("Use manual energy regen", value=True)

    if use_manual_regen:
        energy_regen = st.number_input(
            "Energy Regen per second",
            min_value=0.0,
            value=50.0,
            step=1.0,
        )
    else:
        st.write("Select active energy regen buffs below.")
        energy_regen = get_buff_regen_total()
        st.info(f"Total buff energy regen: {energy_regen:.1f}/s")

# -----------------------
# SKILLS
# -----------------------
st.subheader("🔥 Skills")

skill_col1, skill_col2 = st.columns([1, 5])

with skill_col1:
    fireball_icon = BASE_DIR / "fireball.png"
    fireball_border = "#32cd32" if st.session_state.fireball_enabled else "#444444"
    fireball_bg = "#162016" if st.session_state.fireball_enabled else "#111111"

    if fireball_icon.exists():
        st.markdown(
            f"""
            <div style="
                border: 3px solid {fireball_border};
                border-radius: 10px;
                padding: 4px;
                width: 74px;
                background: {fireball_bg};
                margin-bottom: 6px;
            ">
            """,
            unsafe_allow_html=True,
        )
        st.image(str(fireball_icon), width=64)
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.warning("fireball.png not found")

    fireball_label = "ON" if st.session_state.fireball_enabled else "OFF"
    if st.button(fireball_label, key="toggle_fireball", use_container_width=True):
        st.session_state.fireball_enabled = not st.session_state.fireball_enabled
        st.rerun()

with skill_col2:
    status = "ACTIVE" if st.session_state.fireball_enabled else "OFF"
    st.markdown(f"**Fireball Rank 4** — {status}")
    st.write("Damage: 1250-2250")
    st.write("Cooldown: 0")
    st.write("Energy Cost: 750")
    st.write("Cast Time: 1 sec")

# -----------------------
# BUFFS
# -----------------------
if not use_manual_regen:
    st.subheader("🔋 Energy Regen Buffs")

    buff_cols = st.columns(6)
    for i, buff in enumerate(BUFFS):
        with buff_cols[i]:
            icon_toggle(
                buff_key=buff["key"],
                icon_path=buff["icon"],
                label=f"{buff['name']} (+{buff['regen']:.0f}/s)",
                active=st.session_state[buff["key"]],
                unique_key=f"btn_{buff['key']}",
            )

    energy_regen = get_buff_regen_total()
    st.success(f"Active buff energy regen: {energy_regen:.1f}/s")

# -----------------------
# SIMULATION SETTINGS
# -----------------------
st.subheader("⏱ Simulation")
simulation_time = st.number_input("Simulation Time (seconds)", min_value=1.0, value=60.0)

# -----------------------
# CALCULATE
# -----------------------
if st.button("Calculate DPS", type="primary"):
    if max_damage < min_damage:
        st.error("Auto Max Damage must be greater than or equal to Auto Min Damage.")
    else:
        time = 0.0
        dt = 0.01

        energy = min(starting_energy, max_energy)

        next_auto = 0.0
        next_skill = 0.0
        casting_until = 0.0

        total_damage = 0.0
        auto_damage = 0.0
        skill_damage = 0.0

        auto_hits = 0
        fireball_casts = 0

        pending_hits = []

        while time < simulation_time:
            # Energy regeneration
            energy = min(max_energy, energy + energy_regen * dt)

            # Auto attacks continue independently
            while next_auto <= time:
                dmg = roll_damage(min_damage, max_damage)
                crit = roll_crit_multiplier(crit_chance)
                final = dmg * crit

                total_damage += final
                auto_damage += final
                auto_hits += 1

                next_auto += attack_speed

            # Apply pending spell hits whose cast finished
            remaining_hits = []
            for hit in pending_hits:
                if time >= hit["time"]:
                    total_damage += hit["damage"]
                    skill_damage += hit["damage"]
                else:
                    remaining_hits.append(hit)
            pending_hits = remaining_hits

            # Only one skill can be cast at a time
            if st.session_state.fireball_enabled:
                if time >= casting_until and time >= next_skill and energy >= FIREBALL_COST:
                    energy -= FIREBALL_COST
                    casting_until = time + FIREBALL_CAST
                    next_skill = time + FIREBALL_CD
                    fireball_casts += 1

                    dmg = roll_damage(FIREBALL_MIN, FIREBALL_MAX)
                    crit = roll_crit_multiplier(crit_chance)
                    final = dmg * crit

                    pending_hits.append({
                        "time": casting_until,
                        "damage": final
                    })

            time += dt

        total_dps = total_damage / simulation_time
        auto_dps = auto_damage / simulation_time
        fireball_dps = skill_damage / simulation_time

        st.success(f"🔥 Total DPS: {total_dps:,.2f}")

        r1, r2, r3 = st.columns(3)
        r1.metric("Auto DPS", f"{auto_dps:,.2f}")
        r2.metric("Fireball DPS", f"{fireball_dps:,.2f}")
        r3.metric("Energy Regen", f"{energy_regen:,.1f}/s")

        st.write(f"Auto hits: {auto_hits}")
        st.write(f"Fireball casts: {fireball_casts}")
        st.write(f"Ending Energy: {energy:.2f}")