"use client";

import { useCallback, useMemo, useRef, useState } from "react";
import type { EobServiceGraph } from "@/lib/enterpriseObservabilityClient";

export type GraphNode = {
  id: string;
  label: string;
  type: string;
  route_count: number;
  x: number;
  y: number;
};

export type GraphEdge = {
  from: string;
  to: string;
  type: string;
};

const NODE_W = 148;
const NODE_H = 44;
const COL_GAP = 200;
const ROW_GAP = 72;
const PAD = 48;
const MIN_ZOOM = 0.35;
const MAX_ZOOM = 2.5;
const ZOOM_STEP = 0.15;

const SERVICE_TYPES = ["platform", "context", "infrastructure", "connector"] as const;

const NODE_COLORS: Record<string, string> = {
  platform: "#6366f1",
  context: "#0ea5e9",
  infrastructure: "#64748b",
  connector: "#f59e0b",
};

const TYPE_LABELS: Record<string, string> = {
  platform: "Platform",
  context: "Context",
  infrastructure: "Infrastructure",
  connector: "Connector",
};

const EDGE_COLORS: Record<string, string> = {
  routes_to: "#94a3b8",
  auth_delegate: "#8b5cf6",
  ingress_delegate: "#8b5cf6",
  metrics_delegate: "#22c55e",
  alert_delegate: "#f97316",
  incident_delegate: "#ef4444",
  transport_delegate: "#0ea5e9",
  delivery_delegate: "#0ea5e9",
  kpi_delegate: "#22c55e",
  ai_metrics_delegate: "#a855f7",
  topic_publish: "#f59e0b",
  queue_publish: "#f59e0b",
  dispatch_delegate: "#64748b",
};

function inferNodeType(id: string): string {
  if (["otel_collector", "prometheus", "loki", "tempo", "outbox_dispatcher"].includes(id)) {
    return "infrastructure";
  }
  if (
    id.startsWith("enterprise_") ||
    ["analytics", "notifications", "identity", "integration", "workflow", "ai_governance"].includes(id)
  ) {
    return "platform";
  }
  if (id.includes("connector")) return "connector";
  return "context";
}

function buildGraphModel(graph: EobServiceGraph): { nodes: GraphNode[]; edges: GraphEdge[] } {
  const rawNodes = graph.nodes?.length
    ? graph.nodes
    : graph.services.map((s) => ({
        id: s.service_id,
        label: s.label,
        type: inferNodeType(s.service_id),
        route_count: s.routes.length,
      }));

  const rawEdges: GraphEdge[] = graph.edges?.length
    ? graph.edges
    : graph.services.flatMap((s) =>
        s.dependencies.map((d) => ({ from: s.service_id, to: d.target, type: d.type })),
      );

  const nodeIds = new Set<string>();
  for (const n of rawNodes) nodeIds.add(n.id);
  for (const e of rawEdges) {
    nodeIds.add(e.from);
    nodeIds.add(e.to);
  }

  const adjacency: Record<string, string[]> = { enterprise_observability: [], enterprise_api_gateway: [] };
  for (const id of nodeIds) adjacency[id] = adjacency[id] ?? [];
  for (const e of rawEdges) {
    adjacency[e.from] = adjacency[e.from] ?? [];
    adjacency[e.from].push(e.to);
  }

  const depth: Record<string, number> = {};
  const queue: string[] = [];
  for (const root of ["enterprise_observability", "enterprise_api_gateway"]) {
    if (nodeIds.has(root)) {
      depth[root] = 0;
      queue.push(root);
    }
  }
  if (!queue.length && rawNodes.length) {
    depth[rawNodes[0].id] = 0;
    queue.push(rawNodes[0].id);
  }

  while (queue.length) {
    const current = queue.shift()!;
    const d = depth[current] ?? 0;
    for (const next of adjacency[current] ?? []) {
      if (depth[next] === undefined || depth[next] > d + 1) {
        depth[next] = d + 1;
        queue.push(next);
      }
    }
  }

  const maxDepth = Math.max(0, ...Object.values(depth), 0);
  for (const id of nodeIds) {
    if (depth[id] === undefined) depth[id] = maxDepth + 1;
  }

  const layers: Record<number, typeof rawNodes> = {};
  for (const n of rawNodes) {
    const d = depth[n.id] ?? maxDepth + 1;
    layers[d] = layers[d] ?? [];
    layers[d].push(n);
  }
  for (const id of nodeIds) {
    if (!rawNodes.some((n) => n.id === id)) {
      const d = depth[id] ?? maxDepth + 1;
      layers[d] = layers[d] ?? [];
      layers[d].push({
        id,
        label: id.replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase()),
        type: inferNodeType(id),
        route_count: 0,
      });
    }
  }

  const nodes: GraphNode[] = [];
  for (const [layerStr, layerNodes] of Object.entries(layers)) {
    const layer = Number(layerStr);
    const sorted = [...layerNodes].sort((a, b) => a.label.localeCompare(b.label));
    sorted.forEach((n, i) => {
      nodes.push({
        ...n,
        x: PAD + layer * COL_GAP,
        y: PAD + i * ROW_GAP,
      });
    });
  }

  const height = Math.max(...nodes.map((n) => n.y), PAD) + NODE_H + PAD;
  const centered = nodes.map((n) => {
    const layerNodes = nodes.filter((x) => x.x === n.x);
    const layerH = layerNodes.length * ROW_GAP;
    const offset = (height - layerH) / 2;
    const idx = layerNodes.findIndex((x) => x.id === n.id);
    return { ...n, y: offset + idx * ROW_GAP };
  });

  return { nodes: centered, edges: rawEdges };
}

