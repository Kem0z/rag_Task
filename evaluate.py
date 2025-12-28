import requests
import json
import statistics

API_URL = "http://127.0.0.1:8000/query"

# Sample Questions (TriviaQA style)
test_questions = [
    {"q": "What is the capital of France?", "a": "Paris"},
    {"q": "Who wrote Romeo and Juliet?", "a": "Shakespeare"},
    {"q": "What is the chemical symbol for Gold?", "a": "Au"},
    {"q": "Which planet is known as the Red Planet?", "a": "Mars"},
    {"q": "In which year did Titanic sink?", "a": "1912"}
]

def evaluate():
    print(f"Starting Evaluation on {len(test_questions)} questions...")
    print("-" * 60)
    
    latencies = []
    results = []

    for item in test_questions:
        try:
            response = requests.post(API_URL, json={"question": item["q"]})
            if response.status_code == 200:
                data = response.json()
                latencies.append(data['latency_ms'])
                
                # Basic Keyword matching for 'Correctness' (Simplistic for auto-eval)
                generated_answer = data['answer']
                is_correct = item['a'].lower() in generated_answer.lower()
                
                print(f"Q: {item['q']}")
                print(f"A (Expected): {item['a']}")
                print(f"A (Generated): {generated_answer}")
                print(f"Latency: {data['latency_ms']}ms")
                print(f"Correct Context retrieved? {'Yes' if len(data['retrieved_context']) > 0 else 'No'}")
                print("-" * 60)
                
                results.append(is_correct)
            else:
                print(f"Error calling API: {response.text}")
        except Exception as e:
            print(f"Connection error: {e}")

    if latencies:
        avg_latency = statistics.mean(latencies)
        accuracy = (sum(results) / len(results)) * 100
        
        print("\n=== SUMMARY REPORT ===")
        print(f"Average Latency: {avg_latency:.2f} ms")
        print(f"Accuracy (Keyword Match): {accuracy}%")
        print("======================")

if __name__ == "__main__":
    evaluate()