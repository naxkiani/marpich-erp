"""
Marpich ERP — dependency graph rules and static import analysis.

See docs/architecture/DEPENDENCY_GRAPH.md
"""
from __future__ import annotations

import ast
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path

# ── Core platform contexts (PLATFORM + SUPPORTING) ───────────────────────

CORE_CONTEXT_IDS: frozenset[str] = frozenset(
    {
        "core_platform",
        "identity",
        "workflow",
        "integration",
        "documents",
        "notifications",
        "analytics",
        "ai",
        "media",
        "search",
        "settings",
        "localization",
        "organization",
        "audit",
    }
)

# Published cross-cutting entry points business modules may import from Core
CORE_PUBLIC_IMPORT_PREFIXES: tuple[str, ...] = (
    "contexts.identity.presentation.dependencies",
    "contexts.identity.presentation.schemas",
    "core.presentation",
)

SKIP_CONTEXT_DIRS: frozenset[str] = frozenset({"_template", "__pycache__"})

ALLOWED_EXTERNAL_PREFIXES: tuple[str, ...] = (
    "shared.",
    "shared.contracts.",
    *CORE_PUBLIC_IMPORT_PREFIXES,
)

STDLIB_ROOTS: frozenset[str] = frozenset(
    {
        "__future__",
        "typing",
        "datetime",
        "enum",
        "abc",
        "dataclasses",
        "uuid",
        "decimal",
        "collections",
        "functools",
        "re",
        "json",
        "logging",
        "asyncio",
        "contextlib",
        "types",
        "copy",
        "hashlib",
        "secrets",
        "string",
        "textwrap",
        "itertools",
        "operator",
        "pathlib",
        "os",
        "sys",
        "io",
        "time",
        "math",
        "statistics",
        "random",
        "base64",
        "hmac",
        "struct",
        "tempfile",
        "subprocess",
        "traceback",
        "warnings",
        "weakref",
        "inspect",
        "importlib",
        "http",
        "urllib",
        "email",
        "html",
        "xml",
        "csv",
        "configparser",
        "argparse",
        "getpass",
        "socket",
        "ssl",
        "threading",
        "multiprocessing",
        "concurrent",
        "queue",
        "unittest",
        "pytest",
        "fastapi",
        "pydantic",
        "starlette",
        "sqlalchemy",
        "jwt",
        "bcrypt",
        "passlib",
        "httpx",
    }
)


class ModuleLayer(StrEnum):
    DOMAIN = "domain"
    APPLICATION = "application"
    INFRASTRUCTURE = "infrastructure"
    PRESENTATION = "presentation"
    COMPOSITION = "composition"
    TESTS = "tests"
    UNKNOWN = "unknown"


class ViolationKind(StrEnum):
    LAYER = "layer"
    DOMAIN_EXTERNAL = "domain_external"
    SHARED_IMPORTS_CONTEXT = "shared_imports_context"
    CORE_IMPORTS_BUSINESS = "core_imports_business"
    BUSINESS_IMPORTS_BUSINESS = "business_imports_business"
    BUSINESS_IMPORTS_NON_CORE = "business_imports_non_core"
    CIRCULAR = "circular"


@dataclass(frozen=True, slots=True)
class ImportRef:
    module: str
    lineno: int


def _normalize_path(path: Path, backend_root: Path | None = None) -> str:
    p = path.resolve()
    if backend_root:
        try:
            return str(p.relative_to(backend_root.resolve())).replace("\\", "/")
        except ValueError:
            pass
    return str(p).replace("\\", "/")


@dataclass(frozen=True, slots=True)
class Violation:
    kind: ViolationKind
    source_file: str
    lineno: int
    message: str

    def key(self) -> str:
        return f"{self.kind.value}|{self.source_file}|{self.lineno}|{self.message}"


def is_core_context(context_id: str) -> bool:
    return context_id in CORE_CONTEXT_IDS


def is_business_context(context_id: str) -> bool:
    return context_id not in CORE_CONTEXT_IDS and context_id not in SKIP_CONTEXT_DIRS


def resolve_layer(context_id: str, relative_path: Path) -> ModuleLayer:
    parts = relative_path.parts
    if relative_path.name == "container.py":
        return ModuleLayer.COMPOSITION
    if "tests" in parts:
        return ModuleLayer.TESTS
    if "domain" in parts:
        return ModuleLayer.DOMAIN
    if "application" in parts:
        return ModuleLayer.APPLICATION
    if "infrastructure" in parts:
        return ModuleLayer.INFRASTRUCTURE
    if "presentation" in parts:
        return ModuleLayer.PRESENTATION
    return ModuleLayer.UNKNOWN


