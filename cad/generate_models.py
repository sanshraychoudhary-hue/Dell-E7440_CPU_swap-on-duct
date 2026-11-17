import os
import math
import numpy as np
from manifold3d import Manifold
import trimesh
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

WORKSPACE_DIR = r"c:\Users\sansh\Downloads\projectDellE7440FanEnclosure"
BRAIN_DIR = r"C:\Users\sansh\.gemini\antigravity\brain\e34c7fec-1028-4b69-8611-872c933bb651"

DUCT_STL_PATH      = os.path.join(WORKSPACE_DIR, "dell_e7440_universal_duct.stl")
DELTA40_STL_PATH   = os.path.join(WORKSPACE_DIR, "faceplate_delta_4028.stl")
FAN60_STL_PATH     = os.path.join(WORKSPACE_DIR, "faceplate_60mm_fan.stl")
COMBO_STL_PATH     = os.path.join(WORKSPACE_DIR, "dell_e7440_fan_enclosure_prototype.stl")
PREVIEW_IMG_PATH   = os.path.join(BRAIN_DIR, "prototype_views.png")
SCAD_PATH          = os.path.join(WORKSPACE_DIR, "dell_e7440_fan_duct.scad")

# -------------------------------------------------------------
# 1. PARAMETERS (mm) - EXACT MEASUREMENTS & MODULAR SPECS
# -------------------------------------------------------------
laptop_t     = 14.0   # User measurement: 1.4 cm max laptop thickness
vent_w       = 58.0   # User measurement: 5.8 cm vent width
vent_h       = 10.0   # User measurement: 1.0 cm vent height
clip_w       = 70.0   # 70mm width (seals 6mm past 58mm vent)

lip_top_l    = 23.0   # User exact measurement: 2.3 cm (23.0mm) deck overlap
lip_bot_l    = 18.0   # Bottom clamping lip (18.0mm)
t_wall       = 1.6    # Uniform 1.6mm thin shell for hollow cone
t_tip        = 0.75   # Ultra-thin 0.75mm flexible compliant tip

cone_l       = 32.0   # Aerodynamic transition cone length

# Universal Slide-in Plate & Receiver Slot
plate_w      = 60.0   # Standard universal plate width
plate_h      = 60.0   # Standard universal plate height
plate_t      = 3.5    # 3.5mm thick rigid slide-in plate

slot_w       = 60.8   # 0.8mm total sliding clearance
slot_t       = 4.0    # 0.5mm thickness clearance
rail_lip     = 3.0    # 3mm front retaining rail overlap
rail_t       = 2.2    # 2.2mm front retaining rail thickness

frame_w      = slot_w + 2 * 3.2 # 67.2mm outer receiver width
frame_h      = plate_h + t_wall # 61.6mm outer receiver height
fan_cz       = plate_h / 2.0    # 30.0mm (center of fan axis)

# Delta PFB0412EN-E (40x40x28mm) specs:
delta_hole_pitch = 32.0 # 32mm center-to-center
delta_hole_d     = 3.2  # M3 screw clearance hole
delta_bore       = 38.0 # 38mm circular blade cutout

# Standard 60mm fan specs (bonus plate):
fan60_pitch      = 50.0 # 50mm center-to-center
fan60_hole_d     = 4.2  # M4 screw hole
fan60_bore       = 54.0 # 54mm circular cutout

print("Generating Modular Universal Duct and Delta 4028 Faceplate...")

# -------------------------------------------------------------
# 2. BUILD UNIVERSAL DUCT (WITH SLIDE-IN RECEIVER SLOT)
# -------------------------------------------------------------
# 2.1 Clip Base (Exact 23mm top lip, 14mm slot)
clip_outer = Manifold.cube([lip_top_l, clip_w, laptop_t + 2*t_wall], center=False).translate([-lip_top_l, -clip_w/2, -t_wall])
laptop_slot = Manifold.cube([lip_top_l + 2.0, clip_w + 4.0, laptop_t + 0.2], center=False).translate([-lip_top_l - 1.0, -clip_w/2 - 2.0, 0])
bottom_cut = Manifold.cube([lip_top_l - lip_bot_l, clip_w + 4.0, t_wall + 2.0], center=False).translate([-lip_top_l - 1.0, -clip_w/2 - 2.0, -t_wall - 1.0])

taper_angle_top = -(t_wall - t_tip) / lip_top_l * (180.0 / math.pi)
taper_top = Manifold.cube([lip_top_l + 2.0, clip_w + 4.0, 5.0], center=False).rotate([0, taper_angle_top, 0]).translate([-lip_top_l - 1.0, -clip_w/2 - 2.0, laptop_t + t_tip])

