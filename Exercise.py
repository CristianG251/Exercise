"""
Debugging Challenge: Senate Hearing Transcript Analysis

In this challenge, you’ll work with a real-world HTML transcript from a 2019 U.S. Senate hearing on Facebook’s Libra currency, where David Marcus was questioned by various senators. Your task is to run and debug a pre-written Python script that extracts and analyzes this transcript.

From this URL: https://www.govinfo.gov/content/pkg/CHRG-116shrg37919/html/CHRG-116shrg37919.htm

Objective:
The script downloads the transcript, extracts a specific section of interest, builds a structured representation of the conversation, and prints out formatted question/answer pairs—specifically the answers that Mr. Marcus gave in response to others’ questions.

Expected Final Output:
The console output should look something like:
```
Question from Senator Brown:
   Is there anything, Mr. Marcus, that elected leaders and economic experts can say that will convince you and Facebook that it should not launch this currency?

Answer from Mr. Marcus:
   Senator, we agree with all of the concerns, very legitimate concerns that were raised by Chairman Powell...
```

How the script is structured:
	1.	Downloads the HTML content from the Senate hearing transcript.
	2.	Extracts the text between two marker lines:
        - "STATEMENT OF DAVID A. MARCUS, HEAD OF CALIBRA, FACEBOOK"
        - "PREPARED STATEMENT OF SENATOR SHERROD BROWN"
	3.	Parses the semi-structured dialogue into a list of speaker turns:
        - [{"speaker": "Senator Brown", "text": ["..."]}, {"speaker": "Mr. Marcus", "text": ["..."]}, ...]
	4.	Analyzes the turns to detect questions posed to Mr. Marcus and his subsequent responses.
	5.	Prints the questions and answers in a readable format.

Your job:
    - Run the provided script.
    - Debug it. There are a number of intentional issues and bugs in the code (e.g., parsing logic, structuring errors, formatting issues).
    - You are encouraged to narrate your thought process, explain what you’re seeing in the output, and how you’re approaching each issue.
    - You may run the script as many times as you like.
    - You may consult documentation or look things up online.
    - You may not use AI code completion tools (e.g., Copilot, ChatGPT) to write code.
    - You may ask for hints or clarification at any time.

Note: You may or may not finish the challenge—this is less about completion and more about how you approach debugging a messy but real piece of code.
"""

import requests
import re


def parse_transcript(body):
    start_txt = 'STATEMENT OF DAVID A. MARCUS, HEAD OF CALIBRA, FACEBOOK'
    start_idx = body.find(start_txt)
    end_txt = 'PREPARED STATEMENT OF SENATOR SHERROD BROWN'
    end_idx = body.find(end_txt)
    section = body[start_idx + len(start_txt):end_idx]
    blocks = section.split('\n')

    structured_transcript = []
    speaker_counts = {}

    for i, block in enumerate(blocks):

        matched = re.match(r'    ((?:Senator |Chairman |Mr\. )[A-Za-z ]+\. )',
                           block)

        if matched is not None:
            name = matched.group(1).strip()

            speaker_counts[name] = speaker_counts.get(name, 0) + 1

            structured_transcript.append({
                'speaker':
                    name,
                'text': [block.replace(name, "").strip()]
            })
        elif structured_transcript:
            structured_transcript[-1]['text'].append(block.strip())

    qa_pairs = []

    for i in range(len(structured_transcript) - 1):

        previous_segment = structured_transcript[i]
        # print(f"Previous segment: {previous_segment}")

        segment = structured_transcript[i + 1]
        # print(f"Current segment: {segment}")

        if isinstance(segment["text"], list):
            previous_text = "\n".join(previous_segment["text"])
        else:
            previous_text = previous_segment["text"]

        if isinstance(segment["text"], list):
            text = "\n".join(segment["text"])
        else:
            text = segment["text"]

        if (previous_segment.get("speaker") != 'Mr. Marcus.' and '?' in previous_text
                and segment.get("speaker") == 'Mr. Marcus.'):
            print("Question from", previous_segment["speaker"])
            print("  ", previous_text)
            print("Answer from", segment["speaker"])
            print("  ", text)
            print("")
            qa_pairs.append({
                'question': previous_text,
                'answer': text
            })
            """print(f"Total Q&A Pairs found: {qa_pairs}")
        else:
            print("x no Q&A Match - Conditions not me") 
            This showcases that the conditions have not been met for the Q&A match, so basically that explains why the count of question 
            answer pairs gives 0"""

    print(f"Speaker Count: ")
    for speaker, count in sorted(speaker_counts.items()):
        print(f" {speaker}: {count} times")  # I did this for the challenge #2!

    print("Count of lines of text", len(blocks))
    print("Expected", 2272)
    print("Count of transcript segments", len(structured_transcript))
    print("Expected", 341)
    print("Count of question answer pairs", len(qa_pairs))
    print("Expected", 130)

    # Once you find and fix the issue, try these challenges
    # 1. Add useful logs for the future
    # 2. Print the number times each speaker spoke, total lines they spoke, and how many questions they asked


response = requests.get(
    'https://www.govinfo.gov/content/pkg/CHRG-116shrg37919/html/CHRG-116shrg37919.htm')
response.raise_for_status()
parse_transcript(response.text)

# The problem with this code resided in 4 main errors, that i will detail for future documentation:

# 1- an unaccessible HTTP Domain, the moment it was changed, it was able to be fixed, always check for non-working domains

# 2- A problem of imports, not importing "re" caused a problem at the moment of using Regular Expressions in the program

# 3- There was a bug based on the matched variable not giving results if it was set to True, since every result gave a False boolean,
# setting it up to "if matched is not None" allowed the system to work, taking on both boolean values, also approached it with a more
# comfortable For loop

# 4- The last problem resided on the use of integers when a List was required at qa_pairs = 0, transforming the variable into a List,
# along with setting up Instances for each case allowed a quick fix, printing the total Q&A Pairs found, and the ones that had conditions
# not met helped for the conclusion