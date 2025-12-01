from typing import Dict, List
import tiktoken
import threading

class TokenCounter:
    """Servicio centralizado para conteo de tokens y cálculo de costos."""

    PRICING = {
        'groq-8b': {'input': 0.0, 'output': 0.0},
        'groq-70b': {'input': 0.0, 'output': 0.0},
        'deepseek': {'input': 0.18, 'output': 0.18},
        'gemini-pro': {'input': 0.0, 'output': 0.0},
        'cohere-command-r': {'input': 0.42, 'output': 0.42},
        'cohere-command-r-plus': {'input': 2.50, 'output': 2.50},
        'mistral-agent': {'input': 0.09, 'output': 0.09},
        'mistral-vps': {'input': 0.0, 'output': 0.0},
    }

    def __init__(self):
        # cl100k_base cubre GPT-4/3.5, aproximación para otros modelos
        self.encoder = tiktoken.get_encoding("cl100k_base")
        self._lock = threading.Lock()

    def count_tokens(self, text: str) -> int:
        if not text:
            return 0
        return len(self.encoder.encode(text))

    def count_messages_tokens(self, messages: List[Dict]) -> int:
        total = 0
        for msg in messages:
            total += 4  # overhead por mensaje
            total += self.count_tokens(msg.get('content', ''))
            total += self.count_tokens(msg.get('role', ''))
        total += 2  # overhead final
        return total

    def calculate_cost(self, provider_id: str, input_tokens: int, output_tokens: int) -> Dict[str, float]:
        pricing = self.PRICING.get(provider_id, {'input': 0.0, 'output': 0.0})
        input_cost = (input_tokens / 1_000_000) * pricing['input']
        output_cost = (output_tokens / 1_000_000) * pricing['output']
        total = input_cost + output_cost
        return {
            'provider': provider_id,
            'input_tokens': input_tokens,
            'output_tokens': output_tokens,
            'total_tokens': input_tokens + output_tokens,
            'input_cost_eur': round(input_cost, 6),
            'output_cost_eur': round(output_cost, 6),
            'total_cost_eur': round(total, 6),
        }

# Singleton
token_counter = TokenCounter()
