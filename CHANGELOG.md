# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Guiding Principles

- Changelogs are for humans, not machines.
- There should be an entry for every single version.
- The same types of changes should be grouped.
- Versions and sections should be linkable.
- The latest version comes first.
- The release date of each version is displayed.
- Mention whether you follow Semantic Versioning.

## Types of changes

- `Added` for new features.
- `Changed` for changes in existing functionality.
- `Deprecated` for soon-to-be removed features.
- `Removed` for now removed features.
- `Fixed` for any bug fixes.
- `Security` in case of vulnerabilities.

## [Unreleased]

### Added

- Complete BRD → PRD → FRP workflow for business-driven development
- Business input document templates with multiple input approaches
- Product Requirements Document (PRD) generation from BRD
- Feature-specific FRP generation from PRD with business context traceability
- Make targets for new workflow commands (brd_gen_claude, prd_gen_claude, frp_gen_claude)
- Comprehensive business input template with stakeholder, market, and risk analysis
- Multiple BRD input methods: business input document, interactive session, partial completion
- Example AI assistant business input and BRD demonstrating complete workflow
- Enhanced sequence diagrams showing both new and legacy workflows with input options
- docs/usage-guide.md - Detailed workflow instructions and configuration
- docs/examples.md - Complete examples, best practices, and troubleshooting  
- context/business_inputs/ directory for initial business information
- context/BRDs/ directory for business requirements definitions
- context/PRDs/ directory for product requirements documents
- CABIO vision documents: vision, product roadmap, and implementation guide
- Prominent product state and vision summary in README.md

### Changed

- Restructured README.md for clarity (reduced from 262 to 63 lines)
- Updated paths.md with new BRD, PRD, and business input paths
- Enhanced execute-frp command to reference PRD and BRD context for full traceability
- Legacy Makefile recipes renamed for clarity (frp_gen_legacy_claude, frp_exe_legacy_claude)
- Comprehensive documentation consistency fixes across all files
- Aligned product positioning: template system (current) → enhanced templates (8-12 weeks) → CABIO (12+ months)
- Clarified target market focus on small teams (5-25 people) with enterprise scaling path
- Resolved timeline contradictions and technical architecture inconsistencies

## [0.0.1] - 2025-07-07

### Added

- Initial template containing templates for PRP
