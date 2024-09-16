import base64
from transformers import CLIPProcessor, CLIPModel
from PIL import Image
import torch
from typing import List
from io import BytesIO


class CLIPEmbeddings():
    def __init__(self, clip="patrickjohncyh/fashion-clip"):
        self.device = torch.device(
            "cuda" if torch.cuda.is_available() else "cpu")
        self.model = CLIPModel.from_pretrained(clip).to(self.device)
        self.processor = CLIPProcessor.from_pretrained(clip)

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return [self.embed_document(t) for t in texts]

    def embed_query(self, text):
        return self.embed_document(text)

    def embed_document(self, text):
        return self.embed_text(text)

    def embed_text(self, text):
        text_inputs = self.processor(
            text=text,
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=77
        ).to(self.device)

        # Get the text embedding
        with torch.no_grad():
            text_embedding = self.model.get_text_features(**text_inputs)
        return text_embedding.cpu().tolist()[0]

    def embed_image(self, base64_string):
        image_data = base64.b64decode(base64_string)
        image_io = BytesIO(image_data)
        image = Image.open(image_io)

        inputs = self.processor(
            images=image, return_tensors="pt").to(self.device)

        # Get the image embedding
        with torch.no_grad():
            image_embedding = self.model.get_image_features(**inputs)
        return image_embedding.cpu().tolist()[0]
