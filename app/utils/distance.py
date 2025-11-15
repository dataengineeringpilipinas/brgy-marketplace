"""
Distance calculation utilities
"""
from typing import Optional, Dict, List

# Zone mapping for approximate distance calculation
# This is a simplified mapping - in production, you'd have actual coordinates
ZONE_DISTANCES: Dict[str, Dict[str, float]] = {
    # Example zone distances (in meters)
    # "Zone A": {"Zone B": 150, "Zone C": 300, ...}
}


def calculate_zone_distance(zone1: Optional[str], zone2: Optional[str]) -> Optional[float]:
    """Calculate approximate distance between two zones in meters."""
    if not zone1 or not zone2:
        return None
    
    if zone1 == zone2:
        return 0.0
    
    # Check if we have a direct mapping
    if zone1 in ZONE_DISTANCES and zone2 in ZONE_DISTANCES[zone1]:
        return ZONE_DISTANCES[zone1][zone2]
    
    # Check reverse mapping
    if zone2 in ZONE_DISTANCES and zone1 in ZONE_DISTANCES[zone2]:
        return ZONE_DISTANCES[zone2][zone1]
    
    # Default: assume zones are in same barangay, estimate 200-500m
    return 350.0  # Average distance


def filter_by_distance(
    user_zone: Optional[str],
    business_zones: List[tuple],
    max_distance: float
) -> List[int]:
    """Filter business IDs by distance from user zone."""
    if not user_zone:
        return [bid for bid, _ in business_zones]
    
    filtered = []
    for business_id, business_zone in business_zones:
        distance = calculate_zone_distance(user_zone, business_zone)
        if distance is not None and distance <= max_distance:
            filtered.append(business_id)
    
    return filtered

