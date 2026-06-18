# Semantic Manipulation — Evaluation Results

**Arm:** xArm  ·  **Policy:** VLA (+ SAP baseline)  ·  **Datasets:** coffee 1×1 & 4×4, pouring 5×3, mug-tree 5×1  ·  **Training sizes:** 50 / ~100 / 150 demos (coffee @50/100/150, pouring @50/105/150 + SAP baseline, mug-tree @150 filled)

Legend: ✅ success · ❌ failure · grasp **S**=side / **T**=top · `(n)` = note number (see Legends). ID = in-distribution, OOD = out-of-distribution.

## Task suite

_Seven teleoperated tasks collected on the xArm. Config = object-variation grid; Variations = distinct object pairings; Avg teleop/demo = mean time to teleoperate one demo. Tasks 1–3 have eval grids below; the rest are collected, eval pending._

| # | Task | Objects | Config | Variations | Avg teleop/demo | In report |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | **Cup on Coffee Machine** | cup → coffee machine | 4×4 | 16 | ~30s | ✅ below |
| 2 | **Cup Pour into Bowl** | cup → bowl | 5×3 | 15 | ~35s | ✅ below |
| 3 | **Hang Cup on Mug Tree** | cup → mug tree | 5×1 | 5 | ~27s | ✅ below |
| 4 | **Brick into Drawer** | power brick → drawer | 5×1 | 5 | ~32s | collected |
| 5 | **Power Drill on Pad** | drill → mouse pad | 1×1 | 1 | ~16s | collected |
| 6 | **Bottle/Can on Coaster** | bottle/can → coaster | (1+1)×1 | 2 | ~11s | collected |
| 7 | **Faucet** | turn faucet | 1 | 1 | ~23s | collected |

## Summary — success rate by condition

| Run | ID/ID | ID/OOD | OOD/ID | OOD/OOD | Overall |
| --- | --- | --- | --- | --- | --- |
| **Coffee · 4×4 VLA · @150** | 75% (12/16) | 67% (8/12) | 62% (10/16) | 42% (5/12) | **62% (35/56)** |
| **Coffee · 4×4 VLA · @100** | 44% (7/16) | 58% (7/12) | 50% (8/16) | 33% (4/12) | **46% (26/56)** |
| **Coffee · 4×4 VLA · @50** | 44% (7/16) | 58% (7/12) | 12% (2/16) | 50% (6/12) | **39% (22/56)** |
| **Coffee · 1×1 VLA · @150** | 0% (0/16) | 25% (3/12) | 6% (1/16) | 17% (2/12) | **11% (6/56)** |
| **Coffee · 1×1 VLA · @100** | 6% (1/16) | 25% (3/12) | 0% (0/16) | 25% (3/12) | **12% (7/56)** |
| **Coffee · 1×1 VLA · @50** | 6% (1/16) | 8% (1/12) | 19% (3/16) | 17% (2/12) | **12% (7/56)** |
| **Pouring · 5×3 VLA · @150** | 75% (9/12) | 83% (10/12) | 67% (8/12) | 67% (8/12) | **73% (35/48)** |
| **Pouring · 5×3 VLA · @105** | 83% (10/12) | 58% (7/12) | 50% (6/12) | 25% (3/12) | **54% (26/48)** |
| **Pouring · 5×3 VLA · @50** | 50% (6/12) | 42% (5/12) | 67% (8/12) | 8% (1/12) | **42% (20/48)** |
| **Pouring · 1×1 VLA · @150 (partial)** | 50% (4/8) | 62% (5/8) | 38% (3/8) | 38% (3/8) | **47% (15/32)** |
| **Pouring · 5×3 SAP · baseline** | 50% (6/12) | 42% (5/12) | 33% (4/12) | 58% (7/12) | **46% (22/48)** |

_Dataset-size scaling (coffee): 4×4 climbs 39% → 62% (50→150 demos); 1×1 stays low (12% → 11%)._

_Mug Tree · 5×1 VLA: ID cups 12/20 (60%) + OOD cups 14/25 (56%) so far — single object axis, shown in Task 3._

## Training runs & dataset sizes

_Cross-listed with **Model Train Baselines**. Each task is trained at 50 / ~100 / 150 demos. The eval-complete rows match the grids in this report: Coffee 1×1 & 4×4 @50/100/150, Pour @50/105/150, Mug-Tree @150._

| Dataset | Size | Train | Computer | Started | Eval | On xArm |
| --- | --- | --- | --- | --- | --- | --- |
| Brick_in_Drawer | 50 | Done | Cluster | Last Tuesday | ❌ | ✓ |
| Brick_in_Drawer | 100 | Done | Cluster | Last Tuesday | ❌ | ✓ |
| Brick_in_Drawer | 150 | Done | Cluster | June 2, 2026 | ❌ | ✓ |
| Faucet | 50 | Done | Jinho | Last Tuesday | ❌ | ✓ |
| Mug Tree Task | 50 | Done | Aiden | June 2, 2026 | ❌ | ✓ |
| Mug Tree Task | 100 | Done | Cluster | Last Wednesday | ❌ | ✓ |
| Mug Tree Task | 150 | Done | Maisha | June 2, 2026 | ✅ done | ✓ |
| Mug/Machine 1by1 | 50 | Done | Aiden | June 2, 2026 | ✅ done | ✓ |
| Mug/Machine 1by1 | 100 | Done | Cluster | June 2, 2026 | ✅ done | ✓ |
| Mug/Machine 1by1 | 150 | Done | Aiden | Last Monday | ✅ done | ✓ |
| Mug/Machine 4by4 | 50 | Done | Jinho | — | ✅ done | ✓ |
| Mug/Machine 4by4 | 100 | Done | Maisha | June 2, 2026 | ✅ done | ✓ |
| Mug/Machine 4by4 | 150 | Done | Cluster | June 2, 2026 | ✅ done | ✓ |
| Pour Task 1by1 | 50 | Queued | Aiden | Today | ❌ | — |
| Pour Task 1by1 | 100 | Training | Aiden | Today | ❌ | — |
| Pour Task 1by1 | 150 | Done | Aiden | Today | ✅ done | ✓ |
| Pour Task 5by3 | 50 | Done | Maisha | June 3, 2026 | ✅ done | ✓ |
| Pour Task 5by3 | 105 | Done | Maisha | June 2, 2026 | ✅ done | ✓ |
| Pour Task 5by3 | 150 | Done | Jinho | Last Tuesday | ✅ done | ✓ |

