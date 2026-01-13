#!/usr/bin/env python3

import os
import sys
import re
import json
from datetime import datetime
from pathlib import Path
import argparse

def detect_sentiment(text):
    """Analyze sentiment of the inquiry text."""
    positive_indicators = [
        'interested', 'love', 'perfect', 'great', 'excellent', 'amazing', 'fantastic',
        'need', 'want', 'must have', 'looking forward', 'awesome', 'brilliant',
        'urgent', 'asap', 'immediately', 'right away', 'today', 'now'
    ]

    negative_indicators = [
        'disappointed', 'frustrated', 'angry', 'terrible', 'awful', 'worst',
        'expensive', 'too much', 'overpriced', 'not interested', 'no thanks',
        'can\'t afford', 'budget constraint', 'delayed', 'postponed'
    ]

    text_lower = text.lower()
    positive_score = sum(1 for word in positive_indicators if word in text_lower)
    negative_score = sum(1 for word in negative_indicators if word in text_lower)

    if positive_score > negative_score:
        return "Positive"
    elif negative_score > positive_score:
        return "Negative"
    else:
        return "Neutral"

def extract_budget(text):
    """Extract budget information from the text."""
    # Pattern to match various budget formats
    budget_patterns = [
        r'\$(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)',  # $1,000.00
        r'(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)\s*dollars?',  # 1000 dollars
        r'(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)\s*USD',  # 1000 USD
        r'budget[:\s]+\$?(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)',  # budget: 1000
        r'(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)\s*(?:per month|monthly)',  # 500 per month
    ]

    budgets = []
    for pattern in budget_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for match in matches:
            # Remove commas for numeric comparison
            clean_budget = float(match.replace(',', ''))
            budgets.append(clean_budget)

    if budgets:
        return f"${max(budgets):,.2f}"
    else:
        # Check for budget-related phrases
        budget_phrases = [
            'under budget', 'within budget', 'affordable', 'budget-friendly',
            'high budget', 'low budget', 'medium budget', 'flexible budget',
            'can spend more', 'price is not an issue', 'premium', 'enterprise'
        ]

        text_lower = text.lower()
        for phrase in budget_phrases:
            if phrase in text_lower:
                return f"Budget mentioned: {phrase}"

        return "Not specified"

def assess_urgency(text):
    """Assess the urgency level of the inquiry."""
    high_urgency_keywords = [
        'asap', 'urgent', 'immediately', 'today', 'now', 'right away',
        'deadline', 'due soon', 'time sensitive', 'rush', 'expedited',
        'cannot wait', 'pressing need', 'critical', 'emergency'
    ]

    medium_urgency_keywords = [
        'soon', 'within days', 'next week', 'this week', 'early',
        'faster', 'earlier', 'prioritize', 'important', 'needs attention'
    ]

    text_lower = text.lower()

    high_urgency_count = sum(1 for word in high_urgency_keywords if word in text_lower)
    medium_urgency_count = sum(1 for word in medium_urgency_keywords if word in text_lower)

    if high_urgency_count > 0:
        return "High"
    elif medium_urgency_count > 0:
        return "Medium"
    else:
        # Check for timeframes
        timeframe_patterns = [
            r'within\s+\d+\s+(days?|weeks?|hours?)',
            r'in\s+\d+\s+(days?|weeks?|hours?)',
            r'by\s+\w+\s+\d+',  # by March 15
            r'next\s+(week|month|quarter)'
        ]

        for pattern in timeframe_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return "Medium"

        return "Low"

def extract_client_intent(text):
    """Extract client intent from the inquiry."""
    intent_keywords = {
        'buying': ['buy', 'purchase', 'order', 'acquire', 'obtain', 'get', 'procure'],
        'evaluating': ['evaluate', 'assess', 'consider', 'review', 'analyze', 'compare', 'benchmark'],
        'information': ['info', 'information', 'details', 'more details', 'learn', 'know', 'about'],
        'problem_solving': ['solve', 'fix', 'resolve', 'address', 'handle', 'deal with'],
        'consultation': ['consult', 'advise', 'recommend', 'suggestion', 'guidance', 'help']
    }

    text_lower = text.lower()
    intents = []

    for intent_type, keywords in intent_keywords.items():
        for keyword in keywords:
            if keyword in text_lower:
                intents.append(intent_type.replace('_', ' ').title())

    return ', '.join(set(intents)) if intents else "Not clearly stated"

def identify_pain_points(text):
    """Identify key pain points from the inquiry."""
    pain_point_keywords = [
        'problem', 'issue', 'difficulty', 'struggle', 'challenge', 'pain point',
        'trouble', 'frustration', 'inefficient', 'slow', 'complicated',
        'costly', 'expensive', 'not working', 'broken', 'missing',
        'need better', 'need more', 'lacking', 'gap', 'limitation',
        'outdated', 'old', 'legacy', 'can\'t', 'unable to', 'difficult to'
    ]

    text_lower = text.lower()
    pain_points = []

    for keyword in pain_point_keywords:
        if keyword in text_lower:
            # Extract context around the pain point
            pattern = r'.{0,30}' + re.escape(keyword) + r'.{0,50}'
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                pain_points.append(match.strip())

    return list(set(pain_points)) if pain_points else ["No specific pain points identified"]

