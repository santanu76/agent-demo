"""Generated test for plan_coverage_agent — passes once your business logic
returns something other than the scaffold sample."""
from acmehealth.agents.base import AgentRequest
from acmehealth.agents.plan_coverage_agent import PlanCoverageAgent


def test_plan_coverage_executes():
    result = PlanCoverageAgent().execute(AgentRequest(query="ping"))
    assert result.text
    assert "TODO" not in str(result.card), "replace the sample card fields with real logic"
