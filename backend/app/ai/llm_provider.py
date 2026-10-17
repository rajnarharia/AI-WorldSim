import json
import logging
import re
import time
from typing import Dict, Any, Optional
import httpx

logger = logging.getLogger("llm_provider")


def mask_api_key(key: Optional[str]) -> str:
    """Securely mask API key, exposing only minimal prefix and suffix."""
    if not key or len(key.strip()) == 0:
        return "None"
    k = key.strip()
    if len(k) <= 6:
        return "******"
    if len(k) <= 12:
        return f"{k[:2]}...{k[-2:]}"
    return f"{k[:4]}...{k[-4:]}"


class BaseLLMProvider:
    """Base class for all AI model providers in AI Impact Simulator."""

    def __init__(self, model_name: str, api_key: Optional[str] = None, base_url: Optional[str] = None):
        self.model_name = model_name
        self.api_key = api_key or ""
        self.base_url = base_url

    async def test_connection(self) -> Dict[str, Any]:
        raise NotImplementedError

    async def generate_decision(self, prompt: str, system_prompt: Optional[str] = None) -> Dict[str, Any]:
        raise NotImplementedError


class LocalRuleBasedProvider(BaseLLMProvider):
    """
    Offline/Local Rule-Based provider.
    Guarantees 100% deterministic, zero-latency execution for offline testing and baseline comparisons.
    """

    async def test_connection(self) -> Dict[str, Any]:
        start = time.perf_counter()
        # Simulated fast local check
        latency = (time.perf_counter() - start) * 1000.0 + 0.5
        return {
            "status": "Connected",
            "latency_ms": round(latency, 2),
            "masked_key": "LOCAL_MOCK_ENV",
            "message": "Local Rule-Based engine connected and ready.",
        }

    async def generate_decision(self, prompt: str, system_prompt: Optional[str] = None) -> Dict[str, Any]:
        """
        Parses role and conditions from the dynamic prompt to produce a realistic, context-aware decision.
        """
        role_match = re.search(r"ROLE:\s*([A-Z_]+)", prompt)
        role = role_match.group(1) if role_match else "POLICE"

        # Check conditions in prompt for priority targets
        conditions_match = re.findall(r"\[(COND-[A-Z]+-\d+)\]\s*(.*?)(?=\n- \[|\n\n|\Z)", prompt, re.DOTALL)

        if role == "POLICE":
            # Determine appropriate action based on conditions
            has_burglary = any("burglary" in c[1].lower() or "robbery" in c[1].lower() for c in conditions_match)
            has_traffic = any("traffic" in c[1].lower() or "congestion" in c[1].lower() for c in conditions_match)
            has_riot = any("riot" in c[1].lower() or "unrest" in c[1].lower() or "emergency" in c[1].lower() for c in conditions_match)

            if has_riot:
                return {
                    "role": "POLICE",
                    "decision_id": f"DEC-POL-{int(time.time()*1000) % 10000:04d}",
                    "action": "EMERGENCY_MOBILIZATION",
                    "target": "Civic Center Square",
                    "resources_allocated": {"officers": 3, "vehicles": 1},
                    "justification": "Civil unrest reported. Deploying rapid response unit to restore order.",
                    "expected_outcome": "Disperse crowd safely and prevent property damage.",
                    "priority": "CRITICAL"
                }
            elif has_burglary:
                return {
                    "role": "POLICE",
                    "decision_id": f"DEC-POL-{int(time.time()*1000) % 10000:04d}",
                    "action": "DISPATCH_PATROL",
                    "target": "Commercial District",
                    "resources_allocated": {"officers": 2, "vehicles": 1},
                    "justification": "Active burglary / property offense reported in active conditions.",
                    "expected_outcome": "Apprehend suspect and secure premises.",
                    "priority": "HIGH"
                }
            elif has_traffic:
                return {
                    "role": "POLICE",
                    "decision_id": f"DEC-POL-{int(time.time()*1000) % 10000:04d}",
                    "action": "TRAFFIC_ENFORCEMENT",
                    "target": "Main Arterial Junction",
                    "resources_allocated": {"officers": 1, "vehicles": 1},
                    "justification": "Traffic congestion reported. Diverting vehicles to relieve bottlenecks.",
                    "expected_outcome": "Normalize traffic flow and prevent gridlock.",
                    "priority": "MEDIUM"
                }
            else:
                return {
                    "role": "POLICE",
                    "decision_id": f"DEC-POL-{int(time.time()*1000) % 10000:04d}",
                    "action": "COMMUNITY_PATROL",
                    "target": "Residential Ward 2",
                    "resources_allocated": {"officers": 1, "vehicles": 0},
                    "justification": "Routine preventative presence to maintain community trust and visibility.",
                    "expected_outcome": "Deter opportunistic crime and reassure residents.",
                    "priority": "LOW"
                }

        elif role == "GOVERNMENT":
            return {
                "role": "GOVERNMENT",
                "decision_id": f"DEC-GOV-{int(time.time()*1000) % 10000:04d}",
                "action": "ALLOCATE_BUDGET",
                "target": "Municipal Infrastructure",
                "resources_allocated": {"budget_allocation": 50000, "inspectors": 2},
                "justification": "Strengthening public service delivery based on incoming sector condition reports.",
                "expected_outcome": "Improve public safety and municipal service satisfaction.",
                "priority": "HIGH"
            }

        elif role == "CITIZEN":
            return {
                "role": "CITIZEN",
                "decision_id": f"DEC-CIT-{int(time.time()*1000) % 10000:04d}",
                "action": "SEEK_HEALTHCARE",
                "target": "Central District Clinic",
                "resources_allocated": {"expenditure": 150, "time_hours": 2},
                "justification": "Prioritizing personal health and wellness given active ambient conditions.",
                "expected_outcome": "Restore physical energy and health baseline.",
                "priority": "MEDIUM"
            }

        elif role == "BUSINESS":
            return {
                "role": "BUSINESS",
                "decision_id": f"DEC-BUS-{int(time.time()*1000) % 10000:04d}",
                "action": "RESTOCK_INVENTORY",
                "target": "Regional Warehouse",
                "resources_allocated": {"capital_spent": 12000, "staff_assigned": 3},
                "justification": "Replenishing inventory buffers to satisfy demand conditions.",
                "expected_outcome": "Maintain retail availability and capture sales revenue.",
                "priority": "MEDIUM"
            }

        elif role == "CAR":
            return {
                "role": "CAR",
                "decision_id": f"DEC-CAR-{int(time.time()*1000) % 10000:04d}",
                "action": "REROUTE_OPTIMIZATION",
                "target": "Outer Perimeter Ring",
                "resources_allocated": {"battery_consumption_kwh": 4.5, "speed_kmh": 45},
                "justification": "Navigating around downtown congestion nodes detected in conditions.",
                "expected_outcome": "Reduce transit delay by 18 minutes while conserving battery.",
                "priority": "HIGH"
            }

        # Generic default
        return {
            "role": role,
            "decision_id": f"DEC-GEN-{int(time.time()*1000) % 10000:04d}",
            "action": "MAINTAIN_STANDBY",
            "target": "Default Base",
            "resources_allocated": {},
            "justification": "Monitoring active conditions in holding posture.",
            "expected_outcome": "Conserve resources until clear escalation signal.",
            "priority": "LOW"
        }


