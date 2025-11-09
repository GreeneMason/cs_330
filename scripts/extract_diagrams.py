"""
Extract Mermaid diagrams from markdown and save as separate .mmd files
These can then be converted to images using mermaid-cli
"""

import re
from pathlib import Path

def extract_mermaid_diagrams(md_file):
    """Extract all mermaid code blocks from markdown file"""
    
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all mermaid code blocks
    pattern = r'```mermaid\n(.*?)```'
    diagrams = re.findall(pattern, content, re.DOTALL)
    
    # Create output directory
    output_dir = Path('diagrams')
    output_dir.mkdir(exist_ok=True)
    
    # Save each diagram
    diagram_names = [
        'ufc_database_simple',
        'normalized_ufc_full',
        'normalized_ufc_simplified'
    ]
    
    for i, (name, diagram) in enumerate(zip(diagram_names, diagrams)):
        output_file = output_dir / f'{name}.mmd'
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(diagram.strip())
        
        print(f"✓ Saved: {output_file}")
    
    print(f"\n{len(diagrams)} diagrams extracted to {output_dir}/")
    print("\nTo convert to images:")
    print("1. Install mermaid-cli: npm install -g @mermaid-js/mermaid-cli")
    print("2. Run: mmdc -i diagrams/ufc_database_simple.mmd -o diagrams/ufc_database_simple.png")
    print("\nOr convert all at once:")
    for name in diagram_names:
        print(f"  mmdc -i diagrams/{name}.mmd -o diagrams/{name}.png")

if __name__ == '__main__':
    extract_mermaid_diagrams('docs/database_er_diagrams.md')