## Task 1 — Cup on Coffee Machine

_Dataset **Mug/Machine** · config 1×1 & 4×4 · trained at 50 / ~100 / 150 demos (all three sizes now filled)._

### 150-demo dataset

#### 4×4 VLA @ 150 demos — 35/56 (62%)

**ID Cup / ID Machine** — 12/16 (75%)

| Machine ↓ / Cup → | White Basic | Orange | Black | Red |
| --- | --- | --- | --- | --- |
| **Keurig** | ✅ S | ❌ S | ✅ S | ✅ T |
| **Black** | ✅ S | ✅ S | ❌ T | ✅ S (1) |
| **Teal** | ✅ T (1) | ✅ T (3) | ✅ T (1) | ❌ S |
| **White** | ✅ T (4) | ✅ T | ✅ T (4) | ❌ T |

**ID Cup / OOD Machine** — 8/12 (67%)

| Machine ↓ / Cup → | White Basic | Orange | Black | Red |
| --- | --- | --- | --- | --- |
| **Red** | ✅ S | ✅ T (1) | ✅ T (1,5) | ❌ S (6) |
| **Tastyle** | ✅ S (4) | ❌ S | ❌ S (7) | ❌ S |
| **Blue** | ✅ S (1) | ✅ S (1) | ✅ T | ✅ S (2) |

**OOD Cup / ID Machine** — 10/16 (62%)

| Machine ↓ / Cup → | Brown | White Ceramic | Gray | Pink |
| --- | --- | --- | --- | --- |
| **Keurig** | ✅ S (2) | ✅ S | ✅ S | ✅ S |
| **Black** | ❌ T (8,9) | ✅ S | ✅ S | ❌ S |
| **Teal** | ✅ T (1,2,8) | ❌ S (10) | ❌ T (1,9) | ✅ S |
| **White** | ✅ S (2) | ❌ T (4) | ✅ T (2) | ❌ S (6) |

**OOD Cup / OOD Machine** — 5/12 (42%)

| Machine ↓ / Cup → | Brown | White Ceramic | Gray | Pink |
| --- | --- | --- | --- | --- |
| **Red** | ❌ S | ❌ S | ❌ T | ✅ S |
| **Tastyle** | ✅ S (1) | ❌ S | ✅ S (2) | ❌ S |
| **Blue** | ❌ S (1,7,8) | ❌ S (8) | ✅ S (1) | ✅ S |

#### 1×1 VLA @ 150 demos — 6/56 (11%)

_Single-view model fails nearly everything; only successes are on the OOD (taller-clearance) machines._

**ID Cup / ID Machine** — 0/16 (0%)

| Machine ↓ / Cup → | White Basic | Orange | Black | Red |
| --- | --- | --- | --- | --- |
| **Keurig** | ❌ T | ❌ T (11) | ❌ T | ❌ T (11) |
| **Black** | ❌ S (8) | ❌ T (11) | ❌ T | ❌ T (11) |
| **Teal** | ❌ T (1,7) | ❌ T | ❌ T | ❌ T (7) |
| **White** | ❌ T (1,8) | ❌ T (11) | ❌ T | ❌ S (11) |

**ID Cup / OOD Machine** — 3/12 (25%)

| Machine ↓ / Cup → | White Basic | Orange | Black | Red |
| --- | --- | --- | --- | --- |
| **Red** | ✅ T (1) | ❌ S | ❌ S (11) | ❌ S (7) |
| **Tastyle** | ✅ S | ❌ S | ❌ T (11) | ❌ T (6) |
| **Blue** | ✅ S | ❌ S (5) | ❌ T (11) | ❌ T (7) |

**OOD Cup / ID Machine** — 1/16 (6%)

| Machine ↓ / Cup → | Brown | White Ceramic | Gray | Pink |
| --- | --- | --- | --- | --- |
| **Keurig** | ❌ T (11) | ✅ S | ❌ T | ❌ S (7,8) |
| **Black** | ❌ S | ❌ S | ❌ T | ❌ S |
| **Teal** | ❌ S | ❌ T (7) | ❌ S (11) | ❌ S (7) |
| **White** | ❌ T | ❌ T | ❌ T | ❌ S (10) |

**OOD Cup / OOD Machine** — 2/12 (17%)

| Machine ↓ / Cup → | Brown | White Ceramic | Gray | Pink |
| --- | --- | --- | --- | --- |
| **Red** | ❌ T (11) | ❌ S | ❌ S (7) | ❌ T (7,9) |
| **Tastyle** | ❌ S | ✅ S | ❌ S | ❌ T |
| **Blue** | ✅ S (3,5) | ❌ T (7) | ❌ S (11) | ❌ T (5,7) |

#### 1×1 VLA — White-Basic re-run (supplementary)

| Machine | Result | Grasp | Notes |
| --- | --- | --- | --- |
| WB / Keurig | ✅ | S | redo: 1st attempt F |
| WB / Black | ❌ | S |  |
| WB / Teal | ✅ | T | 2 |
| WB / White | ❌ | T | 1, 7, 10 |
| WB / Red | ✅ | S | 1 |
| WB / Tastyle | ✅ | S | 1 |
| WB / Blue | ❌ | T | 7, 9 |

**Coffee-machine notes (150-demo sheets):**
- 1. Pushed machine back
- 2. Tilted placement and contact on plate
- 3. Took double time
- 4. Pushed cup while trying to grasp
- 5. Dropped cup on edge of platform
- 6. Self collision
- 7. Spilled cup
- 8. Force-torque trigger
- 9. Grasped inside cup
- 10. Gripper hooked on handle
- 11. Cannot lift mug
- **O** Completed but took > 1 min
- ***** Not fully in cup holder
- ****** Released while tilted
- **Grasp:** S = side grasp, T = top grasp.

### 100-demo dataset

_Mid-size training set (newly transcribed); note numbers use the **100-demo legend** below._

#### 4×4 VLA @ 100 demos — 26/56 (46%)

**ID Cup / ID Machine** — 7/16 (44%)

