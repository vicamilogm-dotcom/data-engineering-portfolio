import torch
import transformers

tokenizer = transformers.AutoTokenizer.from_pretrained(
    "prajjwal1/bert-tiny", model_max_length=512
)
model = transformers.AutoModel.from_pretrained("prajjwal1/bert-tiny")


def create_vectorized_representation(string: str):
    """
    Given a string, return a list of floats representing the vectorized
    representation of the string in 128 dimensions.
    """
    tokens = tokenizer(string, truncation=True, return_tensors="pt")
    with torch.no_grad():
        output = model(**tokens)
    embedding = output.last_hidden_state[:, 0, :][0].numpy().tolist()
    return embedding
