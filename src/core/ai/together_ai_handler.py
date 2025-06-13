import json
from together import Together
from config.base_config import conf


class TogetherAIHandler:
    def __init__(self, model="deepseek-ai/DeepSeek-V3"):
        self._api_key = conf["TOGETHER"]["KEY"]
        self._client = Together(api_key=self._api_key)
        self._model = model

    def classify_intent(self, user_input: str) -> str:
        prompt = f"""
        You are an assistant that analyzes user queries about products.

        Your task:

        1. Classify the user's intent into one of the following:
        - "stock_availability"
        - "category_lookup"
        - "product_spec"
        - "brand_lookup"
        - "other"

        2. Determine the product(s) mentioned in the question from this list:
        - T-Shirt
        - Jeans
        - Smartphone
        - Laptop
        - Jacket

        If no product is found, use "None" as the product.

        User Question: "{user_input}"

        Return a raw JSON string (do NOT use markdown or triple backticks), in this format:
        python dict "intention": ["<intent>"],"product": ["<Product>" or "None"] 
        """

        try:
            response = self._client.chat.completions.create(
                model=self._model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0,
                max_tokens=100,
            )
            intent = response.choices[0].message.content
            if "json" in intent:
                json.loads(
                    intent.replace("```", "")
                    .replace("json", "")
                    .replace("```", "")
                    .replace("\n", "")
                )
            print(
                "Classified Question & Product",
                intent,
                "Computed Token: ",
                response.usage.total_tokens,
            )
            return intent
        except Exception as e:
            print(f"[AIHandler] Intent classification failed: {e}")
            return "other"

    def extract_info(self, user_input: str, intent: str) -> dict:
        raise NotImplementedError("")
