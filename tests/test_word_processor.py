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

def test_add_comment_targeted(tmp_path):
    """Test adding a comment to a specific phrase in a paragraph."""
    doc_path = tmp_path / "test_targeted.docx"
    doc = Document()
    doc.add_paragraph("This is a long paragraph with a specific error.")
    doc.save(doc_path)
    
    processor = WordProcessor(doc_path)
    # Target "specific error"
    processor.add_comment(0, "Fix this", author="Conductor", search_text="specific error")
    
    save_path = tmp_path / "targeted.docx"
    processor.save(save_path)
    
    assert os.path.exists(save_path)
    commented_doc = Document(save_path)
    
    # Verify that comments exist
    comments_part = any(
        part.content_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.comments+xml"
        for part in commented_doc.part.related_parts.values()
    )
    assert comments_part
