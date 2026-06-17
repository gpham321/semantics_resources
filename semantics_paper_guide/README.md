# Thesis figure bundle — 2026-06-05

Curated figures + the source HTML guides + PDFs for the R2R2R / armlab_splat_tracking work.
Each `*_assets/` directory holds the figures embedded in the corresponding `<NAME>.html`
guide. Open the HTML guide in a browser to see captions + context for every figure.

| Folder | Source guide | What's in it |
|---|---|---|
| `3dvision_assets/` | `3DVISION.html` | Text-prompt → per-object splat distillation (kaizen/laptop hero, SAM3+SAM2 overlay, render-check 3-panel diagnostic incl. the broken-transform failure mode, stage-4 laptop-only frames, ground-seeded init seed grid, tracked-splat RGB overlay, HAMER hand-grasp, contact auto-tune sweep curve, settled-grasp signals, xArm gripper Phantom/Bohg overlay). |
| `camcal_assets/` | `CAMERA_ALIGNMENT.html` | Automated IsaacSim ↔ real RealSense camera pose match — SAM3 mask, IoU loss landscape, before/after pose visualizations. |
| `dualseed_assets/` | `DUALSEED_IK.html` | Seed-dependent IK over the 60-grasp pool — FK skeletons at most-divergent grasp #37, branch-gap bars, per-seed self-collision plot. |
| `pipeline_assets/` | `PIPELINE_RUN_GUIDE.html` | R2R2R mug-variant pipeline — HAMER + cousin generation + IK + data-gen rollout figures. |
| `perscale_assets/` | `PER_SCALE_GRASPS.html` | Cousin-mug grasps validated at 5 scales — ghost gripper viewer figures. |

## Other content

- **`PAPER_NOTES.pdf`** — written notes for the thesis.
- **`PAPER_OUTLINE.html`** — outline draft (open in browser).
- **`R2R2R_paper.pdf`** — the CVPR 2026 R2R2R paper PDF for reference.
- **`*.html`** — the inline-CSS, self-contained pipeline guides themselves. Each is
  fully viewable offline; figures resolve relative to the `_assets/` dirs in this
  bundle.

## Quick browse

```bash
# open the index of guides
xdg-open ~/Desktop/thesis_share_2026_06_05/PIPELINE_RUN_GUIDE.html
# or the 3D-vision distillation walkthrough (richest figures)
xdg-open ~/Desktop/thesis_share_2026_06_05/3DVISION.html
```

Total bundle size: ~21 MB.
