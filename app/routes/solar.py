from fastapi import APIRouter, HTTPException, Query
from app.services.nasa import get_solar_flares, get_geomagnetic_storms, get_cme
from typing import Optional
import random
from datetime import datetime

router = APIRouter(prefix="/solar", tags=["Solar"])


@router.get("/flares")
def solar_flares(
    start_date: Optional[str] = Query(None, description="Formato: YYYY-MM-DD"),
    end_date: Optional[str] = Query(None, description="Formato: YYYY-MM-DD"),
):
    """Retorna Solar Flares recentes da NASA."""
    try:
        data = get_solar_flares(start_date, end_date)
        return {"source": "NASA DONKI", "count": len(data), "data": data}
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Erro ao buscar dados da NASA: {str(e)}")


@router.get("/storms")
def geomagnetic_storms(
    start_date: Optional[str] = Query(None, description="Formato: YYYY-MM-DD"),
    end_date: Optional[str] = Query(None, description="Formato: YYYY-MM-DD"),
):
    """Retorna Geomagnetic Storms recentes da NASA."""
    try:
        data = get_geomagnetic_storms(start_date, end_date)
        return {"source": "NASA DONKI", "count": len(data), "data": data}
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Erro ao buscar dados da NASA: {str(e)}")


@router.get("/cme")
def coronal_mass_ejections(
    start_date: Optional[str] = Query(None, description="Formato: YYYY-MM-DD"),
    end_date: Optional[str] = Query(None, description="Formato: YYYY-MM-DD"),
):
    """Retorna Coronal Mass Ejections recentes da NASA."""
    try:
        data = get_cme(start_date, end_date)
        return {"source": "NASA DONKI", "count": len(data), "data": data}
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Erro ao buscar dados da NASA: {str(e)}")


@router.get("/risk")
def current_risk():
    """
    Retorna classificação de risco atual.
    TODO: substituir mock pelo modelo real do Integrante 1.
    """
    levels = ["LOW", "MEDIUM", "HIGH", "CRITICAL"]
    mock_level = random.choice(levels)
    return {
        "timestamp": datetime.utcnow().isoformat(),
        "risk_level": mock_level,
        "kp_index": round(random.uniform(0, 9), 1),
        "bz_component": round(random.uniform(-20, 5), 2),
        "solar_wind_speed": round(random.uniform(300, 800), 1),
        "source": "MOCK - aguardando modelo IA (Integrante 1)",
    }


@router.post("/predict")
def predict(data: dict):
    """
    Endpoint de predição de tempestade solar.
    TODO: integrar com modelo do Integrante 1.
    Recebe parâmetros do sol e retorna previsão para 24h, 48h e 72h.
    """
    mock_response = {
        "timestamp": datetime.utcnow().isoformat(),
        "input_received": data,
        "predictions": {
            "24h": {"storm_probability": round(random.uniform(0, 1), 2), "expected_class": "M"},
            "48h": {"storm_probability": round(random.uniform(0, 1), 2), "expected_class": "C"},
            "72h": {"storm_probability": round(random.uniform(0, 1), 2), "expected_class": "B"},
        },
        "source": "MOCK - aguardando modelo IA (Integrante 1)",
    }
    return mock_response
