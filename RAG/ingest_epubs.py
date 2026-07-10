import os
from bs4 import BeautifulSoup

import ebooklib
from ebooklib import epub
from dotenv import load_dotenv

load_dotenv()
os.environ.setdefault("HF_HUB_DISABLE_PROGRESS_BARS", "1")
os.environ.setdefault("TQDM_DISABLE", "1")

import chromadb
from chromadb.utils import embedding_functions


def extract_epub(epub_file):
    epub_file = "Knowledge/" + epub_file
    print(f"### Extracting {epub_file}")

    book = epub.read_epub(epub_file)
    chapters = []

    counter = 1

    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            html_content = item.get_content()

            soup = BeautifulSoup(html_content, "html.parser")
            text = soup.get_text(separator=" ", strip=True)
            if len(text) > 100:
                chapters.append({"chapter_index": counter, "text": text})
                counter += 1
    print("### Successfully Extracted Epub file.")
    return chapters


def chunk_text(text, chunk_size=1000, overlap=200):
    chunks = []
    start = 0
    text_len = len(text)

    while start < text_len:
        end = min(start + chunk_size, text_len)

        if end < text_len and text[end] != " ":
            last_space = text.rfind(" ", start, end)
            if last_space > start + 100:
                end = last_space

        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)

        if end >= text_len:
            break

        start += max(0, end - overlap)

    return chunks


def vector_embed():

    dir_name = "./Knowledge/"
    files = os.listdir(dir_name)

    epub_files = []
    for file in files:
        if file[-4:] == "epub":
            epub_files.append(file)

    # epub_files = [epub_files.pop(1)]

    for i, book in enumerate(epub_files):
        i += 1
        print(f"|==== Working on Book no.{i}: {book} ====|")
        try:
            raw_chapters = extract_epub(book)
        except Exception as e:
            print(f"!!!! Error Occured for Book: {book}\n!!!! Error: {e}")
            print("Skipping This Book")
            continue

        print("## Got Raw Chapter of", book)
        book_name = os.path.basename(book)

        all_chunks = []
        all_metadata = []
        all_ids = []

        global_chunk_counter = 0

        print("Chuning each Chapters")
        for ch in raw_chapters:
            chapter_chunks = chunk_text(ch["text"], chunk_size=1000, overlap=200)

            for sub_idx, text_chunk in enumerate(chapter_chunks):
                all_chunks.append(text_chunk)

                all_metadata.append(
                    {
                        "source": book_name,
                        "chapter": f"Chapter {ch['chapter_index']}",
                        "segment": sub_idx,
                    }
                )

                all_ids.append(f"{book_name}_chunk_{global_chunk_counter}")
                global_chunk_counter += 1

        db_storage_path = "./Knowledge/ChromaDB_Storage"
        chroma_client = chromadb.PersistentClient(path=db_storage_path)

        hf_embedd = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="all-MiniLM-L6-v2",
        )
        print(f"# VECTORIZING {book}.")
        collection = chroma_client.get_or_create_collection(
            name="Epub-Library", embedding_function=hf_embedd
        )

        print("\n===> Generating Embedding and writing vectors to disk")

        collection.upsert(documents=all_chunks, metadatas=all_metadata, ids=all_ids)

        print(f"[SCUCESS]. RAG Database successfully written to {db_storage_path}\n")
        print()


if __name__ == "__main__":
    vector_embed()
