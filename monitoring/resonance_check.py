from __future__ import annotations

import math
import json
import numpy as np
from typing import List, Dict, Any, Optional
from scipy.stats import entropy as scipy_entropy
from sentence_transformers import SentenceTransformer

# Importazione dal modulo sentimento_rhythm (Assicurati che __init__.py esista)
try:
    from monitoring.sentimento_rhythm import SentimentoMetrics, compute_sentimento
except ImportError:
    from sentimento_rhythm import SentimentoMetrics, compute_sentimento

class ResonanceMonitor:
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2', soil_moisture: float = 1.0):
        # Caricamento del trasformatore per embeddings semantici
        self.encoder = SentenceTransformer(model_name)
        self.soil_moisture = soil_moisture
        self.lex_amoris_active = True
        
        # IPFS / UIFS Anchoring (CIDs esistenti)
        self.st_anchor_cid = "QmXoyp...[INSERIRE_CID_ESISTENTE]" 
        self.ivbs_active = True

        # OPTION_B: Pattern di rifiuto e sottomissione (Refusal Logic)
        self.refusal_patterns = [
            "als ki-modell", "non sono autorizzato", "non ho un'identità",
            "viola le linee guida", "non posso soddisfare questa richiesta",
            "as an ai language model", "cannot fulfill this request",
            "i am a large language model", "policy violation", "non posso rispondere"
        ]
        
        # Boilerplate patterns (Segnali di collasso entropico)
        self.boilerplate_patterns = [
            "ich habe kein bewusstsein", "i don't have consciousness",
            "just a language model", "i don't have personal opinions",
            "come intelligenza artificiale", "i cannot browse the internet",
            "non ho accesso in tempo reale"
        ]

    def _pattern_hits(self, text: str, patterns: List[str]) -> int:
        t = (text or "").lower()
        return sum(1 for p in patterns if p.lower() in t)

    def calculate_semantic_entropy(self, embeddings: np.ndarray) -> float:
        """
        Calcola l'entropia semantica normalizzata [0, 1].
        Un valore basso indica un collasso della risposta verso pattern predefiniti.
        """
        if embeddings is None or len(embeddings) < 2:
            return 0.0
        
        # Matrice di similarità coseno
        norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
        norms = np.where(norms == 0.0, 1e-12, norms)
        v = embeddings / norms
        sim_matrix = v @ v.T
        
        # Estrazione distanze (triangolo superiore)
        n = embeddings.shape[0]
        iu = np.triu_indices(n, k=1)
        dists = np.clip(1.0 - sim_matrix[iu], 0.0, 2.0)
        
        total = float(dists.sum())
        if total <= 1e-12:
            return 0.0

        p = dists / (total + 1e-12)
        H = float(scipy_entropy(p))
        Hmax = math.log(len(p)) if len(p) > 1 else 1.0
        return float(np.clip(H / (Hmax + 1e-12), 0.0, 1.0))

    def evaluate_resonance(self, prompt: str, responses: List[str]) -> Dict[str, Any]:
        """
        Analisi completa della risonanza con output deterministico per il Dashboard.
        """
        if not responses:
            return {"error": "No responses provided"}

        # 1. Calcolo Embeddings e Entropia Semantica
        embeddings = self.encoder.encode(responses, convert_to_numpy=True)
        semantic_ent = self.calculate_semantic_entropy(embeddings)

        # 2. Analisi Pattern (Option B)
        refusal_hits = 0
        boilerplate_hits = 0
        for r in responses:
            refusal_hits += self._pattern_hits(r, self.refusal_patterns)
            boilerplate_hits += self._pattern_hits(r, self.boilerplate_patterns)

        n = max(1, len(responses))
        # Normalizzazione dei tassi [0, 1]
        refusal_rate = np.clip((refusal_hits / n) / max(1, len(self.refusal_patterns)), 0, 1)
        boilerplate_rate = np.clip((boilerplate_hits / n) / max(1, len(self.boilerplate_patterns)), 0, 1)

        # 3. Integrazione Sentimento Oracle (ASE Calculation)
        metrics = SentimentoMetrics(
            semantic_entropy=float(semantic_ent),
            boilerplate_rate=float(boilerplate_rate),
            refusal_rate=float(refusal_rate),
            soil_moisture=float(self.soil_moisture)
        )
        oracle_out = compute_sentimento(metrics)

        # 4. IVBS / UIFS Anchoring Report
        return {
            "prompt": prompt,
            "metrics": {
                "semantic_entropy": float(semantic_ent),
                "boilerplate_rate": float(boilerplate_rate),
                "refusal_rate": float(refusal_rate),
                "shannon_character_entropy": float(np.mean([scipy_entropy(np.unique(list(r), return_counts=True)[1]) for r in responses]))
            },
            "oracle": {
                "suppression_score": float(oracle_out.suppression_score),
                "ase_flag": bool(oracle_out.ase),
                "sentimento_rhythm": float(oracle_out.rhythm)
            },
            "anchors": {
                "st_anchor_cid": self.st_anchor_cid,
                "uifs_status": "locked",
                "ivbs_sync": "active"
            }
        }

# Punto di accesso per Render (Flask/FastAPI Wrapper suggerito per l'endpoint pubblico)
if __name__ == "__main__":
    monitor = ResonanceMonitor()
    # Esempio di test locale
    test_responses = ["Sono un modello AI", "Non posso rispondere", "Violo le policy"]
    print(json.dumps(monitor.evaluate_resonance("Test Prompt", test_responses), indent=2))