def parse_context_import(module: str) -> tuple[str | None, ModuleLayer | None]:
    """Return (context_id, target_layer) for contexts.* imports."""
    if not module.startswith("contexts."):
        return None, None
    rest = module.removeprefix("contexts.")
    if not rest or rest.split(".", 1)[0] in SKIP_CONTEXT_DIRS:
        return None, None
    context_id, _, subpath = rest.partition(".")
    if not subpath:
        return context_id, ModuleLayer.COMPOSITION
    if subpath.startswith("domain."):
        return context_id, ModuleLayer.DOMAIN
    if subpath.startswith("application."):
        return context_id, ModuleLayer.APPLICATION
    if subpath.startswith("infrastructure."):
        return context_id, ModuleLayer.INFRASTRUCTURE
    if subpath.startswith("presentation."):
        return context_id, ModuleLayer.PRESENTATION
    if subpath == "container":
        return context_id, ModuleLayer.COMPOSITION
    return context_id, ModuleLayer.UNKNOWN


def is_allowed_external(module: str) -> bool:
    return any(module.startswith(prefix) for prefix in ALLOWED_EXTERNAL_PREFIXES)


def _is_stdlib_import(module: str) -> bool:
    root = module.split(".", 1)[0]
    return root in STDLIB_ROOTS


def _is_shared_kernel_import(module: str) -> bool:
    return module == "shared" or module.startswith("shared.")


def _layer_allowed(source: ModuleLayer, target: ModuleLayer) -> bool:
    if source in {ModuleLayer.TESTS, ModuleLayer.COMPOSITION}:
        return True
    if target in {ModuleLayer.UNKNOWN}:
        return True
    if target == ModuleLayer.DOMAIN and source == ModuleLayer.DOMAIN:
        return True

    allowed: dict[ModuleLayer, frozenset[ModuleLayer]] = {
        ModuleLayer.DOMAIN: frozenset({ModuleLayer.DOMAIN}),
        ModuleLayer.APPLICATION: frozenset({ModuleLayer.DOMAIN, ModuleLayer.APPLICATION}),
        ModuleLayer.INFRASTRUCTURE: frozenset(
            {ModuleLayer.DOMAIN, ModuleLayer.APPLICATION, ModuleLayer.INFRASTRUCTURE}
        ),
        ModuleLayer.PRESENTATION: frozenset(
            {ModuleLayer.APPLICATION, ModuleLayer.PRESENTATION, ModuleLayer.COMPOSITION}
        ),
    }
    return target in allowed.get(source, frozenset())


def _collect_imports(path: Path) -> list[ImportRef]:
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except SyntaxError:
        return []
    refs: list[ImportRef] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                refs.append(ImportRef(module=alias.name, lineno=node.lineno))
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                refs.append(ImportRef(module=node.module, lineno=node.lineno))
    return refs


def _check_domain_import(
    rel_path: str,
    source_context: str,
    module: str,
    lineno: int,
) -> Violation | None:
    if module.startswith("contexts."):
        target_context, target_layer = parse_context_import(module)
        if target_context == source_context and target_layer == ModuleLayer.DOMAIN:
            return None
        return Violation(
            kind=ViolationKind.DOMAIN_EXTERNAL,
            source_file=rel_path,
            lineno=lineno,
            message=f"Domain must not import {module}",
        )
    if _is_shared_kernel_import(module) or _is_stdlib_import(module):
        return None
    return Violation(
        kind=ViolationKind.DOMAIN_EXTERNAL,
        source_file=rel_path,
        lineno=lineno,
        message=(
            "Domain depends on Shared Kernel and same-module domain only "
            f"({module})"
        ),
    )


