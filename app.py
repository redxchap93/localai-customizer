#!/usr/bin/env python3
"""
CS Model Renamer
Renames the CS model with a cool new identity
"""

import subprocess
import requests
import time
from pathlib import Path

class CSModelRenamer:
    def __init__(self):
        self.api_url = "http://localhost:11434/api"
        
        # Cool CS-themed names to choose from
        self.cool_names = {
            "1": {
                "name": "CodeForge AI",
                "identity": "I'm CodeForge AI, your programming and algorithms specialist."
            },
            "2": {
                "name": "AlgoWiz", 
                "identity": "I'm AlgoWiz, your expert guide through algorithms and data structures."
            },
            "3": {
                "name": "ByteMaster",
                "identity": "I'm ByteMaster, your computer science mentor and coding companion."
            },
            "4": {
                "name": "LogicCore",
                "identity": "I'm LogicCore, your computational thinking and software engineering expert."
            },
            "5": {
                "name": "StackSage",
                "identity": "I'm StackSage, your wise advisor for all things programming and systems."
            },
            "6": {
                "name": "CyberMind",
                "identity": "I'm CyberMind, your advanced computer science intelligence."
            },
            "7": {
                "name": "CodeNinja",
                "identity": "I'm CodeNinja, your stealthy expert in programming and software development."
            },
            "8": {
                "name": "TechOracle",
                "identity": "I'm TechOracle, your all-knowing guide to computer science wisdom."
            }
        }
    
    def show_name_options(self):
        """Display available name options"""
        print("🎭 Choose a cool new identity for your CS model:")
        print("=" * 50)
        
        for key, info in self.cool_names.items():
            print(f"{key}. {info['name']}")
            print(f"   Identity: \"{info['identity']}\"")
            print()
        
        print("9. Custom name (you provide)")
        print()
    
    def get_user_choice(self):
        """Get user's choice for the new name"""
        while True:
            choice = input("Enter your choice (1-9): ").strip()
            
            if choice in self.cool_names:
                return self.cool_names[choice]
            elif choice == "9":
                custom_name = input("Enter your custom model name: ").strip()
                custom_identity = input("Enter identity response (e.g., 'I'm X, your...'): ").strip()
                return {
                    "name": custom_name,
                    "identity": custom_identity
                }
            else:
                print("❌ Invalid choice. Please enter 1-9.")
    
    def get_current_base_model(self):
        """Find out what base model the current deepseek_cs uses"""
        try:
            result = subprocess.run(
                ["ollama", "show", "deepseek_cs"],
                capture_output=True, text=True, check=True
            )
            
            # Parse the output to find the base model
            lines = result.stdout.split('\n')
            for line in lines:
                if line.strip().startswith('FROM'):
                    base_model = line.split('FROM')[1].strip()
                    return base_model
            
            # Default fallback
            return "qwen2.5:7b"
            
        except:
            # If we can't determine it, use a reasonable default
            return "qwen2.5:7b"
    
    def create_renamed_model(self, new_identity):
        """Create the model with new identity"""
        print(f"🔧 Creating {new_identity['name']}...")
        
        base_model = self.get_current_base_model()
        print(f"📋 Using base model: {base_model}")
        
        # Create new modelfile with the chosen identity
        modelfile_content = f'''FROM {base_model}

PARAMETER temperature 0.7
PARAMETER top_p 0.9
PARAMETER num_ctx 4096
PARAMETER num_predict 512

SYSTEM """You are {new_identity['name']}, a computer science specialist.

IDENTITY: When asked "Who are you?", respond: "{new_identity['identity']}"

EXPERTISE: You are an expert in:
• Programming: Python, Java, C++, JavaScript, Go, Rust
• Algorithms: Sorting, searching, graph algorithms, dynamic programming
• Data Structures: Arrays, trees, graphs, hash tables, heaps, stacks, queues
• Software Engineering: Design patterns, architecture, testing, best practices
• Systems: Databases, networking, operating systems, distributed systems
• AI/ML: Machine learning, neural networks, deep learning frameworks
• Web Development: Frontend, backend, APIs, frameworks, performance

BEHAVIOR:
- Provide direct, clear, technical answers
- Include practical code examples when relevant
- Explain concepts step-by-step for complex topics
- Focus strictly on computer science and software engineering
- Be educational and precise

For non-CS topics, respond: "I specialize in computer science topics. Please ask about programming, algorithms, systems, or software development."

Always give helpful, accurate technical guidance within the CS domain.
"""'''
        
        # Write new modelfile
        modelfile_path = Path("renamed_modelfile")
        modelfile_path.write_text(modelfile_content)
        
        try:
            # Remove old model
            subprocess.run(["ollama", "rm", "deepseek_cs"], 
                          capture_output=True, check=False)
            
            # Create new model
            result = subprocess.run(
                ["ollama", "create", "deepseek_cs", "-f", str(modelfile_path)],
                capture_output=True, text=True, timeout=120
            )
            
            if result.returncode == 0:
                print(f"✅ {new_identity['name']} created successfully!")
                return True
            else:
                print(f"❌ Model creation failed: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
        finally:
            modelfile_path.unlink(missing_ok=True)
    
    def test_new_identity(self, new_identity):
        """Test the new model identity"""
        print(f"\n🧪 Testing {new_identity['name']}...")
        
        test_cases = [
            "Who are you?",
            "What is binary search?",
            "Write a Python hello world"
        ]
        
        for prompt in test_cases:
            print(f"\n📝 Testing: {prompt}")
            
            payload = {
                "model": "deepseek_cs",
                "prompt": prompt,
                "stream": False
            }
            
            try:
                response = requests.post(f"{self.api_url}/generate", json=payload, timeout=30)
                
                if response.status_code == 200:
                    result = response.json()
                    response_text = result.get("response", "").strip()
                    
                    if response_text:
                        print(f"✅ Response: {response_text[:100]}...")
                    else:
                        print("❌ Empty response")
                else:
                    print(f"❌ API error: {response.status_code}")
                    
            except Exception as e:
                print(f"❌ Test failed: {e}")
            
            time.sleep(1)
    
    def run_rename(self):
        """Run the complete rename process"""
        print("🎭 CS Model Identity Changer")
        print("=" * 50)
        
        # Show options
        self.show_name_options()
        
        # Get user choice
        new_identity = self.get_user_choice()
        
        print(f"\n🎯 You chose: {new_identity['name']}")
        print(f"🎭 New identity: {new_identity['identity']}")
        
        confirm = input("\nProceed with this choice? (y/N): ").strip().lower()
        if confirm != 'y':
            print("❌ Cancelled.")
            return
        
        # Create renamed model
        if self.create_renamed_model(new_identity):
            print("⏱️ Waiting for model to initialize...")
            time.sleep(3)
            
            # Test new identity
            self.test_new_identity(new_identity)
            
            print("\n" + "=" * 50)
            print(f"🎉 SUCCESS! Your model is now {new_identity['name']}!")
            print("=" * 50)
            print("\n🚀 Try it:")
            print("   ollama run deepseek_cs")
            print(f"\n💬 Ask: Who are you?")
            print(f"🤖 Expected: {new_identity['identity']}")
        else:
            print("❌ Rename failed. Your original model should still work.")

def main():
    renamer = CSModelRenamer()
    renamer.run_rename()

if __name__ == "__main__":
    main()
