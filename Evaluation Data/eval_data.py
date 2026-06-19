"""Transcribed evaluation data (handwritten sheets -> structured).
Each cell: (result, grasp, notes) where result in {'P','F'} (pass/fail),
grasp in {'S','T',''} (Side/Top), notes = list of footnote numbers (ints) or
symbol strings ('O','*','**').  '' / None = not run / blank.

Cups:    WB=White Basic, O=Orange, Bk=Black, R=Red            (ID)
         Br=Brown, WC=White Ceramic, Gr=Gray, P=Purple        (OOD)
Machines:K=Keurig, Bk=Black, T=Teal, W=White                 (ID)
         R=Red, TS=Tastyle, Bl=Blue                          (OOD)
Bowls:   BL=Blue, LB=Light Blue, BK=Black                    (ID)
         P=Pink, TB=Tall light-blue, W=White                 (OOD)
"""

CUPS_ID  = ["WB", "O", "Bk", "R"]
CUPS_OOD = ["Br", "WC", "Gr", "P"]
MACH_ID  = ["K", "Bk", "T", "W"]
MACH_OOD = ["R", "TS", "Bl"]
BOWLS_ID = ["BL", "LB", "BK"]
BOWLS_OOD= ["P", "TB", "W"]

CUP_NAMES = {"WB":"White Basic","O":"Orange","Bk":"Black","R":"Red",
             "Br":"Brown","WC":"White Ceramic","Gr":"Gray","P":"Pink","Pu":"Purple",
             "TWC":"Tall White Ceramic"}
MACH_NAMES= {"K":"Keurig","Bk":"Black","T":"Teal","W":"White",
             "R":"Red","TS":"Tastyle","Bl":"Blue"}
BOWL_NAMES= {"BL":"Blue","LB":"Light Blue","BK":"Black",
             "P":"Pink","TB":"Tall (light blue)","W":"White"}

# Coffee-machine footnote legend — 150-size sheets (pages 5, 7, 13).
COFFEE_NOTES = {
    1: "Pushed machine back",
    2: "Tilted placement and contact on plate",
    3: "Took double time",
    4: "Pushed cup while trying to grasp",
    5: "Dropped cup on edge of platform",
    6: "Self collision",
    7: "Spilled cup",
    8: "Force-torque trigger",
    9: "Grasped inside cup",
    10: "Gripper hooked on handle",
    11: "Cannot lift mug",
    "O": "Completed but took > 1 min",
    "*": "Not fully in cup holder",
    "**": "Released while tilted",
}

# Coffee-machine footnote legend — 50/100-size sheets (pages 1, 2).
COFFEE_NOTES_50 = {
    1: "Spilled the cup",
    2: "Failed to grasp (hit cup, grasped air)",
    3: "Hit the coffee machine",
    4: "Good pose, high Z",
    5: "Wrong grasp",
    6: "Torque sensor error",
    7: "Moved machine back",
    8: "Handle hooked on gripper",
    9: "Balancing on edge",
    10: "Dropped cup elsewhere",
}

# Coffee-machine footnote legend — 100-size sheets (pages 3, 4).
COFFEE_NOTES_100 = {
    1: "Pushed machine back",
    2: "Tilted placement and contact on plate",
    3: "Took double time",
    4: "Pushed cup while trying to grasp",
    5: "Dropped cup on edge of platform",
    6: "Self collision",
    7: "Spilled cup",
    8: "Force-torque trigger",
    9: "Grasped inside cup",
    10: "Gripper hooked on handle",
    11: "Cannot grab handle",
    12: "Tried to grab entire cup",
}

# Pouring footnote legend (50/105/150-size sheets share this legend, now 1-21).
POUR_NOTES = {
    1: "Bad return cup to table",
    2: "Went in for second pour",
    3: "A bit off-center for pour",
    4: "Tipped bowl while returning cup",
    5: "Started pushing cup down & didn't move; likely F/T error",
    6: "Tapped bowl while placing down or pouring",
    7: "Picked up cup and stopped moving",
    8: "Tall bowl was pushed while attempting to pour",
    9: "Two partial pours -> completed",
    10: "Gripper opened while pour attempt",
    11: "Severely off center",
    12: "Tipped cup over while picking up cup",
    13: "Gripper hooked on handle",
    14: "Spilled out of bowl / spilled cup",
    15: "Can't place cup after done",
    16: "Didn't pick up cup",
    17: "Poured but didn't return cup properly",
    18: "F/T error",
    19: "Dripped cup in bowl",
    20: "Barely poured",
    21: "Picked up inside of cup",
    "STS": "Succeeded only after trying all three grasp attempts (side -> top -> side)",
}

# Pouring SAP-baseline footnote legend (page 4 — different model, own legend).
POUR_NOTES_SAP = {
    1: "Spilled cup",
    2: "F/T error",
    3: "Missed handle",
    4: "Self collision",
    5: "Tapped the bowl during pour",
    6: "Off-center pour",
    7: "Bad return",
    8: "Grabbed inside of cup",
    9: "Slightly moved cup",
    10: "Hooked on handle while grasping",
    11: "Barely poured",
}

