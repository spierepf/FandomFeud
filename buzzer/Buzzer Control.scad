// Lets make the round bits pretty
$fn=64;

// Load the main library
use <Enclosure.scad>
use <Screws.scad>
use </home/peter/Nextcloud/Hal-Con/FandomFeud/Buzzer/SuperFunky-lgmWw.ttf>

shell = 4;
// Start by describing the basic dimensions of your enclosure
myEnclosure = enclosure([220.0, 140.0, 40.0], shell=shell); // define an enclosure that is 80.0mm x 40.0mm x 25.0mm

module trrs_socket() {
    union() {
        translate([-16.5, -12/2,0 ]) cube([15, 12, 12]);
        translate([-1.55,0,6/2]) rotate([0,90,0]) cylinder(4.5, d=6);
    }
}

module jack_mount() {
    union() {
        translate([0,0,-3]) trrs_socket();
        translate([0, -50, -50]) cube(100);
    }
}

m3_8_round = screw(3, 0.5, 8, "round");

// Now lets render the enclosure cover:
//translate([0, 0, 10]) union() {
//    difference() {
//        // Basic shape for the enclosure cover
//        enclosureCover(myEnclosure);
//        
//        enclosureRight(myEnclosure) rotate([270,270,0]) translate([shell+0.1,0,6]) jack_mount();
//        enclosureRight(myEnclosure) translate([0,20,shell-0.4]) linear_extrude(1) text("Stage Right", halign="center");
//
//        enclosureLeft(myEnclosure) rotate([270,270,0]) translate([shell+0.1,0,6]) jack_mount();
//        enclosureLeft(myEnclosure) translate([0,20,shell-0.4]) linear_extrude(1) text("Stage Left", halign="center");
//
//        enclosureTop(myEnclosure) translate([0, 15, shell-0.4]) linear_extrude(1) text("Fandom", font = "SuperFunky", size=20, halign="center", valign="center");
//        enclosureTop(myEnclosure) translate([0, -15, shell-0.]) linear_extrude(1) text("Feud", font = "SuperFunky", size=20, halign="center", valign="center");
//    }
//    enclosureTop(myEnclosure) {
//        translate([70-shell,35-shell,0]) rotate([0,0,90]){
//            difference() {
//                translate([-21.25, -40, -22]) cube([42.5, 80, 24]);
//                translate([-20.25, -39, -22.1]) cube([40.5, 78, 22]);
//            }
//        }
//    }
//    enclosureTop(myEnclosure) translate([0,-30,0]) {
//        x_centers = 60.1;
//        y_centers = 57.5;
//        for(x = [-x_centers/2, x_centers/2]) for(y = [-y_centers/2, y_centers/2]) {
//            translate([x,y,-7]) {
//                difference() {
//                    cylinder(d=7,h=7);
//                    screw_tap_hole(m3_8_round);
//                }
//            }
//        }
//    }
//}

// Now lets render the snap on base:
translate([0, 0, -10]) union() {
    difference() {
        enclosureBase(myEnclosure);
        
        enclosureRight(myEnclosure) rotate([270,270,0]) translate([shell+0.1,0,6]) jack_mount();
        enclosureLeft(myEnclosure) rotate([270,270,0]) translate([shell+0.1,0,6]) jack_mount();
    }
}   
