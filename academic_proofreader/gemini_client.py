from google import genai

class GeminiClient:
    """Wrapper for interacting with the Google Gemini model."""
    
    def __init__(self, api_key, model_name="gemini-2.0-flash"):
        """
        Initialize the GeminiClient.
        
        Args:
            api_key (str): Google AI API key.
            model_name (str, optional): Name of the model to use. Defaults to "gemini-2.0-flash".
        """
        self.client = genai.Client(api_key=api_key)
        self.model_name = model_name
        
    def generate(self, prompt):
        """
        Generate content based on a prompt.
        
        Args:
            prompt (str): The prompt for the model.
            
        Returns:
            str: The generated text response.
        """
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt
        )
        return response.text

