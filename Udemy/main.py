import tiktoken

enc = tiktoken.encoding_for_model("gpt-4o")

text = "Hey there! my name is Soumadip Majila"

tokens = enc.encode(text)

print(
    "Tokens: ", tokens
)  # Tokens:  [25216, 1354, 922, 1308, 382, 17228, 30273, 488, 18968, 4977]

decoded = enc.decode([25216, 1354, 922, 1308, 382, 17228, 30273, 488, 18968, 4977])
print("Decode Token: ", decoded)