taper_angle_bot = (t_wall - t_tip) / lip_bot_l * (180.0 / math.pi)
taper_bot = Manifold.cube([lip_bot_l + 2.0, clip_w + 4.0, 5.0], center=False).rotate([0, taper_angle_bot, 0]).translate([-lip_bot_l - 1.0, -clip_w/2 - 2.0, -t_tip - 5.0])

chamfer_top = Manifold.cube([3.0, clip_w + 4.0, 3.0], center=False).rotate([0, 30, 0]).translate([-lip_top_l, -clip_w/2 - 2.0, laptop_t])
chamfer_bot = Manifold.cube([3.0, clip_w + 4.0, 3.0], center=False).rotate([0, 30, 0]).translate([-lip_bot_l, -clip_w/2 - 2.0, 0])

clip = clip_outer - laptop_slot - bottom_cut - taper_top - taper_bot - chamfer_top - chamfer_bot

# 2.2 Transition Cone Outer Shell
start_outer = Manifold.cube([0.5, clip_w, laptop_t + 2*t_wall], center=False).translate([0, -clip_w/2, -t_wall])
end_outer   = Manifold.cube([0.5, frame_w, frame_h], center=False).translate([cone_l - 0.5, -frame_w/2, -t_wall])
duct_outer  = (start_outer + end_outer).hull()

# 2.3 Universal Receiver Frame (X: cone_l to cone_l + slot_t + rail_t)
receiver_block = Manifold.cube([slot_t + rail_t, frame_w, frame_h], center=False).translate([cone_l, -frame_w/2, -t_wall])

# Top-loading slide-in slot cut
slot_cut = Manifold.cube([slot_t, slot_w, plate_h + 10.0], center=False).translate([cone_l, -slot_w/2, 0])

# Front window opening between side retaining rails
window_w = slot_w - 2*rail_lip
window_cut = Manifold.cube([rail_t + 2.0, window_w, plate_h - rail_lip], center=False).translate([cone_l + slot_t - 0.5, -window_w/2, rail_lip])

# 2.4 Hollow Airway (From laptop throat to backing circular port)
start_inner = Manifold.cube([1.0, clip_w - 2*t_wall, laptop_t], center=False).translate([-0.5, -(clip_w - 2*t_wall)/2, 0])
backing_bore = Manifold.cylinder(2.0, 52.0/2, center=False, circular_segments=64).rotate([0, 90, 0]).translate([cone_l - 1.0, 0, fan_cz])
airway = (start_inner + backing_bore).hull()
thru_bore = Manifold.cylinder(slot_t + 2.0, 52.0/2, center=False, circular_segments=64).rotate([0, 90, 0]).translate([cone_l - 1.0, 0, fan_cz])

duct_solid = (clip + duct_outer + receiver_block) - airway - thru_bore - slot_cut - window_cut

m_duct = duct_solid.to_mesh()
mesh_duct = trimesh.Trimesh(vertices=m_duct.vert_properties[:, :3], faces=m_duct.tri_verts)
mesh_duct.fix_normals()
print(f"Universal Duct: Triangles={len(mesh_duct.faces)}, Watertight={mesh_duct.is_watertight}")
mesh_duct.export(DUCT_STL_PATH)

# -------------------------------------------------------------
# 3. BUILD DELTA PFB0412EN-E (40x40x28mm) SLIDE-IN FACEPLATE
# -------------------------------------------------------------
plate_box = Manifold.cube([plate_t, plate_w, plate_h], center=False).translate([0, -plate_w/2, 0])

# Circular blade cutout (38mm)
fan_40_bore = Manifold.cylinder(plate_t + 2.0, delta_bore/2, center=False, circular_segments=64).rotate([0, 90, 0]).translate([-1.0, 0, fan_cz])

# 4x M3 screw holes (32x32mm pitch)
plate_delta = plate_box - fan_40_bore
for dy in [-delta_hole_pitch/2, delta_hole_pitch/2]:
    for dz in [-delta_hole_pitch/2, delta_hole_pitch/2]:
        hole = Manifold.cylinder(plate_t + 2.0, delta_hole_d/2, center=False, circular_segments=32).rotate([0, 90, 0]).translate([-1.0, dy, fan_cz + dz])
        plate_delta = plate_delta - hole

