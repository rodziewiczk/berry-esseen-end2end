"""Generalized sign-separated half-gap count kernel; conditional resources only."""
from exact35_core import *
import exact35_core as core
import joint_cubic_normalized_fast as joint_fast
import bernstein_fast
import interval_scalar_fast
bernstein_fast.apply()
interval_scalar_fast.apply()
core.bernstein_interval_min = bernstein_fast.bernstein_interval_min
core.joint = joint_fast
