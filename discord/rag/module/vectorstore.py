from typing import Any, List, Optional
import uuid

from langchain.vectorstores import VectorStore
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document


class MultiModalChroma(Chroma):
    def add_documents(self, documents: List[Document], **kwargs: Any) -> List[str]:
        if type(self).add_texts != VectorStore.add_texts:
            if "ids" not in kwargs:
                ids = [doc.id for doc in documents]

                # If there's at least one valid ID, we'll assume that IDs
                # should be used.
                if any(ids):
                    kwargs["ids"] = ids

            images = [doc.page_content for doc in documents if doc.metadata.get(
                "_type") == 'image']
            image_metadatas = [
                doc.metadata for doc in documents if doc.metadata.get("_type") == 'image']

            texts = [doc.page_content for doc in documents if doc.metadata.get(
                "_type") != 'image']
            text_metadatas = [
                doc.metadata for doc in documents if doc.metadata.get("_type") != 'image']

            ids = []
            if len(images) > 0:
                ids = ids + \
                    self.add_base64_images(images, image_metadatas, **kwargs)
            if len(texts) > 0:
                ids = ids + self.add_texts(texts, text_metadatas, **kwargs)

            return ids

        raise NotImplementedError(
            f"`add_documents` and `add_texts` has not been implemented "
            f"for {self.__class__.__name__} "
        )

    def add_base64_images(
        self,
        b64_texts: List[str],
        metadatas: Optional[List[dict]] = None,
        ids: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> List[str]:
        if ids is None:
            ids = [str(uuid.uuid4()) for _ in b64_texts]
        embeddings = None

        if self._embedding_function is not None and hasattr(
            self._embedding_function, "embed_image"
        ):
            embeddings = [
                self._embedding_function.embed_image(base64_string=b64_text)
                for b64_text in b64_texts
            ]
        if metadatas:
            # fill metadatas with empty dicts if somebody
            # did not specify metadata for all images
            length_diff = len(b64_texts) - len(metadatas)
            if length_diff:
                metadatas = metadatas + [{}] * length_diff
            empty_ids = []
            non_empty_ids = []
            for idx, m in enumerate(metadatas):
                if m:
                    non_empty_ids.append(idx)
                else:
                    empty_ids.append(idx)
            if non_empty_ids:
                metadatas = [metadatas[idx] for idx in non_empty_ids]
                images_with_metadatas = [b64_texts[idx]
                                         for idx in non_empty_ids]
                embeddings_with_metadatas = (
                    [embeddings[idx]
                        for idx in non_empty_ids] if embeddings else None
                )
                ids_with_metadata = [ids[idx] for idx in non_empty_ids]
                try:
                    self._collection.upsert(
                        metadatas=metadatas,  # type: ignore
                        embeddings=embeddings_with_metadatas,  # type: ignore
                        documents=images_with_metadatas,
                        ids=ids_with_metadata,
                    )
                except ValueError as e:
                    if "Expected metadata value to be" in str(e):
                        msg = (
                            "Try filtering complex metadata using "
                            "langchain_community.vectorstores.utils.filter_complex_metadata."
                        )
                        raise ValueError(e.args[0] + "\n\n" + msg)
                    else:
                        raise e
            if empty_ids:
                images_without_metadatas = [b64_texts[j] for j in empty_ids]
                embeddings_without_metadatas = (
                    [embeddings[j] for j in empty_ids] if embeddings else None
                )
                ids_without_metadatas = [ids[j] for j in empty_ids]
                self._collection.upsert(
                    embeddings=embeddings_without_metadatas,
                    documents=images_without_metadatas,
                    ids=ids_without_metadatas,
                )
        else:
            self._collection.upsert(
                embeddings=embeddings,
                documents=b64_texts,
                ids=ids,
            )
        return ids
