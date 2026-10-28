from fastapi import FastAPI
from pydantic import BaseModel
import joblib

app=FastAPI(title='Battery Replacement and Monitoring System')
model = joblib.load('isaac-model.joblib')

@app.get('/')
async def home():
    return{'system':'Battery Replacement and Monitoring System'}

class Battery_information(BaseModel):
    cell_voltage_v:float
    cell_temperature_c:float
    module_current_a:float
    module_power_kw:float
    soc_pct:float

@app.post('/predict')
async def Battery_informations(info:Battery_information):
    row = [[
        info.cell_voltage_v,
        info.cell_temperature_c,
        info.module_current_a,
        info.module_power_kw,
        info.soc_pct
    ]]
    prediction = model.predict(row)
    soh = float(prediction[0])
    
    if soh >= 95.0:
        status = "Optimal"
        health_index = "Tier 1"
        action = "System operating at peak capacity."
    elif soh >= 92.0:
        status = "Good"
        health_index = "Tier 2"
        action = "Normal wear. No action required."
    elif soh >= 89.0:
        status = "Noticeable Degradation"
        health_index = "Tier 3"
        action = "Monitor thermal behavior and voltage under load."
    else:
        status = "Sub-optimal / Accelerated Aging"
        health_index = "Tier 4 (Warning)"
        action = "Inspect cell performance. Prepare for replacement planning."
    
    return{
       'state_of_health': round(soh, 2),
        'health_tier': health_index,
        'battery_status': status,
        'recommendation': action
    }

