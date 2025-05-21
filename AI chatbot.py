import requests
import pyfiglet
import itertools
import threading
import sys

url = "https://simple-chatgpt-api.p.rapidapi.com/ask"

headers = {
    "content-type": "application/json",
    "X-RapidAPI-Key": "YOUR_API_KEY",  # Replace with your actual API key
    "X-RapidAPI-Host": "simple-chatgpt-api.p.rapidapi.com"
}

done = False  # Global flag to control animation

# Predefined Q&A dictionary
predefined_answers = {
    "hi": "Hello! How can I help you today?",
    "hello": "Hi there! What can I do for you?",
    "hey": "Hey! Nice to see you. How’s it going?",
    "good morning": "Good morning! Hope you have a great day ahead.",
    "good afternoon": "Good afternoon! How’s your day so far?",
    "good evening": "Good evening! How can I assist you tonight?",
    "how are you?": "I’m just a bot, but I’m here to help you! How are you doing?",
    "what’s up?": "Not much, just ready to assist you. What’s up with you?",
    "nice to meet you!": "Nice to meet you too! How can I help?",
    "what’s your name?": "I’m ChatGPT, your AI assistant.",
    "who made you?": "I was created by OpenAI.",
    "can you talk?": "I can chat with you by text and help answer your questions.",
    "are you real?": "I’m a virtual AI assistant — here to help you anytime!",
    "what can you do?": "I can answer questions, help with tasks, provide information, and chat with you about many topics.",
    "tell me a joke.": "Why don’t scientists trust atoms? Because they make up everything!",
    "what’s the weather today?": "I don’t have live weather data, but you can check your favorite weather app or website for updates.",
    "can you set a reminder?": "I can’t set reminders directly, but you can use your phone or calendar app to do that easily.",
    "how do i reset my password?": "Usually, click “Forgot password” on the login page and follow the instructions sent to your email.",
    "what time is it?": "I can’t check the current time, but you can see it on your device or ask a smart assistant nearby.",
    "how do i make a cake?": "Here’s a simple recipe: mix flour, sugar, eggs, butter, and baking powder. Bake at 350°F (175°C) for about 30 minutes.",
    "what’s the capital of france?": "The capital of France is Paris.",
    "how does photosynthesis work?": "Plants convert sunlight, water, and carbon dioxide into oxygen and glucose through photosynthesis.",
    "explain the pythagorean theorem.": "In a right triangle, the square of the hypotenuse equals the sum of the squares of the other two sides.",
    "who won the world cup in 2022?": "Argentina won the 2022 FIFA World Cup.",
    "how do i convert inches to centimeters?": "Multiply inches by 2.54 to get centimeters.",
    "what movies do you recommend?": "Some popular movies are “Inception,” “The Shawshank Redemption,” and “The Dark Knight.”",
    "what’s trending in the news?": "I don’t have live news updates, but you can check news websites or apps for the latest.",
    "can you translate “hello” to spanish?": "“Hello” in Spanish is “Hola.”",
    "explain artificial intelligence.": "Artificial Intelligence (AI) is the simulation of human intelligence by machines, enabling them to learn, reason, and solve problems.",
    "what is machine learning?": "Machine learning is a type of AI where computers learn from data without explicit programming.",
    "what’s the difference between supervised and unsupervised learning?": "Supervised learning uses labeled data to train models, while unsupervised learning finds patterns in unlabeled data.",
    "how does the traveling salesman problem work?": "It’s about finding the shortest route visiting a set of cities once and returning to the start.",
    "can you write me a python script to sort a list?": "Sure! Here’s a simple example:\n\nmy_list = [3, 1, 4, 2]\nmy_list.sort()\nprint(my_list)",
    "what are the ethical concerns of ai?": "Issues include privacy, bias, job displacement, and accountability.",
    "explain quantum computing in simple terms.": "Quantum computing uses quantum bits that can represent 0 and 1 simultaneously, enabling faster problem-solving.",
    "how does blockchain technology work?": "It’s a decentralized ledger where transactions are securely recorded in blocks linked together.",
    "what is the complexity class np-complete?": "NP-complete problems are those for which no fast solution is known, but verifying a solution is quick.",
    "can you summarize the plot of “1984” by george orwell?": "It’s a dystopian novel about a totalitarian regime that controls everything and manipulates truth.",
    "how do neural networks function?": "Neural networks mimic brain neurons to process data and learn patterns through layers of nodes.",
    "what is reinforcement learning?": "It’s a machine learning method where an agent learns by rewards and punishments through trial and error.",
    "can you help me debug this code?": "Absolutely! Please share the code, and I’ll help identify the problem.",
    "what are the latest trends in ai research?": "Trends include large language models, AI ethics, explainability, and multimodal learning.",
    "explain how gpt models generate text.": "GPT models predict the next word in a sentence based on the context, generating coherent text.",
    "tell me a story.": "Once upon a time, in a magical forest, a curious fox found a glowing treasure that changed his life forever...",
    "write a poem about the ocean.": "The ocean sings a lullaby, waves whisper secrets to the sky...",
    "can you make a joke about cats?": "Why was the cat sitting on the computer? Because it wanted to keep an eye on the mouse!",
    "suggest a workout plan.": "Try this beginner plan: 10-minute warm-up, 3 sets of push-ups, squats, and planks, then 10-minute cooldown stretches.",
    "give me a fun fact about space.": "Did you know that a day on Venus is longer than a year on Venus?",
    "create a riddle for me.": "What has keys but can’t open locks? A piano.",
    "what’s a good birthday gift idea?": "Personalized items like custom mugs or photo albums are thoughtful gifts.",
    "can you generate a random password?": "Sure! Here’s one: G7k!p9Wq2L",
    "what are some fun weekend activities?": "You could go hiking, visit a museum, try a new recipe, or watch a movie with friends."
}


def animate():
    for c in itertools.cycle(['|', '/', '-', '\\']):
        if done:
            break
        sys.stdout.write('\r' + c)
        sys.stdout.flush()
        threading.Event().wait(0.1)
    sys.stdout.write('\r')
    sys.stdout.flush()


def ask(question):
    key = question.lower().strip()
    if key in predefined_answers:
        return predefined_answers[key]

    try:
        payload = {"question": question}
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        return data.get("answer")
    except Exception:
        return None


if __name__ == "__main__":
    print(pyfiglet.figlet_format("AI Chat BOT"))
    print("Enter the question to ask (type 'q' to quit, 'history' to see past Q&A):")
    print()

    history = []

    while True:
        question = input(">>  ")
        if question.lower() == 'q':
            print(">>  Bye! Thanks for Using...")
            break
        elif question.lower() == 'history':
            print("\n--- Chat History ---")
            if not history:
                print("No questions asked yet.")
            else:
                for i, (q, a) in enumerate(history, 1):
                    print(f"{i}. Q: {q}\n   A: {a if a else 'No answer'}\n")
            continue

        done = False
        t = threading.Thread(target=animate)
        t.start()

        answer = ask(question)

        done = True
        t.join()

        if answer is None:
            print(">>  Hello! I am a Chatbot. I am not able to answer your question. Please try again.")
        else:
            print(">> ", answer)

        history.append((question, answer))

        # Save chat to a file (append mode)
        with open("chat_history.txt", "a", encoding="utf-8") as f:
            f.write(f"Q: {question}\nA: {answer if answer else 'No answer'}\n\n")
