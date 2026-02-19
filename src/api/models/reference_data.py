"""Reference data API models."""

from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class RowsQueryResponse(BaseModel):
    path: str
    total: int
    rows: List[Dict]


class OverwriteRowsRequest(BaseModel):
    path: str
    rows: List[Dict]
    config_path: Optional[str] = None


class UpsertRowRequest(BaseModel):
    path: str
    key_column: str
    row: Dict
    config_path: Optional[str] = None


class DeleteRowRequest(BaseModel):
    path: str
    key_column: str
    key_value: str
    config_path: Optional[str] = None


class RowMutationResponse(BaseModel):
    path: str
    action: Optional[str] = None
    key: Optional[str] = None
    deleted: Optional[int] = None
    count: Optional[int] = None


class ValuesResponse(BaseModel):
    count: int
    values: List[str]


class RequestingAreasQuery(BaseModel):
    ideas_path: str
    ra_weights_path: Optional[str] = None
    config_path: Optional[str] = None


class RevenueStreamsQuery(BaseModel):
    ideas_path: str
    rs_weights_path: Optional[str] = None
    ra_weights_path: Optional[str] = None
    config_path: Optional[str] = None


class RenameRequest(BaseModel):
    old_value: str = Field(min_length=1)
    new_value: str = Field(min_length=1)
    config_path: Optional[str] = None


class RenameRequestingAreaRequest(RenameRequest):
    ideas_path: str
    ra_weights_path: str


class RenameRevenueStreamRequest(RenameRequest):
    ideas_path: str
    ra_weights_path: str
    rs_weights_path: str


class RenameResponse(BaseModel):
    updated_files: List[str]
    replaced: int


class UploadResponse(BaseModel):
    path: str
    filename: str
    size: int
