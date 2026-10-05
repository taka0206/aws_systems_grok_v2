import { catalog } from "@/data/catalog";

const FRACS = [0.125, 0.375, 0.625, 0.875];

type Shape = {
  key: string;
  x: number;
  y: number;
  w: number;
  h: number;
  title: string;
  sub?: string;
  kicker?: string;
  color: string;
  form?: string;
  dash?: string;
};

type Wire = {
  a: string;
  b: string;
  ia: number;
  ib: number;
  color: string;
  preset: string;
  overlay: boolean;
  dashed: boolean;
};

export type Board = {
  cols: number;
  rows: number;
  title: string;
  shapes: readonly Shape[];
  lines: readonly Wire[];
};

const colorOf = Object.fromEntries(catalog.colors.map((c) => [c.key, c.hex]));

function endpoint(shape: Shape, idx: number): [number, number] {
  if (shape.form === "ellipse") {
    const deg = idx * 22.5;
    const rad = (deg * Math.PI) / 180;
    const cx = shape.x + shape.w / 2;
    const cy = shape.y + shape.h / 2;
    return [cx + (shape.w / 2) * Math.cos(rad), cy + (shape.h / 2) * Math.sin(rad)];
  }
  const side = Math.floor(idx / 4);
  const f = FRACS[idx % 4] ?? 0.5;
  if (side === 0) return [shape.x + shape.w * f, shape.y];
  if (side === 1) return [shape.x + shape.w, shape.y + shape.h * f];
  if (side === 2) return [shape.x + shape.w * f, shape.y + shape.h];
  return [shape.x, shape.y + shape.h * f];
}

function route(line: Wire, byKey: Map<string, Shape>): string {
  const a = byKey.get(line.a);
  const b = byKey.get(line.b);
  if (!a || !b) return "";
  const [x1, y1] = endpoint(a, line.ia);
  const [x2, y2] = endpoint(b, line.ib);
  if (line.preset.startsWith("curved")) {
    const cx = x1;
    const cy = y2;
    return `M ${x1} ${y1} Q ${cx} ${cy} ${x2} ${y2}`;
  }
  if (line.preset === "bentConnector5") {
    const xA = x1 + (x2 - x1) * 0.33;
    const xB = x1 + (x2 - x1) * 0.66;
    const yM = y1 + (y2 - y1) * 0.5;
    return `M ${x1} ${y1} H ${xA} V ${yM} H ${xB} V ${y2} H ${x2}`;
  }
  if (line.preset === "straightConnector1") return `M ${x1} ${y1} L ${x2} ${y2}`;
  const mid = (x1 + x2) / 2;
  return `M ${x1} ${y1} H ${mid} V ${y2} H ${x2}`;
}

