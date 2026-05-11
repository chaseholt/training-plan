"""
Rewrite the St. George Marathon plan to include a 4-day strength program.

Priorities (in order):
1. Climbing strength - pulling, finger, core
2. Running injury prevention + strength - posterior chain, single-leg, eccentric quad
3. Aesthetic muscle (lowest priority - skip dedicated bicep/chest pump work)

Schedule:
  Mon: Lift B - Upper Pull (climbing focus, no run impact)
  Tue: AM Quality Run (no lift)
  Wed: AM Easy Run + PM Lift A - Lower Heavy (72hrs from Sat long run)
  Thu: AM Easy/Med Run + PM Lift C - Upper Push + Core (no leg fatigue)
  Fri: Climb or Rest
  Sat: AM Long Run (NO LIFT)
  Sun: AM Climb + PM Lift D - Lower Power/Foot (light, 48hrs before Tue)

= 4 lifts per week (Mon, Wed, Thu, Sun)
"""

import json
from pathlib import Path

INPUT = Path("/sessions/laughing-inspiring-goldberg/mnt/outputs/chase-st-george-marathon-2026-10-03.json")
OUTPUT = Path("/sessions/laughing-inspiring-goldberg/mnt/outputs/chase-st-george-marathon-2026-10-03.json")

# ============================================================
# LIFT TEMPLATES
# ============================================================
# Each template has phase-specific variants:
#   foundation  (W1-4):   3 sets, 8-12 reps, RPE 6-7 - learn form, build base
#   build       (W5-7):   4 sets, 6-8 reps,  RPE 7-8 - load up
#   maintain    (W8-9, 12-14, 19-20): 3 sets, 6-8 reps, RPE 7 - hold gains
#   peak        (W16-17): 4 sets, 5-6 reps,  RPE 8   - max strength + plyo
#   light       (W11, W15, W18, W21): 2 sets, 8 reps, RPE 5-6 - deload
#   skip        (W10 race wk, W22 race wk): mobility only

PHASE_DESC = {
    "foundation": "Foundation phase: 3 sets, 8-12 reps, RPE 6-7 (challenging but 2-3 reps in reserve). Focus on PERFECT FORM.",
    "build":      "Build phase: 4 sets, 6-8 reps, RPE 7-8 (1-2 reps in reserve). Add weight when you hit top of rep range cleanly.",
    "maintain":   "Maintain phase: 3 sets, 6-8 reps, RPE 7. Hold strength while running takes priority.",
    "peak":       "Peak phase: 4 sets, 5-6 reps, RPE 8 (1 rep in reserve). Heavy compound work + plyometrics for downhill prep.",
    "light":      "Deload week: 2 sets, 8 reps, RPE 5-6 (very controlled). Active recovery only.",
    "mobility":   "RACE WEEK: Mobility and activation only. NO loaded lifting.",
}

LIFT_A = """LOWER BODY HEAVY - Posterior chain + eccentric quad
Goal: Hip drive for climbing, posterior chain power for running, eccentric quad for downhill (St. George prep)

{phase_desc}

WARM UP (8-10 min):
  - 5 min easy bike or rowing
  - World's greatest stretch x 5 each side
  - Glute bridge x 15 (activation)
  - Bodyweight squat x 10
  - Cossack squat x 5 each

MAIN LIFT:
1. TRAP BAR DEADLIFT (or Romanian Deadlift if no trap bar): {sets_main}x{reps_main}
   - Drive hips back, neutral spine, push floor away
   - Climbing crossover: hip hinge = body tension on the wall

2. BULGARIAN SPLIT SQUAT (DB in each hand): {sets_main}x{reps_unilateral} EACH leg
   - Front foot far enough that knee tracks over ankle
   - 3-second descent, drive up through heel
   - The single best exercise for runners. Don't skip.

3. BARBELL HIP THRUST (or Glute Bridge with band): {sets_acc}x{reps_glute}
   - Pause 1 sec at top, full glute squeeze
   - Posterior chain power = late-race pace maintenance

4. REVERSE LUNGE - SLOW ECCENTRIC: {sets_acc}x{reps_unilateral} EACH leg
   - 3-second descent with DBs
   - DIRECT downhill marathon prep - eccentric quad load

5. SINGLE-LEG CALF RAISE (off step): {sets_acc}x{reps_calf} EACH
   - Slow 3-sec descent, full stretch at bottom
   - Achilles + foot resilience

6. PALLOF PRESS (anti-rotation): 3x10 each side
   - Core resists rotation - critical for running form + climbing tension

Total time: 45-55 min"""

