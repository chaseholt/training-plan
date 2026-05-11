"""
Reshape the run schedule from Tue/Wed/Thu/Sat to Mon/Wed/Thu/Sat (runcoach-style).

New weekly structure:
  Mon: SPEED Run (AM) + Lift B - Upper Pull (PM)
  Tue: REST or optional light climb
  Wed: EASY Run (AM) + Lift A - Lower Heavy (PM)
  Thu: TEMPO Run (AM) + Lift C - Upper Push + Core (PM)
  Fri: Rest or climb
  Sat: LONG Run (AM only)
  Sun: Climb (AM) + Lift D - Lower Power (PM, light)

This script REPLACES the run workouts with phase-appropriate sessions and
preserves the existing lift workouts already on Mon/Wed/Thu/Sun.
"""

import json
from pathlib import Path
import copy

PLAN_PATH = Path("/sessions/laughing-inspiring-goldberg/mnt/outputs/chase-st-george-marathon-2026-10-03.json")


def run_workout(wn, day, name, run_type, duration, distance, zone, human_readable, completed=False):
    return {
        "id": f"w{wn}-{day.lower()}-run",
        "sport": "run",
        "type": run_type,
        "name": name,
        "description": name,
        "durationMinutes": duration,
        "distanceMiles": distance,
        "primaryZone": zone,
        "humanReadable": human_readable,
        "completed": completed,
    }


def rest_climb_optional(wn):
    return {
        "id": f"w{wn}-tue-rest",
        "sport": "rest",
        "type": "rest",
        "name": "Rest or Light Climb",
        "description": "Tuesday is your true recovery day. Optional easy climbing only.",
        "humanReadable": "REST DAY - or optional easy/technical climbing session (60 min, low intensity).\n\nThis is your hardest recovery day of the week (between Mon speed and Thu tempo). Use it wisely:\n- Sleep in if possible\n- If climbing: technical practice, easy slabs, ARC training (NOT projects or limit bouldering)\n- Mobility work, foam rolling, hip 90/90s are great\n- DO NOT add a run, even an easy one - your legs need this day",
        "completed": False,
    }


def rest_full(wn, day, note=""):
    return {
        "id": f"w{wn}-{day.lower()}-rest",
        "sport": "rest",
        "type": "rest",
        "name": "Rest Day",
        "description": note or "Full rest",
        "humanReadable": note or "Full rest",
        "completed": False,
    }


def climb_session(wn, day, duration, label, note):
    return {
        "id": f"w{wn}-{day.lower()}-climb",
        "sport": "cross",
        "type": "active recovery",
        "name": label,
        "description": label,
        "durationMinutes": duration,
        "humanReadable": note,
        "completed": False,
    }


# ============================================================
# WEEK-SPECIFIC RUN WORKOUTS
# ============================================================
# Each week: (mon, wed, thu, sat) run workouts
# Mon: Speed/quality (or easy in foundation)
# Wed: Easy
# Thu: Tempo (or easy in foundation)
# Sat: Long run