def C(s):
    """Parse a compact cell code like 'F T 8' / 'P S' / 'F T 1,7' / '' .
    Format: <P|F> [grasp] [notes csv].  '-' = blank/not-run."""
    if s in ("", "-", None):
        return None
    parts = s.split()
    res = parts[0]
    grasp = ""
    notes = []
    if len(parts) >= 2 and parts[1] in ("S", "T"):
        grasp = parts[1]; rest = parts[2:]
    else:
        rest = parts[1:]
    for r in rest:
        for tok in r.split(","):
            tok = tok.strip()
            if tok.isdigit():
                notes.append(int(tok))
            elif tok:
                notes.append(tok)
    return (res, grasp, notes)

def grid(rows, cups, machs):
    """rows: dict machine -> list of cell-codes aligned to `cups`."""
    return {m: {c: C(rows[m][i]) for i, c in enumerate(cups)} for m in machs}

# ===========================================================================
# COFFEE — 1x1  X-ARM-VLA   (page 1)
# ===========================================================================
coffee_1x1_vla = {
    "id_id": grid({
        #        WB          O          Bk        R
        "K":  ["F T",     "F T 11",  "F T",    "F T 11"],
        "Bk": ["F S 8",   "F T 11",  "F T",    "F T 11"],
        "T":  ["F T 1,7", "F T",     "F T",    "F T 7"],
        "W":  ["F T 1,8", "F T 11",  "F T",    "F S 11"],
    }, CUPS_ID, MACH_ID),
    "id_od": grid({
        #        WB        O        Bk        R
        "R":  ["P T 1",  "F S",   "F S 11", "F S 7"],
        "TS": ["P S",    "F S",   "F T 11", "F T 6"],
        "Bl": ["P S",    "F S 5", "F T 11", "F T 7"],
    }, CUPS_ID, MACH_OOD),
    "od_id": grid({
        #        Br        WC       Gr       P
        "K":  ["F T 11", "P S",   "F T",   "F S 7,8"],
        "Bk": ["F S",    "F S",   "F T",   "F S"],
        "T":  ["F S",    "F T 7", "F S 11","F S 7"],
        "W":  ["F T",    "F T",   "F T",   "F S 10"],
    }, CUPS_OOD, MACH_ID),
    "od_od": grid({
        #        Br          WC       Gr       P
        "R":  ["F T 11",   "F S",   "F S 7", "F T 7,9"],
        "TS": ["F S",      "P S",   "F S",   "F T"],
        "Bl": ["P S 3,5",  "F T 7", "F S 11","F T 5,7"],
    }, CUPS_OOD, MACH_OOD),
}

# ===========================================================================
# COFFEE — 4x4  X-ARM-VLA   (page 4)  -- main working model
# ===========================================================================
coffee_4x4_vla = {
    "id_id": grid({
        #        WB         O         Bk        R
        "K":  ["P S",    "F S",    "P S",    "P T"],
        "Bk": ["P S",    "P S",    "F T",    "P S 1"],
        "T":  ["P T 1",  "P T 3",  "P T 1",  "F S"],
        "W":  ["P T 4",  "P T",    "P T 4",  "F T"],
    }, CUPS_ID, MACH_ID),
    "id_od": grid({
        #        WB         O         Bk          R
        "R":  ["P S",    "P T 1",  "P T 1,5",  "F S 6"],
        "TS": ["P S 4",  "F S",    "F S 7",    "F S"],
        "Bl": ["P S 1",  "P S 1",  "P T",      "P S 2"],
    }, CUPS_ID, MACH_OOD),
    "od_id": grid({
        #        Br           WC        Gr          P
        "K":  ["P S 2",     "P S",    "P S",      "P S"],
        "Bk": ["F T 8,9",   "P S",    "P S",      "F S"],
        "T":  ["P T 1,2,8", "F S 10", "F T 1,9",  "P S"],
        "W":  ["P S 2",     "F T 4",  "P T 2",    "F S 6"],
    }, CUPS_OOD, MACH_ID),
    "od_od": grid({
        #        Br           WC       Gr         P
        "R":  ["F S",       "F S",   "F T",     "P S"],
        "TS": ["P S 1",     "F S",   "P S 2",   "F S"],
        "Bl": ["F S 1,7,8", "F S 8", "P S 1",   "P S"],
    }, CUPS_OOD, MACH_OOD),
}

# ===========================================================================
# COFFEE — 1x1  X-ARM-VLA   50-size dataset   (page 1)
# Notes use COFFEE_NOTES_50 legend.  Small dataset: mostly failures.
# ===========================================================================
coffee_1x1_vla_50 = {
    "id_id": grid({
        #        WB         O         Bk        R
        "K":  ["P T",    "F T",    "F S",    "F T"],
        "Bk": ["F S 1",  "F T 2",  "F S 2",  "F S 2"],
        "T":  ["F T 2",  "F T 2",  "F S 2",  "F S 1"],
        "W":  ["F T 2",  "F S 2",  "F T 2",  "F T 3"],
    }, CUPS_ID, MACH_ID),
    "id_od": grid({
        #        WB         O         Bk        R
        "R":  ["F T 2",  "F T 2",  "F S 2",  "F T 2"],
        "TS": ["P T",    "F S 2",  "F S 4",  "F S 2"],
        "Bl": ["F T 5",  "F S 2",  "F S 4",  "F T 2"],
    }, CUPS_ID, MACH_OOD),
    "od_id": grid({
        #        Br         WC         Gr          P
        "K":  ["F T 2",  "P S",     "F T 2",    "P S"],
        "Bk": ["F T 2",  "F T 2",   "F T 2",    "F S 2"],
        "T":  ["F S 2",  "F S 2",   "F S 1,2",  "F T 10"],
        "W":  ["F S 1",  "P T 9",   "F T 2",    "F T 1"],
    }, CUPS_OOD, MACH_ID),
    "od_od": grid({
        #        Br         WC         Gr        P
        "R":  ["F S 2",  "P T",     "F T 2",  "F T 2"],
        "TS": ["F S 2",  "F S 2",   "F T 2",  "F S 5"],
        "Bl": ["F S 2",  "F S 6",   "F S 2",  "P T"],
    }, CUPS_OOD, MACH_OOD),
}

