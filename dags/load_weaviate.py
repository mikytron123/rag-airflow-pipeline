from llama_index.core import SimpleDirectoryReader
from llama_index.core.node_parser import MarkdownNodeParser
import weaviate
from teiembedding import TextEmbeddingsInference
from llama_index.core.schema import Document
import os
import pandas as pd
from airflow.decorators import dag, task
import pathlib

WEAVIATE_HOST = os.getenv("WEAVIATE_HOST", default="localhost")
TEI_HOST = os.getenv("TEI_HOST", default="localhost")

@dag(
    schedule=None,
    catchup=False,
    tags=["weaviate"],
)
def load_weaviate():
    """
    """
    @task()
    def extract():
        """
        """
        print(os.listdir())
        pth = pathlib.Path().resolve() / "documents"
        documents = SimpleDirectoryReader(str(pth), recursive=True).load_data()
        return documents
    
    @task(multiple_outputs=True)
    def transform(documents: list[Document]):
        """
        """
        splitter = MarkdownNodeParser()

        nodes = splitter.get_nodes_from_documents(documents, show_progress=True)

        metadata_lst = []
        word = "documents"
        url = "https://docs.pola.rs/user-guide"

        for node in nodes:
            meta = node.metadata | {"text": node.get_text()}
            file_path = node.metadata["file_path"]
            start_idx = file_path.find(word) + len(word)
            link = url + file_path[start_idx:-8]
            meta = meta | {"link": link}

            metadata_lst.append(meta)


        return {"metadata": metadata_lst}
    
    @task()
    def embed(metadata:dict):

        tei_url = f"http://{TEI_HOST}:8070"
        texts = [node["text"] for node in metadata["metadata"]]
        embedding_model = TextEmbeddingsInference(url=tei_url, normalize=True)
        embeddings = embedding_model.embed_documents(texts)
        for idx,node in enumerate(metadata["metadata"]):
            node["embedding"] = embeddings[idx]
        return metadata

    @task()
    def load(metadata: dict):
        """
        """
            # Enter context manager
        client = weaviate.connect_to_local(host=WEAVIATE_HOST, port=8090)
        collection_name="documents"
        metadata_lst = metadata["metadata"]
        documents = client.collections.get(collection_name)
        with documents.batch.dynamic() as batch:
            # Loop through the data
            for idx, doc in enumerate(metadata_lst):
                # Convert data types

                for k, v in doc.items():
                    if "date" in k:
                        doc[k] = pd.to_datetime(v).to_pydatetime()
                vec = doc.pop("embedding")
                # Add object to batch queue
                batch.add_object(properties=doc, vector=vec)
                # Batcher automatically sends batches

        # Check for failed objects
        if len(documents.batch.failed_objects) > 0:
            print(f"Failed to import {len(documents.batch.failed_objects)} objects")

        client.close()

    documents = extract()
    metadata = transform(documents)
    embeddings = embed(metadata)
    load(embeddings)

load_weaviate()