| Machine ↓ / Cup → | White Basic | Orange | Black | Red |
| --- | --- | --- | --- | --- |
| **Keurig** | ✅ S | ❌ S (8,10) | ❌ S (8) | ✅ S |
| **Black** | ❌ S (4) | ❌ S (10) | ❌ T (5) | ✅ S |
| **Teal** | ❌ S (11) | ❌ S (4,11) | ❌ T (11) | ✅ S |
| **White** | ✅ S | ✅ S | ✅ S | ❌ T (11) |

**ID Cup / OOD Machine** — 7/12 (58%)

| Machine ↓ / Cup → | White Basic | Orange | Black | Red |
| --- | --- | --- | --- | --- |
| **Red** | ✅ S | ✅ S (1) | ❌ T (11) | ✅ S |
| **Tastyle** | ❌ S (11) | ✅ S | ✅ S | ❌ S (11) |
| **Blue** | ✅ S (1) | ❌ S (8,10) | ❌ S (11) | ✅ S |

**OOD Cup / ID Machine** — 8/16 (50%)

| Machine ↓ / Cup → | Brown | White Ceramic | Gray | Pink |
| --- | --- | --- | --- | --- |
| **Keurig** | ❌ S (8) | ✅ S | ❌ S (11) | ✅ S (2) |
| **Black** | ❌ S (4) | ❌ S (10,11) | ✅ S (1) | ❌ S (4,11) |
| **Teal** | ❌ S (4,11) | ✅ T | ❌ T (4,11) | ✅ S |
| **White** | ✅ S | ✅ S | ✅ S | ❌ S (11) |

**OOD Cup / OOD Machine** — 4/12 (33%)

| Machine ↓ / Cup → | Brown | White Ceramic | Gray | Pink |
| --- | --- | --- | --- | --- |
| **Red** | ❌ S (4,11) | ✅ S (1) | ❌ S (11) | ❌ S (11) |
| **Tastyle** | ❌ S (2,8) | ✅ S (2) | ❌ S (4,11) | ❌ T (11) |
| **Blue** | ❌ S (11) | ❌ (4,11) | ✅ S | ✅ T |

#### 1×1 VLA @ 100 demos — 7/56 (12%)

**ID Cup / ID Machine** — 1/16 (6%)

| Machine ↓ / Cup → | White Basic | Orange | Black | Red |
| --- | --- | --- | --- | --- |
| **Keurig** | ❌ T (5) | ❌ S (10) | ❌ T (11) | ❌ T (11) |
| **Black** | ❌ T (9) | ❌ S (11) | ❌ T (11) | ❌ S (11) |
| **Teal** | ❌ T (1,5) | ❌ S (1,5) | ❌ T (9,11) | ❌ T (7,9,11) |
| **White** | ❌ T (7,8) | ✅ S | ❌ S (11) | ❌ S (4,11) |

**ID Cup / OOD Machine** — 3/12 (25%)

| Machine ↓ / Cup → | White Basic | Orange | Black | Red |
| --- | --- | --- | --- | --- |
| **Red** | ✅ T (1) | ❌ S (10,11) | ❌ S (11) | ❌ S (11) |
| **Tastyle** | ✅ S | ❌ T (5) | ❌ T (11) | ❌ T (7,11) |
| **Blue** | ✅ S | ❌ S (4,11) | ❌ S (11) | ❌ T (4) |

**OOD Cup / ID Machine** — 0/16 (0%)

| Machine ↓ / Cup → | Brown | White Ceramic | Gray | Pink |
| --- | --- | --- | --- | --- |
| **Keurig** | ❌ T (4) | ❌ T (5) | ❌ T (11) | ❌ S (1,5,7) |
| **Black** | ❌ S (11) | ❌ T (9) | ❌ S (9,11) | ❌ T (7,9) |
| **Teal** | ❌ S (11) | ❌ T (4) | ❌ T (11) | ❌ S (1,4,11) |
| **White** | ❌ T (11) | ❌ S (12) | ❌ T (9,11) | ❌ S (7,9) |

**OOD Cup / OOD Machine** — 3/12 (25%)

| Machine ↓ / Cup → | Brown | White Ceramic | Gray | Pink |
| --- | --- | --- | --- | --- |
| **Red** | ❌ S (4) | ✅ T | ❌ S (11) | ❌ S (7,11) |
| **Tastyle** | ❌ T (4) | ❌ S (11) | ❌ S (9,11) | ✅ S |
| **Blue** | ❌ S (9,11) | ✅ S | ❌ S (11) | ❌ T (5,7,10) |

**Coffee-machine notes (100-demo sheets):**
- 1. Pushed machine back
- 2. Tilted placement and contact on plate
- 3. Took double time
- 4. Pushed cup while trying to grasp
- 5. Dropped cup on edge of platform
- 6. Self collision
- 7. Spilled cup
- 8. Force-torque trigger
- 9. Grasped inside cup
- 10. Gripper hooked on handle
- 11. Cannot grab handle
- 12. Tried to grab entire cup

### 50-demo dataset

_Smaller training set; note numbers use the **50-demo legend** below._

#### 4×4 VLA @ 50 demos — 22/56 (39%)

**ID Cup / ID Machine** — 7/16 (44%)

| Machine ↓ / Cup → | White Basic | Orange | Black | Red |
| --- | --- | --- | --- | --- |
| **Keurig** | ❌ S (2) | ❌ S (2) | ❌ S | ✅ S |
| **Black** | ❌ S (2) | ❌ S (1) | ✅ S | ❌ S |
| **Teal** | ✅ S | ✅ S | ❌ S (1) | ❌ S (1) |
| **White** | ✅ S | ✅ S | ✅ T | ❌ T (2) |

**ID Cup / OOD Machine** — 7/12 (58%)

| Machine ↓ / Cup → | White Basic | Orange | Black | Red |
| --- | --- | --- | --- | --- |
| **Red** | ✅ S | ✅ T | ❌ S (2) | ✅ S |
| **Tastyle** | ❌ S (1) | ✅ S | ✅ S | ✅ S |
| **Blue** | ❌ S (2) | ❌ S (1) | ✅ S | ❌ S (2) |

**OOD Cup / ID Machine** — 2/16 (12%)

| Machine ↓ / Cup → | Brown | White Ceramic | Gray | Pink |
| --- | --- | --- | --- | --- |
| **Keurig** | ❌ S | ✅ S | ❌ S (5) | ❌ S (6) |
| **Black** | ❌ T (6) | ❌ S (2) | ❌ T (2) | ❌ S (1) |
| **Teal** | ❌ T (2) | ❌ S (2) | ❌ S (2) | ❌ S (2) |
| **White** | ❌ S (2) | ✅ S | ❌ T (2) | ❌ T (1) |

