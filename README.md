<<<<<<< HEAD
# email-classifier-gpt4o
This project classifies emails into six categories - Forum, Promotions, Social Media, Spam, Updates, and Verify Code - using OpenAI's GPT-4o model with few-shot prompting. It demonstrates how a large language model can perform text classification without additional training.
=======
# Email Type Classifier using GPT-4o

## Overview
This project classifies emails into six categories - Forum, Promotions, Social Media, Spam, Updates, and Verify Code - using OpenAI's GPT-4o model with few-shot prompting. It demonstrates how a large language model can perform text classification without additional training.

## Motivation
Traditional models for text classification require labeled data and model training. This project evaluates how well a general-purpose LLM can classify emails purely through prompting and examples, serving as a simple and interpretable baseline.

## Dataset
Source: [High-Accuracy Email Classification Dataset - Hugging Face](https://huggingface.co/datasets/jason23322/high-accuracy-email-classifier)  
License: Public academic use  

Columns used:
- `id` - email identifier  
- `text` - email body (sometimes includes subject)  
- `category` - ground-truth label  

Empty or null rows are automatically skipped.

## Project Structure
<pre>
compliance_assistant/
|-- main.py # main classification script
|-- prompts.json # system and few-shot examples
|-- emails.csv # dataset subset (240 rows)
|-- results.csv # output predictions
|-- .env # contains OPENAI_API_KEY
</pre>

## Setup
1. Install dependencies:
   ```
   bash
   pip install openai python-dotenv datasets
   ```
2. Create .env file:
    ini
    OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxx
3. Prepare the dataset:
    ```
    from datasets import load_dataset
    data = load_dataset("jason23322/high-accuracy-email-classifier")
    data["train"].to_pandas().to_csv("emails.csv", index=False)
    ```

## Running the classifier
    ```
    bash
    python main.py
    ``

The script reads emails.csv, classifies each email with GPT-4o, and writes results to results.csv.
Each row includes id, email_text, true_label, pred_label, correct.
Accuracy and label distribution print to the console.

Example output:
    Wrote 240 rows to results.csv
    Accuracy: 0.89
    Predicted label counts: {'promotions': 40, 'updates': 38, ...}

## Method

    Model: GPT-4o (or GPT-4o-mini)
    Prompt: few-shot classification stored in prompts.json
    Temperature: 0 (deterministic output)
    Delay: 0.25 s between calls to prevent rate limits

## Evaluation 
Metric: in-sample accuracy (predicted vs. true label).
Observed accuracy ~ 0.87-0.90 using GPT-4o with the current prompt.
Supervised baselines (CNN, GRU, BERT) reach ~ 0.98 on the same dataset.

## Improving performance
    Add 2-3 more diverse examples per label in prompts.json.
    Refine the system prompt for clearer decision rules.
    Test stronger models or fine-tuned open-source variants.

## License
The dataset is public and does not contain private or confidential information.


>>>>>>> d289f65 (Inital commmit - GPT-4o email classifier Project)
