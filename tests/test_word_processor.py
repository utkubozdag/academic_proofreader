import os
import pytest
from docx import Document
from academic_proofreader.word_processor import WordProcessor

def test_read_paragraphs(tmp_path):
    """Test reading text from paragraphs in a Word document."""
    doc_path = tmp_path / "test.docx"
    doc = Document()
    doc.add_paragraph("Paragraph 1")
    doc.add_paragraph("Paragraph 2")
    doc.save(doc_path)
    
    processor = WordProcessor(doc_path)
    text = processor.get_text()
    
    assert "Paragraph 1" in text
    assert "Paragraph 2" in text
    assert text.strip() == "Paragraph 1\nParagraph 2"

def test_save_document(tmp_path):
    """Test saving the document to a new file."""
    doc_path = tmp_path / "test.docx"
    doc = Document()
    doc.add_paragraph("Original Text")
    doc.save(doc_path)
    
    processor = WordProcessor(doc_path)
    save_path = tmp_path / "saved.docx"
    processor.save(save_path)
    
    assert os.path.exists(save_path)
    new_doc = Document(save_path)
    assert new_doc.paragraphs[0].text == "Original Text"

def test_add_comment(tmp_path):
    """Test adding a comment to a paragraph."""
    doc_path = tmp_path / "test_comment.docx"
    doc = Document()
    doc.add_paragraph("Paragraph to comment on.")
    doc.save(doc_path)
    
    processor = WordProcessor(doc_path)
    # paragraph_index, comment_text, author
    processor.add_comment(0, "This is a test comment", author="Conductor")
    
    save_path = tmp_path / "commented.docx"
    processor.save(save_path)
    
    # Verifying comments in python-docx is tricky as it doesn't have a high-level API for it.
    # We might need to check the XML or rely on the fact that it doesn't crash if we implement it.
    # A better way is to check the document's part for comments.
    
    assert os.path.exists(save_path)
    commented_doc = Document(save_path)
    # Check if a comments part exists in the document's package by looking at content types
    comments_part_exists = any(
        part.content_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.comments+xml"
        for part in commented_doc.part.related_parts.values()
    )
    assert comments_part_exists
