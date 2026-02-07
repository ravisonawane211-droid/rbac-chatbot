
import tempfile
from pathlib import Path
from typing import BinaryIO
from langchain_core.documents import Document
from langchain_community.document_loaders import UnstructuredMarkdownLoader, PyMuPDFLoader
import pymupdf4llm
# from langchain_docling import DoclingLoader
# from langchain_docling.loader import ExportType
# from docling.document_converter import DocumentConverter, PdfFormatOption
# from docling.datamodel.base_models import InputFormat
# from docling.datamodel.pipeline_options import PdfPipelineOptions


from app.utils.logger import get_logger
from app.config.config import get_settings
from langchain_text_splitters import RecursiveCharacterTextSplitter,MarkdownTextSplitter,MarkdownHeaderTextSplitter
import pandas as pd
from typing import Any
from app.utils.util import token_len

class DocumentProcessService:

    def __init__(
        self,
        chunk_size: int | None = None,
        chunk_overlap: int | None = None,
    ):
        """Initialize document processor.

        Args:
            chunk_size: Size of text chunks (default from settings)
            chunk_overlap: Overlap between chunks (default from settings)
        """
        settings = get_settings()
        self.logger = get_logger(__name__)
        self.chunk_size = chunk_size or settings.chunk_size
        self.chunk_overlap = chunk_overlap or settings.chunk_overlap

        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            separators=["\n\n", "\n", ". ", " ", ""],
            length_function=token_len,
        )

        self.markdown_header_text_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=[("##", "section")])

        self.markdown_text_splitter = MarkdownTextSplitter(chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,length_function=token_len)

        self.SUPPORTED_EXTENSIONS = {".pdf", ".txt", ".md"}

        self.logger.info(
            f"DocumentProcessor initialized with chunk_size={self.chunk_size}, "
            f"chunk_overlap={self.chunk_overlap}"
        )

    def _load_csv(self, file_path: str | Path):
        """Load CSV file and convert to Document objects.

        Args:
            file_path: Path to CSV file
        Returns:
            List of Document objects
        """
        self.logger.info(f"Loading CSV file: {file_path}")
        df = pd.read_csv(file_path)
        self.logger.info(f"Loaded {len(df)} rows from CSV: {file_path}")
        return df
    

    
    def _load_markdown(self, file_path: str | Path) -> list[Document]:
        """Load Markdown file and convert to Document objects.

        Args:
            file_path: Path to Markdown file
        Returns:
            List of Document objects
        """
        self.logger.info(f"Loading Markdown file: {file_path} using DoclingLoader")

        loader = UnstructuredMarkdownLoader(  
            file_path,  
            mode="elements",  
            strategy="fast",  
            )
        # markdown_loader = DoclingLoader(file_path=file_path
        #                         ,export_type=ExportType.MARKDOWN)
        documents = loader.load()

        self.logger.info(f"Loaded {len(documents)} documents from Markdown: {file_path}")
        return documents
    
    def _load_pdf(self, file_path: str | Path) -> list[Document]:
        """Load PDF file and convert to Document objects.

        Args:
            file_path: Path to PDF file
        Returns:
            List of Document objects
        """
        self.logger.info(f"Loading PDF file: {file_path} using DoclingLoader")

        # Create custom converter with specific options
        # custom_pipeline = PdfPipelineOptions(
        #     do_ocr=False,
        #     do_table_structure=True,
        # )

        # custom_converter = DocumentConverter(
        #     format_options={
        #         InputFormat.PDF: PdfFormatOption(pipeline_options=custom_pipeline)
        #     }
        # )

        # pdf_loader = DoclingLoader(file_path=file_path
        #                         ,export_type=ExportType.MARKDOWN
        #                         ,document_converter=custom_converter)
        #documents = pdf_loader.load()

        text = pymupdf4llm.to_markdown(file_path)

        doc = Document(page_content=text, metadata={"source": file_path})

        self.logger.info(f"Loaded 1 document from PDF: {file_path}")
        return [doc]


    def _load_file(self, file_path: str | Path) -> Any:
        """Load a file based on its extension.

        Args:
            file_path: Path to file

        Returns:
            List of Document objects

        Raises:
            ValueError: If file extension is not supported
        """
        file_path = Path(file_path)
        extension = file_path.suffix.lower()

        if extension not in self.SUPPORTED_EXTENSIONS:
            raise ValueError(
                f"Unsupported file extension: {extension}. "
                f"Supported: {self.SUPPORTED_EXTENSIONS}"
            )

        loaders = {
            ".pdf": self._load_pdf,
            ".md": self._load_markdown,
            ".csv": self._load_csv,
        }

        return loaders[extension](file_path)


    def _load_from_upload(
        self,
        file: BinaryIO,
        filename: str,
    ) -> list[Document]:
        """Load document from uploaded file.

        Args:
            file: File-like object
            filename: Original filename

        Returns:
            List of Document objects
        """
        self.logger.info(f"Loading uploaded file: {filename}")

        extension = Path(filename).suffix.lower()

        if extension not in self.SUPPORTED_EXTENSIONS:
            raise ValueError(
                f"Unsupported file extension: {extension}. "
                f"Supported: {self.SUPPORTED_EXTENSIONS}"
            )

        # Save to temporary file for processing
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=extension,
        ) as tmp_file:
            tmp_file.write(file.read())
            tmp_path = tmp_file.name

        try:
            documents = self._load_file(tmp_path)

            self.logger.info(f"Loaded {len(documents)} documents from upload: {filename}")

            return documents
        except Exception as e:
            self.logger.error(f"error in processing document : {e}")
            raise e
        finally:
            # Clean up temp file
            Path(tmp_path).unlink(missing_ok=True)

    def _split_documents(self, documents: list[Document]) -> list[Document]:
        """Split documents into chunks.

        Args:
            documents: List of Document objects

        Returns:
            List of chunked Document objects
        """
        self.logger.info(f"Splitting {len(documents)} documents into chunks")

        header_docs: list[Document] = []

        for doc in documents:
            splits = self.markdown_header_text_splitter.split_text(doc.page_content)

            for split in splits:
                # Preserve original metadata
                section = split.metadata.get("section")

                content = split.page_content.strip()

                if section:
                    content = f"## {section}\n\n{content}"

                header_docs.append(Document(page_content=content,
                                            metadata=split.metadata))

        #chunks = self.markdown_text_splitter.split_documents(header_docs)


        self.logger.info(f"Created {len(header_docs)} chunks")
        return header_docs
    
    def process_file(self, file_path: str | Path) -> list[Document]:
        """Load and split a file in one step.

        Args:
            file_path: Path to file

        Returns:
            List of chunked Document objects
        """
        self.logger.info(f"Processing file: {file_path}")
        
        documents = self._load_file(file_path)
        return self._split_documents(documents)

    def process_upload(
        self,
        file: BinaryIO,
        filename: str,
    ) -> list[Document]:
        """Load and split an uploaded file.

        Args:
            file: File-like object
            filename: Original filename

        Returns:
            List of chunked Document objects
        """
        self.logger.info(f"Processing uploaded file: {filename}")
        documents = self._load_from_upload(file, filename)
        file_path = Path(filename)
        extension = file_path.suffix.lower()

        if extension != ".csv":
            documents = self._split_documents(documents)

        return documents
    