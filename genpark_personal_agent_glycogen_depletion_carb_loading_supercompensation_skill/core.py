# -*- coding: utf-8 -*-
"""Muscle Glycogen Depletion & Carb-Loading Supercompensation for GenPark Personal Agent."""
import json
from typing import Dict, Any

class GlycogenCarbLoadingSupercompensationPlanner:
    """Muscle glycogen supercompensation, enzymatic glycogen synthase kinetics, and low-FODMAP fueling engine."""

    @staticmethod
    def calculate_supercompensation_carb_needs(body_weight_kg: float, target_event_duration_hours: float, loading_window_days: int = 2) -> Dict[str, Any]:
        """Compute carbohydrate loading target (8-10g/kg/day) and associated cellular water binding."""
        # For endurance events > 90 mins, target 9.0g CHO per kg body mass
        g_per_kg = 9.0 if target_event_duration_hours >= 1.5 else 7.0
        daily_carbs_grams = round(body_weight_kg * g_per_kg)
        total_loading_carbs = daily_carbs_grams * loading_window_days

        # Each gram of stored glycogen binds 3.0g of intra-cellular water
        expected_glycogen_stored_g = min(650.0, body_weight_kg * 8.5)
        bound_water_kg = round((expected_glycogen_stored_g * 3.0) / 1000.0, 2)

        return {
            "athlete_weight_kg": body_weight_kg,
            "target_carb_intake_g_per_kg_day": g_per_kg,
            "daily_carb_target_grams": daily_carbs_grams,
            "total_window_carbs_grams": total_loading_carbs,
            "expected_water_weight_gain_kg": bound_water_kg,
            "physiological_note": f"Storing ~{int(expected_glycogen_stored_g)}g glycogen binds ~{bound_water_kg}kg water; this is normal supercompensation and supplies hydration during racing."
        }

    @staticmethod
    def synthesize_low_fiber_meal_cadence(daily_target_carbs_grams: int, dietary_preference: str = "standard") -> Dict[str, Any]:
        """Synthesize low-residue (<10g fiber) meal timing to prevent gastrointestinal motility distress."""
        breakfast_cho = int(daily_target_carbs_grams * 0.25)
        lunch_cho = int(daily_target_carbs_grams * 0.30)
        dinner_cho = int(daily_target_carbs_grams * 0.25)
        snacks_cho = int(daily_target_carbs_grams * 0.20)

        return {
            "target_total_carbs_grams": daily_target_carbs_grams,
            "fiber_ceiling_grams": 10,
            "dietary_preference": dietary_preference,
            "meal_breakdown": [
                {"meal": "Breakfast", "carbs_g": breakfast_cho, "recommendation": "White rice porridge / cream of rice with maple syrup, ripe banana, and fruit juice."},
                {"meal": "Lunch", "carbs_g": lunch_cho, "recommendation": "White sourdough bread with fruit jam, pretzels, and electrolyte carbohydrate beverage."},
                {"meal": "Mid-Afternoon Snack", "carbs_g": snacks_cho, "recommendation": "Rice cakes with honey, Haribo gummy candy, peeled boiled potatoes."},
                {"meal": "Dinner (T-12h)", "carbs_g": dinner_cho, "recommendation": "White pasta or jasmine rice with light tomato sauce, skinless chicken/tofu breast."}
            ],
            "gut_safety_rules": "Strictly eliminate cruciferous vegetables, legumes, whole grains, and heavy dairy fats during the final 36 hours."
        }
