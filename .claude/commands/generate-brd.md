# Create Business Requirements Definition (BRD)

This command helps stakeholders capture business context, objectives, and constraints before technical feature development begins. Supports multiple input approaches based on available business information.

## Rules

- Extract filename from `$ARGUMENTS` into `$FILE_NAME` (append `.md` if needed)
- Use TodoWrite tool to track progress throughout the process
- Template: `$CTX_BRD_TEMPLATE`
- Output: `$CTX_BRD_PATH/$FILE_NAME`

## Input Source Detection

**The command automatically detects available input sources and adapts the process:**

1. **Check for Business Input Document**: Look for `context/business_inputs/$FILE_NAME` 
2. **Check for Partial BRD**: Look for existing draft in `$CTX_BRD_PATH/$FILE_NAME`
3. **Check for Feature Requirements**: Look for `$CTX_FEATURES_PATH/$FILE_NAME` with business context
4. **Default to Interactive Process**: If no input sources found

## Approach 1: Input Document Method

**When business input document exists:**

### Input Source
- **File**: `context/business_inputs/$FILE_NAME`
- **Format**: Structured business information document
- **Content**: Business problem statement, objectives, constraints, market context

### Process
1. **Read Business Input Document**
   - Extract business problem and objectives
   - Identify stakeholder requirements
   - Note market context and constraints
   - Capture preliminary success metrics

2. **Expand and Structure**
   - Transform input into comprehensive BRD format
   - Add missing business analysis sections
   - Validate business logic and consistency
   - Enhance with industry best practices

3. **Business Validation**
   - Cross-reference objectives with success metrics
   - Validate target user alignment with business goals
   - Ensure constraint feasibility
   - Verify competitive positioning logic

## Approach 2: Template Completion Method

**When partial BRD draft exists:**

### Input Source
- **File**: `$CTX_BRD_PATH/$FILE_NAME` (partial/draft BRD)
- **Format**: Partially completed BRD template
- **Content**: Some sections filled, others marked with placeholders or TODOs

### Process
1. **Analyze Existing Content**
   - Identify completed sections and quality level
   - Note missing or incomplete sections
   - Validate consistency across completed sections
   - Check for business logic gaps

2. **Complete Missing Sections**
   - Research and fill empty template sections
   - Expand brief sections with comprehensive analysis
   - Add supporting business context where needed
   - Ensure template structure compliance

3. **Integrate and Validate**
   - Ensure new content aligns with existing sections
   - Cross-validate business objectives and success metrics
   - Check for internal consistency and logic
   - Enhance overall document quality

## Approach 3: Interactive Session Method

**When no input documents exist:**

### Input Source
- **Interactive Q&A**: Real-time stakeholder interview process
- **Format**: Structured question sequences
- **Content**: Live capture of business requirements through guided conversation

### Process
1. **Structured Interview Process**
   - **Business Context Questions**: "What business problem are you solving? What market opportunity exists?"
   - **Stakeholder Questions**: "Who are your target users? What are their pain points?"
   - **Success Metrics Questions**: "How will you measure business success? What are your KPIs?"
   - **Constraint Questions**: "What are your budget, timeline, and resource constraints?"

2. **Real-Time Analysis**
   - Analyze responses for business logic consistency
   - Ask follow-up questions for clarity and completeness
   - Validate assumptions with additional questions
   - Guide stakeholder through comprehensive business thinking

3. **Document Generation**
   - Structure responses into BRD template format
   - Add business analysis insights based on responses
   - Include industry context and best practices
   - Present draft for stakeholder review and refinement

## Approach 4: Hybrid Method

**When feature requirements contain business context:**

### Input Source
- **File**: `$CTX_FEATURES_PATH/$FILE_NAME`
- **Format**: Feature description with embedded business context
- **Content**: Technical requirements mixed with business objectives and user needs

### Process
1. **Extract Business Elements**
   - Parse feature description for business objectives
   - Identify user needs and market context clues
   - Extract implicit business constraints and requirements
   - Note success criteria with business implications

2. **Interactive Enhancement**
   - Ask targeted questions to fill business gaps
   - "I found these business objectives in your feature description... what additional context can you provide?"
   - "Your feature mentions these users... can you describe the broader market context?"
   - "What business constraints should I consider beyond what's in the feature description?"

3. **Comprehensive BRD Creation**
   - Combine extracted business elements with interactive responses
   - Structure into full BRD format with business analysis
   - Add market research and competitive context
   - Include comprehensive business validation framework

## Universal Business Analysis Enhancement

**Applied to all approaches:**

### Market Research Component
- Analyze competitive landscape based on business context
- Research market opportunity size and trends
- Validate business value proposition against market needs
- Document differentiation strategy and positioning

### Risk Assessment Component
- Identify business risks based on objectives and market context
- Document regulatory and compliance requirements
- Assess resource, timeline, and technical feasibility constraints
- Define comprehensive success validation approach

### Stakeholder Alignment
- Map business objectives to stakeholder needs
- Validate user personas against business targets
- Ensure success metrics align with business strategy
- Verify constraint realism and business impact

## BRD Generation

Use `$CTX_BRD_TEMPLATE` as base template.

### Include in BRD

- **Clear Problem Statement**: Specific business problem being solved
- **Measurable Objectives**: SMART business goals with success metrics
- **User Context**: Target personas, use cases, and market validation
- **Business Value**: Revenue impact, cost reduction, strategic advantages
- **Constraints**: Budget, timeline, regulatory, integration requirements
- **Risk Mitigation**: Business risks and proposed mitigation strategies

### Business Validation Structure

- Clear business objectives with measurable KPIs
- User personas and market validation
- Competitive analysis and differentiation
- Financial impact and ROI projections
- Implementation constraints and dependencies

## Planning and Execution

**Before writing the BRD:**

1. Create TodoWrite plan for stakeholder engagement
2. Validate business assumptions with data
3. Structure BRD for clear handoff to technical planning

## Quality Checklist

**BRD-Specific:**

- [ ] Clear business problem statement defined
- [ ] Measurable success metrics established
- [ ] Target users and personas documented
- [ ] Competitive landscape analyzed
- [ ] Business constraints and dependencies identified
- [ ] Risk assessment and mitigation strategies documented
- [ ] Stakeholder approval obtained

## BRD Validation Checklist

**Before handoff to FRP generation:**

- [ ] All template sections completed with specific information
- [ ] Business objectives are SMART (Specific, Measurable, Achievable, Relevant, Time-bound)
- [ ] Success metrics are clearly defined and measurable
- [ ] User personas include specific needs and pain points
- [ ] Business constraints are realistic and well-documented
- [ ] Risk mitigation strategies are actionable
- [ ] Stakeholder sign-off obtained

## Success Metrics

- Business objectives clearly aligned with company strategy
- Success metrics are measurable and time-bound
- User needs validated through research or data
- Business value proposition clearly articulated
- Implementation constraints realistically assessed
