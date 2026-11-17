// Dell Latitude E7440 Modular Universal Fan Duct & Slide-in Faceplate System
// Parametric OpenSCAD Model

$fn = 64;

// -------------------------------------------------------------
// SELECT WHAT TO RENDER:
// 1 = Full Assembled Preview (Duct + Delta 4028 Plate inserted)
// 2 = Universal Duct Only (Prints alone)
// 3 = Delta PFB0412EN-E (40x40x28mm) Slide-in Faceplate Only
// 4 = Bonus 60mm Fan Slide-in Faceplate Only
// -------------------------------------------------------------
render_mode = 1;

// 1. LAPTOP & VENT EXACT MEASUREMENTS (mm)
laptop_thick     = 14.0; // User measurement: 1.4 cm max laptop thickness
vent_width       = 58.0; // User measurement: 5.8 cm vent width
vent_height      = 10.0; // User measurement: 1.0 cm vent height

// 2. CLAMP / COMPLIANT LIP DIMENSIONS (mm)
top_lip_length   = 23.0; // User exact measurement: 2.3 cm deck overlap
bottom_lip_length= 18.0; // Bottom base overlap (18mm)
clip_width       = 70.0; // 70mm width (seals 6mm past 58mm vent)
t_wall           = 1.6;  // Uniform thin shell wall thickness
t_tip            = 0.75; // Ultra-thin, flexible tip

// 3. DUCT CONE & UNIVERSAL RECEIVER (mm)
cone_length      = 32.0; // Transition cone length
plate_w          = 60.0; // Universal carrier plate width
plate_h          = 60.0; // Universal carrier plate height
plate_t          = 3.5;  // Carrier plate thickness

slot_w           = 60.8; // Slide-in slot width (0.8mm clearance)
slot_t           = 4.0;  // Slide-in slot thickness (0.5mm clearance)
rail_lip         = 3.0;  // Front retaining lip overlap on sides
rail_t           = 2.2;  // Front retaining lip thickness

frame_w          = slot_w + 2 * 3.2; // 67.2mm outer receiver width
frame_h          = plate_h + t_wall;  // 61.6mm outer receiver height
fan_cz           = plate_h / 2.0;     // 30.0mm (airway axis height)

// 4. DELTA PFB0412EN-E (40x40x28mm) SPECS
delta_hole_pitch = 32.0; // 32mm center-to-center
delta_hole_d     = 3.2;  // M3 screw hole
delta_bore       = 38.0; // 38mm blade opening

// 5. BONUS 60MM FAN SPECS
fan60_pitch      = 50.0; // 50mm center-to-center
fan60_hole_d     = 4.2;  // M4 screw hole
fan60_bore       = 54.0; // 54mm blade opening


module clip_base() {
    difference() {
        translate([-top_lip_length, -clip_width/2, -t_wall])
            cube([top_lip_length, clip_width, laptop_thick + 2*t_wall]);
        
        // Laptop slot (14.2mm for smooth fit)
        translate([-top_lip_length - 1, -clip_width/2 - 1, 0])
            cube([top_lip_length + 2, clip_width + 2, laptop_thick + 0.2]);
        
        // Shorter bottom lip cut
        translate([-top_lip_length - 1, -clip_width/2 - 1, -t_wall - 1])
            cube([top_lip_length - bottom_lip_length + 1, clip_width + 2, t_wall + 2]);
    }
}

module duct_transition() {
    hull() {
        translate([0, -clip_width/2, -t_wall])
            cube([0.5, clip_width, laptop_thick + 2*t_wall]);
        
        translate([cone_length - 0.5, -frame_w/2, -t_wall])
            cube([0.5, frame_w, frame_h]);
    }
}

module receiver_frame() {
    difference() {
        // Outer receiver block
        translate([cone_length, -frame_w/2, -t_wall])
            cube([slot_t + rail_t, frame_w, frame_h]);
        
        // Slide-in slot (open at top Z > plate_h)
        translate([cone_length, -slot_w/2, 0])
            cube([slot_t, slot_w, plate_h + 10]);
        
        // Front window between retaining rails
        translate([cone_length + slot_t - 0.5, -(slot_w - 2*rail_lip)/2, rail_lip])
            cube([rail_t + 2, slot_w - 2*rail_lip, plate_h - rail_lip + 10]);
    }
}

module inner_airway() {
    hull() {
        translate([-1, -(clip_width - 2*t_wall)/2, 0])
            cube([1.5, clip_width - 2*t_wall, laptop_thick]);
        
        translate([cone_length - 0.5, 0, fan_cz])
            rotate([0, 90, 0])
                cylinder(d = 52.0, h = 1.0);
    }
    
    // Pass-through bore to receiver slot
    translate([cone_length - 1, 0, fan_cz])
        rotate([0, 90, 0])
            cylinder(d = 52.0, h = slot_t + 2);
}

module universal_duct() {
    difference() {
        union() {
            clip_base();
            duct_transition();
            receiver_frame();
        }
        inner_airway();
    }
}

module faceplate_delta_4028() {
    difference() {
        union() {
            // Main 60x60 carrier plate
            translate([0, -plate_w/2, 0])
                cube([plate_t, plate_w, plate_h]);
            
            // Top pull-tab for easy slide-in & removal
            translate([0, -9, plate_h])
                cube([plate_t, 18, 4]);
        }
        
        // 38mm circular bore
        translate([-1, 0, fan_cz])
            rotate([0, 90, 0])
                cylinder(d = delta_bore, h = plate_t + 2);
        
        // 4x M3 screw holes (32x32mm pitch)
        for (dy = [-delta_hole_pitch/2, delta_hole_pitch/2]) {
            for (dz = [-delta_hole_pitch/2, delta_hole_pitch/2]) {
                translate([-1, dy, fan_cz + dz])
                    rotate([0, 90, 0])
                        cylinder(d = delta_hole_d, h = plate_t + 2);
            }
        }
    }
}

module faceplate_60mm() {
    difference() {
        union() {
            translate([0, -plate_w/2, 0])
                cube([plate_t, plate_w, plate_h]);
            
            translate([0, -9, plate_h])
                cube([plate_t, 18, 4]);
        }
        
        // 54mm circular bore
        translate([-1, 0, fan_cz])
            rotate([0, 90, 0])
                cylinder(d = fan60_bore, h = plate_t + 2);
        
        // 4x M4 screw holes (50x50mm pitch)
        for (dy = [-fan60_pitch/2, fan60_pitch/2]) {
            for (dz = [-fan60_pitch/2, fan60_pitch/2]) {
                translate([-1, dy, fan_cz + dz])
                    rotate([0, 90, 0])
                        cylinder(d = fan60_hole_d, h = plate_t + 2);
            }
        }
    }
}

// -------------------------------------------------------------
// EXECUTE RENDER SELECTION
// -------------------------------------------------------------
if (render_mode == 1) {
    // Assembled preview
    color("LightBlue") universal_duct();
    color("Crimson") translate([cone_length + 0.2, 0, 0]) faceplate_delta_4028();
} else if (render_mode == 2) {
    universal_duct();
} else if (render_mode == 3) {
    faceplate_delta_4028();
} else if (render_mode == 4) {
    faceplate_60mm();
}