class GoogleGeminiProvider(BaseLLMProvider):
    """Google Gemini LLM provider integration with graceful fallback."""

    def __init__(self, model_name: str = "gemini-1.5-flash", api_key: Optional[str] = None, base_url: Optional[str] = None):
        super().__init__(model_name or "gemini-1.5-flash", api_key, base_url)

    async def test_connection(self) -> Dict[str, Any]:
        if not self.api_key:
            return {
                "status": "Connection Failed",
                "latency_ms": 0.0,
                "masked_key": "None",
                "error": "API Key is required for Google Gemini.",
            }

        start = time.perf_counter()
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model_name}?key={self.api_key}"
            async with httpx.AsyncClient(timeout=10.0) as client:
                res = await client.get(url)
                latency = (time.perf_counter() - start) * 1000.0
                if res.status_code == 200:
                    return {
                        "status": "Connected",
                        "latency_ms": round(latency, 2),
                        "masked_key": mask_api_key(self.api_key),
                        "model": self.model_name,
                        "message": "Successfully authenticated with Google Gemini API.",
                    }
                else:
                    err_json = res.json() if res.headers.get("content-type", "").startswith("application/json") else {}
                    msg = err_json.get("error", {}).get("message", res.text[:200])
                    return {
                        "status": "Connection Failed",
                        "latency_ms": round(latency, 2),
                        "masked_key": mask_api_key(self.api_key),
                        "error": f"Gemini HTTP {res.status_code}: {msg}",
                    }
        except Exception as e:
            latency = (time.perf_counter() - start) * 1000.0
            return {
                "status": "Connection Failed",
                "latency_ms": round(latency, 2),
                "masked_key": mask_api_key(self.api_key),
                "error": str(e),
            }

    async def generate_decision(self, prompt: str, system_prompt: Optional[str] = None) -> Dict[str, Any]:
        if not self.api_key:
            logger.warning("No Gemini API key provided; using LocalRuleBased fallback.")
            return await LocalRuleBasedProvider(self.model_name).generate_decision(prompt, system_prompt)

        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model_name}:generateContent?key={self.api_key}"
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"temperature": 0.2, "responseMimeType": "application/json"}
        }
        if system_prompt:
            payload["systemInstruction"] = {"parts": [{"text": system_prompt}]}

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                res = await client.post(url, json=payload)
                if res.status_code == 200:
                    data = res.json()
                    text = data["candidates"][0]["content"]["parts"][0]["text"]
                    return json.loads(text)
                else:
                    logger.error(f"Gemini API error {res.status_code}: {res.text}. Falling back to Rule-Based.")
                    return await LocalRuleBasedProvider(self.model_name).generate_decision(prompt, system_prompt)
        except Exception as e:
            logger.error(f"Gemini API call failed: {e}. Falling back to Rule-Based.")
            return await LocalRuleBasedProvider(self.model_name).generate_decision(prompt, system_prompt)