# ===========================================================================
# COFFEE — 4x4  X-ARM-VLA   50-size dataset   (page 2)
# Notes use COFFEE_NOTES_50 legend.
# ===========================================================================
coffee_4x4_vla_50 = {
    "id_id": grid({
        #        WB         O         Bk        R
        "K":  ["F S 2",  "F S 2",  "F S",    "P S"],
        "Bk": ["F S 2",  "F S 1",  "P S",    "F S"],
        "T":  ["P S",    "P S",    "F S 1",  "F S 1"],
        "W":  ["P S",    "P S",    "P T",    "F T 2"],
    }, CUPS_ID, MACH_ID),
    "id_od": grid({
        #        WB         O         Bk        R
        "R":  ["P S",    "P T",    "F S 2",  "P S"],
        "TS": ["F S 1",  "P S",    "P S",    "P S"],
        "Bl": ["F S 2",  "F S 1",  "P S",    "F S 2"],
    }, CUPS_ID, MACH_OOD),
    "od_id": grid({
        #        Br         WC         Gr        P
        "K":  ["F S",    "P S",     "F S 5",  "F S 6"],
        "Bk": ["F T 6",  "F S 2",   "F T 2",  "F S 1"],
        "T":  ["F T 2",  "F S 2",   "F S 2",  "F S 2"],
        "W":  ["F S 2",  "P S",     "F T 2",  "F T 1"],
    }, CUPS_OOD, MACH_ID),
    "od_od": grid({
        #        Br          WC          Gr         P
        "R":  ["P S 7",   "P S 7",    "F S 2",   "P S"],
        "TS": ["F S 2",   "F S 7,8",  "F T 2",   "F S 1,8"],
        "Bl": ["P S",     "F S 2,6",  "P T 7,9", "P S"],
    }, CUPS_OOD, MACH_OOD),
}

# ===========================================================================
# COFFEE — 1x1  X-ARM-VLA   100-size dataset   (page 3)
# Notes use COFFEE_NOTES_100 legend.  Mostly failures; one OOD-machine success.
# ===========================================================================
coffee_1x1_vla_100 = {
    "id_id": grid({
        #        WB           O           Bk          R
        "K":  ["F T 5",     "F S 10",   "F T 11",   "F T 11"],
        "Bk": ["F T 9",     "F S 11",   "F T 11",   "F S 11"],
        "T":  ["F T 1,5",   "F S 1,5",  "F T 9,11", "F T 7,9,11"],
        "W":  ["F T 7,8",   "P S",      "F S 11",   "F S 4,11"],
    }, CUPS_ID, MACH_ID),
    "id_od": grid({
        #        WB           O            Bk          R
        "R":  ["P T 1",     "F S 10,11", "F S 11",   "F S 11"],
        "TS": ["P S",       "F T 5",     "F T 11",   "F T 7,11"],
        "Bl": ["P S",       "F S 4,11",  "F S 11",   "F T 4"],
    }, CUPS_ID, MACH_OOD),
    "od_id": grid({
        #        Br           WC          Gr          P
        "K":  ["F T 4",     "F T 5",    "F T 11",   "F S 1,5,7"],
        "Bk": ["F S 11",    "F T 9",    "F S 9,11", "F T 7,9"],
        "T":  ["F S 11",    "F T 4",    "F T 11",   "F S 1,4,11"],
        "W":  ["F T 11",    "F S 12",   "F T 9,11", "F S 7,9"],
    }, CUPS_OOD, MACH_ID),
    "od_od": grid({
        #        Br           WC          Gr          P
        "R":  ["F S 4",     "P T",      "F S 11",   "F S 7,11"],
        "TS": ["F T 4",     "F S 11",   "F S 9,11", "P S"],
        "Bl": ["F S 9,11",  "P S",      "F S 11",   "F T 5,7,10"],
    }, CUPS_OOD, MACH_OOD),
}

