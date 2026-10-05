import { createFileRoute } from "@tanstack/react-router";
import { useState } from "react";
import { Download } from "lucide-react";
import { catalog } from "@/data/catalog";
import { AnchorMap, SheetPreview, type Board } from "@/components/sheet-preview";

export const Route = createFileRoute("/")({ component: Home });

function Home() {
  const [which, setWhich] = useState<"overview" | "detail">("overview");
  const board: Board = which === "overview" ? catalog.overview : catalog.detail;

  return (
    <main className="mx-auto w-full max-w-6xl overflow-x-hidden px-4 py-8 sm:px-6 sm:py-12">
      <header className="border-b border-ink pb-6">
        <p className="text-sm tracking-widest text-muted">EXCEL TEMPLATE</p>
        <div className="mt-3 flex flex-col gap-6 lg:flex-row lg:items-end lg:justify-between">
          <div className="max-w-2xl">
            <h1 className="text-3xl font-semibold tracking-tight sm:text-4xl">システム構成図</h1>
            <p className="mt-3 text-base leading-relaxed text-muted">
              現場、社内、AWS、外部SaaSを一枚に置くための方眼テンプレートです。図形は升目に吸着し、四角の接続点は各辺4つ、計16。経路は墨を含む7色で揃えます。
            </p>
          </div>
          <a
            href="/system-architecture-template.xlsx"
            download="システム構成図テンプレート.xlsx"
            className="inline-flex min-h-11 items-center justify-center gap-2 bg-ink px-5 py-3 text-sm font-semibold text-panel"
          >
            <Download className="size-4" aria-hidden="true" />
            Excelをダウンロード
          </a>
        </div>
      </header>

      <section className="mt-8 grid gap-8 lg:grid-cols-[16rem_minmax(0,1fr)]">
        <ol className="space-y-3 text-sm leading-relaxed">
          {catalog.steps.map((step, i) => (
            <li key={step} className="flex gap-3">
              <span className="mt-0.5 flex size-6 shrink-0 items-center justify-center bg-ink text-xs font-semibold text-panel">
                {i + 1}
              </span>
              <span>{step}</span>
            </li>
          ))}
        </ol>
        <div className="min-w-0">
          <div className="mb-3 flex flex-wrap gap-2">
            <SheetButton active={which === "overview"} onClick={() => setWhich("overview")}>
              概要図
            </SheetButton>
            <SheetButton active={which === "detail"} onClick={() => setWhich("detail")}>
              詳細図
            </SheetButton>
            <p className="self-center text-xs text-muted">横にスクロールできます。太い半透明が上書き線です。</p>
          </div>
          <SheetPreview board={board} />
        </div>
      </section>

      <section className="mt-12">
        <h2 className="text-xl font-semibold">経路は7色だけ</h2>
        <p className="mt-2 max-w-3xl text-sm leading-relaxed text-muted">
          基調は墨。従来の藍・蘇芳・苔に、金茶・江戸紫・浅葱を足しています。図形の左帯、本線、上書き線、付記を同じ色にします。上書き線は白を混ぜた半透明の太線で、すでに引いてある線を消しません。
        </p>
        <ul className="mt-5 grid gap-3 sm:grid-cols-2">
          {catalog.colors.map((c) => (
            <li key={c.key} className="flex gap-3 border border-line bg-panel p-3">
              <span className="mt-0.5 h-12 w-2 shrink-0" style={{ backgroundColor: `#${c.hex}` }} />
              <span className="min-w-0">
                <span className="flex flex-wrap items-baseline gap-x-2">
                  <span className="font-semibold">{c.name}</span>
                  <span className="text-xs text-muted">{c.group === "基調" ? "基調" : c.group === "従来" ? "従来" : "追加"}</span>
                </span>
                <span className="mt-1 block text-sm">{c.role}</span>
                <span className="mt-1 block text-xs leading-relaxed text-muted">{c.hint}</span>
                <svg viewBox="0 0 120 18" className="mt-2 h-5 w-full max-w-48" aria-hidden="true">
                  <path d="M 2 5 H 40 V 13 H 78" fill="none" stroke={`#${c.hex}`} strokeWidth="1.4" />
                  <path d="M 2 9 H 36 V 14 H 78" fill="none" stroke={`#${c.hex}`} strokeWidth="4.5" strokeOpacity="0.4" strokeLinecap="round" />
                </svg>
              </span>
            </li>
          ))}
        </ul>
      </section>

      <section className="mt-12 grid gap-8 border-t border-line pt-8 md:grid-cols-[14rem_1fr]">
        <div>
          <h2 className="text-xl font-semibold">接続点</h2>
          <AnchorMap />
        </div>
        <div className="max-w-3xl text-sm leading-relaxed text-muted">
          <p>
            四角は各辺を、端から 12.5%、37.5%、62.5%、87.5% の位置で受けます。角には点を置かないので、線が角で重なりません。円は 22.5 度ごと、計16点です。
          </p>
          <p className="mt-3">
            Excelでは図形を Alt を押しながら動かすと升目に吸着します。線の端を図形へ近づけると接続点が青く光ります。曲げは線を選択して黄色いハンドルです。直角はカギ線、なめらかに曲げるときは曲線、回り込みは「直角・迂回」を使います。
          </p>
          <p className="mt-3">
            升目は行高 15pt、列幅 {catalog.colWidth}。表示 100% でほぼ正方形です。フォントは Meiryo UI です。
          </p>
        </div>
      </section>

      <section className="mt-12">
        <h2 className="text-xl font-semibold">シート</h2>
        <ul className="mt-4 divide-y divide-line border-y border-line">
          {catalog.sheets.map((sheet) => (
            <li key={sheet.name} className="grid gap-1 py-3 sm:grid-cols-[11rem_1fr] sm:gap-4">
              <span className="font-semibold">{sheet.name}</span>
              <span className="text-sm text-muted">{sheet.text}</span>
            </li>
          ))}
        </ul>
      </section>
    </main>
  );
}

function SheetButton({
  active,
  onClick,
  children,
}: {
  active: boolean;
  onClick: () => void;
  children: string;
}) {
  return (
    <button
      type="button"
      onClick={onClick}
      aria-pressed={active}
      className={
        active
          ? "min-h-11 bg-ink px-4 text-sm font-semibold text-panel"
          : "min-h-11 border border-line bg-panel px-4 text-sm font-semibold text-ink"
      }
    >
      {children}
    </button>
  );
}
