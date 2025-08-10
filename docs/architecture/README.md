# Architecture Documentation

This directory contains the source files for the Context Engineering Template's architecture diagrams and workflow visualizations.

## Purpose

The diagrams illustrate the evolution of the business-driven development workflow from current template-based system to full CABIO (Context-Aware Business Intelligence Orchestration) implementation:

- **Current State**: Template-based BRD→PRD→FRP workflow with AI agent support
- **Enhanced Templates (8-12 weeks)**: Agent orchestration with context compression and market integration  
- **Enterprise CABIO (12+ months)**: Real-time business intelligence with enterprise scalability

All diagrams prominently feature the **Implementation (Key USP)** section, demonstrating how the system transforms business analysis into working code - the critical differentiator from traditional business intelligence tools.

## Rendering

All diagrams are authored in **PlantUML** and designed to render in both light and dark themes using GitHub Primer styles.

### Prerequisites

- Docker installation
- One-time setup: `make setup_plantuml`

### Local Rendering

#### Interactive Mode

```bash
make run_puml_interactive
```

Starts a PlantUML server at `http://localhost:8080` for interactive diagram editing and rendering.

#### Single Diagram Generation

```bash
make run_puml_single INPUT_FILE="docs/architecture/filename.plantuml" STYLE="dark|light" OUTPUT_PATH="assets/images"
```

**Example:**

```bash
make run_puml_single INPUT_FILE="docs/architecture/Business-Driven-Development-Current.plantuml" STYLE="dark" OUTPUT_PATH="assets/images"
```

### Online Rendering

Alternative method using [PlantUML.com](http://www.plantuml.com/plantuml/) web server:

1. **Modify include paths** for online compatibility:

   ```plantuml
   !include https://raw.githubusercontent.com/qte77/context-engineering-template/main/docs/architecture/styles/github-dark.puml
   ```

2. **Copy modified PlantUML source** and paste into the web interface

3. **Generate PNG/SVG** directly from the web service

## Styling

The diagrams use GitHub Primer themes located in `styles/`:

- `github-dark.puml` - Dark theme with GitHub dark mode colors
- `github-light.puml` - Light theme with GitHub light mode colors

Themes are automatically applied based on the `STYLE` parameter during rendering.

## Output

Rendered diagrams are saved to `assets/images/` with the naming convention:
`{diagram-name}-{theme}.png`

## Contributing

When adding new diagrams:

1. Follow the existing naming convention
2. Include both detailed and concise versions where appropriate
3. Ensure compatibility with both light and dark themes
4. Test rendering with both local and online methods
5. Update this README with new diagram information