# Convenient top pull-tab (18mm wide, 4mm tall) for easy slide-in & removal
top_tab = Manifold.cube([plate_t, 18.0, 4.0], center=False).translate([0, -9.0, plate_h])
plate_delta = plate_delta + top_tab

m_delta = plate_delta.to_mesh()
mesh_delta = trimesh.Trimesh(vertices=m_delta.vert_properties[:, :3], faces=m_delta.tri_verts)
mesh_delta.fix_normals()
print(f"Delta 4028 Plate: Triangles={len(mesh_delta.faces)}, Watertight={mesh_delta.is_watertight}")
mesh_delta.export(DELTA40_STL_PATH)

# -------------------------------------------------------------
# 4. BUILD BONUS 60MM SLIDE-IN FACEPLATE
# -------------------------------------------------------------
plate_60 = plate_box - Manifold.cylinder(plate_t + 2.0, fan60_bore/2, center=False, circular_segments=64).rotate([0, 90, 0]).translate([-1.0, 0, fan_cz])
for dy in [-fan60_pitch/2, fan60_pitch/2]:
    for dz in [-fan60_pitch/2, fan60_pitch/2]:
        hole = Manifold.cylinder(plate_t + 2.0, fan60_hole_d/2, center=False, circular_segments=32).rotate([0, 90, 0]).translate([-1.0, dy, fan_cz + dz])
        plate_60 = plate_60 - hole
plate_60 = plate_60 + top_tab

m_60 = plate_60.to_mesh()
mesh_60 = trimesh.Trimesh(vertices=m_60.vert_properties[:, :3], faces=m_60.tri_verts)
mesh_60.fix_normals()
print(f"60mm Plate: Triangles={len(mesh_60.faces)}, Watertight={mesh_60.is_watertight}")
mesh_60.export(FAN60_STL_PATH)

# Also export full assembled model (plate seated in duct) as default preview STL
plate_seated = plate_delta.translate([cone_l + 0.2, 0, 0])
assembled = duct_solid + plate_seated
m_combo = assembled.to_mesh()
mesh_combo = trimesh.Trimesh(vertices=m_combo.vert_properties[:, :3], faces=m_combo.tri_verts)
mesh_combo.fix_normals()
mesh_combo.export(COMBO_STL_PATH)
print(f"Exported combined assembly to: {COMBO_STL_PATH}")

# -------------------------------------------------------------
# 5. RENDER MULTI-PANEL ENGINEERING PREVIEW DIAGRAM
# -------------------------------------------------------------
fig = plt.figure(figsize=(16, 12), dpi=150)
fig.patch.set_facecolor('#1e1e2e')

# Panel 1: 3D Exploded / Slide-in View
ax1 = fig.add_subplot(2, 2, 1, projection='3d')
ax1.set_facecolor('#1e1e2e')

# Duct mesh
poly_duct = [mesh_duct.vertices[f] for f in mesh_duct.faces[::2]]
col_duct = Poly3DCollection(poly_duct, alpha=0.88, edgecolor='#11111b', linewidth=0.1)
col_duct.set_facecolor('#89b4fa')
ax1.add_collection3d(col_duct)

# Floating Plate sliding into slot (shown raised by +25mm Z to illustrate slide-in action!)
plate_raised_verts = mesh_delta.vertices.copy()
plate_raised_verts[:, 0] += (cone_l + 0.2)
plate_raised_verts[:, 2] += 25.0 # Raised in Z
poly_plate = [plate_raised_verts[f] for f in mesh_delta.faces[::2]]
col_plate = Poly3DCollection(poly_plate, alpha=0.95, edgecolor='#11111b', linewidth=0.1)
col_plate.set_facecolor('#f38ba8')
ax1.add_collection3d(col_plate)

# Slide-in arrow in 3D
ax1.quiver(cone_l + 1.8, 0, 85, 0, 0, -20, color='#a6e3a1', arrow_length_ratio=0.3, linewidth=3)
ax1.text(cone_l + 2, 0, 88, 'Slide-In Action', color='#a6e3a1', fontweight='bold', fontsize=10, ha='center')

# Ghost Laptop edge (14mm thickness)
for y_pos in [-40, 40]:
    ax1.plot([-30, 0, 0, -30, -30], [y_pos]*5, [0, 0, laptop_t, laptop_t, 0], color='#f38ba8', linestyle='--', linewidth=1.5)
ax1.plot([-30, -30], [-40, 40], [laptop_t, laptop_t], color='#f38ba8', linestyle='--', linewidth=1.5, label='Dell E7440 Ghost')

