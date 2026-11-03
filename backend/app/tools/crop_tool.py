import json
import os
from typing import Dict, Any, List, Optional
from strands import tool

KNOWLEDGE_PATH = os.path.join(os.path.dirname(__file__), "..", "knowledge", "crop_profiles.json")


def load_crop_knowledge() -> Dict[str, Any]:
    with open(KNOWLEDGE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


@tool
def get_crop_profile(crop_name: str) -> Dict[str, Any]:
    """
    Retrieve comprehensive agronomic requirements, growth stages, and climate thresholds for a crop.
    
    Args:
        crop_name: Name of the crop (e.g. 'Soybean', 'Rice', 'Wheat', 'Maize', 'Cotton').
        
    Returns:
        Crop profile containing scientific name, stages, temperature thresholds, and references.
    """
    data = load_crop_knowledge()
    crops = data.get("crops", {})
    key = crop_name.strip().lower()
    if "paddy" in key or "rice" in key or "dhan" in key:
        key = "rice"
    elif "soybean" in key or "soya" in key:
        key = "soybean"
    elif "wheat" in key or "gehun" in key:
        key = "wheat"
    elif "maize" in key or "corn" in key or "makka" in key:
        key = "maize"
    elif "cotton" in key or "kapas" in key:
        key = "cotton"

    if key in crops:
        return crops[key]

    return {
        "error": f"Crop '{crop_name}' is not currently in the primary knowledge base. Supported crops: Soybean, Rice, Wheat, Maize, Cotton.",
        "supported_crops": ["Soybean", "Rice", "Wheat", "Maize", "Cotton"]
    }


@tool
def get_growth_stage_info(crop_name: str, growth_stage: str) -> Dict[str, Any]:
    """
    Retrieve specific climate vulnerability and environmental thresholds for a given crop growth stage.
    
    Args:
        crop_name: Name of the crop (e.g. 'Soybean').
        growth_stage: Growth stage (e.g. 'Flowering', 'Vegetative', 'Germination', 'Grain Filling').
        
    Returns:
        Stage-specific temperature optimums, water needs, tolerance limits, and monitoring tips.
    """
    profile = get_crop_profile(crop_name)
    if "error" in profile:
        return profile

    stages = profile.get("growth_stages", [])
    query_stage = growth_stage.lower()

    # Find closest matching stage
    matched_stage = None
    for s in stages:
        if query_stage in s["stage_name"].lower() or s["stage_name"].lower() in query_stage:
            matched_stage = s
            break

    if not matched_stage and stages:
        matched_stage = stages[1]  # Default to Vegetative

    return {
        "crop": profile["crop_name"],
        "crop_hi": profile["crop_name_hi"],
        "stage": matched_stage,
        "soil_preferences": profile.get("soil_preferences"),
        "sourced_references": profile.get("sourced_references")
    }

