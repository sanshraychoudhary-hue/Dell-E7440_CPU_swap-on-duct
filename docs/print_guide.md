# 3D Printing & Slicing Guide

## Recommended Materials

| Material | Rating | Why |
| :--- | :---: | :--- |
| **PETG** | ⭐⭐⭐⭐⭐ **(Recommended)** | Glass transition temperature ($T_g \approx 75^\circ\text{C}$) withstands CPU exhaust heat. Excellent layer adhesion and spring elasticity for the compliant lip. |
| **ABS / ASA** | ⭐⭐⭐⭐⭐ | High heat resistance ($T_g \approx 100^\circ\text{C}$). Ideal if your printer has an enclosure. |
| **PLA** | ⭐⭐ | Suitable for fit-testing only. Under heavy CPU load ($>60^\circ\text{C}$ exhaust), PLA will soften and lose clamp tension over time. |

---

## Slicer Settings (Cura / PrusaSlicer / Bambu Studio)

* **Nozzle Diameter:** `0.4 mm`
* **Layer Height:** `0.20 mm` (optimal balance between strength and the $0.75\text{ mm}$ flexible tip)
* **Wall Line Count (Perimeters):** `4 walls` (ensures the $1.6\text{ mm}$ thin shell is 100% solid perimeters)
* **Top/Bottom Layers:** `4 layers`
* **Infill:** `30% Gyroid` (only used in the receiver rails; the duct cone is a hollow shell)
* **Supports:** **DISABLED (0% Supports Needed)**
  * The transition cone slopes at 65°–70° from horizontal, which bridges cleanly without supports.
* **Orientation:**
  * **`dell_e7440_universal_duct.stl`:** Lay the flat front receiver face on the print bed.
  * **`faceplate_delta_4028.stl`:** Lay completely flat on the print bed (prints in ~15 minutes).

---

## Post-Processing & Gasket

1. **Deburr:** Lightly remove any elephant's foot on the slide-in plate edges so it drops smoothly into the duct track.
2. **Airtight Foam Gasket (Optional):** Apply a 1mm thin strip of craft foam or silicone tape to the inner roof of the 23mm deck lip for a 100% airtight seal against the laptop chassis.
