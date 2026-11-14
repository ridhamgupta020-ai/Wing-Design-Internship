
import math
import csv

# ==============================================
# WEEK 1: WING DESIGN AND AEROFOIL SELECTION
# Conceptual Fixed-Wing UAV Project
# ==============================================

# 1. DESIGN INPUTS

MASS = 12.0                    # kg
GRAVITY = 9.81                 # m/s^2
WING_AREA = 1.20               # m^2
WING_SPAN = 3.0                # m
TAPER_RATIO = 0.60

CRUISE_SPEED = 20.0            # m/s
LOW_SPEED = 12.0               # m/s

AIR_DENSITY = 1.225            # kg/m^3
DYNAMIC_VISCOSITY = 1.789e-5   # kg/(m*s)

BASELINE_AEROFOIL = "NACA 2412"


# 2. INPUT VALIDATION

def validate_inputs():
    if MASS <= 0:
        raise ValueError("Mass must be greater than zero.")

    if WING_AREA <= 0:
        raise ValueError("Wing area must be greater than zero.")

    if WING_SPAN <= 0:
        raise ValueError("Wing span must be greater than zero.")

    if not 0 < TAPER_RATIO <= 1:
        raise ValueError("Taper ratio must be between 0 and 1.")

    if CRUISE_SPEED <= 0 or LOW_SPEED <= 0:
        raise ValueError("Aircraft speeds must be positive.")

    if AIR_DENSITY <= 0 or DYNAMIC_VISCOSITY <= 0:
        raise ValueError("Air properties must be positive.")


# 3. BASIC AIRCRAFT CALCULATIONS

def calculate_weight():
    return MASS * GRAVITY


def calculate_aspect_ratio():
    return WING_SPAN ** 2 / WING_AREA


def calculate_wing_loading():
    return calculate_weight() / WING_AREA


def calculate_dynamic_pressure(speed):
    return 0.5 * AIR_DENSITY * speed ** 2


# 4. WING GEOMETRY

def calculate_chords():
    root_chord = (
        2 * WING_AREA /
        (WING_SPAN * (1 + TAPER_RATIO))
    )

    tip_chord = root_chord * TAPER_RATIO

    return root_chord, tip_chord


def calculate_mac(root_chord):
    mac = (
        (2 / 3) * root_chord *
        (1 + TAPER_RATIO + TAPER_RATIO ** 2) /
        (1 + TAPER_RATIO)
    )

    return mac


def calculate_mac_position():
    # Spanwise MAC location measured from wing root
    return (
        WING_SPAN / 6 *
        (1 + 2 * TAPER_RATIO) /
        (1 + TAPER_RATIO)
    )


# 5. AERODYNAMIC CALCULATIONS

def calculate_required_cl(speed):
    weight = calculate_weight()
    pressure = calculate_dynamic_pressure(speed)

    return weight / (pressure * WING_AREA)


def calculate_reynolds_number(speed, chord):
    return (
        AIR_DENSITY * speed * chord /
        DYNAMIC_VISCOSITY
    )


# 6. AEROFOIL COMPARISON
# Qualitative screening only.
# Actual performance requires validated aerofoil data.

def compare_aerofoils():
    aerofoils = [
        {
            "name": "NACA 0012",
            "type": "Symmetrical",
            "thickness": "12%",
            "application": "Comparison profile"
        },
        {
            "name": "NACA 2412",
            "type": "Cambered",
            "thickness": "12%",
            "application": "Selected baseline"
        },
        {
            "name": "NACA 4412",
            "type": "More cambered",
            "thickness": "12%",
            "application": "Comparison profile"
        }
    ]

    return aerofoils


# 7. DISPLAY RESULTS

