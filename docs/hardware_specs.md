# Hardware & Electrical Specifications

## Fan: Delta Electronics PFB0412EN-E

The **Delta PFB0412EN-E** is an ultra-high performance 40x40x28mm DC axial fan originally engineered for high-density 1U server racks. It delivers extreme static pressure, making it capable of forcing air through dense laptop copper fin stacks.

### Technical Data
* **Dimensions:** 40 mm × 40 mm × 28 mm
* **Rated Voltage:** 12.0 V DC
* **Operating Voltage Range:** 7.0 V to 13.2 V DC
* **Input Current:** 0.64 A (nominal) / 0.77 A (max)
* **Input Power:** ~7.68 W
* **Speed:** ~13,000 RPM
* **Mounting Hole Pitch:** 32.0 mm × 32.0 mm
* **Hole Diameter:** 3.2 mm (M3 screw clearance)

---

## 4-Wire Pinout

| Pin | Wire Color | Signal | Description |
| :---: | :---: | :---: | :--- |
| **1** | **Black** | `GND` | System ground reference |
| **2** | **Red** | `+12V` | DC power supply input |
| **3** | **Yellow** | `TACH` | Tachometer / Frequency Generator (2 pulses/rev, open collector) |
| **4** | **Blue** | `PWM` | Pulse Width Modulation speed control (25 kHz target) |

---

## Powering from USB 5V (Portable Setup)

To run this 12V fan from a standard laptop USB port (5V 1A/2A) or power bank:

1. **Boost Converter:** Use an **MT3608** or **XL6009** DC-DC step-up module.
2. **Wiring:**
   * `USB 5V (+)` ──► `VIN+` of MT3608
   * `USB GND (-)` ──► `VIN-` of MT3608
   * Multimeter on `VOUT+` / `VOUT-` ──► Adjust trim pot until output reads **9.0V – 12.0V**.
   * `VOUT+` ──► Fan Red Wire
   * `VOUT-` ──► Fan Black Wire

*(Tip: Running at 9V–10V provides ~80% of max airflow with a substantial noise reduction compared to full 12V).*
