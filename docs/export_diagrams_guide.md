# Save Mermaid Diagrams as Images

## Using Mermaid CLI

### Installation
```bash
npm install -g @mermaid-js/mermaid-cli
```

### Usage
```bash
# Convert single diagram
mmdc -i diagram.mmd -o diagram.png

# Convert with specific theme
mmdc -i diagram.mmd -o diagram.png -t dark

# Convert to SVG
mmdc -i diagram.mmd -o diagram.svg

# High resolution PNG
mmdc -i diagram.mmd -o diagram.png -w 2000 -H 2000
```

## Quick Script to Extract and Convert Diagrams

Save the mermaid code blocks to separate .mmd files, then:

```bash
# For each diagram in database_er_diagrams.md
mmdc -i ufc_database.mmd -o diagrams/ufc_database.png
mmdc -i normalized_db.mmd -o diagrams/normalized_db.png
mmdc -i simplified_db.mmd -o diagrams/simplified_db.png
```

## Alternative: Screenshot in VS Code

1. Install "Markdown Preview Mermaid Support" extension
2. Open `database_er_diagrams.md`
3. Press `Ctrl+Shift+V` to preview
4. Use Windows Snipping Tool (`Win+Shift+S`) to capture
5. Paste into Paint/PowerPoint and save

## Online Tools

1. **Mermaid Live**: https://mermaid.live
   - Paste code → Download as PNG/SVG/PDF
   
2. **Draw.io with Mermaid Plugin**
   - Import mermaid code
   - Export as image

## Best Quality

For presentations/documentation:
- **SVG** - Scalable, perfect quality at any size
- **PNG at 2000x2000** - High resolution raster image
