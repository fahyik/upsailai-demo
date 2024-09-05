import copy
from typing import Iterable, List
import json

from langchain.docstore.document import Document
from langchain.text_splitter import TextSplitter


class ProductDocumentSplitter(TextSplitter):
    def split_text(self, text: str) -> List[str]:
        raise "not implemented, which should not be used"

    def update_metadata(self, metadata, **kwargs):
        _metadata = copy.deepcopy(metadata)
        for k, v in kwargs.items():
            _metadata[k] = v
        return _metadata

    def _split_document(self, document: Document):
        product = json.loads(document.page_content)
        metadata = document.metadata
        docs = [
            Document(page_content=image_encoding, metadata=self.update_metadata(
                metadata, field='image', _type='image'))
            for image_encoding in product['image_encodings']
        ]

        if 'category' in product:
            # docs.append(Document(page_content=product['category'], metadata=self.update_metadata(metadata, field='category', _type='text')))

            color_text = product['color']['color'] + '\n' + \
                '\n'.join(product['color']['descriptions'])
            docs.append(Document(page_content=color_text, metadata=self.update_metadata(
                metadata, field='color', _type='text')))

            # if product['pattern'].get('pattern') is not None:
            #     docs.append(Document(page_content=product['pattern']['pattern'], metadata=self.update_metadata(metadata, field='pattern', _type='text')))
            #     for pattern_description in product['pattern']['descriptions']:
            #         docs.append(Document(page_content=pattern_description, metadata=self.update_metadata(metadata, field='pattern', _type='text')))

            style_text = '\n'.join(product['style']['styles']) + '\n' + product['style']['description'] if isinstance(
                product['style']['description'], str) else '\n'.join(list(product['style']['description'].values()))
            docs.append(Document(page_content=style_text, metadata=self.update_metadata(
                metadata, field='style', _type='text')))

            for occasion in product['occasions']['occasions']:
                docs.append(Document(page_content=occasion['name'] + '\n' + occasion['description'],
                            metadata=self.update_metadata(metadata, field='occasion', _type='text')))

            for season in product['season']:
                docs.append(Document(page_content=season['name'] + '\n' + season['description'],
                            metadata=self.update_metadata(metadata, field='season', _type='text')))

            for weather in product['weather']:
                docs.append(Document(page_content=weather['name'] + '\n' + weather['description'],
                            metadata=self.update_metadata(metadata, field='weather', _type='text')))

            docs.append(Document(page_content=product['description'], metadata=self.update_metadata(
                metadata, field='description', _type='text')))

        return docs

    def split_documents(self, documents: Iterable[Document]) -> List[Document]:
        return [
            sub_doc
            for doc in documents
            for sub_doc in self._split_document(doc)
        ]