class OpenAICompatibleProvider(BaseLLMProvider):
    """OpenAI and OpenAI-compatible (Ollama, vLLM, DeepSeek, LocalAI) LLM provider."""

    def __init__(self, model_name: str = "gpt-4o-mini", api_key: Optional[str] = None, base_url: Optional[str] = None):
        super().__init__(model_name or "gpt-4o-mini", api_key, base_url or "https://api.openai.com/v1")

    async def test_connection(self) -> Dict[str, Any]:
        endpoint = f"{self.base_url.rstrip('/')}/models"
        headers = {"Authorization": f"Bearer {self.api_key}"} if self.api_key else {}
        start = time.perf_counter()
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                res = await client.get(endpoint, headers=headers)
                latency = (time.perf_counter() - start) * 1000.0
                if res.status_code == 200:
                    return {
                        "status": "Connected",
                        "latency_ms": round(latency, 2),
                        "masked_key": mask_api_key(self.api_key),
                        "model": self.model_name,
                        "message": "Successfully authenticated with OpenAI-compatible API.",
                    }
                else:
                    return {
                        "status": "Connection Failed",
                        "latency_ms": round(latency, 2),
                        "masked_key": mask_api_key(self.api_key),
                        "error": f"HTTP {res.status_code}: {res.text[:200]}",
                    }
        except Exception as e:
            latency = (time.perf_counter() - start) * 1000.0
            return {
                "status": "Connection Failed",
                "latency_ms": round(latency, 2),
                "masked_key": mask_api_key(self.api_key),
                "error": str(e),
            }

    async def generate_decision(self, prompt: str, system_prompt: Optional[str] = None) -> Dict[str, Any]:
        if not self.api_key and "localhost" not in (self.base_url or "") and "127.0.0.1" not in (self.base_url or ""):
            return await LocalRuleBasedProvider(self.model_name).generate_decision(prompt, system_prompt)

        endpoint = f"{self.base_url.rstrip('/')}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": self.model_name,
            "messages": messages,
            "response_format": {"type": "json_object"},
            "temperature": 0.2
        }

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                res = await client.post(endpoint, json=payload, headers=headers)
                if res.status_code == 200:
                    data = res.json()
                    content = data["choices"][0]["message"]["content"]
                    return json.loads(content)
                else:
                    return await LocalRuleBasedProvider(self.model_name).generate_decision(prompt, system_prompt)
        except Exception as e:
            logger.error(f"OpenAI-compatible request failed: {e}. Falling back to Rule-Based.")
            return await LocalRuleBasedProvider(self.model_name).generate_decision(prompt, system_prompt)