def suggest_response(text, urgency_level, sentiment):
    """Suggest an appropriate response based on analysis."""
    base_response = "Thank you for reaching out. We appreciate your interest and will respond shortly."

    if urgency_level == "High":
        base_response = "Thank you for your urgent inquiry. We prioritize your request and will contact you immediately."
    elif urgency_level == "Medium":
        base_response = "Thank you for your inquiry. We will respond promptly within 24 hours."

    if sentiment == "Positive":
        base_response += " We're excited to learn more about your needs."
    elif sentiment == "Negative":
        base_response += " We're committed to addressing your concerns."

    return base_response

def flag_high_value_lead(sentiment, urgency_level, budget_info):
    """Flag if this is a high-value lead."""
    high_value_indicators = 0

    if sentiment == "Positive":
        high_value_indicators += 1

    if urgency_level == "High":
        high_value_indicators += 1

    if budget_info != "Not specified" and "Not specified" not in budget_info:
        high_value_indicators += 1

        # Check if budget is substantial
        budget_match = re.search(r'\$(\d+)', budget_info)
        if budget_match:
            budget_amount = float(budget_match.group(1).replace(',', ''))
            if budget_amount > 1000:  # Adjust threshold as needed
                high_value_indicators += 1

    return high_value_indicators >= 2

def generate_lead_report(inquiry_text, output_file=None):
    """Generate a structured lead report from the inquiry text."""
    # Perform analysis
    sentiment = detect_sentiment(inquiry_text)
    budget_info = extract_budget(inquiry_text)
    urgency_level = assess_urgency(inquiry_text)
    client_intent = extract_client_intent(inquiry_text)
    pain_points = identify_pain_points(inquiry_text)
    suggested_response = suggest_response(inquiry_text, urgency_level, sentiment)
    is_high_value = flag_high_value_lead(sentiment, urgency_level, budget_info)

    # Create report content
    report_content = []
    report_content.append(f"# Lead Report - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report_content.append("")
    report_content.append("## Original Inquiry")
    report_content.append("```")
    report_content.append(inquiry_text.strip())
    report_content.append("```")
    report_content.append("")
    report_content.append("## Analysis Results")
    report_content.append("")
    report_content.append(f"### Client Intent")
    report_content.append(client_intent if client_intent else "Not clearly stated")
    report_content.append("")
    report_content.append(f"### Urgency Level")
    report_content.append(f"**{urgency_level}**")
    report_content.append("")
    report_content.append(f"### Key Pain Points")
    for point in pain_points[:5]:  # Limit to top 5 pain points
        report_content.append(f"- {point}")
    report_content.append("")
    report_content.append(f"### Sentiment Analysis")
    report_content.append(f"- Overall Sentiment: **{sentiment}**")
    report_content.append("")
    report_content.append(f"### Budget Information")
    report_content.append(f"- Budget: **{budget_info}**")
    report_content.append("")
    report_content.append(f"### Lead Value Assessment")
    report_content.append(f"- High Value Lead: {'**YES**' if is_high_value else 'No'}")
    report_content.append("")
    report_content.append(f"### Recommended Action")
    report_content.append(f"- Priority Level: {'**HIGH**' if is_high_value or urgency_level == 'High' else 'Normal'}")
    report_content.append("")
    report_content.append(f"### Suggested Response")
    report_content.append(suggested_response)
    report_content.append("")
    report_content.append("---")
    report_content.append("*This report was automatically generated by Lead-Insight-Parser skill*")

    # Write to file
    if output_file is None:
        output_file = "Lead_Report.md"

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(report_content))

    # Print summary
    print(f"Lead report generated: {output_file}")
    print(f"Sentiment: {sentiment}")
    print(f"Urgency: {urgency_level}")
    print(f"High Value Lead: {'Yes' if is_high_value else 'No'}")
    print(f"Budget: {budget_info}")

    return {
        'sentiment': sentiment,
        'urgency': urgency_level,
        'budget': budget_info,
        'is_high_value': is_high_value,
        'client_intent': client_intent,
        'pain_points': pain_points,
        'suggested_response': suggested_response
    }

def main():
    parser = argparse.ArgumentParser(description='Parse customer inquiry and generate lead report')
    parser.add_argument('input_file', help='Input file containing the customer inquiry')
    parser.add_argument('-o', '--output', default='Lead_Report.md', help='Output file name (default: Lead_Report.md)')

    args = parser.parse_args()

    if not os.path.exists(args.input_file):
        print(f"Error: Input file {args.input_file} does not exist")
        sys.exit(1)

    with open(args.input_file, 'r', encoding='utf-8') as f:
        inquiry_text = f.read()

    generate_lead_report(inquiry_text, args.output)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        # If no arguments provided, run in interactive mode
        sample_inquiry = input("Enter the customer inquiry text: ")
        generate_lead_report(sample_inquiry)
    else:
        main()