function truncateLabel(label: string, max = 18): string {
  return label.length > max ? `${label.slice(0, max - 1)}…` : label;
}

function clampZoom(value: number): number {
  return Math.min(MAX_ZOOM, Math.max(MIN_ZOOM, value));
}

type ServiceDependencyGraphCanvasProps = {
  graph: EobServiceGraph;
};

export function ServiceDependencyGraphCanvas({ graph }: ServiceDependencyGraphCanvasProps) {
  const canvasRef = useRef<HTMLDivElement>(null);
  const [selectedId, setSelectedId] = useState<string | null>(null);
  const [hoverId, setHoverId] = useState<string | null>(null);
  const [enabledTypes, setEnabledTypes] = useState<Set<string>>(new Set(SERVICE_TYPES));
  const [zoom, setZoom] = useState(1);
  const [pan, setPan] = useState({ x: 0, y: 0 });
  const [isPanning, setIsPanning] = useState(false);
  const panStart = useRef({ x: 0, y: 0, panX: 0, panY: 0 });

  const { nodes, edges } = useMemo(() => buildGraphModel(graph), [graph]);

  const visibleNodes = useMemo(
    () => nodes.filter((n) => enabledTypes.has(n.type)),
    [nodes, enabledTypes],
  );
  const visibleIds = useMemo(() => new Set(visibleNodes.map((n) => n.id)), [visibleNodes]);
  const visibleEdges = useMemo(
    () => edges.filter((e) => visibleIds.has(e.from) && visibleIds.has(e.to)),
    [edges, visibleIds],
  );

  const nodeMap = useMemo(() => new Map(visibleNodes.map((n) => [n.id, n])), [visibleNodes]);

  const width = Math.max(...nodes.map((n) => n.x), PAD) + NODE_W + PAD;
  const height = Math.max(...nodes.map((n) => n.y), PAD) + NODE_H + PAD;

  const activeId = hoverId ?? selectedId;
  const connected = useMemo(() => {
    if (!activeId || !visibleIds.has(activeId)) return new Set<string>();
    const set = new Set<string>([activeId]);
    for (const e of visibleEdges) {
      if (e.from === activeId) set.add(e.to);
      if (e.to === activeId) set.add(e.from);
    }
    return set;
  }, [activeId, visibleEdges, visibleIds]);

  const selectedService = graph.services.find((s) => s.service_id === selectedId);

  const typeCounts = useMemo(() => {
    const counts: Record<string, number> = {};
    for (const t of SERVICE_TYPES) counts[t] = 0;
    for (const n of nodes) counts[n.type] = (counts[n.type] ?? 0) + 1;
    return counts;
  }, [nodes]);

  const toggleType = useCallback((type: string) => {
    setEnabledTypes((prev) => {
      const next = new Set(prev);
      if (next.has(type)) {
        if (next.size <= 1) return prev;
        next.delete(type);
      } else {
        next.add(type);
      }
      return next;
    });
    setSelectedId(null);
  }, []);

  const resetView = useCallback(() => {
    setZoom(1);
    setPan({ x: 0, y: 0 });
  }, []);

  const zoomIn = useCallback(() => setZoom((z) => clampZoom(z + ZOOM_STEP)), []);
  const zoomOut = useCallback(() => setZoom((z) => clampZoom(z - ZOOM_STEP)), []);

  const handleWheel = useCallback((ev: React.WheelEvent<HTMLDivElement>) => {
    ev.preventDefault();
    const delta = ev.deltaY > 0 ? -ZOOM_STEP : ZOOM_STEP;
    setZoom((z) => clampZoom(z + delta));
  }, []);

  const handlePointerDown = useCallback(
    (ev: React.PointerEvent<HTMLDivElement>) => {
      const target = ev.target as HTMLElement;
      if (target.closest(".eob-graph-node")) return;
      setIsPanning(true);
      panStart.current = { x: ev.clientX, y: ev.clientY, panX: pan.x, panY: pan.y };
      ev.currentTarget.setPointerCapture(ev.pointerId);
    },
    [pan.x, pan.y],
  );

  const handlePointerMove = useCallback(
    (ev: React.PointerEvent<HTMLDivElement>) => {
      if (!isPanning) return;
      const dx = ev.clientX - panStart.current.x;
      const dy = ev.clientY - panStart.current.y;
      setPan({ x: panStart.current.panX + dx, y: panStart.current.panY + dy });
    },
    [isPanning],
  );

  const handlePointerUp = useCallback((ev: React.PointerEvent<HTMLDivElement>) => {
    setIsPanning(false);
    ev.currentTarget.releasePointerCapture(ev.pointerId);
  }, []);

  function edgePath(fromId: string, toId: string): string {
    const from = nodeMap.get(fromId);
    const to = nodeMap.get(toId);
    if (!from || !to) return "";
    const x1 = from.x + NODE_W;
    const y1 = from.y + NODE_H / 2;
    const x2 = to.x;
    const y2 = to.y + NODE_H / 2;
    const midX = (x1 + x2) / 2;
    return `M ${x1} ${y1} C ${midX} ${y1}, ${midX} ${y2}, ${x2} ${y2}`;
  }

  return (
    <div className="eob-graph-wrap">
      <div className="eob-graph-main">
        <div className="eob-graph-toolbar">
          <div className="eob-graph-filters" role="group" aria-label="Filter by service type">
            {SERVICE_TYPES.map((type) => {
              const active = enabledTypes.has(type);
              return (
                <button
                  key={type}
                  type="button"
                  className={`eob-filter-chip eob-filter-chip--${type}${active ? " eob-filter-chip--active" : ""}`}
                  onClick={() => toggleType(type)}
                  aria-pressed={active}
                >
                  {TYPE_LABELS[type]} ({typeCounts[type] ?? 0})
                </button>
              );
            })}
          </div>
          <div className="eob-graph-zoom" role="group" aria-label="Zoom and pan controls">
            <button type="button" className="mp-btn eob-zoom-btn" onClick={zoomOut} aria-label="Zoom out">
              −
            </button>
            <span className="eob-zoom-label">{Math.round(zoom * 100)}%</span>
            <button type="button" className="mp-btn eob-zoom-btn" onClick={zoomIn} aria-label="Zoom in">
              +
            </button>
            <button type="button" className="mp-btn eob-zoom-btn" onClick={resetView}>
              Reset
            </button>
          </div>
        </div>

        <p className="eob-graph-meta">
          Showing {visibleNodes.length} of {nodes.length} services · {visibleEdges.length} edges · scroll to zoom · drag background to pan
        </p>

        <div
          ref={canvasRef}
          className={`eob-graph-canvas${isPanning ? " eob-graph-canvas--panning" : ""}`}
          role="region"
          aria-label="Service dependency graph"
          onWheel={handleWheel}
          onPointerDown={handlePointerDown}
          onPointerMove={handlePointerMove}
          onPointerUp={handlePointerUp}
          onPointerLeave={handlePointerUp}
        >
          <svg viewBox={`0 0 ${width} ${height}`} className="eob-graph-svg" preserveAspectRatio="xMidYMid meet">
            <defs>
              <marker id="eob-arrow" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">
                <path d="M0,0 L6,3 L0,6 Z" fill="#94a3b8" />
              </marker>
            </defs>
            <rect x={0} y={0} width={width} height={height} fill="transparent" className="eob-graph-bg" />
            <g transform={`translate(${pan.x}, ${pan.y}) scale(${zoom})`}>
              {visibleEdges.map((e) => {
                const dimmed = activeId && !connected.has(e.from) && !connected.has(e.to);
                return (
                  <path
                    key={`${e.from}-${e.to}-${e.type}`}
                    d={edgePath(e.from, e.to)}
                    className={`eob-graph-edge${dimmed ? " eob-graph-edge--dim" : ""}`}
                    stroke={EDGE_COLORS[e.type] ?? "#94a3b8"}
                    markerEnd="url(#eob-arrow)"
                  />
                );
              })}
              {visibleNodes.map((node) => {
                const isActive = activeId === node.id;
                const isConnected = connected.has(node.id);
                const dimmed = activeId && !isActive && !isConnected;
                return (
                  <g
                    key={node.id}
                    transform={`translate(${node.x}, ${node.y})`}
                    className={`eob-graph-node${dimmed ? " eob-graph-node--dim" : ""}${isActive ? " eob-graph-node--active" : ""}`}
                    onMouseEnter={() => setHoverId(node.id)}
                    onMouseLeave={() => setHoverId(null)}
                    onClick={(ev) => {
                      ev.stopPropagation();
                      setSelectedId((prev) => (prev === node.id ? null : node.id));
                    }}
                    style={{ cursor: "pointer" }}
                    role="button"
                    tabIndex={0}
                    aria-label={`${node.label}, ${node.type}`}
                    onKeyDown={(ev) => {
                      if (ev.key === "Enter" || ev.key === " ") {
                        ev.preventDefault();
                        setSelectedId((prev) => (prev === node.id ? null : node.id));
                      }
                    }}
                  >
                    <rect
                      width={NODE_W}
                      height={NODE_H}
                      rx={8}
                      fill={NODE_COLORS[node.type] ?? "#94a3b8"}
                      stroke={isActive ? "#1e293b" : "transparent"}
                      strokeWidth={isActive ? 2 : 0}
                    />
                    <text x={NODE_W / 2} y={18} textAnchor="middle" className="eob-graph-node-label">
                      {truncateLabel(node.label)}
                    </text>
                    <text x={NODE_W / 2} y={34} textAnchor="middle" className="eob-graph-node-meta">
                      {node.type}
                      {node.route_count ? ` · ${node.route_count} routes` : ""}
                    </text>
                  </g>
                );
              })}
            </g>
          </svg>
        </div>
      </div>

      <div className="eob-graph-side">
        <div className="eob-graph-legend">
          {SERVICE_TYPES.map((type) => (
            <button
              key={type}
              type="button"
              className={`eob-legend-item eob-legend--${type === "infrastructure" ? "infra" : type}${
                enabledTypes.has(type) ? "" : " eob-legend-item--off"
              }`}
              onClick={() => toggleType(type)}
              aria-pressed={enabledTypes.has(type)}
            >
              {TYPE_LABELS[type]}
            </button>
          ))}
        </div>
        {selectedService && visibleIds.has(selectedService.service_id) ? (
          <div className="eob-graph-detail">
            <h3>{selectedService.label}</h3>
            <p className="eob-muted">
              <strong>{selectedService.routes.length}</strong> routes ·{" "}
              <strong>{selectedService.dependencies.length}</strong> dependencies
            </p>
            {selectedService.routes.length ? (
              <ul className="eob-route-list">
                {selectedService.routes.slice(0, 6).map((r) => (
                  <li key={r}>{r}</li>
                ))}
                {selectedService.routes.length > 6 ? (
                  <li>+{selectedService.routes.length - 6} more</li>
                ) : null}
              </ul>
            ) : null}
            {selectedService.dependencies.length ? (
              <ul className="eob-dep-list">
                {selectedService.dependencies.map((d) => (
                  <li key={`${d.target}-${d.type}`}>
                    → {d.target.replace(/_/g, " ")} <em>({d.type})</em>
                  </li>
                ))}
              </ul>
            ) : null}
          </div>
        ) : (
          <p className="eob-muted eob-graph-hint">
            Filter by type, zoom with scroll or +/- buttons, drag the canvas to pan. Click a node for details.
          </p>
        )}
      </div>

      <style jsx>{`
        .eob-graph-wrap {
          display: grid;
          grid-template-columns: 1fr 240px;
          gap: 1rem;
          margin-bottom: 1rem;
          border: 1px solid var(--mp-border, #e2e8f0);
          border-radius: 8px;
          padding: 1rem;
          background: var(--mp-surface-2, #f8fafc);
        }
        .eob-graph-main { min-width: 0; }
        .eob-graph-toolbar {
          display: flex;
          flex-wrap: wrap;
          gap: 0.75rem;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 0.5rem;
        }
        .eob-graph-filters { display: flex; flex-wrap: wrap; gap: 0.4rem; }
        .eob-filter-chip {
          border: 1px solid var(--mp-border, #e2e8f0);
          border-radius: 999px;
          padding: 0.25rem 0.65rem;
          font-size: 0.75rem;
          background: #fff;
          cursor: pointer;
          transition: opacity 0.15s, border-color 0.15s;
        }
        .eob-filter-chip--active { font-weight: 600; }
        .eob-filter-chip--platform.eob-filter-chip--active { border-color: #6366f1; background: #eef2ff; }
        .eob-filter-chip--context.eob-filter-chip--active { border-color: #0ea5e9; background: #f0f9ff; }
        .eob-filter-chip--infrastructure.eob-filter-chip--active { border-color: #64748b; background: #f1f5f9; }
        .eob-filter-chip--connector.eob-filter-chip--active { border-color: #f59e0b; background: #fffbeb; }
        .eob-filter-chip:not(.eob-filter-chip--active) { opacity: 0.55; }
        .eob-graph-zoom { display: flex; align-items: center; gap: 0.35rem; }
        .eob-zoom-btn { min-width: 2rem; padding: 0.25rem 0.5rem; font-size: 0.85rem; }
        .eob-zoom-label { font-size: 0.78rem; color: var(--mp-text-muted, #64748b); min-width: 3rem; text-align: center; }
        .eob-graph-meta {
          margin: 0 0 0.5rem;
          font-size: 0.75rem;
          color: var(--mp-text-muted, #64748b);
        }
        .eob-graph-canvas {
          overflow: hidden;
          height: 480px;
          border-radius: 6px;
          background: #fff;
          border: 1px solid var(--mp-border, #e2e8f0);
          cursor: grab;
          touch-action: none;
        }
        .eob-graph-canvas--panning { cursor: grabbing; }
        .eob-graph-svg { display: block; width: 100%; height: 100%; }
        .eob-graph-bg { cursor: grab; }
        .eob-graph-edge {
          fill: none;
          stroke-width: 1.5;
          opacity: 0.7;
        }
        .eob-graph-edge--dim { opacity: 0.12; }
        .eob-graph-node--dim { opacity: 0.35; }
        .eob-graph-node-label {
          fill: #fff;
          font-size: 11px;
          font-weight: 600;
          pointer-events: none;
        }
        .eob-graph-node-meta {
          fill: rgba(255, 255, 255, 0.85);
          font-size: 9px;
          pointer-events: none;
        }
        .eob-graph-legend {
          display: flex;
          flex-direction: column;
          gap: 0.35rem;
          margin-bottom: 1rem;
        }
        .eob-legend-item {
          display: flex;
          align-items: center;
          border: none;
          background: transparent;
          font-size: 0.78rem;
          cursor: pointer;
          padding: 0.15rem 0;
          text-align: left;
        }
        .eob-legend-item--off { opacity: 0.4; text-decoration: line-through; }
        .eob-legend-item::before {
          content: "";
          display: inline-block;
          width: 10px;
          height: 10px;
          border-radius: 2px;
          margin-right: 0.4rem;
          flex-shrink: 0;
        }
        .eob-legend--platform::before { background: #6366f1; }
        .eob-legend--context::before { background: #0ea5e9; }
        .eob-legend--infra::before { background: #64748b; }
        .eob-legend--connector::before { background: #f59e0b; }
        .eob-graph-detail h3 { margin: 0 0 0.5rem; font-size: 0.95rem; }
        .eob-route-list, .eob-dep-list {
          margin: 0.5rem 0 0;
          padding-left: 1rem;
          font-size: 0.78rem;
          color: var(--mp-text-muted, #64748b);
        }
        .eob-graph-hint { font-size: 0.8rem; margin: 0; }
        .eob-muted { color: var(--mp-text-muted, #64748b); }
        @media (max-width: 960px) {
          .eob-graph-wrap { grid-template-columns: 1fr; }
        }
      `}</style>
    </div>
  );
}
