# Implementation Plan: Core Academic Proofreader CLI

## Phase 1: Project Setup & Environment [checkpoint: 05ca490]
- [x] Task: Initialize Python project structure (setup.py/pyproject.toml, requirements.txt) [014f333]
- [x] Task: Set up environment variable management (.env, .gitignore) [6d3c128]
- [x] Task: Configure basic logging and error handling [84d79de]
- [x] Task: Conductor - User Manual Verification 'Phase 1: Project Setup & Environment' (Protocol in workflow.md)

## Phase 2: Word File Processing [checkpoint: 5c5258e]
- [x] Task: Implement Word file reader utility using `python-docx` [738532b]
    - [x] Write tests for reading text from paragraphs
    - [x] Implement text extraction logic
- [x] Task: Implement Word file writer utility for creating a copy [738532b]
    - [x] Write tests for saving a new document
    - [x] Implement file save logic
- [x] Task: Implement basic comment injection logic [738532b]
    - [x] Write tests for adding a comment to a specific paragraph/run
    - [x] Implement comment injection using `python-docx`
- [x] Task: Conductor - User Manual Verification 'Phase 2: Word File Processing' (Protocol in workflow.md)

## Phase 3: Gemini Pro Integration
- [~] Task: Set up Gemini Pro client and basic connectivity tests
- [ ] Task: Design and implement the proofreading prompt for academic feedback
    - [ ] Write tests for prompt generation
    - [ ] Implement prompt logic incorporating academic guidelines
- [ ] Task: Implement logic to parse Gemini Pro response into structured feedback
    - [ ] Write tests for parsing various response formats
    - [ ] Implement robust parsing logic
- [ ] Task: Conductor - User Manual Verification 'Phase 3: Gemini Pro Integration' (Protocol in workflow.md)

## Phase 4: Core Logic & Report Generation
- [ ] Task: Orchestrate the proofreading flow (Read -> Analyze -> Comment -> Write)
- [ ] Task: Implement summary report generation logic
    - [ ] Write tests for report data aggregation
    - [ ] Implement Markdown/Word report generation
- [ ] Task: Conductor - User Manual Verification 'Phase 4: Core Logic & Report Generation' (Protocol in workflow.md)

## Phase 5: CLI Interface & Final Integration
- [ ] Task: Implement CLI using `argparse` or `click`
    - [ ] Write tests for CLI arguments
    - [ ] Implement CLI entry point
- [ ] Task: Final end-to-end integration testing with a sample academic paper
- [ ] Task: Conductor - User Manual Verification 'Phase 5: CLI Interface & Final Integration' (Protocol in workflow.md)
