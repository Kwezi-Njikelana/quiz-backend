from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Annotated
import models
from database import SessionLocal, engine
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from anthropic import Anthropic
import json

client = Anthropic()

app = FastAPI(root_path="/api")

app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173",  
        "http://localhost:3000",],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],

)

models.Base.metadata.create_all(bind=engine)

class GenerateQuestionsRequest(BaseModel):
        topic: str
        count: int = 5

class ChoiceBase(BaseModel):
        choice_text: str
        is_correct: bool

class QuestionBase(BaseModel):
        question_text: str
        choices: List[ChoiceBase]

def get_db():
        db = SessionLocal()
        try:
                yield db
        finally:
                db.close()

db_dependency = Annotated[Session, Depends(get_db)]



@app.get("/questions")
async def read_all_questions(db: db_dependency):
        return db.query(models.Questions).all()

@app.get("/questions/{question_id}")
async def read_question(question_id: int, db: db_dependency):
        result = db.query(models.Questions).filter(models.Questions.id == question_id).first()
        if not result:
                raise HTTPException(status_code=404, detail='Question is not found')
        return result


@app.get("/choices/{question_id}")
async def read_choices(question_id: int, db: db_dependency):
        result = db.query(models.Choices).filter(models.Choices.question_id == question_id).all()
        if not result: 
                raise HTTPException(status_code=404, detail='Choices is not found')
        return result


@app.post("/questions")
async def create_question(question: QuestionBase, db: db_dependency):
        db_question = models.Questions(question_text=question.question_text)
        db.add(db_question)
        db.commit()
        db.refresh(db_question)
        for choice in question.choices:
                db_choice = models.Choices(choice_text=choice.choice_text, is_correct=choice.is_correct, question_id=db_question.id)
                db.add(db_choice)
                db.commit()
        return{"message": "Question created successfully"}


@app.put("/questions/{question_id}")
async def update_question(question_id: int, question: QuestionBase, db: db_dependency):
        db_question = db.query(models.Questions).filter(models.Questions.id == question_id).first()
        if not db_question:
                raise HTTPException(status_code=404, detail='Question is not found')
        
        db_question.question_text = question.question_text
        
        # Remove existing choices
        db.query(models.Choices).filter(models.Choices.question_id == question_id).delete()

        # Add new choices
        for choice in question.choices:
                db_choice = models.Choices(choice_text=choice.choice_text, is_correct=choice.is_correct, question_id=question_id)
                db.add(db_choice)

        db.commit()
        return {
                "message": "Question updated successfully"
        }


@app.delete("/questions/{question_id}")
async def delete_question(question_id: int, db: db_dependency):
        db_question = db.query(models.Questions).filter(models.Questions.id == question_id).first()
        if not db_question:
                raise HTTPException(status_code=404, detail='Question is not found')
        db.delete(db_question)
        db.commit()

@app.post("/questions/generate")
async def generate_questions(request: GenerateQuestionsRequest, db: db_dependency):
        prompt = f""" Generate {request.count} multiple choice questions about {request.topic}".

Return ONLY a JSON array, no explanation, no markdown. Each object must have:
- "question_text": string
- "choices": array of exactly 4 objects, each with:
  - "choice_text": string
  - "is_correct": boolean (exactly one must be true)

Example format:
[
  {{
    "question_text": "What is ...?",
    "choices": [
      {{"choice_text": "Answer A", "is_correct": true}},
      {{"choice_text": "Answer B", "is_correct": false}},
      {{"choice_text": "Answer C", "is_correct": false}},
      {{"choice_text": "Answer D", "is_correct": false}}
    ]
  }}
]"""
        message = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=2048,
        messages=[{"role": "user", "content": prompt}]
    )
        
        