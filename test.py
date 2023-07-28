import cohere
import numpy as np

from commons.secret import COHERE_KEY

co = cohere.Client(COHERE_KEY)

user_prompt = "Give me a financial advisor that is an expert at stocks and debt management."

a1 = "Retirement Planning, Stocks, 	Real Estate Investment"
a2 = "General Financial Planning, Debt Management, Bonds"

phrases = [user_prompt, a1, a2]
(user_embed, a1_embed, a2_embed) = co.embed(phrases).embeddings

def calculate_similarity(a, b):
  return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

res1 = calculate_similarity(user_embed, a1_embed)
res2 = calculate_similarity(user_embed, a2_embed)

print(res1)
print(res2)