LIFT_B = """UPPER PULL - Climbing focus
Goal: Maximum pulling strength for climbing. This is your highest-priority lift session for climbing performance.

{phase_desc}

WARM UP (8 min):
  - 5 min light pulling (banded or jumping pull-ups easy)
  - Shoulder CARs x 5 each direction
  - Scap pull-ups x 10
  - Band pull-aparts x 15
  - Easy hangs (bar) 2x 15s

MAIN LIFT:
1. WEIGHTED PULL-UP (or strict bodyweight if not yet weighted): {sets_main}x{reps_pullup}
   - Full ROM: chin clearly over bar, full elbow extension at bottom
   - Climbing's #1 strength predictor

2. ONE-ARM DUMBBELL ROW: {sets_main}x{reps_row} EACH
   - Pause at top, control descent. Lock shoulder blade down.

3. INVERTED ROW or TRX ROW: {sets_acc}x{reps_acc}
   - Horizontal pulling balances vertical (pull-up)

4. HANGBOARD PROTOCOL: {hangboard}
   - 20mm edges, half-crimp or open-hand
   - 90 sec rest between hangs
   - SKIP if fingers feel sore from climbing this week

5. FACE PULL: 3x12-15
   - External rotation + scap retraction = healthy shoulders for high-volume climbing

6. HAMMER CURL (forearm flexor + brachialis): 2x10
   - Forearm endurance for sustained crimping. KEEP this brief - not the goal.

7. WRIST CURL + WRIST EXTENSION: 2x12 each
   - Forearm extensor balance prevents elbow tendinopathy from climbing

8. DEAD HANG (open-hand): 3x max time (target 45s+)
   - Grip endurance + scap stability

Total time: 50-60 min"""

LIFT_C = """UPPER PUSH + CORE - Antagonist + stability
Goal: Antagonist work for climbing (prevents overuse injuries), shoulder stability, anti-extension/rotation core.
This is NOT a chest day. We're balancing the pulling-dominant climbing/back work.

{phase_desc}

WARM UP (5 min):
  - Arm circles + band pass-throughs x 10
  - Cat-cow x 10
  - Push-up to down dog x 8
  - Plank shoulder taps x 10 each

MAIN LIFT:
1. PUSH-UP variations (decline → standard → diamond): {sets_main}x{reps_push}
   - Hollow body position, full ROM, controlled tempo
   - Rotate variations week-to-week to keep stimulus varied

2. DUMBBELL OVERHEAD PRESS (standing): {sets_main}x{reps_ohp}
   - Brace core hard, no lumbar extension. This is core work too.
   - Strong overhead press = healthy shoulders for sustained climbing

3. Y-T-W RAISES (light DB or band, prone): 3x8 each letter
   - Mid/lower trap activation - the muscles that protect your shoulders during climbing pulls

4. BANDED PULL-APART: 3x15
   - High volume, light resistance. Pure shoulder health work.

5. PLANK (front): 3x{plank_time}
   - Hollow body engagement. Glutes squeezed. NO sagging.

6. SIDE PLANK: 2x30-45s EACH side
   - Lateral core stability for running stride + climbing tension

7. DEAD BUG (slow, controlled): 3x10 EACH side
   - Anti-extension. Lock low back to floor.

8. HOLLOW BODY HOLD: 3x{hollow_time}
   - Total body tension. Climbing's #1 core position. Hands and heels OFF floor.

9. PALLOF PRESS HOLD: 2x20s each side
   - Anti-rotation. Climbing on overhangs requires this.

Total time: 35-45 min"""