**OOD Cup / OOD Machine** — 6/12 (50%)

| Machine ↓ / Cup → | Brown | White Ceramic | Gray | Pink |
| --- | --- | --- | --- | --- |
| **Red** | ✅ S (7) | ✅ S (7) | ❌ S (2) | ✅ S |
| **Tastyle** | ❌ S (2) | ❌ S (7,8) | ❌ T (2) | ❌ S (1,8) |
| **Blue** | ✅ S | ❌ S (2,6) | ✅ T (7,9) | ✅ S |

#### 1×1 VLA @ 50 demos — 7/56 (12%)

**ID Cup / ID Machine** — 1/16 (6%)

| Machine ↓ / Cup → | White Basic | Orange | Black | Red |
| --- | --- | --- | --- | --- |
| **Keurig** | ✅ T | ❌ T | ❌ S | ❌ T |
| **Black** | ❌ S (1) | ❌ T (2) | ❌ S (2) | ❌ S (2) |
| **Teal** | ❌ T (2) | ❌ T (2) | ❌ S (2) | ❌ S (1) |
| **White** | ❌ T (2) | ❌ S (2) | ❌ T (2) | ❌ T (3) |

**ID Cup / OOD Machine** — 1/12 (8%)

| Machine ↓ / Cup → | White Basic | Orange | Black | Red |
| --- | --- | --- | --- | --- |
| **Red** | ❌ T (2) | ❌ T (2) | ❌ S (2) | ❌ T (2) |
| **Tastyle** | ✅ T | ❌ S (2) | ❌ S (4) | ❌ S (2) |
| **Blue** | ❌ T (5) | ❌ S (2) | ❌ S (4) | ❌ T (2) |

**OOD Cup / ID Machine** — 3/16 (19%)

| Machine ↓ / Cup → | Brown | White Ceramic | Gray | Pink |
| --- | --- | --- | --- | --- |
| **Keurig** | ❌ T (2) | ✅ S | ❌ T (2) | ✅ S |
| **Black** | ❌ T (2) | ❌ T (2) | ❌ T (2) | ❌ S (2) |
| **Teal** | ❌ S (2) | ❌ S (2) | ❌ S (1,2) | ❌ T (10) |
| **White** | ❌ S (1) | ✅ T (9) | ❌ T (2) | ❌ T (1) |

**OOD Cup / OOD Machine** — 2/12 (17%)

| Machine ↓ / Cup → | Brown | White Ceramic | Gray | Pink |
| --- | --- | --- | --- | --- |
| **Red** | ❌ S (2) | ✅ T | ❌ T (2) | ❌ T (2) |
| **Tastyle** | ❌ S (2) | ❌ S (2) | ❌ T (2) | ❌ S (5) |
| **Blue** | ❌ S (2) | ❌ S (6) | ❌ S (2) | ✅ T |

**Coffee-machine notes (50-demo sheets):**
- 1. Spilled the cup
- 2. Failed to grasp (hit cup, grasped air)
- 3. Hit the coffee machine
- 4. Good pose, high Z
- 5. Wrong grasp
- 6. Torque sensor error
- 7. Moved machine back
- 8. Handle hooked on gripper
- 9. Balancing on edge
- 10. Dropped cup elsewhere

_Codes — Cups: WB White-Basic, O Orange, Bk Black, R Red (ID); Br Brown, WC White-Ceramic, Gr Gray, P Pink (OOD). Machines: K Keurig, Bk Black, T Teal, W White (ID); R Red, TS Tastyle, Bl Blue (OOD)._

## Task 2 — Cup Pouring (into bowl)

_Dataset **Pour Task** · config 5×3 · trained at 50 / ~105 / 150 demos (all three filled) + SAP baseline._

_Tall-White-Ceramic (Tall W.C.) column is an extra OOD cup — shown but not counted in the rate._

### 5×3 VLA @ 150 demos — 35/48 (73%)

**ID Cup / ID Bowl** — 9/12 (75%)

| Bowl ↓ / Cup → | White Basic | Orange | Black | Red | Tall W.C. |
| --- | --- | --- | --- | --- | --- |
| **Blue** | ✅ S | ✅ T (1) | ✅ S | ✅ S | — |
| **Light Blue** | ✅ T | ❌ (16) | ✅ T | ✅ S (20) | — |
| **Black** | ✅ S (21) | ✅ T | ❌ (16,18) | ❌ (16) | — |

**ID Cup / OOD Bowl** — 10/12 (83%)

| Bowl ↓ / Cup → | White Basic | Orange | Black | Red | Tall W.C. |
| --- | --- | --- | --- | --- | --- |
| **Pink** | ❌ (16) | ✅ T | ✅ T | ✅ T | — |
| **Tall (light blue)** | ✅ S (6) | ✅ S (6) | ❌ T (6,20) | ✅ T (6) | — |
| **White** | ✅ S | ✅ T | ✅ T | ✅ S (3) | — |

**OOD Cup / ID Bowl** — 8/12 (67%)

| Bowl ↓ / Cup → | Brown | White Ceramic | Gray | Pink |
| --- | --- | --- | --- | --- |
| **Blue** | ✅ S (3) | ✅ T (20) | ❌ (16) | ❌ (16) |
| **Light Blue** | ✅ T | ✅ S (18) | ✅ T (13,15) | ❌ S (20) |
| **Black** | ✅ S | ❌ (16) | ✅ T | ✅ T (3) |

**OOD Cup / OOD Bowl** — 8/12 (67%)

| Bowl ↓ / Cup → | Brown | White Ceramic | Gray | Pink |
| --- | --- | --- | --- | --- |
| **Pink** | ✅ T | ❌ S (20) | ✅ T | ❌ T (14,21) |
| **Tall (light blue)** | ✅ T (6) | ❌ T (20) | ❌ T (20) | ✅ T (3) |
| **White** | ✅ T | ✅ S | ✅ T | ✅ T |


### 5×3 VLA @ 105 demos — 26/48 (54%)

**ID Cup / ID Bowl** — 10/12 (83%)

