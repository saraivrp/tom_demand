"""Reference data endpoints for CSV-backed entities."""

import os
import re
import shutil
from typing import Optional
from uuid import uuid4

from fastapi import APIRouter, Depends, File, UploadFile

from ..auth import require_role
from ..errors import AppError
from ..models.reference_data import (
    DeleteRowRequest,
    OverwriteRowsRequest,
    RenameRequestingAreaRequest,
    RenameResponse,
    RenameRevenueStreamRequest,
    RevenueStreamsQuery,
    RowMutationResponse,
    RowsQueryResponse,
    RequestingAreasQuery,
    UploadResponse,
    UpsertRowRequest,
    ValuesResponse,
)
from ...services import ReferenceDataService

router = APIRouter(prefix="/api/v1/reference-data", tags=["reference-data"])


def _service(config_path: Optional[str]) -> ReferenceDataService:
    return ReferenceDataService(config_path)


def _read_rows(path: str, limit: Optional[int], offset: int, config_path: Optional[str]) -> RowsQueryResponse:
    result = _service(config_path).read_rows(path, limit=limit, offset=offset)
    return RowsQueryResponse(**result)


@router.post("/upload-ideas", response_model=UploadResponse)
def upload_ideas_file(
    file: UploadFile = File(...),
    _: None = Depends(require_role("viewer")),
) -> UploadResponse:
    filename = os.path.basename(file.filename or "").strip()
    if not filename:
        raise AppError("Missing filename.", status_code=400)
    if not filename.lower().endswith(".csv"):
        raise AppError("Only CSV files are supported.", status_code=400)

    safe_filename = re.sub(r"[^A-Za-z0-9._-]", "_", filename)
    upload_dir = os.getenv("UPLOAD_DIR", "/tmp/tom_demand_uploads")
    os.makedirs(upload_dir, exist_ok=True)
    stored_filename = f"{uuid4().hex}_{safe_filename}"
    stored_path = os.path.join(upload_dir, stored_filename)

    with open(stored_path, "wb") as target:
        shutil.copyfileobj(file.file, target)

    return UploadResponse(
        path=stored_path,
        filename=safe_filename,
        size=os.path.getsize(stored_path),
    )


@router.get("/ideas", response_model=RowsQueryResponse)
def get_ideas(
    path: str,
    limit: Optional[int] = 200,
    offset: int = 0,
    config_path: Optional[str] = None,
    _: None = Depends(require_role("viewer")),
):
    try:
        return _read_rows(path, limit, offset, config_path)
    except (FileNotFoundError, ValueError) as exc:
        raise AppError(str(exc), status_code=400) from exc


@router.get("/ra-weights", response_model=RowsQueryResponse)
def get_ra_weights(
    path: str,
    limit: Optional[int] = 200,
    offset: int = 0,
    config_path: Optional[str] = None,
    _: None = Depends(require_role("viewer")),
):
    try:
        return _read_rows(path, limit, offset, config_path)
    except (FileNotFoundError, ValueError) as exc:
        raise AppError(str(exc), status_code=400) from exc


@router.get("/rs-weights", response_model=RowsQueryResponse)
def get_rs_weights(
    path: str,
    limit: Optional[int] = 200,
    offset: int = 0,
    config_path: Optional[str] = None,
    _: None = Depends(require_role("viewer")),
):
    try:
        return _read_rows(path, limit, offset, config_path)
    except (FileNotFoundError, ValueError) as exc:
        raise AppError(str(exc), status_code=400) from exc


@router.post("/overwrite", response_model=RowMutationResponse)
def overwrite_rows(
    payload: OverwriteRowsRequest, _: None = Depends(require_role("editor"))
) -> RowMutationResponse:
    try:
        result = _service(payload.config_path).overwrite_rows(payload.path, payload.rows)
        return RowMutationResponse(path=result["path"], count=result["count"])
    except (FileNotFoundError, ValueError) as exc:
        raise AppError(str(exc), status_code=400) from exc


@router.post("/upsert", response_model=RowMutationResponse)
def upsert_row(
    payload: UpsertRowRequest, _: None = Depends(require_role("editor"))
) -> RowMutationResponse:
    try:
        result = _service(payload.config_path).upsert_row(payload.path, payload.key_column, payload.row)
        return RowMutationResponse(path=result["path"], action=result["action"], key=result["key"])
    except (FileNotFoundError, ValueError) as exc:
        raise AppError(str(exc), status_code=400) from exc


@router.post("/delete", response_model=RowMutationResponse)
def delete_row(
    payload: DeleteRowRequest, _: None = Depends(require_role("editor"))
) -> RowMutationResponse:
    try:
        result = _service(payload.config_path).delete_row(
            payload.path, payload.key_column, payload.key_value
        )
        return RowMutationResponse(
            path=result["path"], deleted=result["deleted"], key=result["key"]
        )
    except (FileNotFoundError, ValueError) as exc:
        raise AppError(str(exc), status_code=400) from exc


@router.post("/requesting-areas/list", response_model=ValuesResponse)
def list_requesting_areas(
    payload: RequestingAreasQuery, _: None = Depends(require_role("viewer"))
) -> ValuesResponse:
    try:
        result = _service(payload.config_path).list_requesting_areas(
            ideas_path=payload.ideas_path,
            ra_weights_path=payload.ra_weights_path,
        )
        return ValuesResponse(**result)
    except (FileNotFoundError, ValueError) as exc:
        raise AppError(str(exc), status_code=400) from exc


@router.post("/requesting-areas/rename", response_model=RenameResponse)
def rename_requesting_area(
    payload: RenameRequestingAreaRequest, _: None = Depends(require_role("editor"))
) -> RenameResponse:
    try:
        result = _service(payload.config_path).rename_value(
            files=[
                {"path": payload.ideas_path, "column": "RequestingArea"},
                {"path": payload.ra_weights_path, "column": "RequestingArea"},
            ],
            column="RequestingArea",
            old_value=payload.old_value,
            new_value=payload.new_value,
        )
        return RenameResponse(**result)
    except (FileNotFoundError, ValueError) as exc:
        raise AppError(str(exc), status_code=400) from exc


@router.post("/revenue-streams/list", response_model=ValuesResponse)
def list_revenue_streams(
    payload: RevenueStreamsQuery, _: None = Depends(require_role("viewer"))
) -> ValuesResponse:
    try:
        result = _service(payload.config_path).list_revenue_streams(
            ideas_path=payload.ideas_path,
            rs_weights_path=payload.rs_weights_path,
            ra_weights_path=payload.ra_weights_path,
        )
        return ValuesResponse(**result)
    except (FileNotFoundError, ValueError) as exc:
        raise AppError(str(exc), status_code=400) from exc


@router.post("/revenue-streams/rename", response_model=RenameResponse)
def rename_revenue_stream(
    payload: RenameRevenueStreamRequest, _: None = Depends(require_role("editor"))
) -> RenameResponse:
    try:
        result = _service(payload.config_path).rename_value(
            files=[
                {"path": payload.ideas_path, "column": "RevenueStream"},
                {"path": payload.ra_weights_path, "column": "RevenueStream"},
                {"path": payload.rs_weights_path, "column": "RevenueStream"},
            ],
            column="RevenueStream",
            old_value=payload.old_value,
            new_value=payload.new_value,
        )
        return RenameResponse(**result)
    except (FileNotFoundError, ValueError) as exc:
        raise AppError(str(exc), status_code=400) from exc
