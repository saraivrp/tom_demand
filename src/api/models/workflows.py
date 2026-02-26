"""Workflow request and response models."""

from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class ValidateRequest(BaseModel):
    ideas_path: str
    ra_weights_path: str
    rs_weights_path: str
    bg_rs_weights_path: str
    config_path: Optional[str] = None


class ValidateResponse(BaseModel):
    ideas_count: int
    requesting_areas_count: int
    revenue_streams_count: int
    average_size: float


class PrioritizeRequest(BaseModel):
    ideas_path: str
    ra_weights_path: str
    rs_weights_path: str
    bg_rs_weights_path: str
    output_dir: str = "./data/output"
    method: str = "sainte-lague"
    all_methods: bool = False
    now_method: Optional[str] = None
    next_method: Optional[str] = None
    later_method: Optional[str] = None
    config_path: Optional[str] = None


class PrioritizeResponse(BaseModel):
    elapsed_time: float
    ideas_count: int
    requesting_areas_count: int
    revenue_streams_count: int
    queue_counts: Dict[str, int] = Field(default_factory=dict)
    methods_executed: List[str]
    output_directory: str
    queue_methods: Dict[str, str] = Field(default_factory=dict)
    default_method: str
    all_methods: bool


class PrioritizeRsRequest(BaseModel):
    ideas_path: str
    ra_weights_path: str
    output_path: str
    method: str = "sainte-lague"
    config_path: Optional[str] = None


class PrioritizeGlobalRequest(BaseModel):
    rs_prioritized_path: str
    rs_weights_path: str
    output_path: str
    method: str = "sainte-lague"
    config_path: Optional[str] = None


class CompareRequest(BaseModel):
    ideas_path: str
    ra_weights_path: str
    rs_weights_path: str
    bg_rs_weights_path: str
    output_path: str
    top_n: Optional[int] = None
    config_path: Optional[str] = None


class FileWorkflowResponse(BaseModel):
    output: str
    count: int
