import random
import os

def load_question_bank(file_path="question_bank.txt"):
    """
    Loads questions from a file, assuming each question is on one line
    and its answer is on the next line
    """
    question_bank = []
    print(f"Attempting to load bank from: {file_path}")

    try:
        with open(file_path, "r", encoding='utf-8') as file:
            lines = file.readlines()
        #Parse questions and answers, assuming a Q/A alternation
        for i in range(0, len(lines),2):
            if i+1<len(lines):
                question = lines[i].strip()
                answer = lines[i+1].strip()

                if question and answer:
                    question_bank.append({
                        'question':question,
                        'answer': answer
                    })
        print(f"Successfully loaded {len(question_bank)} question-answer pairs.")

    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found in the current directory.")
        print("Please ensure your question_bank.txt is in the same folder as this script.")
        return []

    return question_bank

def generate_exam(bank, num_questions, professor_name= "Professor"):
    """
    Randomly selects a specified number of questions from the bank
    and formats the content into a string.
    """
    if  not bank:
        print("Error: Question bank is empty. Cannot generate exam. ")
        return None
    if num_questions >len(bank):
        print(f"Error: Requested {num_questions} questions, but bank only has{len(bank)}.")
        return None

    # Using random.sample() to select questions without replacement
    selected = random.sample(bank, num_questions)

    exam_content = f"EXAM - Created by Professor {professor_name}\n"
    exam_content += "="* 60 + "\n\n"
    for i, pair in enumerate(selected, 1):
        exam_content += f"Question {i}: {pair['question']}\n"
        exam_content += f"Answer: {pair['answer']}\n\n"

    return exam_content
if __name__ == "__main__":
    bank = load_question_bank()

    if bank:
        # User defined parameters for the test run
        num_to_generate = 3
        professor = os.environ.get('USERNAME', 'Default Professor') #tris to get system username
        output_file = "generated_exam.txt"

        #check if we have enough questions
        if num_to_generate > len(bank):
            num_to_generate = len(bank)
            print(f"Adjusting questions to max available: {num_to_generate}")

        exam_text = generate_exam(bank, num_to_generate, professor)

        if exam_text:
            with open (output_file, 'w', encoding='utf-8') as f:
                f.write(exam_text)

            print("-" * 60)
            print(f"Success! Created a {num_to_generate}-question exam.")
            print(f"Content saved to {output_file}.")
            print("-" * 60)
            print(exam_text)