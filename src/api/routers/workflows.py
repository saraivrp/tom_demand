"""Workflow execution endpoints."""

from typing import Optional

from fastapi import APIRouter, Depends

from ...loader import DataLoadError
from ...services import DemandService
from ..auth import require_role
from ..errors import AppError
from ..models.workflows import (
    CompareRequest,
    FileWorkflowResponse,
    PrioritizeGlobalRequest,
    PrioritizeRequest,
    PrioritizeResponse,
    PrioritizeRsRequest,
    ValidateRequest,
    ValidateResponse,
)

router = APIRouter(prefix="/api/v1/workflows", tags=["workflows"])


def _service(config_path: Optional[str]) -> DemandService:
    return DemandService(config_path)


@router.post("/validate", response_model=ValidateResponse)
def validate_workflow(
    payload: ValidateRequest, _: None = Depends(require_role("viewer"))
) -> ValidateResponse:
    try:
        result = _service(payload.config_path).validate(
            ideas=payload.ideas_path,
            ra_weights=payload.ra_weights_path,
            rs_weights=payload.rs_weights_path,
        )
        return ValidateResponse(**result)
    except (FileNotFoundError, DataLoadError) as exc:
        raise AppError(str(exc), status_code=400) from exc


@router.post("/prioritize", response_model=PrioritizeResponse)
def prioritize_workflow(
    payload: PrioritizeRequest, _: None = Depends(require_role("executor"))
) -> PrioritizeResponse:
    if payload.all_methods and any([payload.now_method, payload.next_method, payload.later_method]):
        raise AppError(
            "Per-queue methods cannot be used with all_methods=true.",
            status_code=400,
        )

    try:
        result = _service(payload.config_path).prioritize(
            ideas=payload.ideas_path,
            ra_weights=payload.ra_weights_path,
            rs_weights=payload.rs_weights_path,
            output_dir=payload.output_dir,
            method=payload.method,
            all_methods=payload.all_methods,
            now_method=payload.now_method,
            next_method=payload.next_method,
            later_method=payload.later_method,
        )
        return PrioritizeResponse(**result)
    except (FileNotFoundError, DataLoadError) as exc:
        raise AppError(str(exc), status_code=400) from exc


@router.post("/prioritize-rs", response_model=FileWorkflowResponse)
def prioritize_rs_workflow(
    payload: PrioritizeRsRequest, _: None = Depends(require_role("executor"))
) -> FileWorkflowResponse:
    try:
        result = _service(payload.config_path).prioritize_rs(
            ideas=payload.ideas_path,
            ra_weights=payload.ra_weights_path,
            output=payload.output_path,
            method=payload.method,
        )
        return FileWorkflowResponse(**result)
    except (FileNotFoundError, DataLoadError) as exc:
        raise AppError(str(exc), status_code=400) from exc


@router.post("/prioritize-global", response_model=FileWorkflowResponse)
def prioritize_global_workflow(
    payload: PrioritizeGlobalRequest, _: None = Depends(require_role("executor"))
) -> FileWorkflowResponse:
    try:
        result = _service(payload.config_path).prioritize_global(
            rs_prioritized=payload.rs_prioritized_path,
            rs_weights=payload.rs_weights_path,
            output=payload.output_path,
            method=payload.method,
        )
        return FileWorkflowResponse(**result)
    except (FileNotFoundError, DataLoadError) as exc:
        raise AppError(str(exc), status_code=400) from exc


@router.post("/compare", response_model=FileWorkflowResponse)
def compare_workflow(
    payload: CompareRequest, _: None = Depends(require_role("executor"))
) -> FileWorkflowResponse:
    try:
        result = _service(payload.config_path).compare(
            ideas=payload.ideas_path,
            ra_weights=payload.ra_weights_path,
            rs_weights=payload.rs_weights_path,
            output=payload.output_path,
            top_n=payload.top_n,
        )
        return FileWorkflowResponse(output=result["output"], count=result["count"])
    except (FileNotFoundError, DataLoadError) as exc:
        raise AppError(str(exc), status_code=400) from exc
