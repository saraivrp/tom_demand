"""Async job endpoints for workflow execution."""

from fastapi import APIRouter, BackgroundTasks, Depends

from ...services import DemandService
from ..auth import require_role
from ..errors import AppError
from ..jobs import job_manager
from ..models.jobs import JobListResponse, JobStatusResponse, JobSubmitResponse
from ..models.workflows import CompareRequest, PrioritizeRequest, ValidateRequest

router = APIRouter(prefix="/api/v1/jobs", tags=["jobs"])


def _as_dict(model):
    if hasattr(model, "model_dump"):
        return model.model_dump()
    return model.dict()


def _submit(job_type: str, payload, background_tasks: BackgroundTasks, worker):
    job = job_manager.create_job(job_type, _as_dict(payload))
    background_tasks.add_task(job_manager.execute, job["job_id"], worker)
    return JobSubmitResponse(
        job_id=job["job_id"],
        job_type=job["job_type"],
        status=job["status"],
        created_at=job["created_at"],
    )


@router.post("/workflows/prioritize", response_model=JobSubmitResponse)
def submit_prioritize_job(
    payload: PrioritizeRequest,
    background_tasks: BackgroundTasks,
    _: None = Depends(require_role("executor")),
):
    if payload.all_methods and any([payload.now_method, payload.next_method, payload.later_method]):
        raise AppError(
            "Per-queue methods cannot be used with all_methods=true.",
            status_code=400,
        )

    def worker():
        service = DemandService(payload.config_path)
        return service.prioritize(
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

    return _submit("prioritize", payload, background_tasks, worker)


@router.post("/workflows/compare", response_model=JobSubmitResponse)
def submit_compare_job(
    payload: CompareRequest,
    background_tasks: BackgroundTasks,
    _: None = Depends(require_role("executor")),
):
    def worker():
        service = DemandService(payload.config_path)
        return service.compare(
            ideas=payload.ideas_path,
            ra_weights=payload.ra_weights_path,
            rs_weights=payload.rs_weights_path,
            output=payload.output_path,
            top_n=payload.top_n,
        )

    return _submit("compare", payload, background_tasks, worker)


@router.post("/workflows/validate", response_model=JobSubmitResponse)
def submit_validate_job(
    payload: ValidateRequest,
    background_tasks: BackgroundTasks,
    _: None = Depends(require_role("viewer")),
):
    def worker():
        service = DemandService(payload.config_path)
        return service.validate(
            ideas=payload.ideas_path,
            ra_weights=payload.ra_weights_path,
            rs_weights=payload.rs_weights_path,
        )

    return _submit("validate", payload, background_tasks, worker)


@router.get("", response_model=JobListResponse)
def list_jobs(limit: int = 50, _: None = Depends(require_role("viewer"))):
    result = job_manager.list(limit=limit)
    jobs = [JobStatusResponse(**job) for job in result["jobs"]]
    return JobListResponse(count=result["count"], jobs=jobs)


@router.get("/{job_id}", response_model=JobStatusResponse)
def get_job(job_id: str, _: None = Depends(require_role("viewer"))):
    job = job_manager.get(job_id)
    if not job:
        raise AppError(f"Job '{job_id}' not found.", status_code=404)
    return JobStatusResponse(**job)
