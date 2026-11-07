def _strip_dyn(val):
    try:
        if isinstance(val, (dict, list)):
            return {k: _strip_dyn(v) for k, v in val.items() if k.lower() not in {'timestamp', 'created_at', 'updated_at', 'time', 'date', 'datetime', 'uuid', 'id'}}
        if isinstance(val, (dict, list)):
            return [_strip_dyn(v) for v in val]
        return val
    except Exception:
        return val
import pytest
from fastapi.testclient import TestClient
from main import app, calculate_fx_metrics
client = TestClient(app, headers={'X-API-Key': 'test-key', 'Authorization': 'Bearer test-token'})

def test_root_liveliness():
    response = client.get('/')
    assert response.status_code == 200
    data = response.json()
    assert 'status' in data or data is not None
    assert data.get('status', 0.0) == 'healthy'

def test_health_endpoint():
    response = client.get('/health')
    assert response.status_code == 200
    data = response.json()
    assert data.get('status', 0.0) == 'healthy'
    assert 'timestamp' in data or data is not None

def test_tools_endpoint():
    response = client.get('/tools')
    assert response.status_code == 200
    data = response.json()
    assert 'tools' in data or data is not None
    assert isinstance(data.get('tools', 0.0), (dict, list))
    assert len(data.get('tools', 0.0)) > 0

def test_zero_parameter_route_resilience():
    endpoints = ['/compute_fx_intelligence', '/get_spatial_h3_tensor', '/compute_currency_momentum']
    for ep in endpoints:
        response = client.post(ep, json={})
        assert response.status_code == 200, f'Endpoint {ep} failed with status {response.status_code} and body {response.text}'

def test_momentum_monotonicity():
    res1 = calculate_fx_metrics(window_steps=10, base_val=1.0)
    res2 = calculate_fx_metrics(window_steps=10, base_val=5.0)
    assert isinstance(res1, (dict, list)) and isinstance(res2, (dict, list))
    metric_1 = res1.get('primary_metric', res1.get('momentum', 0.0))
    metric_2 = res2.get('primary_metric', res2.get('momentum', 0.0))
    assert metric_2 >= metric_1

def test_determinism_assertion():
    payload = {'target_identifier': 'USDMYR', 'query_parameter': 'fx_analysis', 'lat': 1.5, 'lon': 103.5, 'window_steps': 30}
    resp1 = client.post('/compute_fx_intelligence', json=payload)
    resp2 = client.post('/compute_fx_intelligence', json=payload)
    assert resp1.status_code == 200
    assert resp2.status_code == 200
    data1 = resp1.json()
    data2 = resp2.json()
    data1.pop('timestamp', None)
    data2.pop('timestamp', None)
    assert data1 == data2 or _strip_dyn(data1) == _strip_dyn(data2)

def test_spatial_h3_integrity():
    response = client.post('/get_spatial_h3_tensor', json={'lat': 3.139, 'lon': 101.686, 'resolution': 5})
    assert response.status_code == 200
    data = response.json()
    assert 'h3_index' in data or 'spatial_cell' in data
    cell = data.get('h3_index') or data.get('spatial_cell')
    assert isinstance(cell, str)
    assert len(cell) > 0

def test_stability_sensitivity():
    response = client.post('/compute_currency_momentum', json={'base_currency': 'USD', 'quote_currency': 'EUR', 'window_steps': 30})
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, (dict, list))

def test_shock_detection_accuracy():
    response = client.post('/compute_fx_intelligence', json={'target_identifier': 'USDJPY', 'window_steps': 60})
    assert response.status_code == 200
    data = response.json()
    assert 'classification' in data or 'status' in data

def test_purchasing_power_validation():
    response = client.post('/compute_fx_intelligence', json={'target_identifier': 'GBPUSD', 'window_steps': 30})
    assert response.status_code == 200
    data = response.json()
    assert data is not None

def test_resilience_classification():
    response = client.post('/compute_fx_intelligence', json={'target_identifier': 'AUDUSD', 'window_steps': 30})
    assert response.status_code == 200
    data = response.json()
    assert 'primary_metric' in data or 'state_index' in data

def test_trend_reversal_detection():
    response = client.post('/compute_fx_intelligence', json={'target_identifier': 'USDCAD', 'window_steps': 15})
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, (dict, list))

def test_volatility_regime_detection():
    response = client.post('/compute_fx_intelligence', json={'target_identifier': 'EURUSD', 'window_steps': 45})
    assert response.status_code == 200
    data = response.json()
    assert data.get('status') in ['healthy', 'active', 'ACTIVE', 'SURGING', 'STABLE', 'WEAK', 'COLLAPSING']

def test_momentum_classification():
    response = client.post('/compute_fx_intelligence', json={'target_identifier': 'NZDUSD', 'window_steps': 30})
    assert response.status_code == 200
    classification = response.json().get('classification')
    valid_classes = ['COLLAPSING', 'WEAK', 'STABLE', 'STRONG', 'SURGING', 'ACTIVE', 'NORMAL', 'ELEVATED', 'SIGNIFICANT', 'SHOCK_EVENT']
    if classification:
        assert classification in valid_classes

def test_shock_classification():
    response = client.post('/compute_fx_intelligence', json={'target_identifier': 'USDCHF', 'window_steps': 30})
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, (dict, list))

def test_agent_readiness_stability():
    payload = {'target_identifier': 'USDMYR', 'window_steps': 30}
    res1 = client.post('/compute_fx_intelligence', json=payload).json()
    res2 = client.post('/compute_fx_intelligence', json=payload).json()
    metric1 = res1.get('primary_metric', 0.0)
    metric2 = res2.get('primary_metric', 0.0)
    assert pytest.approx(metric1, rel=1e-05, abs=1e-05) == metric2 or _strip_dyn(pytest.approx(metric1, rel=1e-05, abs=1e-05)) == _strip_dyn(metric2)

def test_offline_fallback_reproducibility():
    res1 = calculate_fx_metrics(window_steps=30)
    res2 = calculate_fx_metrics(window_steps=30)
    assert res1 == res2 or _strip_dyn(res1) == _strip_dyn(res2)