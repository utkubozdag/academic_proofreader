from docx import Document
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
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
                    para_element = paragraph._p
                    
                    # Split the run text if original_text is a substring
                    full_text = run.text
                    start_idx = full_text.find(original_text)
                    end_idx = start_idx + len(original_text)
                    
                    before_text = full_text[:start_idx]
                    after_text = full_text[end_idx:]
                    
                    # Get run properties to copy to new runs
                    rPr = run_element.find(qn('w:rPr'))
                    rPr_copy = etree.tostring(rPr) if rPr is not None else None
                    
                    # Find the position of this run in the paragraph
                    run_index = list(para_element).index(run_element)
                    
                    # Remove the original run
                    para_element.remove(run_element)
                    
                    insert_position = run_index
                    
                    # 1. Add run with text before the change (if any)
                    if before_text:
                        before_run = OxmlElement('w:r')
                        if rPr_copy:
                            before_run.append(etree.fromstring(rPr_copy))
                        t_before = OxmlElement('w:t')
                        t_before.text = before_text
                        t_before.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
                        before_run.append(t_before)
                        para_element.insert(insert_position, before_run)
                        insert_position += 1
                    
                    # 2. Create w:del element for original text (at paragraph level)
                    del_elem = OxmlElement('w:del')
                    del_elem.set(qn('w:id'), rev_id)
                    del_elem.set(qn('w:author'), author)
                    del_elem.set(qn('w:date'), date_str)
                    
                    del_run = OxmlElement('w:r')
                    if rPr_copy:
                        del_run.append(etree.fromstring(rPr_copy))
                    
                    del_text = OxmlElement('w:delText')
                    del_text.text = original_text
                    del_text.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
                    del_run.append(del_text)
                    del_elem.append(del_run)
                    
                    para_element.insert(insert_position, del_elem)
                    insert_position += 1
                    
                    # 3. Create w:ins element for replacement text (at paragraph level)
                    ins_elem = OxmlElement('w:ins')
                    ins_elem.set(qn('w:id'), str(int(rev_id) + 1))
                    ins_elem.set(qn('w:author'), author)
                    ins_elem.set(qn('w:date'), date_str)
                    
                    ins_run = OxmlElement('w:r')
                    if rPr_copy:
                        ins_run.append(etree.fromstring(rPr_copy))
                    
                    ins_text = OxmlElement('w:t')
                    ins_text.text = replacement_text
                    ins_text.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
                    ins_run.append(ins_text)
                    ins_elem.append(ins_run)
                    
                    para_element.insert(insert_position, ins_elem)
                    insert_position += 1
                    
                    # 4. Add run with text after the change (if any)
                    if after_text:
                        after_run = OxmlElement('w:r')
                        if rPr_copy:
                            after_run.append(etree.fromstring(rPr_copy))
                        t_after = OxmlElement('w:t')
                        t_after.text = after_text
                        t_after.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
                        after_run.append(t_after)
                        para_element.insert(insert_position, after_run)
                    
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