# ===========================================================================
# COFFEE — 4x4  X-ARM-VLA   100-size dataset   (page 4)
# Notes use COFFEE_NOTES_100 legend.
# ===========================================================================
coffee_4x4_vla_100 = {
    "id_id": grid({
        #        WB           O           Bk          R
        "K":  ["P S",       "F S 8,10", "F S 8",    "P S"],
        "Bk": ["F S 4",     "F S 10",   "F T 5",    "P S"],
        "T":  ["F S 11",    "F S 4,11", "F T 11",   "P S"],
        "W":  ["P S",       "P S",      "P S",      "F T 11"],
    }, CUPS_ID, MACH_ID),
    "id_od": grid({
        #        WB           O           Bk          R
        "R":  ["P S",       "P S 1",    "F T 11",   "P S"],
        "TS": ["F S 11",    "P S",      "P S",      "F S 11"],
        "Bl": ["P S 1",     "F S 8,10", "F S 11",   "P S"],
    }, CUPS_ID, MACH_OOD),
    "od_id": grid({
        #        Br           WC           Gr          P
        "K":  ["F S 8",     "P S",       "F S 11",   "P S 2"],
        "Bk": ["F S 4",     "F S 10,11", "P S 1",    "F S 4,11"],
        "T":  ["F S 4,11",  "P T",       "F T 4,11", "P S"],
        "W":  ["P S",       "P S",       "P S",      "F S 11"],
    }, CUPS_OOD, MACH_ID),
    "od_od": grid({
        #        Br           WC          Gr          P
        "R":  ["F S 4,11",  "P S 1",    "F S 11",   "F S 11"],
        "TS": ["F S 2,8",   "P S 2",    "F S 4,11", "F T 11"],
        "Bl": ["F S 11",    "F 4,11",   "P S",      "P T"],
    }, CUPS_OOD, MACH_OOD),
}

# ===========================================================================
# COFFEE — 1x1  X-ARM-VLA  "WB redo"  (page 6)  -- supplementary re-run of WB cup
# ===========================================================================
# Only the White-Basic cup was re-run. WB/K was run twice (fail then pass).
coffee_1x1_vla_wb_redo = {
    "id_id": {  # machine -> cell
        "K":  ("P", "S", ["redo: 1st attempt F"]),
        "Bk": ("F", "S", []),
        "T":  ("P", "T", [2]),
        "W":  ("F", "T", [1, 7, 10]),
    },
    "id_od": {
        "R":  ("P", "S", [1]),
        "TS": ("P", "S", [1]),
        "Bl": ("F", "T", [7, 9]),
    },
}

# ===========================================================================
# COFFEE — 4x4  X-ARM-VLA   OLD   (page 3)  -- APPENDIX (older run; Blue not run)
# ===========================================================================
coffee_4x4_vla_old = {
    "id_id": grid({
        #        WB        O        Bk        R
        "K":  ["P T",   "P S",   "F T",   "P T"],
        "Bk": ["P S",   "P T",   "P S",   "P T"],
        "T":  ["P S",   "P S",   "P S",   "P T"],
        "W":  ["P S",   "P T",   "P T",   "P T"],
    }, CUPS_ID, MACH_ID),
    "id_od": grid({
        #        WB        O        Bk        R
        "R":  ["P S",   "P T",   "P T",   "P T"],
        "TS": ["F T",   "P S",   "P T",   "P T"],
        "Bl": ["-",     "-",     "-",     "-"],   # not run
    }, CUPS_ID, MACH_OOD),
    "od_id": grid({
        #        Br        WC        Gr       P
        "K":  ["P S",   "P T O",  "P T",   "P S"],
        "Bk": ["P T",   "P S",    "P T",   "P S"],
        "T":  ["P S",   "P S",    "P T",   "P S"],
        "W":  ["P T",   "P T",    "P T",   "P S"],
    }, CUPS_OOD, MACH_ID),
    "od_od": grid({
        #        Br        WC         Gr       P
        "R":  ["P T",   "P S *",   "P T",   "P S"],
        "TS": ["P T",   "P S **",  "P T",   "P S"],
        "Bl": ["-",     "-",       "-",     "-"],  # not run
    }, CUPS_OOD, MACH_OOD),
}

# ===========================================================================
# POURING — 4x4  X-ARM-VLA   (single page)
# cups x bowls.  ID-cup boxes include an extra greyed TWC (tall white ceramic).
# ===========================================================================
POUR_CUPS_ID  = ["WB", "O", "Bk", "R", "TWC"]   # TWC = extra (OOD tall white ceramic)
POUR_CUPS_OOD = ["Br", "WC", "Gr", "P"]

pouring_4x4_vla = {
    "id_id": grid({
        #        WB           O        Bk        R          TWC
        "BL": ["P S",      "P S",   "P T 1",  "P S 2",   "P T 3"],
        "LB": ["P S 2,3",  "P T",   "F T",    "P",       "P STS"],
        "BK": ["P S",      "P T",   "P",      "F",       "P T 4"],
    }, POUR_CUPS_ID, BOWLS_ID),
    "id_od": grid({
        #        WB           O         Bk        R           TWC
        "P":  ["P S 3",    "F",      "P S",    "P S",      "P S 6"],
        "TB": ["F",        "F 7",    "F 11",   "P T 8",    "F"],
        "W":  ["F 11",     "P S 9",  "P S",    "P T 8",    "P T 2"],  # R/W noted 'almost'
    }, POUR_CUPS_ID, BOWLS_OOD),
    "od_id": grid({
        #        Br        WC        Gr       P
        "BL": ["F",      "F 10",   "F 11",  "P S"],
        "LB": ["P S",    "P S 2",  "P S",   "F 11"],
        "BK": ["F 5,6",  "P T 3",  "P S",   "F"],
    }, POUR_CUPS_OOD, BOWLS_ID),
    "od_od": grid({
        #        Br        WC        Gr        P
        "P":  ["F 11",   "F 10",   "P",      "P T 2"],
        "TB": ["F 11",   "F 11",   "F 11",   "F 8"],
        "W":  ["P",      "F 11",   "F 12",   "F 12"],
    }, POUR_CUPS_OOD, BOWLS_OOD),
}

