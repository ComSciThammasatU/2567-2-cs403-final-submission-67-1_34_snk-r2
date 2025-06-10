# model
from model import predict as model_predict
# Web Server
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

# create app
app = FastAPI()
# alow cross origin all origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# # index route
# @app.get('/')
# def index():
#    return {'message': 'This is a sentiment analysis model API.'}

# # predict route
# @app.get('/predict')
# def predict(text: str):
#    return {'text': text, 'sentiment': model_predict(text, decode=True)}

class TextRequest(BaseModel):
    text: str


@app.post("/predict")
def predict_sentiment(request: TextRequest):
    label = model_predict(request.text)
    return {
        "sentiment": str(label)
    }

# start server
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5000)

print("Starting FastAPI server...")