LIFT_D = """LOWER POWER + FOOT/STABILITY - Light, plyometric, prevention
Goal: Plyometric power for running economy + foot/calf injury prevention. KEEP THIS LIGHT.
You did your heavy lower work on Wed; this is pure quality movement, not loading.

{phase_desc}

WARM UP (5 min):
  - Easy jog 5 min OR jump rope
  - Ankle CARs x 10 each direction
  - Calf stretch + Soleus stretch (knee-bent) 30s each
  - A-skips x 20m, B-skips x 20m

MAIN MOVEMENT (POWER):
1. POGO HOPS (low, springy): 3x{pogo}
   - Stay on the ball of foot, minimal ground contact
   - Building tendon stiffness = running economy

2. {plyo_main}

3. SINGLE-LEG BOUNDING (controlled): {bound_sets}x10 EACH (ONLY if form is clean - skip if fatigued)

PREVENTION & STABILITY:
4. SINGLE-LEG GLUTE BRIDGE: 3x10 EACH leg
   - 1-second pause at top
   - Often-neglected glute med work

5. TIBIALIS RAISE (back to wall, lift toes up): 3x15 EACH leg
   - The anterior shin muscle prevents shin splints. Critical for high-mileage weeks.

6. SINGLE-LEG CALF RAISE (slow, off step): 3x12 EACH
   - 3-sec eccentric. Achilles resilience.

7. TOE YOGA / SHORT FOOT: 2-3 minutes
   - Activate intrinsic foot muscles. Spread toes, press big toe down without curling
   - Foot strength = injury prevention (plantar fasciitis, etc.)

8. HIP 90/90 mobility: 2-3 min total
   - Hip rotational mobility - both running and climbing demand this

9. COUCH STRETCH: 90s each side
   - Hip flexor length. You sit a lot.

Total time: 30-40 min"""


