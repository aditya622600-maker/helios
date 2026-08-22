from fastapi import APIRouter, HTTPException, status

from helios.contracts.models import AnalysisRequest, AnalysisRun, RerankRequest
from helios.pipeline.service import AnalysisService

router = APIRouter(prefix="/analysis-runs", tags=["analysis"])
service = AnalysisService()


@router.post("", response_model=AnalysisRun, status_code=status.HTTP_201_CREATED)
def create_analysis_run(request: AnalysisRequest) -> AnalysisRun:
    try:
        return service.create(request)
    except ValueError as err:
        raise HTTPException(status_code=400, detail=str(err)) from err


@router.get("/{run_id}", response_model=AnalysisRun)
def get_analysis_run(run_id: str) -> AnalysisRun:
    run = service.get(run_id)
    if run is None:
        raise HTTPException(status_code=404, detail="Analysis run not found")
    return run


@router.post("/{run_id}/rerank", response_model=AnalysisRun)
def rerank_analysis(run_id: str, request: RerankRequest) -> AnalysisRun:
    run = service.rerank(run_id, request)
    if run is None:
        raise HTTPException(status_code=404, detail="Analysis run not found")
    return run


@router.get("/{run_id}/candidates.geojson")
def candidate_geojson(run_id: str) -> dict:
    feature_collection = service.as_geojson(run_id)
    if feature_collection is None:
        raise HTTPException(status_code=404, detail="Analysis run not found")
    return feature_collection
