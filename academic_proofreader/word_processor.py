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

    def add_comment(self, para_index, comment_text, author="Academic Proofreader", initials="AP", search_text=None):
        """
        Add a comment to a specific paragraph, optionally targeting a phrase.
        
        Args:
            para_index (int): Index of the paragraph to comment on.
            comment_text (str): The text of the comment.
            author (str, optional): Author of the comment. Defaults to "Academic Proofreader".
            initials (str, optional): Initials of the author. Defaults to "AP".
            search_text (str, optional): Specific text within the paragraph to target.
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
        start = OxmlElement('w:commentRangeStart')
        start.set(qn('w:id'), new_id)
        end = OxmlElement('w:commentRangeEnd')
        end.set(qn('w:id'), new_id)
        
        # Target specific text if provided and found
        targeted = False
        if search_text:
            for run in paragraph.runs:
                if search_text in run.text:
                    run._r.addprevious(start)
                    run._r.addnext(end)
                    
                    ref_run = paragraph.add_run()
                    ref = OxmlElement('w:commentReference')
                    ref.set(qn('w:id'), new_id)
                    end.addnext(ref_run._r)
                    ref_run._r.append(ref)
                    targeted = True
                    break
        
        if not targeted:
            # Fallback to wrapping the whole paragraph
            paragraph._p.insert(0, start)
            paragraph._p.append(end)
            ref_run = paragraph.add_run()
            ref = OxmlElement('w:commentReference')
            ref.set(qn('w:id'), new_id)
            ref_run._r.append(ref)
        
        # Update the comments part blob
        comments_part._blob = etree.tostring(comments_xml)

    def add_tracked_change(self, original_text, replacement_text, author="Academic Proofreader"):
        """
        Add a tracked change (revision) to the document.
        
        Finds the original text in the document, wraps it in a w:del element,
        and inserts the replacement text in a w:ins element.
        
        Args:
            original_text (str): The original text to be replaced.
            replacement_text (str): The suggested replacement text.
            author (str, optional): Author of the revision. Defaults to "Academic Proofreader".
            
        Returns:
            bool: True if the change was applied, False if original text was not found.
        """
        from lxml import etree
        
        # Generate unique revision ID
        rev_id = str(id(original_text) % 100000)
        date_str = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
        
        # Search through all paragraphs
        for paragraph in self.doc.paragraphs:
            for run in paragraph.runs:
                if original_text in run.text:
                    # Found the text - now we need to handle it
                    run_element = run._r
                    
                    # Split the run text if original_text is a substring
                    full_text = run.text
                    start_idx = full_text.find(original_text)
                    end_idx = start_idx + len(original_text)
                    
                    before_text = full_text[:start_idx]
                    after_text = full_text[end_idx:]
                    
                    # Clear the current run's text
                    for t_elem in run_element.findall(qn('w:t')):
                        run_element.remove(t_elem)
                    
                    # Add text before the change (if any)
                    if before_text:
                        t_before = OxmlElement('w:t')
                        t_before.text = before_text
                        t_before.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
                        run_element.append(t_before)
                    
                    # Create w:del element for original text
                    del_elem = OxmlElement('w:del')
                    del_elem.set(qn('w:id'), rev_id)
                    del_elem.set(qn('w:author'), author)
                    del_elem.set(qn('w:date'), date_str)
                    
                    del_run = OxmlElement('w:r')
                    # Copy run properties if they exist
                    rPr = run_element.find(qn('w:rPr'))
                    if rPr is not None:
                        del_run.append(etree.fromstring(etree.tostring(rPr)))
                    
                    del_text = OxmlElement('w:delText')
                    del_text.text = original_text
                    del_text.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
                    del_run.append(del_text)
                    del_elem.append(del_run)
                    
                    # Create w:ins element for replacement text
                    ins_elem = OxmlElement('w:ins')
                    ins_elem.set(qn('w:id'), str(int(rev_id) + 1))
                    ins_elem.set(qn('w:author'), author)
                    ins_elem.set(qn('w:date'), date_str)
                    
                    ins_run = OxmlElement('w:r')
                    if rPr is not None:
                        ins_run.append(etree.fromstring(etree.tostring(rPr)))
                    
                    ins_text = OxmlElement('w:t')
                    ins_text.text = replacement_text
                    ins_text.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
                    ins_run.append(ins_text)
                    ins_elem.append(ins_run)
                    
                    # Insert the del and ins elements
                    run_element.append(del_elem)
                    run_element.append(ins_elem)
                    
                    # Add text after the change (if any)
                    if after_text:
                        t_after = OxmlElement('w:t')
                        t_after.text = after_text
                        t_after.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
                        run_element.append(t_after)
                    
                    return True
        
        return False

    def enable_track_revisions(self):
        """
        Enable track revisions mode in the document settings.
        
        This ensures that when the document is opened in Word, it will
        display in "Track Changes" review mode.
        """
        from lxml import etree
        
        # Access the settings part
        settings_part = None
        for rel in self.doc.part.rels.values():
            if "settings" in rel.reltype:
                settings_part = rel.target_part
                break
        
        if settings_part is None:
            return False
        
        # Get the settings element - try different approaches
        ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
        
        # Try to get the element directly first (for SettingsPart objects)
        if hasattr(settings_part, 'element'):
            settings_xml = settings_part.element
        elif hasattr(settings_part, '_blob') and settings_part._blob is not None:
            settings_xml = etree.fromstring(settings_part._blob)
        else:
            # Fall back to reading from the part
            try:
                settings_xml = etree.fromstring(settings_part.blob)
            except:
                return False
        
        # Check if trackRevisions already exists
        track_revisions = settings_xml.find('.//w:trackRevisions', namespaces=ns)
        
        if track_revisions is None:
            # Add trackRevisions element
            track_revisions = OxmlElement('w:trackRevisions')
            settings_xml.insert(0, track_revisions)
        
        # Update the settings part - handle different part types
        if hasattr(settings_part, '_blob'):
            settings_part._blob = etree.tostring(settings_xml)
        
        return True