def build_runs():
    runs = {}

    # W1 - Foundation
    runs[1] = {
        "Mon": run_workout(1, "Mon", "Easy Run + Strides", "easy", 35, 3.5, "Z2",
            "30min easy @ 9:45-10:30/mi (Z2)\n+ 4 x 20s strides on flat road, full walk recovery\nStrides = relaxed, fast turnover - NOT all-out sprints"),
        "Wed": run_workout(1, "Wed", "Easy Run", "easy", 35, 3.5, "Z2",
            "Easy @ 9:45-10:30/mi, conversational pace\nKeep HR < 156"),
        "Thu": run_workout(1, "Thu", "Easy Run", "easy", 35, 3.5, "Z2",
            "30-35min easy @ 9:45-10:30/mi - pure aerobic"),
        "Sat": run_workout(1, "Sat", "Long Run - 6 miles", "long", 60, 6, "Z2",
            "6mi easy @ 10:00-10:30/mi\nWalk breaks fine if HR climbs above 160\nFuel: nothing needed for this distance, just hydrate"),
    }

    # W2 - Foundation
    runs[2] = {
        "Mon": run_workout(2, "Mon", "Easy Run + Strides", "easy", 40, 4, "Z2",
            "35min easy @ 9:45-10:30/mi\n+ 5 x 20s strides on flat road, walk recovery"),
        "Wed": run_workout(2, "Wed", "Easy Run", "easy", 40, 4, "Z2",
            "40min easy @ 9:45-10:30/mi"),
        "Thu": run_workout(2, "Thu", "Easy Run", "easy", 40, 4, "Z2",
            "35-40min easy - conversational"),
        "Sat": run_workout(2, "Sat", "Long Run - 7 miles", "long", 70, 7, "Z2",
            "7mi @ 9:45-10:30/mi\nLast mile can drift to 9:30 if feeling good\nHydrate; no fuel needed yet"),
    }

    # W3 - Foundation + Field Test (on Monday)
    runs[3] = {
        "Mon": run_workout(3, "Mon", "30-min Threshold Field Test", "test", 60, 6, "Z4-5a",
            "FIELD TEST - calibrate your zones\n\nWARM UP: 15min easy + 4x20s strides\nMAIN: Run 30min ALL-OUT sustainable pace (race effort - imagine you'd be racing for 60min)\n  - Find a flat, uninterrupted route\n  - Record AVG HR for the full 30min = your LTHR\n  - Avg pace ≈ threshold pace\nCOOL DOWN: 10min easy\n\nReport back the result and I can update zones if they're off from estimates (175 LTHR, 8:00/mi)."),
        "Wed": run_workout(3, "Wed", "Easy Recovery Run", "easy", 35, 3.5, "Z1-2",
            "35min very easy @ 10:00-10:30/mi - HR < 145\nRecovery from Mon test"),
        "Thu": run_workout(3, "Thu", "Easy Run", "easy", 45, 4.5, "Z2",
            "45min @ 9:45-10:15/mi"),
        "Sat": run_workout(3, "Sat", "Long Run - 8 miles", "long", 80, 8, "Z2",
            "8mi @ 9:45-10:30/mi\nFinal 1mi can drift to 9:15-9:30 if feeling smooth\nStart practicing fueling: take a gel at mile 5"),
    }

    # W4 - Foundation Cutback
    runs[4] = {
        "Mon": run_workout(4, "Mon", "Easy Run + Strides", "easy", 35, 3.5, "Z2",
            "30min easy + 4x20s strides - cutback week, keep it relaxed"),
        "Wed": run_workout(4, "Wed", "Easy Run", "easy", 35, 3.5, "Z2",
            "35min easy"),
        "Thu": rest_full(4, "Thu", "Full rest - cutback week"),
        "Sat": run_workout(4, "Sat", "Long Run - 6 miles (cutback)", "long", 60, 6, "Z2",
            "6mi easy @ 9:45-10:15/mi - this is recovery, don't push"),
    }

    # W5 - Half Build start
    runs[5] = {
        "Mon": run_workout(5, "Mon", "SPEED: 3 x 1mi @ Threshold", "intervals", 50, 5.5, "Z5a / 8:00-8:15/mi",
            "FIRST QUALITY SESSION - threshold work\n\nWARM UP: 1.5mi easy + 4x20s strides\nMAIN: 3 x 1mi @ 8:00-8:15/mi (threshold pace, HR ~175)\n  - 2:00 jog recovery between\nCOOL DOWN: 1mi easy\n\nFeel: \"comfortably hard\" - you could speak only a few words"),
        "Wed": run_workout(5, "Wed", "Easy Run", "easy", 40, 4, "Z2",
            "40min @ 9:45-10:15/mi"),
        "Thu": run_workout(5, "Thu", "Easy Run + Strides", "easy", 45, 4.5, "Z2",
            "40min easy + 5x20s strides at end\nThis is your recovery day between Mon intervals and Sat long run"),
        "Sat": run_workout(5, "Sat", "Long Run - 10 miles", "long", 100, 10, "Z2",
            "10mi @ 9:30-10:00/mi\nLast 2mi can drift to 9:15-9:30 if comfortable\nFUEL: gel at mile 4 and mile 8 - START gut training now\nHYDRATE: 4-6oz every 20-25min"),
    }

    # W6 - Half Build
    runs[6] = {
        "Mon": run_workout(6, "Mon", "SPEED: 4 x 1km @ VO2", "intervals", 55, 6, "Z5b / 7:30-7:40/mi",
            "VO2max intervals\n\nWARM UP: 1.5mi easy + 4x20s strides\nMAIN: 4 x 1km (~0.62mi) @ 7:30-7:40/mi\n  - 90s jog recovery between\nCOOL DOWN: 1mi easy\n\nLast 200m of each rep should be HARD - HR climbing into 180s"),
        "Wed": run_workout(6, "Wed", "Easy Run", "easy", 40, 4, "Z2",
            "40min easy"),
        "Thu": run_workout(6, "Thu", "TEMPO: 3 mile continuous", "tempo", 55, 6, "Z4-5a / 8:10-8:20/mi",
            "Sustained threshold work\n\nWARM UP: 1.5mi easy + 4x20s strides\nMAIN: 3mi continuous @ 8:10-8:20/mi (just under threshold)\n  - HR target: 168-175\n  - If HR rising past 178, ease off\nCOOL DOWN: 1.5mi easy\n\nNote: legs will be slightly tired from Wed PM lift - this is expected. Body adapts."),
        "Sat": run_workout(6, "Sat", "Long Run 11mi - 2mi @ HMP", "long", 110, 11, "Z2 + Z4",
            "11mi total\n  - Mi 1-7: easy @ 9:30-10:00/mi\n  - Mi 8-9: 2mi @ HMP (8:30-8:40/mi)\n  - Mi 10-11: easy cool-down\nFUEL: gel mi 4, mi 8\nThis introduces race pace under fatigue"),
    }

    # W7 - Half Build
    runs[7] = {
        "Mon": run_workout(7, "Mon", "SPEED: 5 x 1km @ VO2", "intervals", 60, 6.5, "Z5b / 7:30-7:40/mi",
            "VO2max + threshold development\n\nWARM UP: 1.5mi easy + 4x20s strides\nMAIN: 5 x 1km @ 7:30-7:40/mi\n  - 90s jog recovery\nCOOL DOWN: 1mi easy\n\nGoal: even splits or slight progression"),
        "Wed": run_workout(7, "Wed", "Easy Run", "easy", 45, 4.5, "Z2",
            "45min easy @ 9:45-10:15/mi"),
        "Thu": run_workout(7, "Thu", "TEMPO: 4 mile continuous", "tempo", 65, 7, "Z4-5a / 8:00-8:15/mi",
            "Extended threshold\n\nWARM UP: 1.5mi easy + 4x20s strides\nMAIN: 4mi continuous @ 8:00-8:15/mi (threshold)\n  - HR target: 170-178\nCOOL DOWN: 1.5mi easy"),
        "Sat": run_workout(7, "Sat", "Long Run - 13 miles (HM distance!)", "long", 130, 13, "Z2 + brief Z3-4",
            "13mi total - your first HM-distance run since rebuild!\n  - Mi 1-9: easy @ 9:30-9:50/mi\n  - Mi 10-12: gradual progression to 8:50/mi\n  - Mi 13: easy cool-down jog\nFUEL: gel mi 4, mi 8, mi 11\nThis is a confidence builder for Bryce"),
    }

    # W8 - Recovery
    runs[8] = {
        "Mon": run_workout(8, "Mon", "Easy Run + Strides", "easy", 40, 4, "Z2",
            "35min easy + 5x20s strides - light shake-out, cutback week"),
        "Wed": run_workout(8, "Wed", "Easy Run", "easy", 40, 4, "Z2",
            "40min easy"),
        "Thu": run_workout(8, "Thu", "Short TEMPO: 2mi @ HMP", "tempo", 45, 5, "Z4 / 8:30/mi",
            "Sharp intensity touch\n\nWARM UP: 1.5mi easy + 4x20s strides\nMAIN: 2mi @ 8:30/mi (HMP - feel sharp not strained)\nCOOL DOWN: 1.5mi easy"),
        "Sat": run_workout(8, "Sat", "Long Run - 9 miles (cutback)", "long", 90, 9, "Z2",
            "9mi easy @ 9:30-10:00/mi - cutback for recovery"),
    }

    # W9 - Half Peak
    runs[9] = {
        "Mon": run_workout(9, "Mon", "SPEED: 4 x 1mi @ HMP", "intervals", 60, 6.5, "Z4 / 8:30/mi",
            "Race-pace intervals - practice your goal race pace\n\nWARM UP: 1.5mi easy + 4x20s strides\nMAIN: 4 x 1mi @ 8:30/mi (Bryce goal pace)\n  - 90s jog between\n  - These should feel CONTROLLED at goal pace - if you're straining, your goal is too aggressive\nCOOL DOWN: 1mi easy"),
        "Wed": run_workout(9, "Wed", "Easy Run", "easy", 40, 4, "Z2",
            "40min easy"),
        "Thu": run_workout(9, "Thu", "TEMPO: 3mi @ HMP", "tempo", 55, 6, "Z4 / 8:30/mi",
            "Race-pace tempo\n\nWARM UP: 1.5mi easy + 4x20s strides\nMAIN: 3mi @ 8:30/mi (HMP - dress rehearsal pace)\nCOOL DOWN: 1.5mi easy"),
        "Sat": run_workout(9, "Sat", "Long Run 12mi - Final Pre-Race", "long", 120, 12, "Z2 + Z4 segment",
            "12mi total - last meaningful long run before Bryce\n  - Mi 1-8: easy @ 9:30-9:50/mi\n  - Mi 9-11: 3mi @ HMP (8:30/mi) - DRESS REHEARSAL\n  - Mi 12: easy\n\nPRACTICE YOUR RACE NUTRITION:\n  - Same breakfast you'll eat on race day\n  - Gel at mile 4, mile 8\n  - Same hydration plan"),
    }

    # W10 - Bryce Half Race Week (race Sat Jul 11)
    runs[10] = {
        "Mon": run_workout(10, "Mon", "Race-Pace Touch: 2 x 1mi @ HMP", "tempo", 45, 5, "Z4 / 8:30/mi",
            "Sharp legs, no fatigue\n\nWARM UP: 1.5mi easy + 4x20s strides\nMAIN: 2 x 1mi @ 8:30/mi (HMP)\n  - 2:00 jog recovery\nCOOL DOWN: 1.5mi easy\n\nShould feel CRISP - that's the goal of race week"),
        "Wed": run_workout(10, "Wed", "Easy Run", "easy", 30, 3, "Z2",
            "30min easy. NO LIFTING this week from here on."),
        "Thu": run_workout(10, "Thu", "Shake-out Run + Strides", "easy", 30, 3, "Z2",
            "25min easy + 4x20s strides\nFOCUS this week: sleep, hydration, carb-up Thurs/Fri, no climbing"),
        "Fri": run_workout(10, "Fri", "Pre-Race Shake-out", "easy", 20, 2, "Z1-2",
            "20min very easy + 4x20s strides\nTravel to Bryce. Carb-load dinner. Lay out race kit. Bed early."),
        "Sat": run_workout(10, "Sat", "🏁 RACE: Bryce Canyon Half Marathon", "race", 110, 13.1, "Z4 / 8:25-8:35/mi avg",
            "🏁 BRYCE CANYON HALF MARATHON 🏁\n\nGOAL: Sub-1:50 (8:23/mi avg) - course is net downhill ~1,000 ft\nBACKUP GOAL: Sub-1:55 (8:46/mi)\n\nPACING:\n  - Mi 1-3: 8:35-8:45 (CONTROLLED - it will feel TOO easy on the descent. Resist!)\n  - Mi 4-9: 8:25-8:35 (settle into rhythm)\n  - Mi 10-13.1: 8:15-8:25 (push the final 5K)\n\nNUTRITION:\n  - Pre-race breakfast 3hr before: 100g carbs (oatmeal + banana)\n  - 30min before: half gel + sip drink\n  - During: Gel at mi 4, mi 8 (carry 2)\n  - Water at every aid station\n\nQUAD MANAGEMENT (downhill):\n  - Slight forward lean from ankles\n  - High cadence (180+), short stride\n  - Don't 'brake' - let gravity work but stay relaxed\n\nThis is your dress rehearsal for St. George downhill mechanics"),
    }

    # W11 - Post-race Recovery
    runs[11] = {
        "Mon": rest_full(11, "Mon", "Full rest - post-race recovery. Walk only."),
        "Wed": run_workout(11, "Wed", "First Run Back", "easy", 25, 2.5, "Z1-2",
            "25min very easy @ 10:00+/mi. If anything feels off, walk it in.\nFirst run after Bryce - listen to body."),
        "Thu": rest_full(11, "Thu", "Rest or light climb (technical only)"),
        "Sat": run_workout(11, "Sat", "Easy Long-ish Run - 7 miles", "long", 70, 7, "Z2",
            "7mi easy @ 9:45-10:15/mi\nNo intensity, just time on feet"),
    }

    # W12 - Marathon Base start
    runs[12] = {
        "Mon": run_workout(12, "Mon", "Easy Run + Strides", "easy", 45, 4.5, "Z2",
            "40min easy + 6x20s strides - re-introducing structure"),
        "Wed": run_workout(12, "Wed", "Easy Run", "easy", 45, 4.5, "Z2",
            "45min easy"),
        "Thu": run_workout(12, "Thu", "Medium-Long Run - 6 miles", "medium", 60, 6, "Z2",
            "6mi @ 9:30-10:00/mi - building aerobic durability mid-week\nNo tempo yet - just steady aerobic"),
        "Sat": run_workout(12, "Sat", "Long Run - 12 miles", "long", 120, 12, "Z2",
            "12mi @ 9:30-9:50/mi\nFUEL: gel mi 4, 8 - keep practicing race nutrition"),
    }

    # W13 - Marathon Base
    runs[13] = {
        "Mon": run_workout(13, "Mon", "SPEED: 4 x 1mi @ Threshold", "intervals", 60, 6.5, "Z5a / 8:00/mi",
            "Threshold development\n\nWARM UP: 1.5mi easy + 4x20s strides\nMAIN: 4 x 1mi @ 8:00/mi\n  - 90s jog recovery\nCOOL DOWN: 1mi easy"),
        "Wed": run_workout(13, "Wed", "Easy Run", "easy", 45, 4.5, "Z2",
            "45min easy"),
        "Thu": run_workout(13, "Thu", "TEMPO: 3mi @ MP", "tempo", 55, 6, "Z3 / 8:35/mi (MP)",
            "First marathon-pace work\n\nWARM UP: 1.5mi easy + 4x20s strides\nMAIN: 3mi @ 8:35/mi (St. George goal MP)\n  - HR target: 158-165\n  - Should feel COMFORTABLE - if it doesn't, MP is too aggressive\nCOOL DOWN: 1.5mi easy"),
        "Sat": run_workout(13, "Sat", "Long Run - 14 miles", "long", 140, 14, "Z2",
            "14mi @ 9:30-9:50/mi\nFUEL: gel mi 4, 8, 12\nFind a route with rolling/downhill sections - start practicing downhill mechanics"),
    }

    # W14 - Marathon Base cap
    runs[14] = {
        "Mon": run_workout(14, "Mon", "SPEED: 5 x 1km @ VO2", "intervals", 60, 6.5, "Z5b / 7:30-7:45/mi",
            "VO2max development\n\nWARM UP: 1.5mi easy + 4x20s strides\nMAIN: 5 x 1km @ 7:30-7:45/mi\n  - 90s jog recovery\nCOOL DOWN: 1mi easy"),
        "Wed": run_workout(14, "Wed", "Easy Run", "easy", 45, 4.5, "Z2",
            "45min easy"),
        "Thu": run_workout(14, "Thu", "Medium-Long w/ MP: 8mi (last 2mi @ MP)", "medium", 75, 8, "Z2 + Z3",
            "First MP work in the medium-long\n\n8mi total\n  - Mi 1-6: easy @ 9:30-9:45/mi\n  - Mi 7-8: 2mi @ 8:35/mi (MP)\n\nThis teaches running MP on tired legs"),
        "Sat": run_workout(14, "Sat", "Long Run - 16 miles", "long", 160, 16, "Z2",
            "16mi @ 9:30-9:50/mi - find a course with descents\nFUEL: gel mi 4, 8, 12 + sips of sports drink\nTAKE 1 GEL with caffeine in second half - test caffeine response\nPRACTICE: race-morning breakfast routine"),
    }

    # W15 - Recovery before peak block
    runs[15] = {
        "Mon": run_workout(15, "Mon", "TEMPO Short: 3mi @ MP", "tempo", 55, 6, "Z3 / 8:35/mi",
            "Maintain intensity touch\n\nWARM UP: 1.5mi easy + 4x20s strides\nMAIN: 3mi @ 8:30-8:35/mi (MP)\nCOOL DOWN: 1.5mi easy"),
        "Wed": run_workout(15, "Wed", "Easy Run", "easy", 40, 4, "Z2",
            "40min easy - cutback week, keep it relaxed"),
        "Thu": run_workout(15, "Thu", "Easy Run + Strides", "easy", 45, 4.5, "Z2",
            "40min easy + 6x20s strides"),
        "Sat": run_workout(15, "Sat", "Long Run - 12 miles (cutback)", "long", 120, 12, "Z2",
            "12mi easy @ 9:30-9:50/mi - cutback for recovery"),
    }

    # W16 - Marathon Build start
    runs[16] = {
        "Mon": run_workout(16, "Mon", "SPEED: 5 x 1km @ VO2", "intervals", 65, 7, "Z5b / 7:30-7:45/mi",
            "Aerobic capacity development\n\nWARM UP: 2mi easy + 4x20s strides\nMAIN: 5 x 1km @ 7:30-7:45/mi\n  - 400m (~2:30) jog recovery between\nCOOL DOWN: 1mi easy\n\nFeel: HARD - HR ~180-185 by the last 200m of each rep"),
        "Wed": run_workout(16, "Wed", "Easy Run", "easy", 45, 4.5, "Z2",
            "45min easy @ 9:45-10:15/mi"),
        "Thu": run_workout(16, "Thu", "Medium-Long w/ MP: 8mi (3mi @ MP)", "medium", 75, 8, "Z2 + Z3",
            "MP fitness on moderate fatigue\n\n8mi total\n  - Mi 1-4: easy @ 9:30-9:45/mi\n  - Mi 5-7: 3mi @ 8:35/mi (MP)\n  - Mi 8: easy cool"),
        "Sat": run_workout(16, "Sat", "Long Run - 18 miles", "long", 180, 18, "Z2",
            "18mi @ 9:30-9:50/mi - first 18-miler of marathon block\nFUEL: gel every 4 miles (mi 4, 8, 12, 16) + sports drink throughout\nROUTE: prioritize courses with sustained downhill segments to train quad eccentric loading\nThis is St. George prep - your quads must learn to handle descent"),
    }

    # W17 - Marathon Build, heaviest week
    runs[17] = {
        "Mon": run_workout(17, "Mon", "SPEED: 5 x 1mi @ Threshold", "intervals", 70, 7.5, "Z5a / 8:00/mi",
            "Threshold development\n\nWARM UP: 2mi easy + 4x20s strides\nMAIN: 5 x 1mi @ 8:00/mi (threshold)\n  - 90s jog recovery\nCOOL DOWN: 1mi easy"),
        "Wed": run_workout(17, "Wed", "Easy Run", "easy", 50, 5, "Z2",
            "50min easy"),
        "Thu": run_workout(17, "Thu", "TEMPO: 5mi continuous", "tempo", 75, 8, "Z4 / 8:10-8:20/mi",
            "Sustained threshold work\n\nWARM UP: 2mi easy + 4x20s strides\nMAIN: 5mi continuous @ 8:10-8:20/mi (just under threshold)\n  - HR ceiling: 175\nCOOL DOWN: 1mi easy"),
        "Sat": run_workout(17, "Sat", "Long Run - 20 miles", "long", 200, 20, "Z2",
            "20mi @ 9:30-9:50/mi - YOUR FIRST 20-MILER OF THIS BLOCK\nFUEL: gel every 4mi (mi 4, 8, 12, 16) + sports drink\nROUTE: include 3-4mi sustained descent if possible\n\nThis run builds glycogen capacity, mitochondrial density, and mental toughness"),
    }

    # W18 - Recovery mid-block
    runs[18] = {
        "Mon": run_workout(18, "Mon", "SPEED: 4 x 800m @ I pace", "intervals", 50, 5, "Z5b / 7:30-7:40/mi",
            "Maintain intensity touch\n\nWARM UP: 1.5mi easy + 4x20s strides\nMAIN: 4 x 800m @ 7:30-7:40/mi\n  - 400m jog recovery\nCOOL DOWN: 1mi easy"),
        "Wed": run_workout(18, "Wed", "Easy Run", "easy", 40, 4, "Z2",
            "40min easy - cutback week"),
        "Thu": run_workout(18, "Thu", "Easy Run + Strides", "easy", 45, 4.5, "Z2",
            "40min easy + 5x20s strides"),
        "Sat": run_workout(18, "Sat", "Long Run - 14 miles (cutback)", "long", 140, 14, "Z2",
            "14mi easy @ 9:30-9:50/mi"),
    }

    # W19 - PEAK WEEK
    runs[19] = {
        "Mon": run_workout(19, "Mon", "SPEED: 5 x 1mi @ Threshold", "intervals", 70, 8, "Z5a / 7:55-8:05/mi",
            "Threshold development - peak\n\nWARM UP: 2mi easy + 4x20s strides\nMAIN: 5 x 1mi @ 7:55-8:05/mi (threshold)\n  - 90s jog recovery\nCOOL DOWN: 1mi easy"),
        "Wed": run_workout(19, "Wed", "Easy Run", "easy", 50, 5, "Z2",
            "50min easy"),
        "Thu": run_workout(19, "Thu", "Medium-Long w/ MP: 9mi (4mi @ MP)", "medium", 85, 9, "Z2 + Z3",
            "Heavy MP work mid-week\n\n9mi total\n  - Mi 1-4: easy @ 9:30-9:45/mi\n  - Mi 5-8: 4mi @ 8:35/mi (MP)\n  - Mi 9: easy cool\n\nMP should feel STEADY. If it's straining, your goal pace needs review."),
        "Sat": run_workout(19, "Sat", "PEAK Long Run - 20mi w/ 6mi @ MP", "long", 200, 20, "Z2 + Z3",
            "20mi total - PEAK SESSION\n  - Mi 1-12: easy @ 9:30-9:45/mi\n  - Mi 13-18: 6mi @ 8:35/mi (MP - on tired legs)\n  - Mi 19-20: easy cool down\n\nFUEL: gel mi 4, 8, 12, 16, 18\nINCLUDE 1 caffeine gel in second half\nROUTE: must include sustained downhill\n\nThis workout is the single best predictor of race-day performance. Execute it well = you can run sub-3:45."),
    }

    # W20 - Marathon Peak - final 22mi dress rehearsal
    runs[20] = {
        "Mon": run_workout(20, "Mon", "TEMPO: 4mi @ Threshold", "tempo", 65, 7, "Z4-5a / 8:00-8:15/mi",
            "Sharp threshold touch\n\nWARM UP: 1.5mi easy + 4x20s strides\nMAIN: 4mi continuous @ 8:00-8:15/mi\nCOOL DOWN: 1mi easy"),
        "Wed": run_workout(20, "Wed", "Easy Run", "easy", 50, 5, "Z2",
            "50min easy"),
        "Thu": run_workout(20, "Thu", "Easy Run + Strides", "easy", 50, 5, "Z2",
            "45min easy + 6x20s strides\nKeep this CONTROLLED - big day Saturday"),
        "Sat": run_workout(20, "Sat", "FINAL Long Run - 22mi w/ 8mi @ MP", "long", 220, 22, "Z2 + Z3",
            "22mi - FINAL DRESS REHEARSAL\n  - Mi 1-12: easy @ 9:30-9:45/mi\n  - Mi 13-20: 8mi @ 8:35/mi (MP)\n  - Mi 21-22: easy cool down\n\nFUEL EXACTLY as you'll fuel on race day:\n  - Pre-run breakfast = race-morning breakfast\n  - Gel mi 4, 8, 12, 16, 20 (+ caffeine in second half)\n  - Sports drink throughout\n\nWear race shoes & race kit. Note any blisters/chafing.\n\nIf you can hold MP for 8mi after 12mi easy, you can run a 26.2mi marathon at MP with downhill assist. This is THE confidence builder."),
    }

    # W21 - Taper Week 1
    runs[21] = {
        "Mon": run_workout(21, "Mon", "SPEED: 3 x 1mi @ Threshold", "intervals", 55, 6, "Z5a / 8:00/mi",
            "Maintain threshold sharpness\n\nWARM UP: 1.5mi easy + 4x20s strides\nMAIN: 3 x 1mi @ 8:00/mi\n  - 90s jog recovery\nCOOL DOWN: 1mi easy\n\nReps should feel CONTROLLED"),
        "Wed": run_workout(21, "Wed", "Easy Run", "easy", 40, 4, "Z2",
            "40min easy"),
        "Thu": run_workout(21, "Thu", "TEMPO: 3mi @ MP Touch", "tempo", 55, 6, "Z3 / 8:35/mi",
            "Race-pace feel\n\nWARM UP: 1.5mi easy + 4x20s strides\nMAIN: 3mi @ 8:35/mi (MP)\n  - Should feel CRISP and EASY\nCOOL DOWN: 1.5mi easy"),
        "Sat": run_workout(21, "Sat", "Long Run - 14 miles", "long", 140, 14, "Z2",
            "14mi @ 9:30-9:45/mi - feels short after recent volume\nLast significant long run before race"),
    }

    # W22 - RACE WEEK
    runs[22] = {
        "Mon": run_workout(22, "Mon", "Race-Pace Touch: 2 x 1mi @ MP", "tempo", 45, 5, "Z3 / 8:35/mi",
            "Sharpening, no fatigue\n\nWARM UP: 1.5mi easy + 4x20s strides\nMAIN: 2 x 1mi @ 8:35/mi (MP)\n  - 2:00 jog recovery\nCOOL DOWN: 1.5mi easy\n\nShould feel EFFORTLESS. That's what we want."),
        "Wed": run_workout(22, "Wed", "Easy Run", "easy", 30, 3, "Z2",
            "30min easy. NO LIFTING this week."),
        "Thu": run_workout(22, "Thu", "Shake-out + Strides", "easy", 25, 2.5, "Z2",
            "20min easy + 4x20s strides\nFOCUS: Sleep, hydration, electrolytes. Begin carb-loading: 8-10g carbs/kg body weight today + tomorrow"),
        "Fri": run_workout(22, "Fri", "Pre-Race Shake-out", "easy", 20, 2, "Z1-2",
            "20min very easy + 4x20s strides\n\nRACE DAY MINUS 1:\n  - Travel to Pine Valley / St. George area\n  - Heavy carb dinner (pasta, rice, bread - low fiber, low fat)\n  - Lay out race kit, pin bib, prepare gels\n  - Drink water with electrolytes throughout day\n  - In bed by 9pm; alarm set EARLY"),
        "Sat": run_workout(22, "Sat", "🏁 ST. GEORGE MARATHON 🏁", "race", 225, 26.2, "Z3 / 8:35/mi avg",
            "🏁 ST. GEORGE MARATHON - YOUR A-RACE 🏁\n\nGOAL TIERS:\n  A: Sub-3:45 (8:35/mi) - target goal\n  B: Sub-3:55 (8:58/mi) - solid PR\n  C: Sub-4:06 (9:23/mi) - any PR over Big Sur\n\nRACE MORNING:\n  - 4:00 AM: Wake up. Coffee, water, light breakfast (3hr before start)\n    - 100-150g carbs (oatmeal + banana + bagel + honey)\n  - 5:00 AM: Bus to start at Pine Valley (5,200ft elevation, COLD - bring throwaway clothes)\n  - 6:30 AM: Last bathroom, last sip of water\n  - 6:45 AM: Race kit on, half gel + 8oz water\n  - 7:00 AM: GUN\n\nPACING - KEY TO ST. GEORGE SUCCESS:\n  - Mi 1-5 (downhill from Pine Valley): 8:50-9:05 - GO SLOWER THAN GOAL. The descent is steep & runnable. Holding back here saves your quads for mile 18+\n  - Mi 6-8 (Veyo Hill - the only major climb): power hike if needed, HR <175. Don't go in the red here.\n  - Mi 9-13 (rolling, mostly down): settle into 8:30-8:40\n  - Mi 14-19 (sustained gentle descent): 8:25-8:35 - this is where you make time\n  - Mi 20-26.2 (mostly flat into St. George): 8:30-8:45 - HOLD FORM, this is where everyone falls apart. You won't, because your quads are intact from holding back early.\n\nQUAD MANAGEMENT (the difference between 3:45 and 4:30):\n  - Slight forward lean from ankles (not waist)\n  - Quick cadence 180+, short stride\n  - Don't \"brake\" - let gravity pull, stay relaxed\n  - If quads start to scream by mi 18, you went too fast early\n\nFUEL/HYDRATION:\n  - Gel every 4 miles (mi 4, 8, 12, 16, 20, 24)\n  - At least 2 caffeine gels (mi 16 and mi 20)\n  - Sports drink at every aid station (~every 1.5mi)\n  - Total target: 60-90g carbs/hr\n\nMENTAL CHECKPOINTS:\n  - Mi 5: \"How easy am I going?\" - it should feel TOO easy\n  - Mi 13: \"Halfway. Do I feel fresh?\" - if yes, hold pace\n  - Mi 18: \"How are the quads?\" - if good, push to MP. If sore, hold conservative\n  - Mi 22: \"4 miles to go. Now I race.\"\n\nYOU TRAINED FOR THIS. Trust the plan. Trust your fitness. Run YOUR race."),
    }

    return runs


