import re

def parse_mcqs(text: str):
    questions = []

    blocks = text.split("Q:")

    for block in blocks:
        if not block.strip():
            continue

        try:
            q = re.search(r"^(.*)\nA:", block, re.DOTALL)
            a = re.search(r"A:\s*(.*)", block)
            b = re.search(r"B:\s*(.*)", block)
            c = re.search(r"C:\s*(.*)", block)
            d = re.search(r"D:\s*(.*)", block)
            ans = re.search(r"ANSWER:\s*([A-D])", block)

            if not (q and a and b and c and d and ans):
                continue

            questions.append({
                "question": q.group(1).strip(),
                "options": {
                    "A": a.group(1).strip(),
                    "B": b.group(1).strip(),
                    "C": c.group(1).strip(),
                    "D": d.group(1).strip()
                },
                "correct_answer": ans.group(1).strip()
            })

        except:
            continue

    return questions