| Bowl ↓ / Cup → | White Basic | Orange | Black | Red | Tall W.C. |
| --- | --- | --- | --- | --- | --- |
| **Blue** | ✅ S | ✅ S | ✅ T (1) | ✅ S (2) | ✅ T (3) |
| **Light Blue** | ✅ S (2,3) | ✅ T | ❌ T | ✅ | ✅ (STS) |
| **Black** | ✅ S | ✅ T | ✅ | ❌ | ✅ T (4) |

**ID Cup / OOD Bowl** — 7/12 (58%)

| Bowl ↓ / Cup → | White Basic | Orange | Black | Red | Tall W.C. |
| --- | --- | --- | --- | --- | --- |
| **Pink** | ✅ S (3) | ❌ | ✅ S | ✅ S | ✅ S (6) |
| **Tall (light blue)** | ❌ | ❌ (7) | ❌ (11) | ✅ T (8) | ❌ |
| **White** | ❌ (11) | ✅ S (9) | ✅ S | ✅ T (8) | ✅ T (2) |

**OOD Cup / ID Bowl** — 6/12 (50%)

| Bowl ↓ / Cup → | Brown | White Ceramic | Gray | Pink |
| --- | --- | --- | --- | --- |
| **Blue** | ❌ | ❌ (10) | ❌ (11) | ✅ S |
| **Light Blue** | ✅ S | ✅ S (2) | ✅ S | ❌ (11) |
| **Black** | ❌ (5,6) | ✅ T (3) | ✅ S | ❌ |

**OOD Cup / OOD Bowl** — 3/12 (25%)

| Bowl ↓ / Cup → | Brown | White Ceramic | Gray | Pink |
| --- | --- | --- | --- | --- |
| **Pink** | ❌ (11) | ❌ (10) | ✅ | ✅ T (2) |
| **Tall (light blue)** | ❌ (11) | ❌ (11) | ❌ (11) | ❌ (8) |
| **White** | ✅ | ❌ (11) | ❌ (12) | ❌ (12) |


### 5×3 VLA @ 50 demos — 20/48 (42%)

**ID Cup / ID Bowl** — 6/12 (50%)

| Bowl ↓ / Cup → | White Basic | Orange | Black | Red | Tall W.C. |
| --- | --- | --- | --- | --- | --- |
| **Blue** | ❌ S (13,14,15) | ✅ T | ✅ S (3) | ❌ (16) | — |
| **Light Blue** | ❌ (16) | ❌ T (1,3,17,18) | ❌ T (1,3,17,18) | ✅ S | — |
| **Black** | ✅ T (11) | ❌ (5) | ✅ T (2) | ✅ S | — |

**ID Cup / OOD Bowl** — 5/12 (42%)

| Bowl ↓ / Cup → | White Basic | Orange | Black | Red | Tall W.C. |
| --- | --- | --- | --- | --- | --- |
| **Pink** | ✅ S (1,14,17) | ❌ S (19) | ❌ T (20) | ❌ T (20) | — |
| **Tall (light blue)** | ❌ T (20) | ✅ S (6,14) | ❌ S (20) | ✅ T (6) | — |
| **White** | ✅ S (11) | ✅ T | ❌ S (18) | ❌ (7) | — |

**OOD Cup / ID Bowl** — 8/12 (67%)

| Bowl ↓ / Cup → | Brown | White Ceramic | Gray | Pink |
| --- | --- | --- | --- | --- |
| **Blue** | ✅ T (3) | ❌ T (20) | ❌ (7,21) | ✅ S (1) |
| **Light Blue** | ❌ (5) | ❌ (7) | ✅ T (6) | ✅ S |
| **Black** | ✅ T (3) | ✅ S (1,3) | ✅ T (12) | ✅ S |

**OOD Cup / OOD Bowl** — 1/12 (8%)

| Bowl ↓ / Cup → | Brown | White Ceramic | Gray | Pink |
| --- | --- | --- | --- | --- |
| **Pink** | ❌ T (20) | ❌ T (18) | ❌ (14,18) | ❌ (5,16) |
| **Tall (light blue)** | ❌ (5,16,18) | ❌ (18) | ❌ (20) | ❌ (16) |
| **White** | ❌ (16,18,21) | ❌ T (11,18) | ❌ (20) | ✅ T (11,21) |


_Dataset-size scaling (pouring): 42% → 54% → 73% across 50 → 105 → 150 demos._

**Pouring notes (VLA 50/105/150-demo sheets):**
- 1. Bad return cup to table
- 2. Went in for second pour
- 3. A bit off-center for pour
- 4. Tipped bowl while returning cup
- 5. Started pushing cup down & didn't move; likely F/T error
- 6. Tapped bowl while placing down or pouring
- 7. Picked up cup and stopped moving
- 8. Tall bowl was pushed while attempting to pour
- 9. Two partial pours -> completed
- 10. Gripper opened while pour attempt
- 11. Severely off center
- 12. Tipped cup over while picking up cup
- 13. Gripper hooked on handle
- 14. Spilled out of bowl / spilled cup
- 15. Can't place cup after done
- 16. Didn't pick up cup
- 17. Poured but didn't return cup properly
- 18. F/T error
- 19. Dripped cup in bowl
- 20. Barely poured
- 21. Picked up inside of cup
- **STS** Succeeded only after trying all three grasp attempts (side -> top -> side)
- **Grasp:** S = side grasp, T = top grasp.

### 1×1 VLA @ 150 demos (partial) — 15/32 (47%)

_Separate 1×1-config pouring model evaluated on the full grid; 16 of 48 cells were intentionally left un-run (blank)._

**ID Cup / ID Bowl** — 4/8 (50%)

| Bowl ↓ / Cup → | White Basic | Orange | Black | Red | Tall W.C. |
| --- | --- | --- | --- | --- | --- |
| **Blue** | ❌ T (20) | ❌ S (20) | ✅ S (6,20) | ❌ T (11) | — |
| **Light Blue** | ✅ S | ✅ T (1) | — | — | — |
| **Black** | — | — | ❌ S (5) | ✅ T (3) | — |

**ID Cup / OOD Bowl** — 5/8 (62%)

| Bowl ↓ / Cup → | White Basic | Orange | Black | Red | Tall W.C. |
| --- | --- | --- | --- | --- | --- |
| **Pink** | ✅ T | — | ❌ (16,18) | — | — |
| **Tall (light blue)** | ✅ T (6) | ❌ T (16) | ❌ (5,16) | ✅ S | — |
| **White** | — | ✅ S (3) | — | ✅ S | — |

