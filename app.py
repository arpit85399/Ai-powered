=== Project 1: AI-Powered Chatbot ===

Requirements: flask, transformers, sqlite3

from flask import Flask, request, jsonify from transformers import pipeline import sqlite3

Initialize chatbot and DB

chatbot = pipeline("text-generation", model="gpt2") app = Flask(__name__) conn = sqlite3.connect("chatlogs.db", check_same_thread=False) cursor = conn.cursor() cursor.execute("CREATE TABLE IF NOT EXISTS logs (user_input TEXT, reply TEXT)")

@app.route("/chat", methods=["POST"]) def chat(): data = request.json user_input = data.get("message", "") response = chatbot(user_input, max_length=50) reply = response[0]['generated_text']

# Log conversation
cursor.execute("INSERT INTO logs VALUES (?, ?)", (user_input, reply))
conn.commit()

return jsonify({"reply": reply})

if name == 'main': app.run(debug=True)

=== Project 2: Automated Resume Parser ===

Requirements: flask, pdfplumber, spacy, psycopg2-binary

import pdfplumber import spacy import psycopg2 from flask import Flask, request, jsonify
 app = Flask(__name__) nlp = spacy.load("en_core_web_sm")

PostgreSQL Connection (update credentials)

conn = psycopg2.connect( database="resume_db", user="postgres", password="yourpass", host="localhost", port="5432" ) cursor = conn.cursor() cursor.execute(""" CREATE TABLE IF NOT EXISTS candidates ( name TEXT, skills TEXT, education TEXT ) """)

Extract text from PDF

def extract_text_from_pdf(file): with pdfplumber.open(file) as pdf: return "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])

Extract entities

def extract_details(text): doc = nlp(text) name = doc.ents[0].text if doc.ents else "Unknown" skills = [ent.text for ent in doc.ents if ent.label_ == "SKILL"] education = [ent.text for ent in doc.ents if ent.label_ == "EDUCATION"] return name, skills, education

@app.route("/upload", methods=["POST"]) def upload(): file = request.files['resume'] text = extract_text_from_pdf(file) name, skills, education = extract_details(text)

# Save to DB
cursor.execute("INSERT INTO candidates VALUES (%s, %s, %s)", (name, str(skills), str(education)))
conn.commit()

return jsonify({
    "name": name,
    "skills": skills,
    "education": education
})

if name == 'main': app.run(port=5001, debug=True)

