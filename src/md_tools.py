from markdown_it import MarkdownIt
import re
from src import setup_logger

log = setup_logger(__name__)

def split_markdown_message(text, chunk_size=2000):
    """
    Safely splits Markdown based on markdown-it-py token analysis,
    ensuring that it is not split in the middle of tags and accurately preserves all newlines in the original document.
    """
    md = MarkdownIt()
    tokens = md.parse(text)
    
    # Find all safe break positions (end of paragraphs, headings, etc.)
    safe_break_positions = []
    
    for token in tokens:
        if token.type in ['paragraph_close', 'heading_close', 'fence', 'hr', 'code_block'] and token.map:
            # Get the end position of the paragraph
            _, end_line = token.map
            
            # Calculate the character position of the corresponding line in the original text
            line_position = len('\n'.join(text.splitlines()[:end_line]))
            safe_break_positions.append(line_position)
            
    log.debug(f"Found {len(safe_break_positions)} safe break positions.")
    
    # If there are not enough safe breakpoints, consider breaking at blank lines
    if len(safe_break_positions) < (len(text) // chunk_size):
        # Find all positions of blank lines
        blank_line_positions = [m.end() for m in re.finditer(r'\n\s*\n', text)]
        safe_break_positions.extend(blank_line_positions)
        safe_break_positions.sort()
        
    log.debug(safe_break_positions)
    
    # If there are still not enough breakpoints, break at the end of code blocks, list items, etc.
    if len(safe_break_positions) < (len(text) // chunk_size):
        for token in tokens:
            if token.type in ['list_item_close', 'bullet_list_close', 'ordered_list_close'] and token.map:
                _, end_line = token.map
                line_position = len('\n'.join(text.splitlines()[:end_line]))
                if line_position not in safe_break_positions:
                    safe_break_positions.append(line_position)
        safe_break_positions.sort()
        
    log.debug(safe_break_positions)
    
    # split the text into chunks
    chunks = []
    start = 0
    
    while start < len(text):
        # find the next suitable break point
        best_break = None
        
        for pos in safe_break_positions:
            if pos > start and pos - start <= chunk_size:
                best_break = pos
            elif pos - start > chunk_size:
                break
        
        # if no suitable break point is found, just cut at the length
        if best_break is None:
            best_break = min(start + chunk_size, len(text))
            # make sure not to cut in the middle of a word
            if best_break < len(text):
                # try to backtrack to the nearest whitespace
                space_before = text.rfind(' ', start, best_break)
                newline_before = text.rfind('\n', start, best_break)
                if newline_before > space_before:
                    best_break = newline_before + 1  # +1 to include the newline
                elif space_before != -1:
                    best_break = space_before + 1  # +1 to include the space
        
        # append the current chunk
        chunk = text[start:best_break]
        if chunk:  # make sure not to add an empty chunk
            chunks.append(chunk)
        
        # update the start position
        start = best_break
    
    return chunks