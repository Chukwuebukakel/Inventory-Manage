from geopy.distance import geodesic

def is_within_branch_location(user_lat, user_long, branch):
    """Check if user is within the branch's location radius."""
    try:
        branch_location = (float(branch.latitude), float(branch.longitude))
        user_location = (float(user_lat), float(user_long))
        return geodesic(user_location, branch_location).km <= branch.radius
    except (ValueError, TypeError):
        return False