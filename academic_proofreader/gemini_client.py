import google.generativeai as genai

class GeminiClient:
    """Wrapper for interacting with the Google Gemini model."""
    
    def __init__(self, api_key, model_name="gemini-2.5-pro"):
        """
        Initialize the GeminiClient.
        
        Args:
            api_key (str): Google AI API key.
            model_name (str, optional): Name of the model to use. Defaults to "gemini-2.5-pro".
        """
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name=model_name)
        
    def generate(self, prompt):
        """
        Generate content based on a prompt.
        
        Args:
            prompt (str): The prompt for the model.
            
        Returns:
            str: The generated text response.
        """
        response = self.model.generate_content(prompt)
        return response.text
