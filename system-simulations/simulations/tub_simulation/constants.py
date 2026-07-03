# simulations/tub_simulation/constants.py

"""
Physical constants and unit conversions.
All units are SI: meters, kilograms, seconds, etc.
"""

# Gravitational acceleration (m/s^2)
STANDARD_GRAVITY = 9.81
MOON_GRAVITY = 1.62
MARS_GRAVITY = 3.71
JUPITER_GRAVITY = 24.79

# Standard atmospheric pressure (Pa)
STANDARD_ATMOSPHERIC_PRESSURE = 101_325

# Water properties at ~20°C (for reference)
WATER_DENSITY = 998.2       # kg/m^3
WATER_VISCOSITY = 0.001002  # Pa·s

# Useful constants
PI = 3.141592653589793

# Unit conversions
LITER_TO_CUBIC_METER = 0.001
CUBIC_METER_TO_LITER = 1000.0

MILLIMETER_TO_METER = 0.001
CENTIMETER_TO_METER = 0.01

# Time conversions
MINUTE_TO_SECOND = 60
HOUR_TO_SECOND = 3600

# Numerical precision (for comparisons)
EPSILON = 1e-9
