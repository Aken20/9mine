import os


# Helper function to resolve the actual file path with fallbacks
def resolve_cv_path(cv_path, candidate_name=None):
    # These are the possible locations to check for CV files
    possible_paths = []

    # Get the base directory
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Add the original path
    if not os.path.isabs(cv_path):
        possible_paths.append(os.path.join(base_dir, cv_path))
    else:
        possible_paths.append(cv_path)
        
    # Try the extracted directory structure
    filename = os.path.basename(cv_path)
    
    # Docker container paths (these are the most likely to work)
    possible_paths.append("/app/media/CVs To Share June 2024/" + filename)
    
    # Also check in various locations
    possible_paths.append(os.path.join(base_dir, "media", "CVs To Share June 2024", filename))
    possible_paths.append(os.path.join(base_dir, "media", filename))
    possible_paths.append(os.path.join("/app/media", filename))
    
    # Additionally, try to find by candidate name
    if candidate_name:
        candidate_name_clean = candidate_name.replace(" ", "_")
        possible_paths.append(f"/app/media/CVs To Share June 2024/{candidate_name_clean}_CV.pdf")
        possible_paths.append(f"/app/media/CVs To Share June 2024/{candidate_name_clean.split('_')[0]}_CV.pdf")
    
    # Check all paths
    for path in possible_paths:
        print(f"Checking path: {path}")
        if os.path.exists(path):
            print(f"Found CV file at: {path}")
            return path
            
    # No valid path found
    return None