def display_results(results):

    print("\n========================================")
    print("       WING DESIGN ANALYSIS REPORT")
    print("========================================")

    print("\nAIRCRAFT INPUTS")
    print("----------------------------------------")

    print(f"Aircraft Mass       : {MASS:.2f} kg")
    print(f"Wing Area           : {WING_AREA:.2f} m^2")
    print(f"Wing Span           : {WING_SPAN:.2f} m")
    print(f"Taper Ratio         : {TAPER_RATIO:.2f}")
    print(f"Cruise Speed        : {CRUISE_SPEED:.2f} m/s")
    print(f"Low Speed           : {LOW_SPEED:.2f} m/s")

    print("\nWING GEOMETRY")
    print("----------------------------------------")

    print(f"Aircraft Weight     : {results['weight']:.2f} N")
    print(f"Aspect Ratio        : {results['aspect_ratio']:.2f}")
    print(f"Wing Loading        : {results['wing_loading']:.2f} N/m^2")
    print(f"Root Chord          : {results['root_chord']:.3f} m")
    print(f"Tip Chord           : {results['tip_chord']:.3f} m")
    print(f"Mean Chord (MAC)    : {results['mac']:.3f} m")
    print(f"MAC Position        : {results['mac_position']:.3f} m")

    print("\nAERODYNAMIC RESULTS")
    print("----------------------------------------")

    print(f"Cruise Dynamic Pressure : {results['dynamic_pressure']:.2f} Pa")
    print(f"Cruise Required CL      : {results['cruise_cl']:.3f}")
    print(f"Low-Speed Required CL   : {results['low_speed_cl']:.3f}")
    print(f"Reynolds Number         : {results['reynolds']:.0f}")

    print("\nAEROFOIL COMPARISON")
    print("----------------------------------------")

    for foil in compare_aerofoils():
        print(
            f"{foil['name']} | "
            f"{foil['type']} | "
            f"{foil['thickness']} | "
            f"{foil['application']}"
        )

    print("\nSelected Baseline:", BASELINE_AEROFOIL)

    print("\n========================================")
    print("Analysis completed successfully.")
    print("========================================")


# 8. EXPORT RESULTS TO CSV

def export_results(results):

    with open(
        "wing_design_results.csv",
        "w",
        newline=""
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            "Parameter",
            "Value",
            "Unit"
        ])

        rows = [
            ["Mass", MASS, "kg"],
            ["Aircraft Weight", results["weight"], "N"],
            ["Wing Area", WING_AREA, "m^2"],
            ["Wing Span", WING_SPAN, "m"],
            ["Aspect Ratio", results["aspect_ratio"], "-"],
            ["Wing Loading", results["wing_loading"], "N/m^2"],
            ["Root Chord", results["root_chord"], "m"],
            ["Tip Chord", results["tip_chord"], "m"],
            ["Mean Aerodynamic Chord", results["mac"], "m"],
            ["MAC Position", results["mac_position"], "m"],
            ["Dynamic Pressure", results["dynamic_pressure"], "Pa"],
            ["Cruise Required CL", results["cruise_cl"], "-"],
            ["Low Speed Required CL", results["low_speed_cl"], "-"],
            ["Reynolds Number", results["reynolds"], "-"]
        ]

        writer.writerows(rows)

    print("\nCSV file created: wing_design_results.csv")


# 9. MAIN PROGRAM

def main():

    try:
        validate_inputs()

        root_chord, tip_chord = calculate_chords()

        results = {
            "weight": calculate_weight(),
            "aspect_ratio": calculate_aspect_ratio(),
            "wing_loading": calculate_wing_loading(),
            "root_chord": root_chord,
            "tip_chord": tip_chord,
            "mac": calculate_mac(root_chord),
            "mac_position": calculate_mac_position(),
            "dynamic_pressure": calculate_dynamic_pressure(CRUISE_SPEED),
            "cruise_cl": calculate_required_cl(CRUISE_SPEED),
            "low_speed_cl": calculate_required_cl(LOW_SPEED),
            "reynolds": calculate_reynolds_number(
                CRUISE_SPEED,
                calculate_mac(root_chord)
            )
        }

        display_results(results)
        export_results(results)

    except ValueError as error:
        print("\nInput Error:", error)


if __name__ == "__main__":
    main()