**OOD Cup / ID Bowl** — 3/8 (38%)

| Bowl ↓ / Cup → | Brown | White Ceramic | Gray | Pink |
| --- | --- | --- | --- | --- |
| **Blue** | ✅ T | — | ✅ T (3) | ❌ T (11) |
| **Light Blue** | ❌ T (6,20) | ✅ T | — | ❌ (14,16) |
| **Black** | — | ❌ (16) | ❌ T (6,11) | — |

**OOD Cup / OOD Bowl** — 3/8 (38%)

| Bowl ↓ / Cup → | Brown | White Ceramic | Gray | Pink |
| --- | --- | --- | --- | --- |
| **Pink** | ❌ T (16) | — | — | ✅ S |
| **Tall (light blue)** | — | ❌ S (11) | ❌ (16,21) | ❌ T (11) |
| **White** | ✅ S | ✅ T (3) | ❌ S (11) | — |


### 5×3 SAP baseline — 22/48 (46%)

_Secondary baseline (SAP, not VLA) on the pouring task; the sheet header reads “1×1 X-ARM-SAP” but the grid is the same 5×3 task. Note numbers use the SAP legend below._

**ID Cup / ID Bowl** — 6/12 (50%)

| Bowl ↓ / Cup → | White Basic | Orange | Black | Red | Tall W.C. |
| --- | --- | --- | --- | --- | --- |
| **Blue** | ✅ S | ❌ (1,2) | ✅ S | ❌ (3) | — |
| **Light Blue** | ❌ S (3,4) | ✅ S | ❌ (3) | ✅ S (6) | — |
| **Black** | ✅ S (6) | ❌ (3) | ❌ (3) | ✅ S (4) | — |

**ID Cup / OOD Bowl** — 5/12 (42%)

| Bowl ↓ / Cup → | White Basic | Orange | Black | Red | Tall W.C. |
| --- | --- | --- | --- | --- | --- |
| **Pink** | ✅ S | ❌ (3) | ✅ S | ✅ S (7) | — |
| **Tall (light blue)** | ❌ S (8) | ❌ (3) | ❌ (3) | ❌ S (1,8) | — |
| **White** | ✅ S | ❌ (3) | ❌ (3) | ✅ S (9) | — |

**OOD Cup / ID Bowl** — 4/12 (33%)

| Bowl ↓ / Cup → | Brown | White Ceramic | Gray | Pink |
| --- | --- | --- | --- | --- |
| **Blue** | ❌ (3) | ✅ S | ❌ (3) | ❌ (3) |
| **Light Blue** | ✅ S | ✅ S | ❌ (3) | ❌ (3) |
| **Black** | ❌ (3) | ✅ S | ❌ (3) | ❌ (3) |

**OOD Cup / OOD Bowl** — 7/12 (58%)

| Bowl ↓ / Cup → | Brown | White Ceramic | Gray | Pink |
| --- | --- | --- | --- | --- |
| **Pink** | ❌ (3) | ✅ S | ✅ S (6) | ❌ (3) |
| **Tall (light blue)** | ❌ S (1,8) | ✅ S (11) | ✅ S (6) | ❌ (3) |
| **White** | ❌ (3) | ✅ S (6) | ✅ S (4) | ✅ S |


**Pouring notes (SAP baseline sheet):**
- 1. Spilled cup
- 2. F/T error
- 3. Missed handle
- 4. Self collision
- 5. Tapped the bowl during pour
- 6. Off-center pour
- 7. Bad return
- 8. Grabbed inside of cup
- 9. Slightly moved cup
- 10. Hooked on handle while grasping
- 11. Barely poured
- **Grasp:** S = side grasp, T = top grasp.

_Codes — Cups: WB White-Basic, O Orange, Bk Black, R Red, TWC Tall-White-Ceramic* (ID box); Br Brown, WC White-Ceramic, Gr Gray, P Pink (OOD). Bowls: BL Blue, LB Light-Blue, BK Black (ID); P Pink, TB Tall, W White (OOD)._

## Task 3 — Hang Cup on Mug Tree

_Dataset **Mug Tree Task** · config 5×1 · trained at 50 / ~100 / 150 demos · eval complete._

### 5×1 VLA @ 150 demos — ID cups 12/20 (60%)

_One object axis (fixed mug tree): each cup is run 5 times; no grasp tag. Tall-White-Ceramic (*) shown but not scored._

**ID cups**

| Cup ↓ / Trial → | 1 | 2 | 3 | 4 | 5 | Rate |
| --- | --- | --- | --- | --- | --- | --- |
| **White Basic** | ✅ | ✅ | ✅ | ✅ | ✅ | 100% (5/5) |
| **Orange** | ✅ (1) | ❌ (1,2) | ✅ (1) | ❌ (1,2) | ✅ | 60% (3/5) |
| **Black** | ❌ (3) | ❌ (3,4) | ❌ (3,4) | ❌ (3) | ❌ (3) | 0% (0/5) |
| **Red** | ✅ | ✅ | ✅ (4) | ❌ (3) | ✅ | 80% (4/5) |
| **Tall White Ceramic *** | ❌ (2) | ✅ | ✅ (1) | ❌ (2) | ❌ (3) | 40% (2/5) |

**OOD cups** — 14/25 (56%) so far

| Cup ↓ / Trial → | 1 | 2 | 3 | 4 | 5 | Rate |
| --- | --- | --- | --- | --- | --- | --- |
| **Brown** | ✅ | ❌ (1,3) | ✅ | ✅ (1) | ✅ (5) | 80% (4/5) |
| **White Ceramic** | ❌ (3) | ❌ (6) | ✅ | ❌ (7) | ✅ | 40% (2/5) |
| **Gray** | ✅ (1) | ✅ (1) | ✅ (1) | ❌ (2) | ❌ | 60% (3/5) |
| **Pink** | ❌ (2) | ✅ | ✅ | ❌ | ❌ | 40% (2/5) |
| **Purple** | ✅ | ✅ | ✅ | ❌ | ❌ (2) | 60% (3/5) |

_All five OOD cups (Brown, White-Ceramic, Gray, Pink, Purple) now run._

**Mug-tree notes:**
- 1. Pushed the tree
- 2. Hung on edge, so dropped cup
- 3. Dropped mug while not on branch
- 4. Tilted grasp on mug lip
- 5. Hanging mug on edge
- 6. Arm errored out
- 7. Tried to grab entire cup

