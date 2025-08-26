use <Screws.scad>

$fn = $preview ? 64 : 256;

base_diameter = 145;
top_diameter = 105;
wall_thickness = 5;
total_height = 80;
    
module pancake_switch_hole(depth) {
    translate([0,0,-0.05]) cylinder(depth+0.1, d=88);
    translate([44,0,-0.05]) cylinder(depth+0.1, r=3);
    translate([-44,0,-0.05]) cylinder(depth+0.1, r=3);
}

module trrs_socket() {
    union() {
        translate([-16.5, -12/2,0 ]) cube([15, 12, 12]);
        translate([-1.55,0,6/2]) rotate([0,90,0]) cylinder(4.5, d=6);
    }
}

module jack_mount() {
    translate([base_diameter/2-2,0,0]) union() {
        translate([0,0,-3]) trrs_socket();
        translate([0, -50, -50]) cube(100);
    }
}

module switch_mount() {
    translate([0,0,total_height-(2*wall_thickness)-0.05]) pancake_switch_hole(5.1);
}

m3_15_flat = screw(3, 0.5, 15, "flat");

module screws() {
    for(theta = [0:60:360])
        rotate([0,0,theta])
            translate([0,base_diameter / 2 - wall_thickness - 3, -wall_thickness])
                children();
}

module hull_core() {
    cylinder(total_height - 2*wall_thickness, d1=base_diameter-(2*wall_thickness), d2=top_diameter-(2*wall_thickness));
}

module hull() {
    intersection() {
        difference() {
            union() {
                difference() {  
                    minkowski() {
                        hull_core();
                        difference() {
                            cylinder(r=wall_thickness);
                            translate([0,0,-2*wall_thickness+0.05]) cube(4*wall_thickness, center = true);
                        }
                    }
                    hull_core();
                    switch_mount();
                    jack_mount();
                }
                screws() translate([0,0,wall_thickness]) cylinder(15+2, d1=9+1, d2=1);
            }
            translate([0,0,-5]) base_core();
            screws() screw_tap_hole(m3_15_flat);
        }
        cylinder(total_height, d=base_diameter);
    }
}

module base_core() {
    cylinder(5, d=base_diameter);
    translate([0,0,4.995]) cylinder(3, d1=base_diameter-2*wall_thickness+1, d2=base_diameter-2*wall_thickness-1);
}

module base() {
    difference() {
        translate([0,0,-5]) base_core();
        jack_mount();
        screws() screw_through_hole(m3_15_flat);
    }
}

module sock() {
    difference() {
        translate([0,0,-7]) cylinder(4, d=base_diameter+4);
        translate([0,0,-5]) cylinder(5, d=base_diameter);
        translate([0,0,-10]) cylinder(6, d=base_diameter-30);
        jack_mount();
    }
}

translate([0,0,0]) base();
translate([0,0,-10]) sock();
translate([0,0,10]) hull();