ax1.set_title("1. Modular Slide-In Action (Plate Inserts from Top)", color='#cdd6f4', fontsize=13, fontweight='bold', pad=12)
ax1.view_init(elev=24, azim=-128)
ax1.set_xlim([-35, 45])
ax1.set_ylim([-42, 42])
ax1.set_zlim([-10, 95])
ax1.set_xlabel('X mm', color='#a6adc8')
ax1.set_ylabel('Y mm', color='#a6adc8')
ax1.set_zlabel('Z mm', color='#a6adc8')
ax1.tick_params(colors='#a6adc8')

# Panel 2: Side Profile Cross-Section (Slide Slot & Receiver)
ax2 = fig.add_subplot(2, 2, 2)
ax2.set_facecolor('#181825')

# Outer duct profile
total_x = cone_l + slot_t + rail_t
outer_wall_x = [-lip_bot_l, 0, cone_l, total_x, total_x, cone_l, 0, -lip_top_l, -lip_top_l, 0, 0, -lip_bot_l, -lip_bot_l]
outer_wall_z = [-t_wall, -t_wall, -t_wall, -t_wall, 61.6, 61.6, laptop_t + t_wall, laptop_t + t_tip, laptop_t, laptop_t, 0, 0, -t_wall]

# Inner hollow cavity
inner_hollow_x = [0, cone_l, cone_l, 0, 0]
inner_hollow_z = [0, 4.0, 56.0, laptop_t, 0]

ax2.fill(outer_wall_x, outer_wall_z, color='#89b4fa', alpha=0.9, label='Universal Duct Body')
ax2.fill(inner_hollow_x, inner_hollow_z, color='#181825', label='100% Hollow Interior')

# Slide-in Slot cross-section
slot_poly_x = [cone_l, cone_l + slot_t, cone_l + slot_t, cone_l]
slot_poly_z = [0, 0, 60.0, 60.0]
ax2.fill(slot_poly_x, slot_poly_z, color='#f38ba8', alpha=0.8, label='Slide-in Plate Slot (4mm gap)')

# Front retaining rail
rail_poly_x = [cone_l + slot_t, total_x, total_x, cone_l + slot_t]
rail_poly_z = [0, 0, 3.0, 3.0]
ax2.fill(rail_poly_x, rail_poly_z, color='#cba6f7', label='Front Retaining Lip')

# Laptop ghost
ax2.fill([-45, 0, 0, -45], [0, 0, laptop_t, laptop_t], color='#45475a', alpha=0.6, label='Dell E7440 (14mm)')

# Annotations
ax2.annotate('Slide-in Plate Slot\n(Top-loading, bottoms out at Z=0)', xy=(cone_l + 2, 35), xytext=(cone_l - 18, 55),
             arrowprops=dict(facecolor='#f38ba8', edgecolor='#f38ba8', shrink=0.08, width=1.5, headwidth=6),
             color='#f38ba8', fontweight='bold', fontsize=10, ha='center')

ax2.annotate('C = 23mm Lip\n(14mm Chassis Slot)', xy=(-12, 14), xytext=(-35, 28),
             arrowprops=dict(facecolor='#a6e3a1', edgecolor='#a6e3a1', shrink=0.08, width=1.5, headwidth=6),
             color='#a6e3a1', fontweight='bold', fontsize=10, ha='center')

ax2.set_xlim([-50, 50])
ax2.set_ylim([-25, 75])
ax2.set_aspect('equal')
ax2.set_title("2. Side Profile (Universal Top-Loading Receiver Track)", color='#cdd6f4', fontsize=13, fontweight='bold')
ax2.set_xlabel('X Dimension (mm)', color='#a6adc8')
ax2.set_ylabel('Z Dimension (mm)', color='#a6adc8')
ax2.grid(True, color='#313244', linestyle=':')
ax2.tick_params(colors='#a6adc8')
ax2.legend(loc='lower left', facecolor='#1e1e2e', edgecolor='#313244', labelcolor='#cdd6f4', fontsize=8)

# Panel 3: Delta PFB0412EN-E Faceplate Technical Drawing
ax3 = fig.add_subplot(2, 2, 3)
ax3.set_facecolor('#181825')

# 60x60 carrier plate
ax3.fill([-30, 30, 30, -30], [0, 0, 60, 60], color='#f38ba8', alpha=0.85, label='60x60mm Carrier Plate (3.5mm thick)')

# Top pull-tab
ax3.fill([-9, 9, 9, -9], [60, 60, 64, 64], color='#f9e2af', label='Top Pull-Tab (Easy Swapping)')