# ===========================================================================
# POURING — 5x3  X-ARM-VLA   50-size dataset   (page 1)
# Notes use POUR_NOTES legend.  TWC column not run at this size.
# ===========================================================================
pouring_5x3_vla_50 = {
    "id_id": grid({
        #        WB              O                Bk               R          TWC
        "BL": ["F S 13,14,15", "P T",           "P S 3",         "F 16",    "-"],
        "LB": ["F 16",         "F T 1,3,17,18", "F T 1,3,17,18", "P S",     "-"],
        "BK": ["P T 11",       "F 5",           "P T 2",         "P S",     "-"],
    }, POUR_CUPS_ID, BOWLS_ID),
    "id_od": grid({
        #        WB              O           Bk         R          TWC
        "P":  ["P S 1,14,17",  "F S 19",   "F T 20",  "F T 20",  "-"],
        "TB": ["F T 20",       "P S 6,14", "F S 20",  "P T 6",   "-"],
        "W":  ["P S 11",       "P T",      "F S 18",  "F 7",     "-"],
    }, POUR_CUPS_ID, BOWLS_OOD),
    "od_id": grid({
        #        Br         WC          Gr         P
        "BL": ["P T 3",   "F T 20",   "F 7,21",  "P S 1"],
        "LB": ["F 5",     "F 7",      "P T 6",   "P S"],
        "BK": ["P T 3",   "P S 1,3",  "P T 12",  "P S"],
    }, POUR_CUPS_OOD, BOWLS_ID),
    "od_od": grid({
        #        Br             WC          Gr         P
        "P":  ["F T 20",      "F T 18",   "F 14,18", "F 5,16"],
        "TB": ["F 5,16,18",   "F 18",     "F 20",    "F 16"],
        "W":  ["F 16,18,21",  "F T 11,18","F 20",    "P T 11,21"],
    }, POUR_CUPS_OOD, BOWLS_OOD),
}

# ===========================================================================
# POURING — 5x3  X-ARM-VLA   150-size dataset   (page 3)
# Notes use POUR_NOTES legend.  TWC column not run at this size.
# ===========================================================================
pouring_5x3_vla_150 = {
    "id_id": grid({
        #        WB          O          Bk           R          TWC
        "BL": ["P S",      "P T 1",   "P S",       "P S",     "-"],
        "LB": ["P T",      "F 16",    "P T",       "P S 20",  "-"],
        "BK": ["P S 21",   "P T",     "F 16,18",   "F 16",    "-"],
    }, POUR_CUPS_ID, BOWLS_ID),
    "id_od": grid({
        #        WB          O          Bk           R          TWC
        "P":  ["F 16",     "P T",     "P T",       "P T",     "-"],
        "TB": ["P S 6",    "P S 6",   "F T 6,20",  "P T 6",   "-"],
        "W":  ["P S",      "P T",     "P T",       "P S 3",   "-"],
    }, POUR_CUPS_ID, BOWLS_OOD),
    "od_id": grid({
        #        Br         WC          Gr           P
        "BL": ["P S 3",   "P T 20",   "F 16",      "F 16"],
        "LB": ["P T",     "P S 18",   "P T 13,15", "F S 20"],
        "BK": ["P S",     "F 16",     "P T",       "P T 3"],
    }, POUR_CUPS_OOD, BOWLS_ID),
    "od_od": grid({
        #        Br         WC          Gr         P
        "P":  ["P T",     "F S 20",   "P T",     "F T 14,21"],
        "TB": ["P T 6",   "F T 20",   "F T 20",  "P T 3"],
        "W":  ["P T",     "P S",      "P T",     "P T"],
    }, POUR_CUPS_OOD, BOWLS_OOD),
}

# ===========================================================================
# POURING — 1x1  X-ARM-SAP   baseline   (page 4)
# Secondary baseline (SAP, not VLA).  Notes use POUR_NOTES_SAP legend.
# Sheet header reads "1x1 X-ARM-SAP" — this is the 1x1-config pouring task
# (variable name kept as `pouring_5x3_sap` for backward compatibility).
# ===========================================================================
pouring_5x3_sap = {
    "id_id": grid({
        #        WB          O         Bk       R          TWC
        "BL": ["P S",      "F 1,2",  "P S",   "F 3",     "-"],
        "LB": ["F S 3,4",  "P S",    "F 3",   "P S 6",   "-"],
        "BK": ["P S 6",    "F 3",    "F 3",   "P S 4",   "-"],
    }, POUR_CUPS_ID, BOWLS_ID),
    "id_od": grid({
        #        WB          O         Bk       R          TWC
        "P":  ["P S",      "F 3",    "P S",   "P S 7",   "-"],
        "TB": ["F S 8",    "F 3",    "F 3",   "F S 1,8", "-"],
        "W":  ["P S",      "F 3",    "F 3",   "P S 9",   "-"],
    }, POUR_CUPS_ID, BOWLS_OOD),
    "od_id": grid({
        #        Br         WC        Gr       P
        "BL": ["F 3",     "P S",    "F 3",   "F 3"],
        "LB": ["P S",     "P S",    "F 3",   "F 3"],
        "BK": ["F 3",     "P S",    "F 3",   "F 3"],
    }, POUR_CUPS_OOD, BOWLS_ID),
    "od_od": grid({
        #        Br         WC        Gr       P
        "P":  ["F 3",     "P S",    "P S 6", "F 3"],
        "TB": ["F S 1,8", "P S 11", "P S 6", "F 3"],
        "W":  ["F 3",     "P S 6",  "P S 4", "P S"],
    }, POUR_CUPS_OOD, BOWLS_OOD),
}

