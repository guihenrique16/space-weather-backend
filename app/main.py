from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import solar, events

app = FastAPI(
    title="Space Weather Guardian API",
    description="API para monitoramento e previsão de tempestades solares. Protegendo infraestrutura crítica na Terra e no Espaço.",
    version="0.1.0",
)

# CORS liberado para o frontend do time
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: restringir ao domínio do frontend em produção
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rotas
app.include_router(solar.router)
app.include_router(events.router)


@app.get("/", tags=["Health"])
def root():
    return {
        "project": "Space Weather Guardian",
        "status": "online",
        "docs": "/docs",
        "version": "0.1.0",
    }


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok"}
