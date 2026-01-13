---
name: lead-insight-parser
description: Parses raw customer inquiries and converts them into structured Lead_Report.md files. Analyzes sentiment, budget, urgency, client intent, pain points, and suggests responses. Flags high-value leads for priority follow-up. Use when processing customer inquiries, sales leads, or marketing messages.
---

# Lead-Insight-Parser Skill

This skill parses raw customer inquiries and converts them into structured Lead_Report.md files. It analyzes sentiment, budget, urgency, client intent, pain points, and suggests responses, flagging high-value leads for priority follow-up.

## Usage

Trigger this skill when you need to:
- Process customer inquiry emails or messages
- Qualify sales leads automatically
- Generate structured lead reports
- Prioritize follow-up based on lead value
- Analyze customer sentiment and urgency

## Process

1. Analyze raw customer inquiry text
2. Extract key information (client intent, budget, timeline, pain points)
3. Assess sentiment and urgency level
4. Flag high-value leads
5. Generate structured Lead_Report.md with suggested responses

## Key Features

- **Sentiment Analysis**: Determines positive, negative, or neutral sentiment
- **Budget Detection**: Identifies budget ranges or willingness to pay
- **Urgency Assessment**: Rates urgency level (High/Medium/Low)
- **Pain Point Extraction**: Identifies key customer problems
- **Intent Classification**: Assesses purchase readiness
- **Response Suggestions**: Provides tailored follow-up recommendations
- **Lead Scoring**: Flags high-value leads for priority attention

## Scripts

The skill uses helper scripts in the `scripts/` directory to analyze inquiries and generate reports.