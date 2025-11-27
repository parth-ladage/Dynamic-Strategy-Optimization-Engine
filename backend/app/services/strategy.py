import joblib
import numpy as np
import os
import pandas as pd

# Define path to the model
# We use os.path to make it work on Windows/Mac/Linux
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, 'ml_models', 'tire_models_v1.pkl')

# Global variable to store models
tire_models = None

def load_tire_models():
    """Loads the ML models from the .pkl file if not already loaded."""
    global tire_models
    if tire_models is None:
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(f"Model file not found at {MODEL_PATH}. Did you move it there?")
        tire_models = joblib.load(MODEL_PATH)
        print(f"✅ ML Models loaded: {list(tire_models.keys())}")
    return tire_models

def predict_stint_time(compound, start_tire_age, laps_to_drive):
    """
    Predicts the total time for a stint using the loaded ML model.
    """
    models = load_tire_models()
    
    # Handle missing compounds (Fallback to Hard if unknown)
    if compound not in models:
        print(f"⚠️ Warning: {compound} not found in model. Defaulting to HARD.")
        compound = 'HARD'
        
    model = models[compound]
    
    # Create input array for the model: [[start_age], [start_age+1], ...]
    tire_age_range = np.arange(start_tire_age, start_tire_age + laps_to_drive).reshape(-1, 1)
    
    # Predict lap times
    predicted_lap_times = model.predict(tire_age_range)
    
    return np.sum(predicted_lap_times)

def compare_strategies(total_laps=57):
    """
    Runs the 1-Stop vs 2-Stop simulation and returns the best one.
    This is the API response logic.
    """
    PIT_LOSS = 22.5
    
    # Define the two strategies to compare
    # 1-Stop: Soft (18) -> Hard (39)
    strat_1 = [('SOFT', 18), ('HARD', total_laps - 18)]
    
    # 2-Stop: Soft (13) -> Hard (24) -> Soft (20)
    strat_2 = [('SOFT', 13), ('HARD', 24), ('SOFT', total_laps - 13 - 24)]
    
    results = []
    
    for strategy_name, stints in [("1-Stop", strat_1), ("2-Stop", strat_2)]:
        total_time = 0
        pit_stops = len(stints) - 1
        
        for compound, laps in stints:
            # Assume new tires (age 0) for simplicity in MVP
            total_time += predict_stint_time(compound, 0, laps)
            
        # Add pit stop time
        total_time += (pit_stops * PIT_LOSS)
        
        results.append({
            "name": strategy_name,
            "total_time": round(total_time, 2),
            "pit_stops": pit_stops,
            "details": [f"{c} ({l} laps)" for c, l in stints]
        })
        
    # Find the winner
    best_strategy = min(results, key=lambda x: x['total_time'])
    
    return {
        "recommended": best_strategy,
        "alternatives": results
    }