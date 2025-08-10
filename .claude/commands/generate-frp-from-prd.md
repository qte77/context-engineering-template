# Create Feature-Specific Requirements Prompt (FRP) from Product Requirements Document (PRD)

This command creates a focused FRP for a single feature using PRD context and business alignment from BRD.

## Rules

- Extract PRD filename from first argument: `$PRD_FILE_NAME` (append `.md` if needed)
- Extract feature name from second argument: `$FEATURE_NAME`
- Use TodoWrite tool to track progress throughout the process
- Input PRD: `$CTX_PRD_PATH/$PRD_FILE_NAME` (must exist)
- Input BRD: `$CTX_BRD_PATH/$PRD_FILE_NAME` (for business context)
- Template: `$CTX_FRP_TEMPLATE`
- Output: `$CTX_FRP_PATH/${PRD_FILE_NAME}_${FEATURE_NAME}.md`

## Feature-Focused Translation Process

1. **Load Product Context**
   - Read specified PRD file for product specifications
   - Identify target feature and its specifications
   - Extract feature-specific user stories and acceptance criteria
   - Understand feature dependencies and implementation priority

2. **Load Business Alignment**
   - Reference corresponding BRD for business context
   - Understand how this feature serves business objectives
   - Note business constraints that affect this feature
   - Connect feature success to business KPIs

3. **Feature Isolation**
   - Focus on single feature while maintaining product context
   - Identify feature boundaries and scope
   - Define integration points with other features
   - Establish feature-specific success criteria

## Enhanced FRP Generation

Use `$CTX_FRP_TEMPLATE` as base template, enhanced with PRD feature context and BRD business alignment.

### PRD-Enhanced FRP Sections

**Goal Section Enhancement:**

- Focus on specific feature from PRD feature list
- Reference feature's business value from BRD alignment
- Include feature priority and user impact
- Define feature boundaries and scope

**Why Section Enhancement:**

- Include feature-specific business value from PRD
- Reference user personas this feature serves
- Connect to business objectives from BRD
- Explain feature's role in overall product vision

**What Section Enhancement:**

- Include feature's user stories from PRD
- Translate acceptance criteria into technical requirements
- Define feature-specific user experience requirements
- Include integration requirements with other features

**Success Criteria Enhancement:**

- Include feature acceptance criteria from PRD
- Reference feature success metrics from PRD
- Include business impact measurement from BRD alignment
- Define feature completion and validation criteria

### Implementation Blueprint Enhancement

**Feature-Focused Implementation:**

- Consider PRD constraints in technical design
- Plan for feature-specific user experience requirements
- Include integration points with other features from PRD
- Address feature dependencies from PRD implementation strategy

**Business-Technical Bridge:**

- **Feature User Stories → Technical Requirements**: Transform feature user stories into functional specifications
- **Feature Acceptance Criteria → Validation Tests**: Convert acceptance criteria into technical validation approaches
- **Feature Success Metrics → Technical Metrics**: Feature KPIs inform technical validation criteria
- **Feature Dependencies → Technical Dependencies**: PRD feature dependencies become technical integration requirements

## Research Process

1. **Feature-Informed Codebase Analysis**
   - Search for patterns that align with feature requirements
   - Identify existing code that serves similar user stories
   - Consider feature constraints for technical implementation choices
   - Look for integration patterns with dependent features

2. **Context Gathering**
   - Verify alignment between feature requirements and technical capabilities
   - Check integration points support feature user journeys
   - Ensure technical patterns serve feature acceptance criteria

**Research Completeness:** Comprehensive research combining feature context with technical analysis to minimize additional research during execution.

## Planning and Execution

**Before writing the FRP:**

1. Create TodoWrite plan combining feature analysis with technical implementation
2. Validate feature-technical alignment against PRD specifications
3. Structure FRP for focused feature implementation success

## Quality Checklist

**PRD-FRP Feature Integration:**

- [ ] Feature scope clearly defined from PRD specifications
- [ ] User stories translated to technical requirements
- [ ] Feature acceptance criteria reflected in technical validation
- [ ] Feature success metrics included in technical success criteria
- [ ] Feature dependencies identified and addressed
- [ ] Integration points with other features documented
- [ ] Business alignment maintained from BRD context

## PRD-FRP Validation Checklist

**Before handoff to execution:**

- [ ] Clear traceability from PRD feature to FRP implementation
- [ ] Feature user stories directly inform technical requirements
- [ ] Acceptance criteria converted to testable technical criteria
- [ ] Feature success metrics integrated into technical validation
- [ ] Implementation approach respects feature dependencies from PRD
- [ ] Technical design supports feature user experience requirements
- [ ] Feature boundaries clearly defined and respected
- [ ] Quality evaluation scores meet AGENTS.md thresholds
- [ ] FRP enables independent feature implementation while maintaining product context

## Success Metrics

- Apply AGENTS.md Quality Evaluation Framework enhanced with feature context
- Feature user stories clearly drive technical implementation approach
- Feature acceptance criteria directly inform technical validation
- Feature success metrics measurable through technical implementation
- Implementation approach respects feature dependencies and integration requirements