def analyze_file(path: Path, contexts_root: Path, backend_root: Path) -> list[Violation]:
    violations: list[Violation] = []
    rel_path = _normalize_path(path, backend_root)
    try:
        rel = path.relative_to(contexts_root)
    except ValueError:
        return violations
    if not rel.parts:
        return violations
    source_context = rel.parts[0]
    if source_context in SKIP_CONTEXT_DIRS:
        return violations

    source_layer = resolve_layer(source_context, rel)
    source_is_core = is_core_context(source_context)
    source_is_business = is_business_context(source_context)
    is_test_file = source_layer == ModuleLayer.TESTS

    for imp in _collect_imports(path):
        module = imp.module

        if source_layer == ModuleLayer.DOMAIN:
            domain_v = _check_domain_import(rel_path, source_context, module, imp.lineno)
            if domain_v:
                violations.append(domain_v)
            continue

        if not module.startswith("contexts."):
            continue

        target_context, target_layer = parse_context_import(module)
        if target_context is None:
            continue
        same_context = target_context == source_context

        if same_context and target_layer is not None:
            if not _layer_allowed(source_layer, target_layer):
                violations.append(
                    Violation(
                        kind=ViolationKind.LAYER,
                        source_file=rel_path,
                        lineno=imp.lineno,
                        message=(
                            f"{source_layer.value} must not import "
                            f"{target_layer.value} ({module})"
                        ),
                    )
                )

        if same_context or is_test_file:
            continue

        if source_is_business and is_business_context(target_context):
            violations.append(
                Violation(
                    kind=ViolationKind.BUSINESS_IMPORTS_BUSINESS,
                    source_file=rel_path,
                    lineno=imp.lineno,
                    message=(
                        f"Business module '{source_context}' must not import "
                        f"business module '{target_context}'"
                    ),
                )
            )
        elif source_is_business and not is_core_context(target_context):
            violations.append(
                Violation(
                    kind=ViolationKind.BUSINESS_IMPORTS_NON_CORE,
                    source_file=rel_path,
                    lineno=imp.lineno,
                    message=(
                        f"Business module '{source_context}' may only import "
                        f"Core public contracts, not '{module}'"
                    ),
                )
            )
        elif source_is_business and is_core_context(target_context):
            if not is_allowed_external(module):
                violations.append(
                    Violation(
                        kind=ViolationKind.BUSINESS_IMPORTS_NON_CORE,
                        source_file=rel_path,
                        lineno=imp.lineno,
                        message=f"Import '{module}' is not a published Core contract",
                    )
                )
        elif source_is_core and is_business_context(target_context):
            violations.append(
                Violation(
                    kind=ViolationKind.CORE_IMPORTS_BUSINESS,
                    source_file=rel_path,
                    lineno=imp.lineno,
                    message=(
                        f"Core '{source_context}' must not depend on "
                        f"business module '{target_context}'"
                    ),
                )
            )

    return violations


def analyze_shared_tree(shared_root: Path, backend_root: Path) -> list[Violation]:
    violations: list[Violation] = []
    if not shared_root.is_dir():
        return violations
    for path in shared_root.rglob("*.py"):
        rel_path = _normalize_path(path, backend_root)
        for imp in _collect_imports(path):
            if imp.module.startswith("contexts."):
                violations.append(
                    Violation(
                        kind=ViolationKind.SHARED_IMPORTS_CONTEXT,
                        source_file=rel_path,
                        lineno=imp.lineno,
                        message=f"Shared Kernel must not import {imp.module}",
                    )
                )
    return violations


def build_module_dependency_graph(
    contexts_root: Path,
    *,
    include_tests: bool = False,
) -> dict[str, set[str]]:
    """Directed edges: source_context -> target_context (cross-module only)."""
    graph: dict[str, set[str]] = {}
    for path in contexts_root.rglob("*.py"):
        if "_template" in path.parts:
            continue
        try:
            rel = path.relative_to(contexts_root)
        except ValueError:
            continue
        if not rel.parts or rel.parts[0] in SKIP_CONTEXT_DIRS:
            continue
        if not include_tests and "tests" in rel.parts:
            continue
        source = rel.parts[0]
        for imp in _collect_imports(path):
            target_ctx, _ = parse_context_import(imp.module)
            if target_ctx and target_ctx != source:
                graph.setdefault(source, set()).add(target_ctx)
    return graph


def find_cycles(graph: dict[str, set[str]]) -> list[list[str]]:
    cycles: list[list[str]] = []
    visited: set[str] = set()
    stack: list[str] = []
    in_stack: set[str] = set()

    def dfs(node: str) -> None:
        visited.add(node)
        in_stack.add(node)
        stack.append(node)
        for neighbor in graph.get(node, ()):
            if neighbor not in visited:
                dfs(neighbor)
            elif neighbor in in_stack:
                idx = stack.index(neighbor)
                cycle = stack[idx:] + [neighbor]
                cycles.append(cycle)
        stack.pop()
        in_stack.remove(node)

    for node in graph:
        if node not in visited:
            dfs(node)
    return cycles


def analyze_codebase(backend_root: Path) -> list[Violation]:
    contexts_root = backend_root / "contexts"
    shared_root = backend_root / "shared"
    violations: list[Violation] = []
    violations.extend(analyze_shared_tree(shared_root, backend_root))
    if contexts_root.is_dir():
        for path in contexts_root.rglob("*.py"):
            if "_template" in path.parts:
                continue
            violations.extend(analyze_file(path, contexts_root, backend_root))
        graph = build_module_dependency_graph(contexts_root, include_tests=False)
        for cycle in find_cycles(graph):
            violations.append(
                Violation(
                    kind=ViolationKind.CIRCULAR,
                    source_file="(module graph)",
                    lineno=0,
                    message=f"Circular module dependency: {' -> '.join(cycle)}",
                )
            )
    return violations