# Phase parameters: (sets_main, reps_main, sets_acc, reps_unilateral, reps_glute, reps_calf,
#                   reps_pullup, reps_row, reps_acc, hangboard, reps_push, reps_ohp,
#                   plank_time, hollow_time, pogo, plyo_main, bound_sets)
PHASE_PARAMS = {
    "foundation": {
        "sets_main": 3, "reps_main": "8-10", "sets_acc": 3, "reps_unilateral": "8-10",
        "reps_glute": "10-12", "reps_calf": "10-12", "reps_pullup": "5-8 (unweighted, full ROM)",
        "reps_row": "10 (moderate weight)", "reps_acc": "10-12",
        "hangboard": "5 sets max hang 7s on 20mm edge (start with bodyweight only)",
        "reps_push": "8-12", "reps_ohp": "8-10", "plank_time": "45s", "hollow_time": "20-30s",
        "pogo": "30s", "plyo_main": "BOX JUMP DOWN + STICK landing: 2x6 (low box, focus on quiet absorption)",
        "bound_sets": 2,
    },
    "build": {
        "sets_main": 4, "reps_main": "6-8", "sets_acc": 3, "reps_unilateral": "6-8",
        "reps_glute": "8-10", "reps_calf": "10-12", "reps_pullup": "4-6 (add weight if 6+ unweighted is easy)",
        "reps_row": "8 (heavier)", "reps_acc": "10",
        "hangboard": "6 sets max hang 8s on 20mm edge (add weight 5lb if last week's hangs felt easy)",
        "reps_push": "8-10 (decline or weighted)", "reps_ohp": "6-8 (heavier)",
        "plank_time": "60s", "hollow_time": "30-40s",
        "pogo": "30s", "plyo_main": "BROAD JUMP: 3x5 (max distance, full recovery between)",
        "bound_sets": 2,
    },
    "maintain": {
        "sets_main": 3, "reps_main": "6-8", "sets_acc": 3, "reps_unilateral": "6-8",
        "reps_glute": "8-10", "reps_calf": "10-12", "reps_pullup": "4-6", "reps_row": "8",
        "reps_acc": "10", "hangboard": "5 sets max hang 7s on 20mm edge",
        "reps_push": "8-10", "reps_ohp": "6-8", "plank_time": "60s", "hollow_time": "30s",
        "pogo": "30s", "plyo_main": "BOX JUMP UP: 3x5 (moderate height, soft landing)",
        "bound_sets": 2,
    },
    "peak": {
        "sets_main": 4, "reps_main": "5-6", "sets_acc": 3, "reps_unilateral": "5-6 (heavier)",
        "reps_glute": "6-8 (heavy)", "reps_calf": "10-12", "reps_pullup": "3-5 (weighted)",
        "reps_row": "6-8 (heavy)", "reps_acc": "8-10",
        "hangboard": "6 sets max hang 10s on 20mm edge (push the weight if form holds)",
        "reps_push": "6-8 (weighted/decline)", "reps_ohp": "5-6 (heavy)",
        "plank_time": "60s", "hollow_time": "40s",
        "pogo": "30s", "plyo_main": "DEPTH JUMP (24-inch box): 3x5 (eccentric absorption + reactive jump - DOWNHILL PREP)",
        "bound_sets": 3,
    },
    "light": {
        "sets_main": 2, "reps_main": "8 (light)", "sets_acc": 2, "reps_unilateral": "8 (light)",
        "reps_glute": "10 (light)", "reps_calf": "10", "reps_pullup": "3-5 (well below max)",
        "reps_row": "8 (moderate)", "reps_acc": "10",
        "hangboard": "3 sets max hang 5s on 20mm edge (just to maintain feel)",
        "reps_push": "8 (no failure)", "reps_ohp": "8 (light)",
        "plank_time": "30-45s", "hollow_time": "20s",
        "pogo": "20s", "plyo_main": "POGO HOPS only (skip box jumps this week)",
        "bound_sets": 0,
    },
    "mobility": {  # Race week
        "sets_main": 0, "reps_main": "0", "sets_acc": 0, "reps_unilateral": "0",
        "reps_glute": "0", "reps_calf": "0", "reps_pullup": "0", "reps_row": "0",
        "reps_acc": "0", "hangboard": "skip",
        "reps_push": "0", "reps_ohp": "0", "plank_time": "0", "hollow_time": "0",
        "pogo": "0", "plyo_main": "0", "bound_sets": 0,
    },
}


def render_lift(template, phase):
    if phase == "mobility":
        return ("MOBILITY ONLY (race week):\n"
                "- 5 min easy bike\n"
                "- World's greatest stretch x 5 each\n"
                "- Hip 90/90 mobility 3 min\n"
                "- Couch stretch 90s each\n"
                "- Glute bridge x 15\n"
                "- Band pull-apart x 20\n"
                "- Cat-cow x 10\n"
                "- Easy hang from bar 30s x 2\n"
                "Total: 15-20 min. NO loaded lifting.")
    params = dict(PHASE_PARAMS[phase])
    params["phase_desc"] = PHASE_DESC[phase]
    return template.format(**params)


# ============================================================
# WEEK -> PHASE MAPPING for strength
# ============================================================
WEEK_PHASE = {
    1: "foundation", 2: "foundation", 3: "foundation", 4: "light",  # W4 cutback
    5: "build", 6: "build", 7: "build", 8: "light",  # W8 cutback
    9: "maintain", 10: "mobility",  # W10 = Bryce race week
    11: "light",  # post-race recovery
    12: "maintain", 13: "maintain", 14: "maintain",
    15: "light",  # cutback before peak block
    16: "peak", 17: "peak",
    18: "light",  # cutback
    19: "peak",  # peak long run week
    20: "maintain",  # 22mi LR week
    21: "light",  # taper
    22: "mobility",  # race week
}


