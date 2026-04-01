#pip install transformers sentencepiece torch --quiet

from transformers import MarianMTModel, MarianTokenizer

model_name = "Helsinki-NLP/opus-mt-en-ur"
tokenizer = MarianTokenizer.from_pretrained(model_name)
model = MarianMTModel.from_pretrained(model_name)

sentences = [
    "Hello, how are you?",
    "Machine Translation is a powerful NLP task.",
    "Transformers are widely used in modern NLP.",
]

for text in sentences:
    tokens = tokenizer(text, return_tensors="pt", padding=True)
    translation = model.generate(**tokens)
    output = tokenizer.decode(translation[0], skip_special_tokens=True)
    print(f"English: {text}")
    print(f"Urdu: {output}\n")
