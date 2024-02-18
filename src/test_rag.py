from chains import Chains

Chains.setLlm()

history = """
Customer: Hi, I am looking for a lift chair but wonder the types.
Customer Rep: Sure, there are 4 types
Customer: What are they?
"""

"""question = Chains.generateQuestion(history=history)

print("question:",question)

answer = Chains.rag(question=question)

print("answer:",answer)"""

res = Chains.decide(history=history)
print(res)