_Codes — Cups: WB White-Basic, O Orange, Bk Black, R Red, TWC Tall-White-Ceramic* (ID); Br Brown, WC White-Ceramic, Gr Gray, P Pink, Pu Purple (OOD)._

## Appendix A — Coffee 4×4 VLA @ 150 demos (OLD run)

_Earlier run; Blue (OOD) machine not yet available (blank cells). Overall 46/48 (96%) of run trials._

**ID Cup / ID Machine** — 15/16 (94%)

| Machine ↓ / Cup → | White Basic | Orange | Black | Red |
| --- | --- | --- | --- | --- |
| **Keurig** | ✅ T | ✅ S | ❌ T | ✅ T |
| **Black** | ✅ S | ✅ T | ✅ S | ✅ T |
| **Teal** | ✅ S | ✅ S | ✅ S | ✅ T |
| **White** | ✅ S | ✅ T | ✅ T | ✅ T |

**ID Cup / OOD Machine** — 7/8 (88%)

| Machine ↓ / Cup → | White Basic | Orange | Black | Red |
| --- | --- | --- | --- | --- |
| **Red** | ✅ S | ✅ T | ✅ T | ✅ T |
| **Tastyle** | ❌ T | ✅ S | ✅ T | ✅ T |
| **Blue** | — | — | — | — |

**OOD Cup / ID Machine** — 16/16 (100%)

| Machine ↓ / Cup → | Brown | White Ceramic | Gray | Pink |
| --- | --- | --- | --- | --- |
| **Keurig** | ✅ S | ✅ T (O) | ✅ T | ✅ S |
| **Black** | ✅ T | ✅ S | ✅ T | ✅ S |
| **Teal** | ✅ S | ✅ S | ✅ T | ✅ S |
| **White** | ✅ T | ✅ T | ✅ T | ✅ S |

**OOD Cup / OOD Machine** — 8/8 (100%)

| Machine ↓ / Cup → | Brown | White Ceramic | Gray | Pink |
| --- | --- | --- | --- | --- |
| **Red** | ✅ T | ✅ S (*) | ✅ T | ✅ S |
| **Tastyle** | ✅ T | ✅ S (**) | ✅ T | ✅ S |
| **Blue** | — | — | — | — |

## Appendix B — Secondary baseline: SAP

SAP is the secondary baseline. The **pouring** eval is now filled in (see Task 2 — 5×3 SAP baseline). The coffee configs remain blank templates:

- X-ARM · SAP · 1x1
- X-ARM · SAP · 4x4

## Appendix C — Optional baselines: Diffusion Policy & R2R2R (may not run)

DP and R2R2R are kept as an **option** — we may not run these:

- X-ARM · DP · 1x1
- X-ARM · DP · 4x4
- X-ARM · R2R2R · 1x1
- X-ARM · R2R2R · 4x4

## Appendix D — Empty grids for pending dataset sizes (fill in later)

_Blank templates for the dataset sizes not yet evaluated; fill in as each eval completes (sizes already done are omitted)._

### Cup on Coffee Machine — 1×1 VLA @ 50 demos (blank)

**ID Cup / ID Machine**

| Machine ↓ / Cup → | White Basic | Orange | Black | Red |
| --- | --- | --- | --- | --- |
| **Keurig** |  |  |  |  |
| **Black** |  |  |  |  |
| **Teal** |  |  |  |  |
| **White** |  |  |  |  |

**ID Cup / OOD Machine**

| Machine ↓ / Cup → | White Basic | Orange | Black | Red |
| --- | --- | --- | --- | --- |
| **Red** |  |  |  |  |
| **Tastyle** |  |  |  |  |
| **Blue** |  |  |  |  |

**OOD Cup / ID Machine**

| Machine ↓ / Cup → | Brown | White Ceramic | Gray | Pink |
| --- | --- | --- | --- | --- |
| **Keurig** |  |  |  |  |
| **Black** |  |  |  |  |
| **Teal** |  |  |  |  |
| **White** |  |  |  |  |

**OOD Cup / OOD Machine**

| Machine ↓ / Cup → | Brown | White Ceramic | Gray | Pink |
| --- | --- | --- | --- | --- |
| **Red** |  |  |  |  |
| **Tastyle** |  |  |  |  |
| **Blue** |  |  |  |  |

### Cup on Coffee Machine — 1×1 VLA @ 100 demos (blank)

**ID Cup / ID Machine**

| Machine ↓ / Cup → | White Basic | Orange | Black | Red |
| --- | --- | --- | --- | --- |
| **Keurig** |  |  |  |  |
| **Black** |  |  |  |  |
| **Teal** |  |  |  |  |
| **White** |  |  |  |  |

**ID Cup / OOD Machine**

| Machine ↓ / Cup → | White Basic | Orange | Black | Red |
| --- | --- | --- | --- | --- |
| **Red** |  |  |  |  |
| **Tastyle** |  |  |  |  |
| **Blue** |  |  |  |  |

**OOD Cup / ID Machine**

| Machine ↓ / Cup → | Brown | White Ceramic | Gray | Pink |
| --- | --- | --- | --- | --- |
| **Keurig** |  |  |  |  |
| **Black** |  |  |  |  |
| **Teal** |  |  |  |  |
| **White** |  |  |  |  |

**OOD Cup / OOD Machine**

| Machine ↓ / Cup → | Brown | White Ceramic | Gray | Pink |
| --- | --- | --- | --- | --- |
| **Red** |  |  |  |  |
| **Tastyle** |  |  |  |  |
| **Blue** |  |  |  |  |

### Cup on Coffee Machine — 4×4 VLA @ 50 demos (blank)

**ID Cup / ID Machine**

| Machine ↓ / Cup → | White Basic | Orange | Black | Red |
| --- | --- | --- | --- | --- |
| **Keurig** |  |  |  |  |
| **Black** |  |  |  |  |
| **Teal** |  |  |  |  |
| **White** |  |  |  |  |

**ID Cup / OOD Machine**

| Machine ↓ / Cup → | White Basic | Orange | Black | Red |
| --- | --- | --- | --- | --- |
| **Red** |  |  |  |  |
| **Tastyle** |  |  |  |  |
| **Blue** |  |  |  |  |

**OOD Cup / ID Machine**

