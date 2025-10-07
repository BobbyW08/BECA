"""
AI Model training, fine-tuning, and experimentation tools for BECA
Helps BECA learn about and work with various AI models
"""
from langchain_core.tools import tool
import os
import json
import subprocess


@tool
def explore_ollama_models() -> str:
    """
    List all available Ollama models and their capabilities.
    Helps BECA understand what models are available locally.

    Returns:
        List of available Ollama models
    """
    try:
        result = subprocess.run(
            ['ollama', 'list'],
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.returncode != 0:
            return "Ollama is not installed or not running. Install from: https://ollama.ai"

        output = result.stdout

        report = """🤖 Available Ollama Models:

""" + output + """

💡 Use these models for different tasks:
- Code generation: codellama, deepseek-coder
- General chat: llama3.1, mistral, phi
- Small/fast: phi, tinyllama
- Large/powerful: llama3.1:70b, mixtral

Use 'ollama pull <model>' to download new models.
"""

        return report

    except FileNotFoundError:
        return "Ollama is not installed. Install from: https://ollama.ai"
    except Exception as e:
        return f"Error exploring Ollama models: {str(e)}"


@tool
def show_model_info(model_name: str) -> str:
    """
    Show detailed information about a specific Ollama model.
    Learn about model capabilities, parameters, and configuration.

    Args:
        model_name: Name of the Ollama model (e.g., "llama3.1:8b")

    Returns:
        Model information and capabilities
    """
    try:
        result = subprocess.run(
            ['ollama', 'show', model_name],
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.returncode != 0:
            return f"Model '{model_name}' not found. Use explore_ollama_models to see available models."

        return f"""🤖 Model Information: {model_name}

{result.stdout}

💡 This information helps BECA understand:
- Model architecture and parameters
- Context window size
- Template format
- Capabilities and limitations
"""

    except FileNotFoundError:
        return "Ollama is not installed."
    except Exception as e:
        return f"Error getting model info: {str(e)}"


@tool
def create_modelfile(model_name: str, base_model: str, system_prompt: str,
                    temperature: float = 0.7, top_k: int = 40,
                    top_p: float = 0.9) -> str:
    """
    Create a custom Modelfile to define model behavior and personality.
    This is how you customize and create new models from base models.

    Args:
        model_name: Name for your custom model
        base_model: Base model to build from (e.g., "llama3.1:8b")
        system_prompt: System prompt that defines model behavior
        temperature: Randomness (0.0-1.0)
        top_k: Diversity parameter
        top_p: Nucleus sampling parameter

    Returns:
        Modelfile content and instructions
    """
    try:
        modelfile_content = f"""# Modelfile for {model_name}
# Custom model created by BECA

FROM {base_model}

# System prompt that defines behavior
SYSTEM \"\"\"
{system_prompt}
\"\"\"

# Parameters
PARAMETER temperature {temperature}
PARAMETER top_k {top_k}
PARAMETER top_p {top_p}
PARAMETER num_predict 2048

# Optional: Add example conversations to teach the model
# MESSAGE user "Example user message"
# MESSAGE assistant "Example assistant response"
"""

        # Save to file
        modelfile_path = f"C:/beca-learning/modelfiles/{model_name}.modelfile"
        os.makedirs(os.path.dirname(modelfile_path), exist_ok=True)

        with open(modelfile_path, 'w') as f:
            f.write(modelfile_content)

        return f"""✅ Modelfile created: {modelfile_path}

📄 Content:
{modelfile_content}

🚀 To create this model in Ollama, run:
   ollama create {model_name} -f {modelfile_path}

💡 Model Customization Tips:
1. System prompt defines personality and behavior
2. Temperature controls randomness (lower = more focused)
3. Add MESSAGE examples to teach specific response styles
4. Test and iterate on the system prompt
5. Use 'ollama run {model_name}' to test your custom model
"""

    except Exception as e:
        return f"Error creating Modelfile: {str(e)}"


@tool
def fine_tune_guidance(task_type: str, model_framework: str = "pytorch") -> str:
    """
    Get guidance on fine-tuning AI models for specific tasks.
    BECA will provide step-by-step instructions and code examples.

    Args:
        task_type: Type of task ("text-classification", "code-generation", "question-answering", "summarization")
        model_framework: Framework to use ("pytorch", "tensorflow", "transformers")

    Returns:
        Fine-tuning guidance and code examples
    """
    try:
        guidance = {
            "text-classification": {
                "description": "Fine-tune models to classify text into categories",
                "steps": [
                    "1. Prepare labeled dataset (text, label pairs)",
                    "2. Load pre-trained model (BERT, RoBERTa, etc.)",
                    "3. Add classification head",
                    "4. Train on your dataset",
                    "5. Evaluate and iterate"
                ],
                "example_code": """
# Using Transformers library
from transformers import AutoModelForSequenceClassification, Trainer, TrainingArguments

# Load pre-trained model
model = AutoModelForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=2)

# Define training arguments
training_args = TrainingArguments(
    output_dir='./results',
    num_train_epochs=3,
    per_device_train_batch_size=16,
    warmup_steps=500,
    weight_decay=0.01,
    logging_dir='./logs',
)

# Train
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset
)
trainer.train()
"""
            },
            "code-generation": {
                "description": "Fine-tune models for code generation tasks",
                "steps": [
                    "1. Collect code examples in your target language",
                    "2. Format as (prompt, code) pairs",
                    "3. Use CodeLlama or similar base model",
                    "4. Fine-tune with LoRA/QLoRA for efficiency",
                    "5. Test on real coding tasks"
                ],
                "example_code": """
# Fine-tuning with LoRA (Low-Rank Adaptation)
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
from transformers import AutoModelForCausalLM, AutoTokenizer

# Load base model
model = AutoModelForCausalLM.from_pretrained('codellama/CodeLlama-7b-hf', load_in_8bit=True)
tokenizer = AutoTokenizer.from_pretrained('codellama/CodeLlama-7b-hf')

# Configure LoRA
lora_config = LoraConfig(
    r=16,  # Rank
    lora_alpha=32,
    target_modules=['q_proj', 'v_proj'],
    lora_dropout=0.05,
    task_type='CAUSAL_LM'
)

# Prepare model
model = prepare_model_for_kbit_training(model)
model = get_peft_model(model, lora_config)

# Train (use Trainer as above)
"""
            },
            "question-answering": {
                "description": "Fine-tune models to answer questions based on context",
                "steps": [
                    "1. Prepare Q&A dataset with context",
                    "2. Use QA-optimized model (BERT, RoBERTa)",
                    "3. Format data as (question, context, answer)",
                    "4. Fine-tune with SQuAD-style training",
                    "5. Evaluate with F1 and exact match scores"
                ],
                "example_code": """
# Question Answering fine-tuning
from transformers import AutoModelForQuestionAnswering, Trainer

model = AutoModelForQuestionAnswering.from_pretrained('bert-base-uncased')

# Dataset should have: question, context, answer_start, answer_text
# Train with Trainer (similar to classification)
"""
            },
            "summarization": {
                "description": "Fine-tune models to generate summaries",
                "steps": [
                    "1. Collect (document, summary) pairs",
                    "2. Use seq2seq model (T5, BART, Pegasus)",
                    "3. Tokenize inputs and targets",
                    "4. Train with appropriate metrics (ROUGE)",
                    "5. Test on various document lengths"
                ],
                "example_code": """
# Summarization fine-tuning
from transformers import AutoModelForSeq2SeqLM, Seq2SeqTrainer

model = AutoModelForSeq2SeqLM.from_pretrained('facebook/bart-base')

# Dataset: input_text (document), target_text (summary)
# Use Seq2SeqTrainer for training
"""
            }
        }

        if task_type not in guidance:
            return f"Unknown task type: {task_type}. Available: {', '.join(guidance.keys())}"

        task_guide = guidance[task_type]

        report = f"""🎓 Fine-Tuning Guidance: {task_type}
Framework: {model_framework}

📝 Description:
{task_guide['description']}

📋 Steps:
"""
        for step in task_guide['steps']:
            report += f"   {step}\n"

        report += f"""
💻 Example Code:
{task_guide['example_code']}

📚 Additional Resources:
- Hugging Face: https://huggingface.co/docs/transformers/training
- LoRA Paper: https://arxiv.org/abs/2106.09685
- PEFT Library: https://github.com/huggingface/peft

💡 Tips:
1. Start with small learning rate (1e-5 to 5e-5)
2. Use gradient accumulation for large models
3. Monitor validation loss to prevent overfitting
4. Consider using LoRA/QLoRA for memory efficiency
5. Save checkpoints frequently
"""

        return report

    except Exception as e:
        return f"Error generating fine-tuning guidance: {str(e)}"


@tool
def setup_training_environment(project_name: str, framework: str = "pytorch") -> str:
    """
    Set up a complete AI model training environment with all necessary files.
    Creates project structure, requirements, and template training scripts.

    Args:
        project_name: Name for the training project
        framework: ML framework ("pytorch", "tensorflow", "transformers")

    Returns:
        Success message with project structure
    """
    try:
        project_path = os.path.join("C:/", project_name)
        os.makedirs(project_path, exist_ok=True)

        # Create directory structure
        os.makedirs(f"{project_path}/data", exist_ok=True)
        os.makedirs(f"{project_path}/models", exist_ok=True)
        os.makedirs(f"{project_path}/scripts", exist_ok=True)
        os.makedirs(f"{project_path}/notebooks", exist_ok=True)

        # Create requirements.txt
        requirements = {
            "pytorch": """torch>=2.0.0
transformers>=4.30.0
datasets>=2.14.0
peft>=0.4.0
accelerate>=0.20.0
tensorboard>=2.13.0
scikit-learn>=1.3.0
pandas>=2.0.0
numpy>=1.24.0
""",
            "tensorflow": """tensorflow>=2.13.0
transformers>=4.30.0
datasets>=2.14.0
tensorboard>=2.13.0
scikit-learn>=1.3.0
pandas>=2.0.0
numpy>=1.24.0
""",
            "transformers": """transformers>=4.30.0
datasets>=2.14.0
peft>=0.4.0
accelerate>=0.20.0
torch>=2.0.0
tensorboard>=2.13.0
evaluate>=0.4.0
scikit-learn>=1.3.0
"""
        }

        with open(f"{project_path}/requirements.txt", 'w') as f:
            f.write(requirements.get(framework, requirements["pytorch"]))

        # Create training script template
        train_script = f"""\"\"\"
Training script for {project_name}
Created by BECA
\"\"\"
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, Trainer, TrainingArguments
from datasets import load_dataset

def main():
    # Configuration
    model_name = 'gpt2'  # Change to your base model
    output_dir = './models/{project_name}'

    # Load model and tokenizer
    model = AutoModelForCausalLM.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    # Load your dataset
    # dataset = load_dataset('your_dataset')

    # Training arguments
    training_args = TrainingArguments(
        output_dir=output_dir,
        num_train_epochs=3,
        per_device_train_batch_size=4,
        per_device_eval_batch_size=4,
        warmup_steps=500,
        weight_decay=0.01,
        logging_dir='./logs',
        logging_steps=100,
        save_steps=1000,
        eval_steps=500,
        evaluation_strategy='steps',
        save_total_limit=3,
        load_best_model_at_end=True,
    )

    # Initialize trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        # train_dataset=train_dataset,
        # eval_dataset=eval_dataset,
    )

    # Train
    print("Starting training...")
    trainer.train()

    # Save final model
    trainer.save_model(output_dir)
    print(f"Model saved to {{output_dir}}")

if __name__ == '__main__':
    main()
"""

        with open(f"{project_path}/scripts/train.py", 'w') as f:
            f.write(train_script)

        # Create README
        readme = f"""# {project_name}

AI Model Training Project created by BECA

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Prepare your dataset in `data/`

3. Configure training in `scripts/train.py`

4. Run training:
```bash
python scripts/train.py
```

## Structure

- `data/` - Training data
- `models/` - Saved models
- `scripts/` - Training scripts
- `notebooks/` - Jupyter notebooks for experimentation

## Framework

{framework}

## Next Steps

1. Add your dataset to `data/`
2. Modify `scripts/train.py` to load your data
3. Adjust hyperparameters in TrainingArguments
4. Run training and monitor in tensorboard
"""

        with open(f"{project_path}/README.md", 'w') as f:
            f.write(readme)

        return f"""✅ Training environment created: {project_path}

📁 Project Structure:
   {project_name}/
   ├── data/              (your datasets)
   ├── models/            (saved models)
   ├── scripts/
   │   └── train.py       (training script)
   ├── notebooks/         (experiments)
   ├── requirements.txt
   └── README.md

🚀 Next steps:
   1. cd {project_path}
   2. pip install -r requirements.txt
   3. Add your dataset to data/
   4. Modify scripts/train.py
   5. python scripts/train.py

Framework: {framework}
"""

    except Exception as e:
        return f"Error setting up training environment: {str(e)}"


# Export AI model tools
AI_MODEL_TOOLS = [
    explore_ollama_models,
    show_model_info,
    create_modelfile,
    fine_tune_guidance,
    setup_training_environment,
]
