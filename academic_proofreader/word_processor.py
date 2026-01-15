from docx import Document
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.opc.constants import CONTENT_TYPE as CT
from docx.opc.packuri import PackURI
import datetime

class WordProcessor:
    """Handles reading and writing Microsoft Word documents."""
    
    def __init__(self, file_path):
        """
        Initialize the WordProcessor.
        
        Args:
            file_path (str): Path to the .docx file.
        """
        self.file_path = file_path
        self.doc = Document(file_path)
        
    def get_text(self):
        """
        Extract all text from the document.
        
        Returns:
            str: The extracted text.
        """
        return "\n".join([para.text for para in self.doc.paragraphs])

    def save(self, output_path):
        """
        Save the document to a new file.
        
        Args:
            output_path (str): Path to save the .docx file.
        """
        self.doc.save(output_path)

    def add_comment(self, para_index, comment_text, author="Academic Proofreader", initials="AP"):
        """
        Add a comment to a specific paragraph.
        
        Args:
            para_index (int): Index of the paragraph to comment on.
            comment_text (str): The text of the comment.
            author (str, optional): Author of the comment. Defaults to "Academic Proofreader".
            initials (str, optional): Initials of the author. Defaults to "AP".
        """
        if para_index >= len(self.doc.paragraphs):
            return

        paragraph = self.doc.paragraphs[para_index]
        
        # 1. Get or create comments part
        comments_part = None
        for rel in self.doc.part.rels.values():
            if "comments" in rel.reltype:
                comments_part = rel.target_part
                break
        
        if comments_part is None:
            # Create a new comments part
            comments_xml = OxmlElement('w:comments')
            
            # This is a bit of a hack to create the part
            from docx.opc.part import Part
            comments_part = Part(
                PackURI('/word/comments.xml'),
                CT.WML_COMMENTS,
                comments_xml.xml,
                self.doc.part.package
            )
            self.doc.part.relate_to(comments_part, "http://schemas.openxmlformats.org/officeDocument/2006/relationships/comments")
        
        # 2. Find next comment ID
        from lxml import etree
        comments_xml = etree.fromstring(comments_part._blob)
        
        # Namespace map for xpath
        ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
        ids = [int(c.get(qn('w:id'))) for c in comments_xml.xpath('//w:comment', namespaces=ns)]
        new_id = str(max(ids) + 1) if ids else "0"
        
        # 3. Create the comment element
        comment = OxmlElement('w:comment')
        comment.set(qn('w:id'), new_id)
        comment.set(qn('w:author'), author)
        comment.set(qn('w:initials'), initials)
        comment.set(qn('w:date'), datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ'))
        
        p = OxmlElement('w:p')
        r = OxmlElement('w:r')
        t = OxmlElement('w:t')
        t.text = comment_text
        r.append(t)
        p.append(r)
        comment.append(p)
        comments_xml.append(comment)
        
        # 4. Reference the comment in the paragraph
        # We wrap the whole paragraph in the comment range
        start = OxmlElement('w:commentRangeStart')
        start.set(qn('w:id'), new_id)
        end = OxmlElement('w:commentRangeEnd')
        end.set(qn('w:id'), new_id)
        
        # Insert start at the beginning of the paragraph
        paragraph._p.insert(0, start)
        # Insert end at the end of the paragraph
        paragraph._p.append(end)
        
        # Add comment reference
        ref_run = paragraph.add_run()
        ref = OxmlElement('w:commentReference')
        ref.set(qn('w:id'), new_id)
        ref_run._r.append(ref)
        
        # Update the comments part blob
        comments_part._blob = etree.tostring(comments_xml)