export function SheetPreview({ board, cell = 11 }: { board: Board; cell?: number }) {
  const byKey = new Map(board.shapes.map((s) => [s.key, s]));
  const width = board.cols * cell;
  const height = board.rows * cell;
  const zones = board.shapes.filter((s) => s.form === "zone");
  const nodes = board.shapes.filter((s) => s.form !== "zone" && s.form !== "note" && s.form !== "label");
  const notes = board.shapes.filter((s) => s.form === "note" || s.form === "label");
  const base = board.lines.filter((l) => !l.overlay);
  const over = board.lines.filter((l) => l.overlay);

  return (
    <div className="min-w-0 max-w-full overflow-x-auto rounded-card border border-line bg-panel">
      <svg
        width={width}
        height={height}
        viewBox={`0 0 ${board.cols} ${board.rows}`}
        role="img"
        aria-label={board.title}
        className="block"
      >
        <defs>
          <pattern id="minor" width="1" height="1" patternUnits="userSpaceOnUse">
            <path d="M 1 0 L 0 0 0 1" fill="none" stroke="var(--color-line)" strokeWidth="0.03" />
          </pattern>
          <pattern id="major" width="5" height="5" patternUnits="userSpaceOnUse">
            <path d="M 5 0 L 0 0 0 5" fill="none" stroke="var(--color-major)" strokeWidth="0.06" />
          </pattern>
          {catalog.colors.map((c) => (
            <marker
              key={c.key}
              id={`arrow-${c.key}`}
              viewBox="0 0 10 10"
              refX="9"
              refY="5"
              markerWidth="5"
              markerHeight="5"
              orient="auto-start-reverse"
            >
              <path d="M 0 0 L 10 5 L 0 10 z" fill={`#${c.hex}`} />
            </marker>
          ))}
        </defs>
        <rect width={board.cols} height={board.rows} fill="url(#minor)" />
        <rect width={board.cols} height={board.rows} fill="url(#major)" />
        <rect width={board.cols} height="1.15" fill="var(--color-ink)" />
        <text x="0.6" y="0.82" fill="var(--color-panel)" fontSize="0.62" fontFamily="var(--font-sans)">
          {board.title}
        </text>
        {zones.map((s) => (
          <g key={s.key}>
            <rect
              x={s.x + 0.08}
              y={s.y + 0.08}
              width={s.w - 0.16}
              height={s.h - 0.16}
              rx="0.35"
              fill={`#${colorOf[s.color]}`}
              fillOpacity="0.07"
              stroke={`#${colorOf[s.color]}`}
              strokeWidth="0.08"
              strokeDasharray={s.dash === "solid" ? undefined : "0.45 0.28"}
            />
            <text x={s.x + 0.7} y={s.y + 1.35} fill={`#${colorOf[s.color]}`} fontSize="0.72" fontWeight="700" fontFamily="var(--font-sans)">
              {s.kicker}
            </text>
            <text x={s.x + 0.7} y={s.y + 2.35} fill="var(--color-ink)" fontSize="0.95" fontWeight="700" fontFamily="var(--font-sans)">
              {s.title}
            </text>
          </g>
        ))}
        {nodes.map((s) =>
          s.form === "ellipse" ? (
            <g key={s.key}>
              <ellipse
                cx={s.x + s.w / 2}
                cy={s.y + s.h / 2}
                rx={s.w / 2 - 0.08}
                ry={s.h / 2 - 0.08}
                fill="var(--color-panel)"
                stroke={`#${colorOf[s.color]}`}
                strokeWidth="0.1"
              />
              <text
                x={s.x + s.w / 2}
                y={s.y + s.h / 2 + 0.3}
                textAnchor="middle"
                fill="var(--color-ink)"
                fontSize="0.85"
                fontWeight="700"
                fontFamily="var(--font-sans)"
              >
                {s.title}
              </text>
            </g>
          ) : (
            <g key={s.key}>
              <rect
                x={s.x + 0.06}
                y={s.y + 0.06}
                width={s.w - 0.12}
                height={s.h - 0.12}
                rx="0.28"
                fill="var(--color-panel)"
                stroke={`#${colorOf[s.color]}`}
                strokeWidth="0.09"
              />
              <rect x={s.x + 0.06} y={s.y + 0.28} width="0.28" height={Math.max(0.4, s.h - 0.56)} fill={`#${colorOf[s.color]}`} />
              {s.kicker ? (
                <text x={s.x + 0.7} y={s.y + 1.35} fill={`#${colorOf[s.color]}`} fontSize="0.62" fontWeight="700" fontFamily="var(--font-sans)">
                  {s.kicker}
                </text>
              ) : null}
              <text x={s.x + 0.7} y={s.y + (s.kicker ? 2.45 : 1.8)} fill="var(--color-ink)" fontSize="0.85" fontWeight="700" fontFamily="var(--font-sans)">
                {s.title}
              </text>
            </g>
          ),
        )}
        {base.map((line, i) => (
          <path
            key={`b${i}`}
            d={route(line, byKey)}
            fill="none"
            stroke={`#${colorOf[line.color]}`}
            strokeWidth="0.14"
            strokeLinejoin="miter"
            strokeDasharray={line.dashed ? "0.45 0.28" : undefined}
            markerEnd={`url(#arrow-${line.color})`}
          />
        ))}
        {over.map((line, i) => (
          <path
            key={`o${i}`}
            d={route(line, byKey)}
            fill="none"
            stroke={`#${colorOf[line.color]}`}
            strokeWidth="0.55"
            strokeOpacity="0.42"
            strokeLinecap="round"
            strokeLinejoin="round"
            markerEnd={`url(#arrow-${line.color})`}
          />
        ))}
        {notes.map((s) => (
          <g key={s.key}>
            <rect
              x={s.x + 0.06}
              y={s.y + 0.06}
              width={s.w - 0.12}
              height={s.h - 0.12}
              rx="0.25"
              fill="var(--color-panel)"
              stroke={`#${colorOf[s.color]}`}
              strokeWidth="0.08"
            />
            <rect x={s.x + 0.06} y={s.y + 0.06} width={s.w - 0.12} height="0.36" fill={`#${colorOf[s.color]}`} />
            <text x={s.x + 0.5} y={s.y + 1.5} fill="var(--color-ink)" fontSize="0.78" fontWeight="700" fontFamily="var(--font-sans)">
              {s.title}
            </text>
            {s.sub ? (
              <text x={s.x + 0.5} y={s.y + 2.45} fill="var(--color-muted)" fontSize="0.62" fontFamily="var(--font-sans)">
                {s.sub}
              </text>
            ) : null}
          </g>
        ))}
      </svg>
    </div>
  );
}

export function AnchorMap() {
  const dots = FRACS.flatMap((f, i) => [
    { x: 10 + 60 * f, y: 8, id: `t${i}` },
    { x: 70, y: 8 + 28 * f, id: `r${i}` },
    { x: 10 + 60 * f, y: 36, id: `b${i}` },
    { x: 10, y: 8 + 28 * f, id: `l${i}` },
  ]);
  return (
    <svg viewBox="0 0 80 46" className="h-36 w-full max-w-64" aria-hidden="true">
      <rect x="10" y="8" width="60" height="28" rx="2" fill="var(--color-panel)" stroke="var(--color-ink)" strokeWidth="0.8" />
      <rect x="10" y="10" width="2.2" height="24" fill="var(--color-ink)" />
      {dots.map((d) => (
        <circle key={d.id} cx={d.x} cy={d.y} r="1.15" fill="var(--color-ink)" />
      ))}
    </svg>
  );
}