# ===========================================================================
# POURING — 1x1  X-ARM-VLA   150-size dataset   (page 1)
# 1x1-config pouring model, evaluated on the same cups x bowls grid.
# Eval was INTENTIONALLY run only partially — blank ('-') cells = not run.
# Notes use POUR_NOTES legend.
# ===========================================================================
pouring_1x1_vla_150 = {
    "id_id": grid({
        #        WB         O          Bk          R          TWC
        "BL": ["F T 20",  "F S 20",  "P S 6,20", "F T 11",  "-"],
        "LB": ["P S",     "P T 1",   "-",        "-",       "-"],
        "BK": ["-",       "-",       "F S 5",    "P T 3",   "-"],
    }, POUR_CUPS_ID, BOWLS_ID),
    "id_od": grid({
        #        WB         O          Bk          R          TWC
        "P":  ["P T",     "-",       "F 16,18",  "-",       "-"],
        "TB": ["P T 6",   "F T 16",  "F 5,16",   "P S",     "-"],
        "W":  ["-",       "P S 3",   "-",        "P S",     "-"],
    }, POUR_CUPS_ID, BOWLS_OOD),
    "od_id": grid({
        #        Br          WC        Gr          P
        "BL": ["P T",      "-",      "P T 3",    "F T 11"],
        "LB": ["F T 6,20", "P T",    "-",        "F 14,16"],
        "BK": ["-",        "F 16",   "F T 6,11", "-"],
    }, POUR_CUPS_OOD, BOWLS_ID),
    "od_od": grid({
        #        Br         WC         Gr         P
        "P":  ["F T 16",  "-",       "-",        "P S"],
        "TB": ["-",       "F S 11",  "F 16,21",  "F T 11"],
        "W":  ["P S",     "P T 3",   "F S 11",   "-"],
    }, POUR_CUPS_OOD, BOWLS_OOD),
}

# ===========================================================================
# POURING — 1x1  X-ARM-VLA   50-size dataset   (page 1)
# 1x1-config pouring model.  Sheet marks ✓ = pass, X = fail (with notes); blank
# cells = intentionally not run (partial eval, like the 150-size sheet).
# Notes use POUR_NOTES legend.  TWC column not run.
# ===========================================================================
pouring_1x1_vla_50 = {
    "id_id": grid({
        #        WB         O           Bk         R          TWC
        "BL": ["F 13,18", "F S 6,20", "F 5,16",  "F 5,16",  "-"],
        "LB": ["F 16",    "-",        "F 5,16",  "-",       "-"],
        "BK": ["-",       "F 5,16",   "-",       "F 5,16",  "-"],
    }, POUR_CUPS_ID, BOWLS_ID),
    "id_od": grid({
        #        WB        O          Bk         R           TWC
        "P":  ["P T 2",  "-",       "F 16",    "P T 6",    "-"],
        "TB": ["-",      "P T 6",   "F 5,16",  "F 14,16",  "-"],
        "W":  ["P T",    "F T 11",  "-",       "-",        "-"],
    }, POUR_CUPS_ID, BOWLS_OOD),
    "od_id": grid({
        #        Br         WC         Gr         P
        "BL": ["F 5,16",  "F S 11",  "F 5,16",  "P T 3"],
        "LB": ["F 5,16",  "P T 6",   "-",       "-"],
        "BK": ["-",       "-",       "F 5,16",  "F 5,16"],
    }, POUR_CUPS_OOD, BOWLS_ID),
    "od_od": grid({
        #        Br         WC          Gr         P
        "P":  ["F 5,16",  "-",        "F 5,16",  "P T"],
        "TB": ["-",       "F T 6,20", "F 5,16",  "F 5,16"],
        "W":  ["P T 3",   "F 5,16",   "-",       "-"],
    }, POUR_CUPS_OOD, BOWLS_OOD),
}

