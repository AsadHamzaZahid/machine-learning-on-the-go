import joblib
from pydantic import BaseModel, Field
from typing import Literal
import pandas as pd
from fastapi import FastAPI

app = FastAPI()

model = joblib.load('Machine learning on the go.pkl')

top_countries = ['Other', 'India', 'USA', 'Canada',
                 'Australia', 'UK', 'Germany', 'Mexico', 'Turkey', 'France']


@app.get("/")
def health():
    return "hello"


class input(BaseModel):
    age: int = Field(..., le=100, gt=0)
    gender: Literal["Male", "Female"]
    academic_level: Literal["Undergraduate", 'High School', 'Graduate']
    most_used_platform: Literal['Facebook', 'LinkedIn', 'Instagram', 'Snapchat', 'Twitter',
                                'YouTube', 'TikTok', 'LINE', 'KakaoTalk', 'VKontakte', 'WhatsApp',
                                'WeChat']

    purpose_of_use: Literal['Networking', 'Education', 'Entertainment', 'News']
    avg_daily_usage_hours: int = Field(..., ge=0, le=24)
    daily_unlocks: int = Field(..., ge=0,)
    study_hours: int = Field(..., ge=0, le=24)
    physical_activity_hours: int = Field(..., ge=0, le=24)
    sleep_hours_per_night: int = Field(..., ge=0, le=24)
    stress_level: Literal['Low', "Middle", "High", 'Super High']
    country: str


class prediction(BaseModel):
    predicted_mental_health_score: float


@app.post("/predict", response_model=prediction)
def predict(data: input):
    country_group = data.country if data.country in top_countries else "Other"

    input_row = pd.DataFrame([{
        'Age': data.age,
        'Gender': data.gender,
        'Country': data.country,
        'Academic_Level': data.academic_level,
        'Most_Used_Platform': data.most_used_platform,
        'Purpose_Of_Use': data.purpose_of_use,
        'Avg_Daily_Usage_Hours': data.avg_daily_usage_hours,
        'Daily_Unlocks': data.daily_unlocks,
        'Study_Hours': data.study_hours,
        'Physical_Activity_Hours': data.physical_activity_hours,
        'Sleep_Hours_Per_Night': data.sleep_hours_per_night,
        'Stress_Level': data.stress_level,
        'Grouped_country': country_group
    }])

    prediction1 = model.predict(input_row)[0]
    return prediction(predicted_mental_health_score=round(float(prediction1), 2))