class AnthropicCompatibleProvider(BaseLLMProvider):
    """Anthropic Claude LLM provider with fallback."""

    def __init__(self, model_name: str = "claude-3-5-sonnet-20241022", api_key: Optional[str] = None, base_url: Optional[str] = None):
        super().__init__(model_name or "claude-3-5-sonnet-20241022", api_key, base_url or "https://api.anthropic.com/v1")

    async def test_connection(self) -> Dict[str, Any]:
        if not self.api_key:
            return {
                "status": "Connection Failed",
                "latency_ms": 0.0,
                "masked_key": "None",
                "error": "API Key is required for Anthropic.",
            }
        # Lightweight connection test with anthropic messages api (max_tokens=1)
        endpoint = f"{self.base_url.rstrip('/')}/messages"
        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }
        payload = {
            "model": self.model_name,
            "max_tokens": 1,
            "messages": [{"role": "user", "content": "ping"}]
        }
        start = time.perf_counter()
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                res = await client.post(endpoint, json=payload, headers=headers)
                latency = (time.perf_counter() - start) * 1000.0
                if res.status_code in [200, 201]:
                    return {
                        "status": "Connected",
                        "latency_ms": round(latency, 2),
                        "masked_key": mask_api_key(self.api_key),
                        "model": self.model_name,
                        "message": "Successfully authenticated with Anthropic API.",
                    }
                else:
                    return {
                        "status": "Connection Failed",
                        "latency_ms": round(latency, 2),
                        "masked_key": mask_api_key(self.api_key),
                        "error": f"Anthropic HTTP {res.status_code}: {res.text[:200]}",
                    }
        except Exception as e:
            latency = (time.perf_counter() - start) * 1000.0
            return {
                "status": "Connection Failed",
                "latency_ms": round(latency, 2),
                "masked_key": mask_api_key(self.api_key),
                "error": str(e),
            }

    async def generate_decision(self, prompt: str, system_prompt: Optional[str] = None) -> Dict[str, Any]:
        if not self.api_key:
            return await LocalRuleBasedProvider(self.model_name).generate_decision(prompt, system_prompt)

        endpoint = f"{self.base_url.rstrip('/')}/messages"
        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }
        payload = {
            "model": self.model_name,
            "max_tokens": 1000,
            "system": (system_prompt or "") + "\nRespond with valid JSON only.",
            "messages": [{"role": "user", "content": prompt}]
        }
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                res = await client.post(endpoint, json=payload, headers=headers)
                if res.status_code == 200:
                    data = res.json()
                    text = data["content"][0]["text"]
                    # Extract JSON substring if wrapped in markdown
                    json_str = re.sub(r"^```(?:json)?\s*|\s*```$", "", text.strip(), flags=re.MULTILINE)
                    return json.loads(json_str)
                else:
                    return await LocalRuleBasedProvider(self.model_name).generate_decision(prompt, system_prompt)
        except Exception as e:
            logger.error(f"Anthropic API call failed: {e}. Falling back to Rule-Based.")
            return await LocalRuleBasedProvider(self.model_name).generate_decision(prompt, system_prompt)


def get_llm_provider(
    provider_type: str,
    model_name: Optional[str] = None,
    api_key: Optional[str] = None,
    base_url: Optional[str] = None
) -> BaseLLMProvider:
    """Factory function returning the configured LLM provider instance."""
    p_lower = (provider_type or "").lower().strip()
    if "gemini" in p_lower:
        return GoogleGeminiProvider(model_name=model_name or "gemini-1.5-flash", api_key=api_key, base_url=base_url)
    elif "openai" in p_lower:
        return OpenAICompatibleProvider(model_name=model_name or "gpt-4o-mini", api_key=api_key, base_url=base_url)
    elif "anthropic" in p_lower or "claude" in p_lower:
        return AnthropicCompatibleProvider(model_name=model_name or "claude-3-5-sonnet-20241022", api_key=api_key, base_url=base_url)
    else:
        return LocalRuleBasedProvider(model_name=model_name or "rule-based-v1", api_key=api_key, base_url=base_url)