def lift_workout(lift_id, lift_letter, name, sport_label, template, phase, day_id):
    return {
        "id": day_id,
        "sport": "strength",
        "type": "strength",
        "name": f"{lift_letter}: {name}",
        "description": f"Lift {lift_letter} - {sport_label}. Phase: {phase}.",
        "durationMinutes": 50 if phase != "mobility" else 20,
        "primaryZone": f"Strength - {phase} block",
        "humanReadable": render_lift(template, phase),
        "completed": False,
    }


# ============================================================
# MAIN
# ============================================================

def main():
    plan = json.loads(INPUT.read_text())

    # Update meta
    plan["meta"]["updatedAt"] = "2026-04-30T12:00:00Z"
    plan["meta"]["event"] = "St. George Marathon (A-Race) + Bryce Canyon Half + 4-Day Strength"

    # Add strength program section
    plan["strengthProgram"] = {
        "philosophy": "Climbing-first, running-injury-prevention second, aesthetic muscle is not a goal. Pulling-dominant for climbing performance, posterior chain + eccentric quad for running and St. George downhill, antagonist work to keep shoulders/elbows healthy under climbing volume.",
        "weeklyStructure": {
            "Mon": "Lift B - Upper Pull (climbing-focused)",
            "Tue": "AM Quality Run only (no lift)",
            "Wed": "AM Easy Run + PM Lift A - Lower Heavy",
            "Thu": "AM Easy/Med Run + PM Lift C - Upper Push + Core",
            "Fri": "Climb or rest (no lift)",
            "Sat": "AM Long Run only (no lift)",
            "Sun": "AM Climb + PM Lift D - Lower Power/Foot (light)",
        },
        "intensityProgression": {
            "foundation_W1-3": "3x8-12, RPE 6-7 (form first)",
            "build_W5-7": "4x6-8, RPE 7-8 (load up)",
            "maintain_W9,12-14,20": "3x6-8, RPE 7 (hold gains)",
            "peak_W16-17,19": "4x5-6, RPE 8 + plyo (max strength + downhill prep)",
            "light/cutback": "2x8, RPE 5-6 (deload weeks)",
            "race_weeks_W10,W22": "Mobility only - NO loaded lifting",
        },
        "rules": [
            "Lift A (Lower Heavy) is on WED to leave 72 hours before Sat long run",
            "Lift B (Upper Pull) is on MON because pulling doesn't fatigue legs",
            "Lift C (Upper Push) is on THU because no leg fatigue interferes with Sat long run",
            "Lift D (Lower Power) is on SUN, kept LIGHT, 48 hours before next Tue quality run",
            "If something has to give, drop Lift D (Sun) first, then Lift C (Thu)",
            "Always do strength AFTER running on the same day, separated by 4-6 hours minimum",
            "Skip all lifting in the 5 days before a race (W10 from Tue, W22 from Tue)",
        ],
    }

    # Update phases descriptions to mention strength
    for phase in plan["phases"]:
        phase["strengthFocus"] = {
            "Re-Base": "Foundation: master form on all 4 lifts, build base strength",
            "Half Marathon Build": "Build: increase load on compounds, add plyometrics",
            "Half Marathon Peak & Race": "W9 maintain, W10 race week mobility only",
            "Recovery & Reset": "Light only - 2x8 RPE 5-6",
            "Marathon Base": "Maintain: hold strength gains while volume rebuilds",
            "Marathon Build": "Peak strength block: 4x5-6 RPE 8, depth jumps for downhill prep",
            "Marathon Peak": "W20 maintain, W21 deload",
            "Marathon Taper & Race": "Mobility only - NO loaded lifting",
        }.get(phase["name"], "")

    # Update weeks - add lift workouts and remove old strength references
    for week in plan["weeks"]:
        wn = week["weekNumber"]
        phase = WEEK_PHASE[wn]
        days_by_dow = {d["dayOfWeek"]: d for d in week["days"]}

        # MONDAY: Add Lift B (Upper Pull) - except race week W22
        # In race week W22, Mon stays as full rest
        mon = days_by_dow.get("Monday")
        if mon:
            # Remove rest workout if we're adding lift, or keep rest if mobility week
            if phase == "mobility":
                # Mon stays rest in race week
                pass
            else:
                # Replace/add Mon Pull workout
                new_workouts = []
                # Keep any non-rest workouts (none expected)
                for w in mon["workouts"]:
                    if w["sport"] not in ("rest",):
                        new_workouts.append(w)
                new_workouts.append(lift_workout(
                    f"w{wn}-mon-lift", "B", "Upper Pull (Climbing)", "Climbing-focused pulling",
                    LIFT_B, phase, f"w{wn}-mon-lift"
                ))
                mon["workouts"] = new_workouts

        # WEDNESDAY: Add Lift A (Lower Heavy) - skip in race weeks
        wed = days_by_dow.get("Wednesday")
        if wed and phase != "mobility":
            # Remove old lift placeholder, keep run
            new_workouts = [w for w in wed["workouts"] if w["sport"] not in ("strength",)]
            new_workouts.append(lift_workout(
                f"w{wn}-wed-lift", "A", "Lower Body Heavy", "Posterior chain + eccentric quad",
                LIFT_A, phase, f"w{wn}-wed-lift"
            ))
            wed["workouts"] = new_workouts
        elif wed and phase == "mobility":
            # Race week - drop the lift entirely (it was already in W22 plan as no lift)
            wed["workouts"] = [w for w in wed["workouts"] if w["sport"] not in ("strength",)]

        # THURSDAY: Add Lift C (Upper Push + Core) - skip in race weeks
        thu = days_by_dow.get("Thursday")
        if thu and phase != "mobility":
            new_workouts = [w for w in thu["workouts"] if w["sport"] not in ("strength",)]
            new_workouts.append(lift_workout(
                f"w{wn}-thu-lift", "C", "Upper Push + Core", "Antagonist + stability",
                LIFT_C, phase, f"w{wn}-thu-lift"
            ))
            thu["workouts"] = new_workouts

        # SUNDAY: Add Lift D (Lower Power) - skip in race weeks and recovery W11 if very fatigued
        sun = days_by_dow.get("Sunday")
        if sun and phase not in ("mobility",):
            new_workouts = [w for w in sun["workouts"] if w["sport"] not in ("strength",)]
            new_workouts.append(lift_workout(
                f"w{wn}-sun-lift", "D", "Lower Power + Foot", "Plyometric + injury prevention",
                LIFT_D, phase, f"w{wn}-sun-lift"
            ))
            sun["workouts"] = new_workouts

        # Update week summary - add strength sessions
        sessions_added = 4 if phase != "mobility" else 0
        if phase == "mobility":
            # Race weeks: no loaded lifting, mobility-only Mon mentioned via Mon rest
            sessions_added = 0
        if "summary" in week and "bySport" in week["summary"]:
            existing_strength = week["summary"]["bySport"].get("strength", {"sessions": 0, "hours": 0})
            week["summary"]["bySport"]["strength"] = {
                "sessions": sessions_added,
                "hours": round(sessions_added * 0.75, 2),  # ~45min average
                "notes": f"4 lifts/wk in {phase} phase" if sessions_added else "Race week - mobility only",
            }

    OUTPUT.write_text(json.dumps(plan, indent=2))
    print(f"Wrote {OUTPUT}")
    print(f"Total weeks: {len(plan['weeks'])}")
    print(f"Strength phase mapping: {len(WEEK_PHASE)} weeks mapped")


if __name__ == "__main__":
    main()
