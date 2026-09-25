from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy
from datasets import Dataset

from src.rag_engine import ask_firesafe


questions = [
    "What are the components of means of egress?",
    "What does NBC 2016 Part 4 cover?",
    "What is the role of life safety provisions?"
]


answers = []
contexts = []

for question in questions:

    answer, results = ask_firesafe(question)

    answers.append(answer)

    context = [
        document.page_content
        for document in results
    ]

    contexts.append(context)


data = {
    "question": questions,
    "answer": answers,
    "contexts": contexts
}


dataset = Dataset.from_dict(data)


result = evaluate(
    dataset,
    metrics=[
        faithfulness,
        answer_relevancy
    ]
)


print("=" * 60)
print("FireSafe-AI RAGAS Evaluation")
print("=" * 60)

print(result)