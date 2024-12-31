import json
from difflib import get_close_matches
import pyautogui
from datetime import datetime
from generateFacts import extract_facts_with_titles, save_facts_to_json


def calculate_time():
    # Get the current date and time
    current_datetime = datetime.now()

    # Extract the current time
    current_time = current_datetime.time()

    # Format the current time as a string
    formatted_time = current_time.strftime("%H:%M:%S")

    return ("Current Time is " , formatted_time)


def load_chat_data( file_path : str ):
    with open( file_path, 'r' ) as file:
        data : dict = json.load(file)
    return data

def save_chat_data( file_path : str , data : json):
    with open( file_path , 'w' ) as file:
        json.dump( data , file , indent=2 )


def find_best_match( user_question : str , questions : list[str] ):
    matches : list  = get_close_matches(user_question , questions , n= 1 )
    if( matches ):
        return matches[0]
    return None

def get_answer_for_question( question : str , knowledge_base : dict):
    for q in knowledge_base['questions']:
        if  q['question'] == question:
            return q['answer']
        
def chatbot(user_input: str):
    knowledge_base: dict = load_chat_data(r"C:\Users\RAJ ENTERPRISES\Downloads\chatbot\flask-server\extracted_facts.json")
    
    best_matches: str = find_best_match(user_input, [q["question"] for q in knowledge_base["questions"]])
    if best_matches: 
        answer: str = get_answer_for_question(best_matches, knowledge_base)
        print(f'{answer}')
        return f'{answer}' 
    elif user_input.lower() == "skip":
        print(f'{"alright sir"}')
        return f'{"alright sir"}'
    elif "time" in user_input.lower():
        return calculate_time()
    elif "switch" in user_input.lower(): 
        pyautogui.hotkey('alt', 'tab') 
        return "switching tab"
    elif "close tab" in user_input.lower():
        pyautogui.hotkey('ctrl', 'w')
        return "closing tab"
    elif 'ans is' in user_input.lower():
        user_data = user_input.split("-")
        get_question = user_data[1].strip()
        get_answer = user_data[2].strip()
        knowledge_base['questions'].append({"question": get_question, "answer": get_answer})
        save_chat_data(r"C:\Users\RAJ ENTERPRISES\Downloads\chatbot\flask-server\extracted_facts.json", knowledge_base)
        print("Bot: Thank you! I learned a new response")
        return "Thank you! I learned a new response"
    else:
        return "ok give me answer"

# while True:
#     user_input : str = input("User: ")
#     if( user_input.lower() == "quit" ):
#         break
#     chatbot(user_input)


from flask import Flask, request, jsonify
from flask_cors import CORS 

app = Flask(__name__)
CORS(app)


@app.route('/chat', methods=['POST'])
def handle_chat():
    data = request.json
    user_input = data['input']
    response = chatbot(user_input)  # Call your chatbot function
    return jsonify({'response': response})


@app.route('/generate-facts', methods=['POST'])
def generate_facts():
    data = request.json
    input_text = data.get('text', '')

    if not input_text:
        return jsonify({'error': 'No text provided'}), 400

    try:
        extracted_facts = extract_facts_with_titles(input_text)
        save_facts_to_json(extracted_facts)
        return jsonify({'facts': extracted_facts})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)


# stramlit code

# import streamlit as st
# import json
# import spacy
# from spacy.lang.en.stop_words import STOP_WORDS
# from string import punctuation
# from collections import Counter
# from heapq import nlargest
# from difflib import get_close_matches
# from datetime import datetime

# # Initialize spaCy
# @st.cache_resource
# def load_spacy_model():
#     return spacy.load("en_core_web_sm")

# def extract_facts_with_titles(text):
#     nlp = load_spacy_model()
#     doc = nlp(text)
    
#     # Calculate word frequencies
#     word_frequencies = Counter()
#     for word in doc:
#         if word.text.lower() not in STOP_WORDS and word.text.lower() not in punctuation:
#             word_frequencies[word.text] += 1
    
#     # Normalize word frequencies
#     max_frequency = max(word_frequencies.values()) if word_frequencies else 1
#     for word in word_frequencies.keys():
#         word_frequencies[word] = word_frequencies[word] / max_frequency
    
#     # Calculate sentence scores
#     sentence_scores = {}
#     for sent in doc.sents:
#         for word in sent:
#             if word.text.lower() in word_frequencies.keys():
#                 if sent not in sentence_scores.keys():
#                     sentence_scores[sent] = word_frequencies[word.text.lower()]
#                 else:
#                     sentence_scores[sent] += word_frequencies[word.text.lower()]
    
