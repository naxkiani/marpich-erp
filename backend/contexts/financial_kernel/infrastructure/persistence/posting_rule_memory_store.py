"""In-memory posting rule repository."""
from __future__ import annotations

from contexts.financial_kernel.domain.aggregates.posting_rules import ConfigurablePostingRule
from contexts.financial_kernel.domain.ports.posting_rule_repositories import IPostingRuleRepository


class InMemoryPostingRuleRepository(IPostingRuleRepository):
    _rules: dict[str, ConfigurablePostingRule] = {}

    @classmethod
    def reset(cls) -> None:
        cls._rules = {}

    async def save(self, rule: ConfigurablePostingRule) -> None:
        self._rules[f"{rule.tenant_id}:{rule.rule_id}"] = rule

    async def find_by_rule_id(self, tenant_id: str, rule_id: str) -> ConfigurablePostingRule | None:
        return self._rules.get(f"{tenant_id}:{rule_id}")

    async def list_by_tenant(self, tenant_id: str) -> list[ConfigurablePostingRule]:
        return [r for k, r in self._rules.items() if k.startswith(f"{tenant_id}:")]

    async def delete(self, tenant_id: str, rule_id: str) -> bool:
        key = f"{tenant_id}:{rule_id}"
        if key in self._rules:
            del self._rules[key]
            return True
        return False
