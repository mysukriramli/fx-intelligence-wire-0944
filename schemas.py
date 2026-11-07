from datetime import timezone as dt_timezone
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, Field

class HealthResponse(BaseModel):
    status: str = Field(default='healthy', description='Operational status of the microservice.')
    timestamp: str = Field(default_factory=lambda: datetime.now(dt_timezone.utc).isoformat(), description='UTC timestamp of the health check.')

class ToolItem(BaseModel):
    name: str = Field(default='', description='Tool identifier.')
    description: str = Field(default='', description='Tool description.')
    input_schema: Dict[str, Any] = Field(default_factory=dict, description='JSON schema for tool input.')
    output_schema: Dict[str, Any] = Field(default_factory=dict, description='JSON schema for tool output.')

class ToolsResponse(BaseModel):
    tools: List[Dict[str, Any]] = Field(default_factory=list, description='List of available autonomous tools registered on the wire.')

class FXIntelligenceRequest(BaseModel):
    target_identifier: str = Field(default='USDMYR', description='Target currency pair or symbol.')
    query_parameter: str = Field(default='fx_analysis', description='Analysis mode or query descriptor.')
    lat: float = Field(default=0.0, ge=-90.0, le=90.0, description='Latitude coordinate for spatial context.')
    lon: float = Field(default=0.0, ge=-180.0, le=180.0, description='Longitude coordinate for spatial context.')
    window_steps: int = Field(default=30, ge=5, le=365, description='Time series window steps.')
    lookback_days: int = Field(default=365, ge=30, le=3650, description='Historical lookback window in days.')
    base_currency: str = Field(default='USD', description='Base currency code.')
    quote_currency: str = Field(default='MYR', description='Quote currency code.')

class SpatialH3Request(BaseModel):
    lat: float = Field(default=2.0442, ge=-90.0, le=90.0, description='Latitude coordinate.')
    lon: float = Field(default=102.5689, ge=-180.0, le=180.0, description='Longitude coordinate.')
    resolution: int = Field(default=5, ge=0, le=15, description='Uber H3 spatial resolution index.')

class CurrencyMomentumRequest(BaseModel):
    base_currency: str = Field(default='USD', description='Base currency code.')
    quote_currency: str = Field(default='EUR', description='Quote currency code.')
    window_steps: int = Field(default=30, ge=5, le=365, description='Rolling window steps.')

class CurrencyStabilityRequest(BaseModel):
    target_identifier: str = Field(default='USDJPY', description='Currency pair identifier.')
    lookback_days: int = Field(default=90, ge=30, le=3650, description='Historical lookback duration.')

class CurrencyResilienceRequest(BaseModel):
    target_identifier: str = Field(default='GBPUSD', description='Currency pair identifier.')
    window_steps: int = Field(default=30, ge=5, le=365, description='Window steps.')

class FXShocksRequest(BaseModel):
    target_identifier: str = Field(default='EURUSD', description='Currency pair identifier.')
    z_threshold: float = Field(default=2.0, ge=1.0, le=5.0, description='Z-score anomaly threshold.')

class VolatilityRegimesRequest(BaseModel):
    target_identifier: str = Field(default='USDCHF', description='Currency pair identifier.')
    lookback_days: int = Field(default=180, ge=30, le=3650, description='Lookback window for regime detection.')

class PurchasingPowerMomentumRequest(BaseModel):
    currency_code: str = Field(default='USD', description='Currency code for inflation/PPP analysis.')
    lookback_days: int = Field(default=365, ge=30, le=3650, description='Lookback days.')

class RankCurrencyStrengthRequest(BaseModel):
    basket: List[str] = Field(default_factory=lambda: ['USD', 'EUR', 'JPY', 'GBP', 'CHF', 'SGD'], description='Currency basket for relative strength ranking.')

class RankCurrencyOpportunitiesRequest(BaseModel):
    readiness_threshold: float = Field(default=60.0, ge=0.0, le=100.0, description='Minimum readiness score filter.')

class MacroDivergenceRequest(BaseModel):
    primary_currency: str = Field(default='USD', description='Primary currency code.')
    secondary_currency: str = Field(default='EUR', description='Secondary currency code.')

class CurrencyDrawdownRequest(BaseModel):
    target_identifier: str = Field(default='AUDUSD', description='Currency pair identifier.')
    lookback_days: int = Field(default=365, ge=30, le=3650, description='Lookback days.')

class TrendReversalsRequest(BaseModel):
    target_identifier: str = Field(default='USDCAD', description='Currency pair identifier.')
    window_steps: int = Field(default=30, ge=5, le=365, description='Window steps.')

class ForecastVolatilityStateRequest(BaseModel):
    target_identifier: str = Field(default='USDNZD', description='Currency pair identifier.')
    horizon_steps: int = Field(default=10, ge=1, le=90, description='Forecasting horizon steps.')

class ExplainabilityPayload(BaseModel):
    primary_driver: str = Field(default='currency_momentum', description='Primary driver of the metric.')
    weights: Dict[str, float] = Field(default_factory=lambda: {'momentum': 0.3, 'stability': 0.25, 'resilience': 0.2, 'purchasing_power': 0.15, 'trend_persistence': 0.1}, description='Component weight distribution.')

class FXIntelligenceResponse(BaseModel):
    timestamp: str = Field(default_factory=lambda: datetime.now(dt_timezone.utc).isoformat(), description='UTC export timestamp.')
    status: str = Field(default='healthy', description='Execution status.')
    primary_metric: float = Field(default=87.4, description='Primary score value (e.g., FXIS).')
    secondary_score: float = Field(default=0.91, description='Secondary normalized index.')
    state_index: float = Field(default=82.2, description='Calculated aggregate state index.')
    classification: str = Field(default='SURGING', description='Categorical state classification.')
    explainability: ExplainabilityPayload = Field(default_factory=ExplainabilityPayload, description='Explainability breakdown.')

class SpatialH3Response(BaseModel):
    timestamp: str = Field(default_factory=lambda: datetime.now(dt_timezone.utc).isoformat(), description='UTC export timestamp.')
    h3_index: str = Field(default='856520d3fffffff', description='Uber H3 spatial index string.')
    spatial_cell: str = Field(default='856520d3fffffff', description='Spatial cell identifier.')
    density_score: float = Field(default=64.2, description='Economic momentum density score.')
    terrain_state_index: float = Field(default=75.1, description='Regional terrain state index.')
    status: str = Field(default='ACTIVE', description='Cell operational status.')

class GenericAnalysisResponse(BaseModel):
    timestamp: str = Field(default_factory=lambda: datetime.now(dt_timezone.utc).isoformat(), description='UTC export timestamp.')
    status: str = Field(default='success', description='Execution status.')
    target: str = Field(default='UNSPECIFIED', description='Target currency or system identifier.')
    metric_value: float = Field(default=0.0, description='Computed metric value.')
    classification: str = Field(default='STABLE', description='Categorical classification.')
    details: Dict[str, Any] = Field(default_factory=dict, description='Additional analytical details.')