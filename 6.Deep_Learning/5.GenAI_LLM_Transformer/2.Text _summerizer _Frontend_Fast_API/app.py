from fastapi import FastAPI, Request
from pydantic import BaseModel
from transformers import T5ForConditionalGeneration, AutoTokenizer
import torch
import re
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles


# create the app
app = FastAPI(
    title="Text Summarizer App",
    description="A simple text summarizer app Using T5 Transformer",
    version="0.1"
)

# 👇 FIX: Mount the current directory so FastAPI can serve background.png
app.mount("/static", StaticFiles(directory="."), name="static")


# model and tokenizer loading
model = T5ForConditionalGeneration.from_pretrained("./saved_summary_model")
tokenizer = AutoTokenizer.from_pretrained(
    "./saved_summary_model",
    use_fast=True
)


# Device configuration
if torch.backends.mps.is_available():
    device = "mps"
elif torch.cuda.is_available():
    device = "cuda"
elif hasattr(torch, "xpu") and torch.xpu.is_available():
    device = "xpu"
elif hasattr(torch.backends, "hip") and torch.backends.hip.is_available():
    device = "hip"
else:
    device = "cpu"

model.to(device)
print(f"Model loaded on {device}")


# templates configuration
templates = Jinja2Templates(directory=".")


# Input Schema for dialogue => string
class DailogueInput(BaseModel):
    dialogue: str


# clean the dialogue text
def clean_data(text):
    text = re.sub(r"\r\n", " ", text)  # remove \n lines that kind of symbol
    text = re.sub(r"\s+", " ", text)   # remove extra spaces
    text = re.sub(r"<.*?>", " ", text) # remove HTML tags ex:- <h1>, <b>
    text = text.strip().lower()
    return text


# summarization function
def summerize_dialogue(dialogue: str) -> str:
    dialogue = clean_data(dialogue)  # clean the text remove space, html tag, to lowercase

    # tokenize
    inputs = tokenizer(
        dialogue,
        padding="max_length",
        max_length=512,       # limit words to 512
        truncation=True,      # cut extra words
        return_tensors="pt"   # make tensor for PyTorch
    ).to(device)

    # generate the summary ==> token ids
    targets = model.generate(
        input_ids=inputs["input_ids"],             # input text ids
        attention_mask=inputs["attention_mask"],  # focus on real words
        max_length=150,
        num_beams=4,      # Transformer generate 4 outputs, compare and select best summary
        early_stopping=True
    )

    # decode the output tokenization ===> Readable Word
    # ex:- [213,32424,4232] =====> "I love Python"
    summary = tokenizer.decode(
        targets[0],
        skip_special_tokens=True
    )

    return summary


# API Endpoint for summarization Route
@app.post("/summarize/")
async def create_item(Dialogue_input: DailogueInput):
    summary = summerize_dialogue(Dialogue_input.dialogue)
    return {"summary": summary}


# Home Page Route
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )













# from fastapi import FastAPI, Request
# from pydantic import BaseModel
# from transformers import T5ForConditionalGeneration, AutoTokenizer
# import torch
# import re
# from fastapi.templating import Jinja2Templates
# from fastapi.responses import HTMLResponse
# from fastapi.staticfiles import StaticFiles


# # create the app
# app = FastAPI(
#     title="Text Summarizer App",
#     description="A simple text summarizer app Using T5 Transformer",
#     version="0.1"
# )


# # model and tokenizer loading
# model = T5ForConditionalGeneration.from_pretrained("./saved_summary_model")
# tokenizer = AutoTokenizer.from_pretrained(
#     "./saved_summary_model",
#     use_fast=True
# )


# # Device configuration
# if torch.backends.mps.is_available():
#     device = "mps"
# elif torch.cuda.is_available():
#     device = "cuda"
# elif hasattr(torch, "xpu") and torch.xpu.is_available():
#     device = "xpu"
# elif hasattr(torch.backends, "hip") and torch.backends.hip.is_available():
#     device = "hip"
# else:
#     device = "cpu"

# model.to(device)


# # templates configuration
# templates = Jinja2Templates(directory=".")


# # Input Schema for dialogue => string
# class DailogueInput(BaseModel):
#     dialogue: str


# # clean the dialogue text
# def clean_data(text):
#     text = re.sub(r"\r\n", " ", text)  # remove \n lines that kind of symbol
#     text = re.sub(r"\s+", " ", text)   # remove extra spaces
#     text = re.sub(r"<.*?>", " ", text) # remove HTML tags ex:- <h1>, <b>
#     text = text.strip().lower()
#     return text


# # summarization function
# def summerize_dialogue(dialogue: str) -> str:
#     dialogue = clean_data(dialogue)  # clean the text remove space, html tag, to lowercase

#     # tokenize
#     inputs = tokenizer(
#         dialogue,
#         padding="max_length",
#         max_length=512,       # limit words to 512
#         truncation=True,      # cut extra words
#         return_tensors="pt"   # make tensor for PyTorch
#     ).to(device)

#     # generate the summary ==> token ids
#     targets = model.generate(
#         input_ids=inputs["input_ids"],             # input text ids
#         attention_mask=inputs["attention_mask"],  # focus on real words
#         max_length=150,
#         num_beams=4,      # Transformer generate 4 outputs, compare and select best summary
#         early_stopping=True
#     )

#     # decode the output tokenization ===> Readable Word
#     # ex:- [213,32424,4232] =====> "I love Python"
#     summary = tokenizer.decode(
#         targets[0],
#         skip_special_tokens=True
#     )

#     return summary


# # API Endpoint for summarization Route
# @app.post("/summarize/")
# async def create_item(Dialogue_input: DailogueInput):
#     summary = summerize_dialogue(Dialogue_input.dialogue)
#     return {"summary": summary}


# # Home Page Route
# @app.get("/", response_class=HTMLResponse)
# async def home(request: Request):
#     return templates.TemplateResponse(
#         "index.html",
#         {"request": request}
#     )