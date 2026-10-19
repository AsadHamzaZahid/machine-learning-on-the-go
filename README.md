# Machine Learning On The Go

A small project that predicts a student's mental health score based on their social media habits and daily routine.

I trained a model on a student survey dataset, wrapped it in a FastAPI backend, and built a Streamlit app on top so anyone can try it without touching code.

## What it does

You enter some basic details about yourself:

- Age, gender, country and academic level
- Most used social media platform and why you use it
- Hours spent on social media each day and how often you unlock your phone
- Study, sleep and physical activity hours
- Your stress level

The app sends this to the API, the model makes a prediction, and you get a mental health score back with a short message.

The score is only an estimate from a model trained on survey data. It is not a medical diagnosis.

## How it works

1. The data comes from `Student Social Media And Mental Health Impact.csv`.
2. The notebook (`Machine_learning_on_the_go.ipynb`) cleans the data, builds a preprocessing pipeline and trains two models: Linear Regression and Random Forest.
3. Random Forest did better, with an R2 score of about 0.91 on the test set, so that is the one I saved.
4. `main.py` loads the saved model and serves it through a FastAPI endpoint called `/predict`.
5. `streamlit_app.py` is the interface. It collects the inputs and calls the API.

## Project files

```
main.py                 FastAPI backend
streamlit_app.py        Streamlit frontend
Machine_learning_on_the_go.ipynb   Notebook with training and analysis
Student Social Media And Mental Health Impact.csv   Dataset
.streamlit/config.toml  Theme settings for the app
```

You also need the saved model file (the `.pkl`) in the same folder. Its name must match the one written in `main.py`.

## How to run it

Clone the repo:

```
git clone https://github.com/AsadHamzaZahid/machine-learning-on-the-go.git
cd machine-learning-on-the-go
```

Install the packages:

```
pip install fastapi uvicorn scikit-learn pandas joblib pydantic streamlit requests
```

Try to use the same scikit-learn version that you used to train the model. A pickle file saved with one version can act strangely or fail on another.

Start the API in one terminal:

```
uvicorn main:app --reload
```

Start the app in a second terminal:

```
streamlit run streamlit_app.py
```

The app opens in your browser. If your API is running somewhere other than `http://127.0.0.1:8000`, change the address in the sidebar.

You can also check the API docs at `http://127.0.0.1:8000/docs`.

## Example request

```
POST /predict

{
  "age": 20,
  "gender": "Female",
  "academic_level": "Undergraduate",
  "most_used_platform": "Instagram",
  "purpose_of_use": "Entertainment",
  "avg_daily_usage_hours": 5,
  "daily_unlocks": 80,
  "study_hours": 3,
  "physical_activity_hours": 1,
  "sleep_hours_per_night": 7,
  "stress_level": "Medium",
  "country": "India"
}
```

Response:

```
{
  "predicted_mental_health_score": 6.85
}
```

(The number above is just an example.)

Stress level can be `Low`, `Medium`, `High` or `Very High`. These are the same values the model was trained with.

## Built with

- Python
- scikit-learn
- FastAPI
- Streamlit
- pandas

## Things I want to improve

- Deploy the API and the app online so people can use it without running anything
- Try other models and compare them properly
- Add more details to the result, like which habits affect the score the most

## A note

The dataset is small and comes from a survey, so the predictions will not be perfect and should not be used to make real health decisions. If you or someone you know is struggling, please talk to someone you trust or a professional.
