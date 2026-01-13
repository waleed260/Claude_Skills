# Lead-Insight-Parser Skill - Reference Guide

## Overview

The Lead-Insight-Parser skill automates the process of analyzing customer inquiries and generating structured lead reports. It saves sales teams 2-3 hours daily by automatically qualifying leads and prioritizing follow-ups.

## Key Features

### Sentiment Analysis
- Determines positive, negative, or neutral sentiment in inquiries
- Uses keyword-based analysis with weighted scoring
- Helps identify enthusiastic prospects vs. dissatisfied customers

### Budget Detection
- Identifies explicit budget mentions ($1000, $5,000, etc.)
- Recognizes budget-related phrases and constraints
- Flags high-value opportunities

### Urgency Assessment
- Categorizes urgency as High, Medium, or Low
- Identifies time-sensitive requests and deadlines
- Helps prioritize immediate follow-ups

### Intent Classification
- Identifies buying, evaluating, information-seeking, or problem-solving intent
- Helps tailor appropriate responses
- Assists in qualification process

### Pain Point Extraction
- Identifies specific customer problems and challenges
- Helps prepare targeted solutions
- Enables consultative selling approach

### Lead Scoring
- Flags high-value leads based on multiple factors
- Combines sentiment, urgency, and budget indicators
- Enables priority-based follow-up

## Usage

### Single Inquiry Processing
```bash
python scripts/parse_lead.py <input_file.txt> [-o output_report.md]
```

### Batch Processing
```bash
python scripts/batch_parse.py <input_directory> [output_directory]
```

## Output Format

The skill generates a comprehensive Lead_Report.md with:

- **Original Inquiry**: Full text of the customer message
- **Client Intent**: Purpose of the inquiry
- **Urgency Level**: High/Medium/Low classification
- **Key Pain Points**: Identified customer challenges
- **Sentiment Analysis**: Positive/Negative/Neutral assessment
- **Budget Information**: Financial capacity indicators
- **Lead Value Assessment**: High value lead flag
- **Recommended Action**: Priority level suggestion
- **Suggested Response**: Tailored response template

## Supported Input Formats

- Plain text files (.txt)
- Email files (.eml)
- Markdown files (.md)

## Customization

### Threshold Adjustment
Modify the `flag_high_value_lead` function to adjust the criteria for high-value leads based on your business needs.

### Keyword Expansion
Add more keywords to the sentiment, urgency, and pain point detection functions to improve accuracy for your industry.

### Response Templates
Customize the `suggest_response` function to align with your company's communication style.

## Best Practices

### Before Processing
- Ensure inquiry text is clean and complete
- Remove any confidential information if necessary
- Verify file encoding (UTF-8 recommended)

### After Generation
- Review the generated report for accuracy
- Customize the suggested response as needed
- Update CRM systems with extracted information
- Follow up based on priority level indicated

## Integration

The skill works well with:
- CRM systems (manually import reports)
- Email platforms (process inquiry threads)
- Customer support tools
- Sales automation workflows

## Accuracy Considerations

- Results are based on keyword analysis and pattern matching
- Complex inquiries may require manual review
- Sarcasm or nuanced language might be misinterpreted
- Regular updates to keyword lists improve accuracy