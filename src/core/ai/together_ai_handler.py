import json
from together import Together
from config.base_config import conf
from typing import Dict, Any, Optional
from src.logger.custom_logger import SingletonLogger
import re


class TogetherAIHandler:
    def __init__(self, model="deepseek-ai/DeepSeek-V3"):
        self._api_key = conf["TOGETHER"]["KEY"]
        self._client = Together(api_key=self._api_key)
        self._model = model
        self._logger = SingletonLogger()

    @staticmethod
    def _clean_intention_response(intent_response: str) -> Dict[str, Any]:
        try:
            intent_response = re.sub(r"```json|```", "", intent_response).strip()
            return json.loads(intent_response)
        except json.JSONDecodeError as e:
            raise ValueError(f"JSON parsing failed: {str(e)}\nRaw content: {intent_response}")


    def classify_intent(self, user_input: str) -> Optional[Dict[str, Any]]:
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

            intent = self._clean_intention_response(intent)
            self._logger.log_ai_event(
                user_prompt=prompt,
                tokens_used=response.usage.total_tokens,
                model_response=f"{intent}",
                query=user_input
            )
            return intent
        except Exception as e:
            self._logger._logger.error(f"[AIHandler] Intent classification failed: {str(e)}")
            return None

    def respond_product_info(
            self,
            product_summary_info: list,
            user_query: str,
            intent: str,
            available_products: str
    ) -> str:
        if intent == "other":
            return """
            Sorduğunuz soruya maalesef cevap veremeyeceğim. Yardımcı olabileceğim konular:
            - stok durumu
            - kategori sorgulama
            - ürün özellikleri
            - marka sorgulama
            """
        else:
            prompt = f"""
                You are a helpful assistant with access to structured product information. Your job is to answer the user's question **strictly using the data provided below**.
                ### User Query
                    "{user_query}"
                ### Classified Context:
                    - Intent: "{intent}"
                    - Mentioned Products: {product_summary_info}
                ### Product Data (JSON List)
                    Here is the list of available products in the system:{available_products}
                ### Instructions:
                    - Use only the product data to answer.
                    - Answer based on the user’s intent and product(s) mentioned.
                    - For "stock_availability", return quantity and availability.
                    - For "product_spec", return product details like description, size, color, etc.
                    - For "brand_lookup", identify which brand(s) are associated with the mentioned product.
                    - For "category_lookup", identify the category of the product.
                    - If intent is "other", provide a relevant answer based only on the data.
                ### Final Answer:
                Answer concisely and helpfully based on the data above.
            """
            response = self._client.chat.completions.create(
                model=self._model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0,
                max_tokens=1000,
            )
            self._logger.log_ai_event(
                user_prompt=prompt,
                tokens_used=response.usage.total_tokens,
                model_response=f"{intent}",
                query=user_query
            )
            return response.choices[0].message.content