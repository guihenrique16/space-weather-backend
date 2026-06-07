from fastapi import APIRouter, HTTPException, Query
from app.services.supabase_client import supabase
from typing import Optional

router = APIRouter(prefix="/events", tags=["Events"])

FAMOUS_EVENTS = [
    {
        "name": "Carrington Event",
        "date": "1859-09-01",
        "class": "X",
        "kp_index": 9.0,
        "description": "O maior evento solar registrado. Derrubou sistemas de telégrafo no mundo todo.",
        "impact": ["telecomunicações", "energia elétrica"],
    },
    {
        "name": "Quebec Blackout",
        "date": "1989-03-13",
        "class": "X",
        "kp_index": 9.0,
        "description": "Tempestade geomagnética que deixou Quebec sem energia por 9 horas.",
        "impact": ["energia elétrica"],
    },
    {
        "name": "Halloween Storms",
        "date": "2003-10-28",
        "class": "X",
        "kp_index": 9.0,
        "description": "Série de tempestades que danificou satélites e causou blackouts na Suécia.",
        "impact": ["satélites", "energia elétrica", "GPS"],
    },
    {
        "name": "Starlink Loss",
        "date": "2022-02-03",
        "class": "M",
        "kp_index": 5.0,
        "description": "Tempestade geomagnética destruiu 40 satélites Starlink recém-lançados.",
        "impact": ["satélites", "telecomunicações"],
    },
]


@router.get("/famous")
def famous_events():
    """Retorna eventos solares históricos famosos (hardcoded)."""
    return {"count": len(FAMOUS_EVENTS), "events": FAMOUS_EVENTS}


# --- eventos_solares ---

@router.get("/historico")
def get_historico(limit: int = Query(50, le=200)):
    """Retorna eventos solares históricos salvos no banco."""
    try:
        res = supabase.table("eventos_solares").select("*").order("data", desc=True).limit(limit).execute()
        return {"count": len(res.data), "events": res.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/historico")
def save_evento(evento: dict):
    """Salva um novo evento solar. Campos: data, classe, intensidade, fonte."""
    try:
        res = supabase.table("eventos_solares").insert(evento).execute()
        return {"message": "Evento salvo", "data": res.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# --- previsoes ---

@router.get("/previsoes")
def get_previsoes(limit: int = Query(20, le=100)):
    """Retorna as últimas previsões geradas pela IA."""
    try:
        res = supabase.table("previsoes").select("*").order("timestamp_geracao", desc=True).limit(limit).execute()
        return {"count": len(res.data), "previsoes": res.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/previsoes/ultima")
def get_ultima_previsao():
    """Retorna a previsão mais recente gerada pela IA."""
    try:
        res = supabase.table("previsoes").select("*").order("timestamp_geracao", desc=True).limit(1).execute()
        if not res.data:
            raise HTTPException(status_code=404, detail="Nenhuma previsão encontrada")
        return res.data[0]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/previsoes")
def save_previsao(previsao: dict):
    """Salva uma previsão gerada pela IA. Campos: status, probabilidade, dados_completos_json."""
    try:
        res = supabase.table("previsoes").insert(previsao).execute()
        return {"message": "Previsão salva", "data": res.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# --- setores_afetados ---

@router.get("/setores/{previsao_id}")
def get_setores(previsao_id: str):
    """Retorna setores afetados de uma previsão específica."""
    try:
        res = supabase.table("setores_afetados").select("*").eq("previsao_id", previsao_id).execute()
        return {"count": len(res.data), "setores": res.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# --- alertas_espaciais ---

@router.get("/alertas/{previsao_id}")
def get_alertas(previsao_id: str):
    """Retorna alertas de missões espaciais de uma previsão específica."""
    try:
        res = supabase.table("alertas_espaciais").select("*").eq("previsao_id", previsao_id).execute()
        return {"count": len(res.data), "alertas": res.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# --- regioes_impacto ---

@router.get("/regioes/{previsao_id}")
def get_regioes(previsao_id: str):
    """Retorna regiões geográficas impactadas de uma previsão específica."""
    try:
        res = supabase.table("regioes_impacto").select("*").eq("previsao_id", previsao_id).execute()
        return {"count": len(res.data), "regioes": res.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