# 40x40 fan boundary outline (dashed)
ax3.plot([-20, 20, 20, -20, -20], [10, 10, 50, 50, 10], color='#ffffff', linestyle=':', linewidth=2, label='Delta 40x40mm Fan Footprint')

# 38mm circular bore
circ_t = np.linspace(0, 2*np.pi, 100)
ax3.fill(19.0 * np.cos(circ_t), 30.0 + 19.0 * np.sin(circ_t), color='#181825', label='38mm Blade Bore')

# 4x M3 screw holes (32x32 pitch)
for dy in [-16, 16]:
    for dz in [14, 46]:
        hc = plt.Circle((dy, dz), 1.6, color='#a6e3a1', ec='#11111b', lw=1.5)
        ax3.add_patch(hc)
ax3.plot([], [], 'o', color='#a6e3a1', label='4x M3 Screw Holes (32x32mm pitch)')

# Dimension arrows for 32mm pitch
ax3.annotate('', xy=(16, 46), xytext=(-16, 46), arrowprops=dict(arrowstyle='<->', color='#a6e3a1', lw=1.8))
ax3.text(0, 48, '32mm Pitch', color='#a6e3a1', fontsize=9, fontweight='bold', ha='center')

ax3.annotate('', xy=(16, 14), xytext=(16, 46), arrowprops=dict(arrowstyle='<->', color='#a6e3a1', lw=1.8))
ax3.text(19, 30, '32mm', color='#a6e3a1', fontsize=9, fontweight='bold', va='center')

ax3.set_xlim([-40, 40])
ax3.set_ylim([-5, 75])
ax3.set_aspect('equal')
ax3.set_title("3. Delta PFB0412EN-E (40x40x28mm) Custom Faceplate", color='#cdd6f4', fontsize=13, fontweight='bold')
ax3.set_xlabel('Y Dimension (mm)', color='#a6adc8')
ax3.set_ylabel('Z Dimension (mm)', color='#a6adc8')
ax3.grid(True, color='#313244', linestyle=':')
ax3.tick_params(colors='#a6adc8')
ax3.legend(loc='lower left', facecolor='#1e1e2e', edgecolor='#313244', labelcolor='#cdd6f4', fontsize=8)

# Panel 4: Front View (Assembled Faceplate in Receiver Frame)
ax4 = fig.add_subplot(2, 2, 4)
ax4.set_facecolor('#181825')

# Outer receiver frame (67.2 x 61.6mm)
ax4.fill([-frame_w/2, frame_w/2, frame_w/2, -frame_w/2], [-t_wall, -t_wall, 60, 60], color='#89b4fa', alpha=0.9, label='Duct Receiver Rails')

# Front window cutout (revealing plate)
ax4.fill([-window_w/2, window_w/2, window_w/2, -window_w/2], [rail_lip, rail_lip, 60, 60], color='#f38ba8', alpha=0.9, label='Delta 4028 Plate (Inserted)')

# Circular bore
ax4.fill(19.0 * np.cos(circ_t), 30.0 + 19.0 * np.sin(circ_t), color='#181825', label='Airflow Bore (38mm)')

# Top pull-tab protruding
ax4.fill([-9, 9, 9, -9], [60, 60, 64, 64], color='#f9e2af', label='Pull-Tab for Quick Swapping')

# 4x M3 screw holes
for dy in [-16, 16]:
    for dz in [14, 46]:
        hc = plt.Circle((dy, dz), 1.6, color='#a6e3a1', ec='#11111b', lw=1.5)
        ax4.add_patch(hc)

ax4.set_xlim([-42, 42])
ax4.set_ylim([-8, 75])
ax4.set_aspect('equal')
ax4.set_title("4. Front View — Assembled System (Locked by Rails)", color='#cdd6f4', fontsize=13, fontweight='bold')
ax4.set_xlabel('Y Dimension (mm)', color='#a6adc8')
ax4.set_ylabel('Z Dimension (mm)', color='#a6adc8')
ax4.grid(True, color='#313244', linestyle=':')
ax4.tick_params(colors='#a6adc8')
ax4.legend(loc='lower right', facecolor='#1e1e2e', edgecolor='#313244', labelcolor='#cdd6f4', fontsize=8)

plt.tight_layout()
plt.savefig(PREVIEW_IMG_PATH, facecolor=fig.get_facecolor(), edgecolor='none')
print(f"Rendered multi-panel views to: {PREVIEW_IMG_PATH}")
