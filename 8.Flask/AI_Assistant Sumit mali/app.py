from flask import Flask, render_template, request, redirect, url_for
import os
import markdown
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY")

client = OpenAI(
    api_key=api_key,
    base_url="https://openrouter.ai/api/v1"
)

app = Flask(__name__, static_folder="static", template_folder="templates")

@app.route("/")
def home():
    # Pass empty variables initially so the template renders cleanly
    return render_template("index.html", question="", result="", email="", ans="")

@app.route("/ask", methods=["POST"])
def ask():
    question = request.form.get("question", "")
    try:
        # Correct OpenAI/OpenRouter syntax
        response = client.chat.completions.create(
            model="openai/gpt-4o-mini", # Corrected model name format
            max_tokens=800,
            temperature=0.7,
            messages=[
                {"role": "system", "content": "Act like a helpful personal assistant. Format your responses with clear paragraphs and bullet points."},
                {"role": "user", "content": question}
            ]
        )
        raw_text = response.choices[0].message.content.strip()
        
        # Convert the AI's markdown (**, -, etc) into HTML
        result_html = markdown.markdown(raw_text)
        
        return render_template("index.html", question=question, result=result_html, email="", ans="")
    except Exception as e:
        return render_template("index.html", question=question, result=f"<p>Error: {str(e)}</p>", email="", ans="")

@app.route("/summarize", methods=["POST"])
def summarize():
    email_text = request.form.get("email", "")
    prompt = f"Summarize the following email in 2-3 sentences:\n\n{email_text}"
    try:
        response = client.chat.completions.create(
            model="openai/gpt-4o-mini",
            max_tokens=500,
            temperature=0.7,
            messages=[
                {"role": "system", "content": "Act like an expert email assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        raw_text = response.choices[0].message.content.strip()
        ans_html = markdown.markdown(raw_text)
        
        return render_template("index.html", question="", result="", email=email_text, ans=ans_html)
    except Exception as e:
        return render_template("index.html", question="", result="", email=email_text, ans=f"<p>Error: {str(e)}</p>")

if __name__ == "__main__":
    app.run(debug=True)








# from flask import Flask,render_template,url_for,request , jsonify ,redirect
# import os

# from dotenv import load_dotenv
# load_dotenv()

# api_key = os.getenv("OPENROUTER_API_KEY")
# from openai import OpenAI

# client = OpenAI(
#     api_key=api_key,
#     base_url="https://openrouter.ai/api/v1"
# )



# app = Flask(__name__,static_folder="static",template_folder="templates")

# @app.route("/")
# def home():
#     return render_template("index.html")
 

# @app.route("/ask",methods=["POST"])
# def ask():
#     if request.method == "POST":
#         question =request.form["question"]
#         response = client.responses.create(
#             model="openai/gpt-4.1-mini",
#             max_output_tokens=500,
#             temperature = 0.7,
#             input=[{"role":"system" , "Content": "Act like a Help full personal assistant"},
#                 {"role":"user" , "content":question}]
#             )
#         result = response.output_text.strip()
#         return render_template("index.html", result= result)
#     else:
#         redirect(url_for("/"))

# @app.route("/summarize",methods=["POST"])
# def summarize():
#     if request.method == "POST":
#         email_text = request.form["email"]
#         prompt= f"summarize the following email in 2-3 sentences:{email_text}"
#         response = client.responses.create(
#             model="openai/gpt-4.1-mini",
#             max_output_tokens=500,
#             temperature = 0.7,
#             input=[{"role":"system" , "Content": "Act like a expert email Assistant"},
#               {"role":"user" , "content":prompt}]
#             )
#         ans = response.output_text.strip()
#         return render_template("index.html",ans = ans)
#     else:
#         redirect(url_for("/"))
# if __name__ == "__main__":
#     app.run(debug=True)