def main():
    plan = json.loads(PLAN_PATH.read_text())
    runs_by_week = build_runs()

    # Helper to extract existing lifts and other workouts
    for week in plan["weeks"]:
        wn = week["weekNumber"]
        existing_days = {d["dayOfWeek"]: d for d in week["days"]}

        # Get existing lifts (already on Mon, Wed, Thu, Sun by day)
        existing_lifts = {}
        for dow in ["Monday", "Wednesday", "Thursday", "Sunday"]:
            if dow in existing_days:
                for w in existing_days[dow]["workouts"]:
                    if w["sport"] == "strength":
                        existing_lifts[dow] = w
                        break

        # Get existing Sun climb and Fri rest/climb
        sun_climb = None
        for w in existing_days.get("Sunday", {"workouts": []})["workouts"]:
            if w["sport"] == "cross":
                sun_climb = w
                break
        fri_workout = None
        if "Friday" in existing_days:
            fri_workout = existing_days["Friday"]["workouts"][0] if existing_days["Friday"]["workouts"] else None

        # Build new days array
        new_days = []
        new_runs = runs_by_week[wn]

        # MONDAY - new speed run + existing lift B (if present)
        mon_workouts = [new_runs["Mon"]]
        if "Monday" in existing_lifts:
            mon_workouts.append(existing_lifts["Monday"])
        # Handle case where Mon was rest (W11)
        if isinstance(new_runs["Mon"], dict) and new_runs["Mon"].get("sport") == "rest":
            mon_workouts = [new_runs["Mon"]]  # Just rest, no lift on race recovery
        new_days.append({"date": existing_days["Monday"]["date"], "dayOfWeek": "Monday", "workouts": mon_workouts})

        # TUESDAY - rest or light climb
        new_days.append({"date": existing_days["Tuesday"]["date"], "dayOfWeek": "Tuesday", "workouts": [rest_climb_optional(wn)]})

        # WEDNESDAY - easy run + lift A
        wed_workouts = [new_runs["Wed"]]
        if "Wednesday" in existing_lifts:
            wed_workouts.append(existing_lifts["Wednesday"])
        new_days.append({"date": existing_days["Wednesday"]["date"], "dayOfWeek": "Wednesday", "workouts": wed_workouts})

        # THURSDAY - tempo run + lift C
        thu_workouts = [new_runs["Thu"]]
        if "Thursday" in existing_lifts:
            thu_workouts.append(existing_lifts["Thursday"])
        new_days.append({"date": existing_days["Thursday"]["date"], "dayOfWeek": "Thursday", "workouts": thu_workouts})

        # FRIDAY - existing rest/climb, plus optional Friday run (W10, W22 race weeks)
        if "Fri" in new_runs:
            fri_workouts = [new_runs["Fri"]]
        else:
            fri_workouts = [fri_workout] if fri_workout else [rest_full(wn, "Fri", "Rest or light climb")]
        new_days.append({"date": existing_days["Friday"]["date"], "dayOfWeek": "Friday", "workouts": fri_workouts})

        # SATURDAY - long run / race
        new_days.append({"date": existing_days["Saturday"]["date"], "dayOfWeek": "Saturday", "workouts": [new_runs["Sat"]]})

        # SUNDAY - climb + lift D
        sun_workouts = []
        if sun_climb:
            sun_workouts.append(sun_climb)
        if "Sunday" in existing_lifts:
            sun_workouts.append(existing_lifts["Sunday"])
        if not sun_workouts:
            sun_workouts = [rest_full(wn, "Sun")]
        new_days.append({"date": existing_days["Sunday"]["date"], "dayOfWeek": "Sunday", "workouts": sun_workouts})

        week["days"] = new_days

        # Update week summary
        run_sessions = sum(1 for d in new_days for w in d["workouts"] if w["sport"] == "run")
        strength_sessions = sum(1 for d in new_days for w in d["workouts"] if w["sport"] == "strength")
        total_miles = sum(w.get("distanceMiles", 0) for d in new_days for w in d["workouts"] if w["sport"] == "run")
        total_run_hours = sum(w.get("durationMinutes", 0) for d in new_days for w in d["workouts"] if w["sport"] == "run") / 60

        week["summary"]["bySport"]["run"] = {
            "sessions": run_sessions,
            "hours": round(total_run_hours, 1),
            "miles": round(total_miles, 1),
        }
        week["summary"]["bySport"]["strength"] = {
            "sessions": strength_sessions,
            "hours": round(strength_sessions * 0.75, 2),
        }

    # Update meta
    plan["meta"]["updatedAt"] = "2026-04-30T14:00:00Z"
    plan["meta"]["scheduleNote"] = "Mon/Wed/Thu/Sat run schedule (Mon=Speed, Wed=Easy, Thu=Tempo, Sat=Long)"

    # Update strengthProgram weekly structure
    plan["strengthProgram"]["weeklyStructure"] = {
        "Mon": "AM SPEED Run + PM Lift B (Upper Pull - climbing focus)",
        "Tue": "Rest or light climb (true recovery day)",
        "Wed": "AM Easy Run + PM Lift A (Lower Heavy - posterior chain)",
        "Thu": "AM TEMPO Run + PM Lift C (Upper Push + Core)",
        "Fri": "Rest or climb",
        "Sat": "AM LONG Run (no lift)",
        "Sun": "AM Climb (moderate) + PM Lift D (Lower Power - light)",
    }
    plan["strengthProgram"]["scheduleNotes"] = [
        "Mon speed run + Mon PM upper pull lift = climbing-focused upper work on your hardest leg day",
        "Tue is a TRUE recovery day - rest or technical/easy climbing only",
        "Wed Lower Heavy lift comes before Thu Tempo - legs will feel mildly tired Thu morning. This is by design and adapts within 2-3 weeks. If Thu tempos feel impossible to hit, swap Lift A to Tue PM.",
        "Thu Tempo + Sat Long Run = 1 day rest (Fri). Honor the Fri rest day - no leg lifting Friday.",
        "Sun light lower power lift is 48 hours before Mon speed - plenty of recovery",
    ]

    PLAN_PATH.write_text(json.dumps(plan, indent=2))
    print(f"Wrote {PLAN_PATH}")
    print(f"Total weeks: {len(plan['weeks'])}")
    print("\nSample week (W7 - Half Build) days:")
    for d in plan["weeks"][6]["days"]:
        print(f"  {d['dayOfWeek']}:")
        for w in d["workouts"]:
            print(f"    - [{w['sport']}] {w['name']}")


if __name__ == "__main__":
    main()
