import nltk
from nltk.tokenize import sent_tokenize
from rake_nltk import Rake
import random
import requests
import re

# Step 1: Import the text file
with open("file.txt", "r") as file:
    text = file.read()

# Step 2: Text Preprocessing
def preprocess_text(text):
    sentences = sent_tokenize(text)
    cleaned_sentences = []
    for sentence in sentences:
        sentence = sentence.strip()
        if len(sentence) > 15:
            cleaned_sentences.append(sentence)
    return cleaned_sentences

cleaned_sentences = preprocess_text(text)

# Step 3: Keyword Extraction using RAKE
def get_important_words(text):
    r = Rake()
    r.extract_keywords_from_text(text)
    return r.get_ranked_phrases()[:25]

important_words = get_important_words(text)

# Step 4: Generate MCQs with matched answers and random distractors
num_questions = int(input("Enter the number of questions to generate: "))

with open("mcq_with_matched_answers.txt", "w") as mcq_file:
    for iterator in range(1, num_questions + 1):
        keyword = random.choice(important_words)
        sentence = random.choice(cleaned_sentences)  # Randomly select a sentence
        pattern = re.compile(keyword, re.IGNORECASE)
        question = pattern.sub("________", sentence)

        # Generate random distractors
        def generate_random_distractors(answer, distractor_count, important_words):
            distractors = []
            while len(distractors) < distractor_count:
                random_word = random.choice(important_words)
                if random_word.lower() != answer.lower() and random_word not in distractors:
                    distractors.append(random_word)
            return distractors

        answer = keyword.capitalize()
        distractors = generate_random_distractors(answer, 3, important_words)
        options = [answer] + distractors
        random.shuffle(options)
        option_letters = ['a', 'b', 'c', 'd'][:len(options)]  # Ensure option_letters match the number of options

        mcq_file.write(f"Question {iterator} -> {question}\n")

        for i, option in enumerate(options):
            mcq_file.write(f"\t{option_letters[i]}) {option}\n")

        # Write the answer immediately after the options
        mcq_file.write(f"Answer: {answer}\n\n")

print(f"{num_questions} MCQs generated with matched answers and random distractors have been saved to mcq_with_matched_answers.txt")
