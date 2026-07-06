from app.aggregator import HealthAggregator
from app.models import ComponentHealth



def _component(component_id: str, status: str) -> ComponentHealth:
    return ComponentHealth(id=component_id, name=f"name-{component_id}", endpoint=f"http://{component_id}.local", status=status, response_time_ms=10)



def test_all_healthy_components_produce_overall_healthy() -> None:
    results = [_component("a", "healthy"), _component("b", "healthy")]
    assert HealthAggregator().aggregate(results).overall_status == "healthy"



def test_one_unhealthy_component_produces_overall_unhealthy() -> None:
    results = [_component("a", "healthy"), _component("b", "unhealthy")]
    assert HealthAggregator().aggregate(results).overall_status == "unhealthy"



def test_summary_counts_are_correct() -> None:
    results = [_component("a", "healthy"), _component("b", "unhealthy"), _component("c", "healthy")]
    assert HealthAggregator().summarize(results).model_dump() == {"total_components": 3, "healthy_components": 2, "unhealthy_components": 1}



def test_table_output_contains_component_names_and_status() -> None:
    output = HealthAggregator().table([_component("a", "unhealthy")])
    assert "name-a" in output and "unhealthy" in output
