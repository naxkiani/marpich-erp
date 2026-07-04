"""Shared kernel unit tests."""
from decimal import Decimal

import pytest

from shared.application.pagination import PageRequest, PageResult
from shared.application.sorting import SortField, SortOrder, SortSpec
from shared.domain.context.tenant_context import TenantContext
from shared.domain.context.user_context import UserContext
from shared.domain.value_objects.address import Address
from shared.domain.value_objects.country import Country
from shared.domain.value_objects.currency import Currency
from shared.domain.value_objects.language import Language
from shared.domain.value_objects.money import Money
from shared.kernel.localization import text_direction
from shared.presentation.responses import success_response


def test_money_arithmetic():
    usd = Currency("USD")
    a = Money(Decimal("10.00"), usd)
    b = Money(Decimal("5.50"), usd)
    assert a.add(b).amount == Decimal("15.50")


def test_money_currency_mismatch():
    with pytest.raises(ValueError, match="Currency mismatch"):
        Money(Decimal("1"), Currency("USD")).add(Money(Decimal("1"), Currency("EUR")))


def test_address_format():
    addr = Address(
        line1="123 Main St",
        city="Tehran",
        country=Country("IR"),
        postal_code="12345",
    )
    assert "IR" in addr.formatted()


def test_page_request_offset():
    page = PageRequest(page=3, page_size=25)
    assert page.offset == 50


def test_sort_field_desc():
    field = SortField.parse("-created_at")
    assert field.field == "created_at"
    assert field.order == SortOrder.DESC


def test_user_context_wildcard_permission():
    user = UserContext(user_id="u1", email="a@b.com", permissions=("*",))
    assert user.has_permission("hospital.patients.read")


def test_tenant_context_direction():
    ctx = TenantContext.create(tenant_id="acme-hospital", locale="fa-IR")
    assert ctx.direction == "rtl"


def test_text_direction_en():
    assert text_direction("en-US") == "ltr"


def test_success_response_envelope():
    body = success_response({"id": "1"}, correlation_id="c-1")
    assert body["data"]["id"] == "1"
    assert body["meta"]["correlation_id"] == "c-1"


def test_language_tag_normalization():
    assert str(Language("en_US")) == "en-US"
