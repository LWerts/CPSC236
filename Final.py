import time
from random import randint

# Validate student ID
def is_valid_id(student_id):
    """Checks if the ID starts with 'A' followed by 5 digits between 1-9."""
    if len(student_id) != 6 or student_id[0] != 'A':
        return False
    for ch in student_id[1:]:
        if ch not in '123456789':
            return False
    return True

# Get student information
def get_student_info():
    """Prompt for and validate student's name and ID."""
    attempts = 0
    while attempts < 3:
        first_name = input("Enter your first name: ").strip().title()
        last_name = input("Enter your last name: ").strip().title()
        student_id = input("Enter your student ID (e.g., A12345): ").strip()

        if is_valid_id(student_id):
            return student_id, first_name, last_name
        else:
            attempts += 1
            print("Invalid ID. Attempts remaining:", 3 - attempts)

    print("Too many failed attempts. Exiting program.")
    exit()

# Load questions from a plain text file
def load_questions_from_txt(Capitals_Quiz_Testbank):
    """Reads questions from a TXT file with a specific format."""
    questions = []
    try:
        with open(Capitals_Quiz_Testbank, "r") as file:
            lines = [line.strip() for line in file if line.strip() != ""]

        i = 0
        while i + 5 < len(lines):
            question = lines[i]
            choices = [lines[i+1], lines[i+2], lines[i+3], lines[i+4]]
            answer_line = lines[i+5]
            if "Answer:" in answer_line:
                answer = answer_line.split(":")[-1].strip().upper()
                questions.append({
                    "question": question,
                    "choices": choices,
                    "answer": answer
                })
            i += 6
    except Exception as e:
        print("Error reading the TXT file:", e)
        exit()

    return questions

# Ask questions
def ask_questions(selected_questions):
    """Display one question at a time, validate input, and return user answers."""
    answers = {}
    index = 1

    for q in selected_questions:
        print(f"\nQuestion {index}: {q['question']}")
        for choice in q['choices']:
            print(choice)

        user_answer = input("Your answer (A/B/C/D): ").strip().upper()
        while user_answer not in ['A', 'B', 'C', 'D']:
            print("Invalid answer. Please enter A, B, C, or D.")
            user_answer = input("Your answer (A/B/C/D): ").strip().upper()

        answers[q['question']] = (q['answer'], user_answer)
        index += 1

    return answers

# Calculate score
def calculate_score(answers):
    """Calculate score based on correct answers."""
    correct = 0
    for correct_ans, user_ans in answers.values():
        if correct_ans == user_ans:
            correct += 1
    return correct

# Save results to file
def save_results(student_id, first_name, last_name, score, elapsed_time, answers):
    """Write the quiz results to a file named StudentID_First_Last.txt"""
    Capitals_Quiz_Testbank = f"{student_id}_{first_name}_{last_name}.txt"
    with open(Capitals_Quiz_Testbank, "w") as file:
        file.write(f"Student: {first_name} {last_name}\n")
        file.write(f"ID: {student_id}\n")
        file.write(f"Score: {score}/10\n")
        file.write(f"Elapsed Time: {elapsed_time:.2f} seconds\n\n")
        for q in answers:
            correct, user = answers[q]
            file.write(f"Q: {q}\n")
            file.write(f"Correct: {correct}, Your Answer: {user}\n\n")
    print("Results saved to", Capitals_Quiz_Testbank, "\n")

# Get current time in seconds
def current_time_seconds():
    return time.time()

# Run the quiz
def run_quiz():
    """Run one full quiz session."""
    student_id, first_name, last_name = get_student_info()
    questions = load_questions_from_txt("Capitals_Quiz_Testbank.txt")

    if len(questions) < 10:
        print("Not enough questions in the test bank. Please add more questions.")
        exit()

    selected_indices = []
    while len(selected_indices) < 10:
        i = randint(0, len(questions) - 1)
        if i not in selected_indices:
            selected_indices.append(i)

    selected_questions = [questions[i] for i in selected_indices]

    start_time = current_time_seconds()
    answers = ask_questions(selected_questions)
    elapsed_time = current_time_seconds() - start_time

    score = calculate_score(answers)
    print(f"\nQuiz complete!\nScore: {score}/10\nTime Taken: {elapsed_time:.2f} seconds")

    save_results(student_id, first_name, last_name, score, elapsed_time, answers)

# Main loop
def main():
    """Main menu loop for restarting or exiting."""
    while True:
        run_quiz()
        choice = input("Enter 'S' to start a new quiz, or 'Q' to quit: ").strip().upper()
        if choice == 'Q':
            print("Goodbye!")
            break
        elif choice == 'S':
            print("\nStarting a new quiz...\n")
        else:
            print("Invalid choice. Exiting.")
            break

if __name__ == "__main__":
    main()