# ===========================================================================
# POURING — 1x1  X-ARM-VLA   100-size dataset   (page 2)
# 1x1-config pouring model.  Same notation as the 50-size sheet (✓ pass /
# X fail; blank = not run).  Notes use POUR_NOTES legend.  TWC column not run.
# ===========================================================================
pouring_1x1_vla_100 = {
    "id_id": grid({
        #        WB             O        Bk          R           TWC
        "BL": ["P S",         "P T",   "-",        "-",        "-"],
        "LB": ["-",           "-",     "F 5,16",   "F T 6,20", "-"],
        "BK": ["F 13,16,18",  "P T",   "F 16,18",  "F 16,18",  "-"],
    }, POUR_CUPS_ID, BOWLS_ID),
    "id_od": grid({
        #        WB             O              Bk         R            TWC
        "P":  ["F 13,16,18",  "-",           "F 16",    "F S 19,20", "-"],
        "TB": ["-",           "F 13,16,18",  "F 5,16",  "-",         "-"],
        "W":  ["F T 11",      "P T 3",       "-",       "P T 1,6",   "-"],
    }, POUR_CUPS_ID, BOWLS_OOD),
    "od_id": grid({
        #        Br         WC         Gr          P
        "BL": ["P T 3",   "F 20",    "F 18,20",  "-"],
        "LB": ["F T 20",  "-",       "-",        "P T 6,20"],
        "BK": ["-",       "P S 3",   "F 16",     "F S 6,11,20"],
    }, POUR_CUPS_OOD, BOWLS_ID),
    "od_od": grid({
        #        Br          WC         Gr         P
        "P":  ["P T",      "-",       "F 16",    "P S"],
        "TB": ["-",        "F 5,16",  "F 5,16",  "P T 3,6"],
        "W":  ["F 14,21",  "F T 6,11","-",       "-"],
    }, POUR_CUPS_OOD, BOWLS_OOD),
}

# ===========================================================================
# Dataset / training metadata
# Each task is collected as an N×M demo grid and trained at three dataset
# sizes (50 / ~100 / 150 demos).  Coffee has 50- and 150-size grids filled;
# pouring is the 105-size grid; mug-tree is the 150-size grid.  Remaining
# sizes are blank templates.  Cross-listed with "Model Train Baselines.png".
# ===========================================================================
TASK_CONFIG = {
    # key:      (display name,                dataset label,     N×M variants,  sizes)
    "coffee":  ("Cup on Coffee Machine",      "Mug/Machine",     ["1×1", "4×4"], [50, 100, 150]),
    "pouring": ("Cup Pouring (into bowl)",    "Pour Task",       ["5×3"],        [50, 105, 150]),
    "mugtree": ("Hang Cup on Mug Tree",       "Mug Tree Task",   ["5×1"],        [50, 100, 150]),
}

# Training-run tracker, transcribed from "Model Train Baselines.png".
# fields: (model, dataset, size, train_status, computer, started_date, eval_status, on_xarm)
#   train_status ∈ {Done, Training, Queued, ""}
#   eval_status  ∈ {Yes, No, In Progress, ""}   ("" = not started / blank)
#   on_xarm = checkpoint present on the xArm desktop (path filled in the sheet)
TRAIN_RUNS = [
    ("Xarm VLA", "Brick_in_Drawer",  50,  "Done",     "Cluster", "Last Tuesday",   "No",  True),
    ("Xarm VLA", "Brick_in_Drawer",  100, "Done",     "Cluster", "Last Tuesday",   "No",  True),
    ("Xarm VLA", "Brick_in_Drawer",  150, "Done",     "Cluster", "June 2, 2026",   "No",  True),
    ("Xarm VLA", "Faucet",           50,  "Done",     "Jinho",   "Last Tuesday",   "No",  True),
    ("Xarm VLA", "Mug Tree Task",    50,  "Done",     "Aiden",   "June 2, 2026",   "No",  True),
    ("Xarm VLA", "Mug Tree Task",    100, "Done",     "Cluster", "Last Wednesday", "No",  True),
    ("Xarm VLA", "Mug Tree Task",    150, "Done",     "Maisha",  "June 2, 2026",   "Yes", True),
    ("Xarm VLA", "Mug/Machine 1by1", 50,  "Done",     "Aiden",   "June 2, 2026",   "Yes", True),
    ("Xarm VLA", "Mug/Machine 1by1", 100, "Done",     "Cluster", "June 2, 2026",   "Yes", True),
    ("Xarm VLA", "Mug/Machine 1by1", 150, "Done",     "Aiden",   "Last Monday",    "Yes", True),
    ("Xarm VLA", "Mug/Machine 4by4", 50,  "Done",     "Jinho",   "Last Monday",    "Yes", True),
    ("Xarm VLA", "Mug/Machine 4by4", 100, "Done",     "Maisha",  "June 2, 2026",   "Yes", True),
    ("Xarm VLA", "Mug/Machine 4by4", 150, "Done",     "Cluster", "June 2, 2026",   "Yes", True),
    ("Xarm VLA", "Pour Task 1by1",   50,  "Done",     "Aiden",   "Yesterday",      "Yes", True),
    ("Xarm VLA", "Pour Task 1by1",   100, "Done",     "Aiden",   "Yesterday",      "Yes", True),
    ("Xarm VLA", "Pour Task 1by1",   150, "Done",     "Aiden",   "Yesterday",      "Yes", True),
    ("Xarm VLA", "Pour Task 5by3",   50,  "Done",     "Maisha",  "June 3, 2026",   "Yes", True),
    ("Xarm VLA", "Pour Task 5by3",   105, "Done",     "Maisha",  "June 2, 2026",   "Yes", True),
    ("Xarm VLA", "Pour Task 5by3",   150, "Done",     "Jinho",   "Last Tuesday",   "Yes", True),
]

