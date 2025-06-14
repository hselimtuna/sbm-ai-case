from src.core.ai.together_ai_handler import TogetherAIHandler
from src.extract.product_detail_extractor import ProductDetailExtractor

class ChatBot:
    def __init__(self):
        self._ai_handler = TogetherAIHandler()
        self._product_detail_extractor = ProductDetailExtractor()


    def converse(self, query: str) -> str:
        classification_result = self._ai_handler.classify_intent(
            user_input=query
        )
        if classification_result:
            product_summary_info = self._product_detail_extractor.extract_product_detail(
                product_name=classification_result.get("product")[0]
            )
            available_products = self._product_detail_extractor.extract_unique_products()
            final_response = self._ai_handler.respond_product_info(
                intent=classification_result.get("intention")[0],
                product_summary_info=product_summary_info,
                user_query=query,
                available_products=','.join(available_products)
            )
            return final_response
        else:
            return "Yazdığını Anlayamadım, farklı bir şekilde sorabilir misin"