#     # Extract top sentences as facts
#     select_length = min(5, len(sentence_scores))
#     summary_sentences = nlargest(select_length, sentence_scores, key=sentence_scores.get)
    
#     def generate_title(sentence):
#         # Try to find a named entity for the title
#         for ent in sentence.ents:
#             if ent.label_ in ['ORG', 'PERSON', 'GPE', 'PRODUCT']:
#                 return ent.text

#         # If no suitable named entity, use the subject of the sentence
#         for token in sentence:
#             if token.dep_ == 'nsubj':
#                 return token.text

#         # If no subject found, use the first noun chunk
#         for chunk in sentence.noun_chunks:
#             return chunk.text

#         # If all else fails, return the first three words
#         return ' '.join([token.text for token in sentence[:3]])

#     facts = []
#     for sentence in summary_sentences:
#         title = generate_title(sentence)
#         facts.append({"question": title, "answer": sentence.text.strip()})
    
#     return facts

# def save_facts_to_json(facts, filename="extracted_facts.json"):
#     try:
#         with open(filename, 'r', encoding='utf-8') as file:
#             existing_data = json.load(file)
#     except (FileNotFoundError, json.JSONDecodeError):
#         existing_data = {"questions": []}
    
#     existing_data["questions"].extend(facts)
    
#     with open(filename, 'w', encoding='utf-8') as file:
#         json.dump(existing_data, file, indent=4)

# def load_chat_data(file_path: str):
#     try:
#         with open(file_path, 'r') as file:
#             return json.load(file)
#     except (FileNotFoundError, json.JSONDecodeError):
#         return {"questions": []}

# def find_best_match(user_question: str, questions: list[str]):
#     matches = get_close_matches(user_question, questions, n=1, cutoff=0.6)
#     return matches[0] if matches else None

# def get_answer_for_question(question: str, knowledge_base: dict):
#     for q in knowledge_base["questions"]:
#         if q["question"] == question:
#             return q["answer"]
#     return None

# def calculate_time():
#     current_time = datetime.now().strftime("%H:%M:%S")
#     return f"Current Time is {current_time}"

# def main():
#     st.title("AI Chatbot with Fact Extraction")
    
#     # Initialize session state for chat history if it doesn't exist
#     if "chat_history" not in st.session_state:
#         st.session_state.chat_history = []
    
#     # Sidebar for fact extraction
#     st.sidebar.header("Fact Extraction")
#     input_text = st.sidebar.text_area("Enter text for fact extraction:", height=200)
#     if st.sidebar.button("Extract Facts"):
#         if input_text:
#             facts = extract_facts_with_titles(input_text)
#             save_facts_to_json(facts)
#             st.sidebar.success("Facts extracted and saved successfully!")
#             st.sidebar.write("Extracted Facts:")
#             for fact in facts:
#                 st.sidebar.markdown(f"**{fact['question']}**")
#                 st.sidebar.write(fact['answer'])
    
#     # Main chat interface
#     st.header("Chat Interface")
    
#     # Display chat history
#     for message in st.session_state.chat_history:
#         with st.chat_message(message["role"]):
#             st.write(message["content"])
    
#     # Chat input
#     if prompt := st.chat_input("What's on your mind?"):
#         # Add user message to chat history
#         st.session_state.chat_history.append({"role": "user", "content": prompt})
        
#         # Process the message
#         knowledge_base = load_chat_data("extracted_facts.json")
        
#         if "time" in prompt.lower():
#             response = calculate_time()
#         else:
#             best_match = find_best_match(prompt, [q["question"] for q in knowledge_base["questions"]])
#             if best_match:
#                 response = get_answer_for_question(best_match, knowledge_base)
#             elif 'ans is' in prompt.lower():
#                 try:
#                     user_data = prompt.split("-")
#                     get_question = user_data[1].strip()
#                     get_answer = user_data[2].strip()
#                     knowledge_base['questions'].append({"question": get_question, "answer": get_answer})
#                     save_facts_to_json([{"question": get_question, "answer": get_answer}])
#                     response = "Thank you! I learned a new response"
#                 except IndexError:
#                     response = "Please format your answer as 'ans is - question - answer'"
#             else:
#                 response = "I don't know the answer to that. You can teach me using 'ans is - question - answer' format."
        
#         # Add assistant response to chat history
#         st.session_state.chat_history.append({"role": "assistant", "content": response})
        
#         # Display the new message
#         with st.chat_message("assistant"):
#             st.write(response)

# if __name__ == "__main__":
#     main()