# Baseline policies that exist only as blank eval templates (no results yet).
# SAP is the planned secondary baseline; DP and R2R2R are OPTIONAL — we may not
# run them — but are kept as an appendix option.
PLANNED_BASELINES = [
    ("X-ARM", "SAP", "1x1"), ("X-ARM", "SAP", "4x4"),
]
OPTIONAL_BASELINES = [
    ("X-ARM", "DP",    "1x1"), ("X-ARM", "DP",    "4x4"),
    ("X-ARM", "R2R2R", "1x1"), ("X-ARM", "R2R2R", "4x4"),
]

# Backward-compatible flat list (all blank templates)
PENDING_RUNS = PLANNED_BASELINES + OPTIONAL_BASELINES

# ===========================================================================
# Our-method (SAP) training tracker, transcribed from "Our Method Train.png".
# Only the rows that are *underlined* on the sheet AND carry a Yes/No in the
# "Eval Completed?" column are listed here (the rest are still in-flight with a
# blank eval status and are intentionally omitted).
# fields: (model, dataset, size, status, computer, started, eval_status)
#   status      ∈ {Checkpoint, Done, Failed}
#   eval_status ∈ {Yes, No}
# ===========================================================================
OUR_METHOD_TRAINS = [
    ("Xarm VLA (4by4 mug/cm)",  "lfg_coffee_machine_scaled_2k", 2000, "Checkpoint", "Maisha",  "Today",     "No"),
    ("Xarm VLA (r2r2r baseline)","corl_mug_2k_1cm",              2000, "Checkpoint", "Jinho",   "Yesterday", "No"),
    ("Xarm VLA",                 "pour_cousins_2k_lerobot",      2000, "Checkpoint", "Cluster", "Yesterday", "No"),
    ("Xarm VLA",                 "pour_quality_2k_lerobot",      2000, "Done",       "Judith",  "Tuesday",   "Yes"),
]

# ===========================================================================
# MUG TREE — 5x1  X-ARM-VLA   (Data/Semantic Evaluation Mug Tree.pdf, 150 size)
# Single object axis (cup hung on a fixed mug tree): each cup = 5 repeat trials.
# No grasp tag on this sheet. All ID and OD cups now run.
# ===========================================================================
MUGTREE_NOTES = {
    1: "Pushed the tree",
    2: "Hung on edge, so dropped cup",
    3: "Dropped mug while not on branch",
    4: "Tilted grasp on mug lip",
    5: "Hanging mug on edge",
    6: "Arm errored out",
    7: "Tried to grab entire cup",
}

MUGTREE_CUPS_ID  = ["WB", "O", "Bk", "R", "TWC"]   # TWC = extra (tall white ceramic)
MUGTREE_CUPS_OOD = ["Br", "WC", "Gr", "P", "Pu"]

def trials(rows):
    """rows: dict cup -> list of 5 cell-codes."""
    return {cup: [C(code) for code in cells] for cup, cells in rows.items()}

mugtree_5x1_vla = {
    "id_cup": trials({
        #        t1       t2          t3       t4          t5
        "WB":  ["P",     "P",        "P",     "P",        "P"],
        "O":   ["P 1",   "F 1,2",    "P 1",   "F 1,2",    "P"],
        "Bk":  ["F 3",   "F 3,4",    "F 3,4", "F 3",      "F 3"],
        "R":   ["P",     "P",        "P 4",   "F 3",      "P"],
        "TWC": ["F 2",   "P",        "P 1",   "F 2",      "F 3"],
    }),
    "od_cup": trials({   # all OD cups now run
        #        t1       t2          t3       t4          t5
        "Br":  ["P",     "F 1,3",    "P",     "P 1",      "P 5"],
        "WC":  ["F 3",   "F 6",      "P",     "F 7",      "P"],
        "Gr":  ["P 1",   "P 1",      "P 1",   "F 2",      "F"],
        "P":   ["F 2",   "P",        "P",     "F",        "F"],
        "Pu":  ["P",     "P",        "P",     "F",        "F 2"],
    }),
}

# Backward-compatible alias (mug tree was previously mislabeled 4x4)
mugtree_4x4_vla = mugtree_5x1_vla

# ===========================================================================
# Per-dataset-size registry of coffee grids (VLA).  value None = blank
# template (collected/queued but not yet evaluated).  Note legend differs by
# size: 50/100 use COFFEE_NOTES_50, 150 uses COFFEE_NOTES.
# ===========================================================================
COFFEE_BY_SIZE = {
    "1×1": {50: coffee_1x1_vla_50, 100: coffee_1x1_vla_100, 150: coffee_1x1_vla},
    "4×4": {50: coffee_4x4_vla_50, 100: coffee_4x4_vla_100, 150: coffee_4x4_vla},
}

# Per-dataset-size registry of pouring grids (VLA).  105 is the original
# mid-size grid; 50 and 150 added from the updated sheets.
POURING_BY_SIZE = {
    "5×3": {50: pouring_5x3_vla_50, 105: pouring_4x4_vla, 150: pouring_5x3_vla_150},
}

# Which demo-sizes have real (filled-in) grids per task — used to decide which
# sizes still need blank fill-in templates.
FILLED_SIZES = {
    "coffee":  {50, 100, 150},
    "pouring": {50, 105, 150},
    "mugtree": {150},
}