| Machine ↓ / Cup → | Brown | White Ceramic | Gray | Pink |
| --- | --- | --- | --- | --- |
| **Keurig** |  |  |  |  |
| **Black** |  |  |  |  |
| **Teal** |  |  |  |  |
| **White** |  |  |  |  |

**OOD Cup / OOD Machine**

| Machine ↓ / Cup → | Brown | White Ceramic | Gray | Pink |
| --- | --- | --- | --- | --- |
| **Red** |  |  |  |  |
| **Tastyle** |  |  |  |  |
| **Blue** |  |  |  |  |

### Cup on Coffee Machine — 4×4 VLA @ 100 demos (blank)

**ID Cup / ID Machine**

| Machine ↓ / Cup → | White Basic | Orange | Black | Red |
| --- | --- | --- | --- | --- |
| **Keurig** |  |  |  |  |
| **Black** |  |  |  |  |
| **Teal** |  |  |  |  |
| **White** |  |  |  |  |

**ID Cup / OOD Machine**

| Machine ↓ / Cup → | White Basic | Orange | Black | Red |
| --- | --- | --- | --- | --- |
| **Red** |  |  |  |  |
| **Tastyle** |  |  |  |  |
| **Blue** |  |  |  |  |

**OOD Cup / ID Machine**

| Machine ↓ / Cup → | Brown | White Ceramic | Gray | Pink |
| --- | --- | --- | --- | --- |
| **Keurig** |  |  |  |  |
| **Black** |  |  |  |  |
| **Teal** |  |  |  |  |
| **White** |  |  |  |  |

**OOD Cup / OOD Machine**

| Machine ↓ / Cup → | Brown | White Ceramic | Gray | Pink |
| --- | --- | --- | --- | --- |
| **Red** |  |  |  |  |
| **Tastyle** |  |  |  |  |
| **Blue** |  |  |  |  |

### Cup Pouring (into bowl) — 5×3 VLA @ 50 demos (blank)

**ID Cup / ID Bowl**

| Bowl ↓ / Cup → | White Basic | Orange | Black | Red | Tall W.C. |
| --- | --- | --- | --- | --- | --- |
| **Blue** |  |  |  |  |  |
| **Light Blue** |  |  |  |  |  |
| **Black** |  |  |  |  |  |

**ID Cup / OOD Bowl**

| Bowl ↓ / Cup → | White Basic | Orange | Black | Red | Tall W.C. |
| --- | --- | --- | --- | --- | --- |
| **Pink** |  |  |  |  |  |
| **Tall (light blue)** |  |  |  |  |  |
| **White** |  |  |  |  |  |

**OOD Cup / ID Bowl**

| Bowl ↓ / Cup → | Brown | White Ceramic | Gray | Pink |
| --- | --- | --- | --- | --- |
| **Blue** |  |  |  |  |
| **Light Blue** |  |  |  |  |
| **Black** |  |  |  |  |

**OOD Cup / OOD Bowl**

| Bowl ↓ / Cup → | Brown | White Ceramic | Gray | Pink |
| --- | --- | --- | --- | --- |
| **Pink** |  |  |  |  |
| **Tall (light blue)** |  |  |  |  |
| **White** |  |  |  |  |

### Cup Pouring (into bowl) — 5×3 VLA @ 105 demos (blank)

**ID Cup / ID Bowl**

| Bowl ↓ / Cup → | White Basic | Orange | Black | Red | Tall W.C. |
| --- | --- | --- | --- | --- | --- |
| **Blue** |  |  |  |  |  |
| **Light Blue** |  |  |  |  |  |
| **Black** |  |  |  |  |  |

**ID Cup / OOD Bowl**

| Bowl ↓ / Cup → | White Basic | Orange | Black | Red | Tall W.C. |
| --- | --- | --- | --- | --- | --- |
| **Pink** |  |  |  |  |  |
| **Tall (light blue)** |  |  |  |  |  |
| **White** |  |  |  |  |  |

**OOD Cup / ID Bowl**

| Bowl ↓ / Cup → | Brown | White Ceramic | Gray | Pink |
| --- | --- | --- | --- | --- |
| **Blue** |  |  |  |  |
| **Light Blue** |  |  |  |  |
| **Black** |  |  |  |  |

**OOD Cup / OOD Bowl**

| Bowl ↓ / Cup → | Brown | White Ceramic | Gray | Pink |
| --- | --- | --- | --- | --- |
| **Pink** |  |  |  |  |
| **Tall (light blue)** |  |  |  |  |
| **White** |  |  |  |  |

### Hang Cup on Mug Tree — 5×1 VLA @ 50 demos (blank)

**ID cups**

| Cup ↓ / Trial → | 1 | 2 | 3 | 4 | 5 | Rate |
| --- | --- | --- | --- | --- | --- | --- |
| **White Basic** |  |  |  |  |  |  |
| **Orange** |  |  |  |  |  |  |
| **Black** |  |  |  |  |  |  |
| **Red** |  |  |  |  |  |  |
| **Tall White Ceramic *** |  |  |  |  |  |  |

**OOD cups**

| Cup ↓ / Trial → | 1 | 2 | 3 | 4 | 5 | Rate |
| --- | --- | --- | --- | --- | --- | --- |
| **Brown** |  |  |  |  |  |  |
| **White Ceramic** |  |  |  |  |  |  |
| **Gray** |  |  |  |  |  |  |
| **Pink** |  |  |  |  |  |  |
| **Purple** |  |  |  |  |  |  |

### Hang Cup on Mug Tree — 5×1 VLA @ 100 demos (blank)

**ID cups**

| Cup ↓ / Trial → | 1 | 2 | 3 | 4 | 5 | Rate |
| --- | --- | --- | --- | --- | --- | --- |
| **White Basic** |  |  |  |  |  |  |
| **Orange** |  |  |  |  |  |  |
| **Black** |  |  |  |  |  |  |
| **Red** |  |  |  |  |  |  |
| **Tall White Ceramic *** |  |  |  |  |  |  |

**OOD cups**

| Cup ↓ / Trial → | 1 | 2 | 3 | 4 | 5 | Rate |
| --- | --- | --- | --- | --- | --- | --- |
| **Brown** |  |  |  |  |  |  |
| **White Ceramic** |  |  |  |  |  |  |
| **Gray** |  |  |  |  |  |  |
| **Pink** |  |  |  |  |  |  |
| **Purple** |  |  |  |  |  |  |
