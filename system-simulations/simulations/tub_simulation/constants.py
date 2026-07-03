"""
Physical constants used throughout the simulation.

Units:
- Length: meters (m)
- Volume: cubic meters (m³)
- Time: seconds (s)
- Mass: kilograms (kg)
- Pressure: Pascals (Pa)
- Flow Rate: m³/s
"""

# ===========================
# Gravity
# ===========================

STANDARD_GRAVITY = 9.81  # m/s²

# Planetary gravities (for experiments)
MOON_GRAVITY = 1.62
MARS_GRAVITY = 3.71
EARTH_GRAVITY = 9.81
JUPITER_GRAVITY = 24.79

# ===========================
# Atmospheric Pressure
# ===========================

STANDARD_ATMOSPHERIC_PRESSURE = 101_325  # Pa

# ===========================
# Water Properties (20°C)
# ===========================

WATER_DENSITY = 998.2             # kg/m³
WATER_VISCOSITY = 0.001002        # Pa·s

# ===========================
# Useful Mathematical Constants
# ===========================

PI = 3.141592653589793

# ===========================
# Unit Conversions
# ===========================

LITER_TO_CUBIC_METER = 0.001
CUBIC_METER_TO_LITER = 1000

MILLIMETER_TO_METER = 0.001
CENTIMETER_TO_METER = 0.01

MINUTE_TO_SECOND = 60
HOUR_TO_SECOND = 3600

# ===========================
# Numerical Precision
# ===========================

EPSILON = 1e-9