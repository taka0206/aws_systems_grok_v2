import { i as __toESM } from "../_runtime.mjs";
import { K as require_react, b as require_jsx_runtime } from "../_libs/@tanstack/react-router+[...].mjs";
import { n as Download } from "../_libs/lucide-react.mjs";
//#region node_modules/.nitro/vite/services/ssr/assets/routes-CdXGuP_n.js
var import_react = /* @__PURE__ */ __toESM(require_react());
var import_jsx_runtime = require_jsx_runtime();
var catalog = {
	"colors": [
		{
			"key": "sumi",
			"name": "墨",
			"hex": "1C1C1C",
			"role": "標準・未分類・境界",
			"group": "基調",
			"hint": "色を決めない線、枠、補足"
		},
		{
			"key": "ai",
			"name": "藍",
			"hex": "2A4668",
			"role": "イントラ・社内LAN",
			"group": "従来",
			"hint": "拠点間、VPC内の通常通信"
		},
		{
			"key": "suoh",
			"name": "蘇芳",
			"hex": "7C3A3A",
			"role": "外部・インターネット",
			"group": "従来",
			"hint": "公開側、利用者、Ingress"
		},
		{
			"key": "koke",
			"name": "苔",
			"hex": "3C5644",
			"role": "現場・オンプレ",
			"group": "従来",
			"hint": "工場、拠点、閉域の機器"
		},
		{
			"key": "kincha",
			"name": "金茶",
			"hex": "7A5A2C",
			"role": "Salesforce・SaaS",
			"group": "追加",
			"hint": "外部SaaSとの業務連携"
		},
		{
			"key": "murasaki",
			"name": "江戸紫",
			"hex": "53425F",
			"role": "運用・監視・管理",
			"group": "追加",
			"hint": "監視、ログ、運用者の経路"
		},
		{
			"key": "asagi",
			"name": "浅葱",
			"hex": "1F5C58",
			"role": "データ連携・API",
			"group": "追加",
			"hint": "API、バッチ、キュー、DB"
		}
	],
	"colWidth": 2.4297,
	"rowPt": 15,
	"sheets": [
		{
			"name": "00_使い方",
			"text": "手順、升目、7色の約束"
		},
		{
			"name": "01_凡例",
			"text": "図形・本線・上書き線・付記を色別に並べた見本"
		},
		{
			"name": "02_概要図",
			"text": "システム単位。現場、閉域、AWS、SaaSの見取り図"
		},
		{
			"name": "03_詳細図",
			"text": "サブネット、AWSサービス、現場機器"
		},
		{
			"name": "04_部品_概要",
			"text": "大きいノード、領域、図記号。各7色"
		},
		{
			"name": "05_部品_詳細",
			"text": "AWSサービス名つきの小さいノード。各7色"
		},
		{
			"name": "06_線_経路",
			"text": "直線、直角、曲線、破線、双方向"
		},
		{
			"name": "07_線_上書き",
			"text": "半透明の太線。直角、迂回、曲線、S字"
		},
		{
			"name": "08_コメント",
			"text": "付記カード、吹き出し、番号、短ラベル"
		}
	],
	"steps": [
		"概要図か詳細図を開く",
		"部品シートから図形をコピーする",
		"Altを押しながら置くと升目に吸着する",
		"経路線の端を、辺16点のどれかに接続する",
		"黄色いハンドルで直角か曲線に曲げる",
		"下の線を残したまま、上書き線で流れを足す"
	],
	"overview": {
		"cols": 100,
		"rows": 58,
		"title": "02  概要図    サンプルは消して使ってよい    Alt+ドラッグで升目に吸着    線は06    上書きは07    付記は08",
		"shapes": [
			{
				"key": "z_site",
				"title": "現場・工場",
				"sub": "オンプレ",
				"kicker": "SITE",
				"color": "koke",
				"x": 1,
				"y": 2,
				"w": 24,
				"h": 34,
				"dash": "dash",
				"form": "zone"
			},
			{
				"key": "z_intra",
				"title": "拠点閉域",
				"sub": "社内WAN",
				"kicker": "WAN",
				"color": "ai",
				"x": 26,
				"y": 2,
				"w": 16,
				"h": 34,
				"dash": "dash",
				"form": "zone"
			},
			{
				"key": "z_aws",
				"title": "AWS  東京",
				"sub": "アカウント",
				"kicker": "CLOUD",
				"color": "sumi",
				"x": 43,
				"y": 2,
				"w": 36,
				"h": 52,
				"dash": "dash",
				"form": "zone"
			},
			{
				"key": "z_vpc",
				"title": "VPC",
				"sub": "10.0.0.0/16",
				"kicker": "VPC",
				"color": "ai",
				"x": 45,
				"y": 6,
				"w": 32,
				"h": 44,
				"dash": "solid",
				"form": "zone"
			},
			{
				"key": "z_pub",
				"title": "Public",
				"sub": "10.0.1.0/24",
				"kicker": "SUB",
				"color": "suoh",
				"x": 47,
				"y": 10,
				"w": 28,
				"h": 10,
				"dash": "sysDash",
				"form": "zone"
			},
			{
				"key": "z_app",
				"title": "App",
				"sub": "10.0.2.0/24",
				"kicker": "SUB",
				"color": "ai",
				"x": 47,
				"y": 21,
				"w": 28,
				"h": 12,
				"dash": "sysDash",
				"form": "zone"
			},
			{
				"key": "z_data",
				"title": "Data",
				"sub": "10.0.3.0/24",
				"kicker": "SUB",
				"color": "asagi",
				"x": 47,
				"y": 34,
				"w": 28,
				"h": 12,
				"dash": "sysDash",
				"form": "zone"
			},
			{
				"key": "z_saas",
				"title": "外部SaaS",
				"sub": "業務",
				"kicker": "SAAS",
				"color": "kincha",
				"x": 80,
				"y": 2,
				"w": 18,
				"h": 18,
				"dash": "dash",
				"form": "zone"
			},
			{
				"key": "z_users",
				"title": "利用者・外部",
				"sub": "公開側",
				"kicker": "EXT",
				"color": "suoh",
				"x": 80,
				"y": 21,
				"w": 18,
				"h": 24,
				"dash": "dash",
				"form": "zone"
			},
			{
				"key": "factory",
				"title": "工場拠点",
				"kicker": "SITE",
				"sub": "現場",
				"color": "koke",
				"x": 4,
				"y": 6,
				"w": 16,
				"h": 5,
				"form": "node"
			},
			{
				"key": "term",
				"title": "現場端末",
				"kicker": "CLT",
				"sub": "作業",
				"color": "koke",
				"x": 4,
				"y": 13,
				"w": 16,
				"h": 5,
				"form": "node"
			},
			{
				"key": "fw",
				"title": "拠点FW",
				"kicker": "FW",
				"sub": "境界",
				"color": "koke",
				"x": 4,
				"y": 20,
				"w": 16,
				"h": 5,
				"form": "node"
			},
			{
				"key": "odb",
				"title": "オンプレDB",
				"kicker": "DB",
				"sub": "実績",
				"color": "koke",
				"x": 4,
				"y": 27,
				"w": 16,
				"h": 5,
				"form": "node"
			},
			{
				"key": "router",
				"title": "拠点ルータ",
				"kicker": "L3",
				"sub": "閉域",
				"color": "ai",
				"x": 28,
				"y": 7,
				"w": 12,
				"h": 5,
				"form": "node"
			},
			{
				"key": "vpn",
				"title": "VPN",
				"kicker": "VPN",
				"sub": "対AWS",
				"color": "ai",
				"x": 28,
				"y": 16,
				"w": 12,
				"h": 5,
				"form": "node"
			},
			{
				"key": "mon",
				"title": "監視基盤",
				"kicker": "OPS",
				"sub": "死活",
				"color": "murasaki",
				"x": 28,
				"y": 25,
				"w": 12,
				"h": 5,
				"form": "node"
			},
			{
				"key": "alb",
				"title": "ALB",
				"kicker": "ALB",
				"sub": "公開",
				"color": "suoh",
				"x": 49,
				"y": 13,
				"w": 12,
				"h": 4,
				"form": "node"
			},
			{
				"key": "igw",
				"title": "IGW",
				"kicker": "IGW",
				"sub": "入口",
				"color": "suoh",
				"x": 63,
				"y": 13,
				"w": 10,
				"h": 4,
				"form": "node"
			},
			{
				"key": "web",
				"title": "Web",
				"kicker": "EC2",
				"sub": "フロント",
				"color": "ai",
				"x": 49,
				"y": 24,
				"w": 12,
				"h": 4,
				"form": "node"
			},
			{
				"key": "api",
				"title": "API",
				"kicker": "EC2",
				"sub": "業務",
				"color": "ai",
				"x": 63,
				"y": 24,
				"w": 10,
				"h": 4,
				"form": "node"
			},
			{
				"key": "rds",
				"title": "業務DB",
				"kicker": "RDS",
				"sub": "本番",
				"color": "asagi",
				"x": 49,
				"y": 37,
				"w": 12,
				"h": 4,
				"form": "node"
			},
			{
				"key": "s3",
				"title": "証跡",
				"kicker": "S3",
				"sub": "保管",
				"color": "asagi",
				"x": 63,
				"y": 37,
				"w": 10,
				"h": 4,
				"form": "node"
			},
			{
				"key": "sfdc",
				"title": "Salesforce",
				"kicker": "SFDC",
				"sub": "顧客",
				"color": "kincha",
				"x": 82,
				"y": 7,
				"w": 14,
				"h": 5,
				"form": "node"
			},
			{
				"key": "net",
				"title": "Internet",
				"kicker": "",
				"sub": "",
				"color": "suoh",
				"x": 83,
				"y": 24,
				"w": 12,
				"h": 8,
				"form": "ellipse"
			},
			{
				"key": "user",
				"title": "本部利用者",
				"kicker": "",
				"sub": "",
				"color": "suoh",
				"x": 83,
				"y": 34,
				"w": 12,
				"h": 8,
				"form": "ellipse"
			},
			{
				"key": "n1",
				"title": "受注はSalesforce",
				"sub": "金茶でたどる",
				"kicker": "金茶",
				"color": "kincha",
				"x": 82,
				"y": 13,
				"w": 14,
				"h": 5,
				"form": "note"
			},
			{
				"key": "n2",
				"title": "監視は紫",
				"sub": "死活・ログ",
				"kicker": "紫",
				"color": "murasaki",
				"x": 28,
				"y": 31,
				"w": 12,
				"h": 4,
				"form": "note"
			}
		],
		"lines": [
			{
				"a": "factory",
				"ia": 9,
				"b": "term",
				"ib": 1,
				"color": "koke",
				"preset": "bentConnector3",
				"overlay": false,
				"dashed": false
			},
			{
				"a": "term",
				"ia": 9,
				"b": "fw",
				"ib": 1,
				"color": "koke",
				"preset": "bentConnector3",
				"overlay": false,
				"dashed": false
			},
			{
				"a": "fw",
				"ia": 9,
				"b": "odb",
				"ib": 1,
				"color": "koke",
				"preset": "bentConnector3",
				"overlay": false,
				"dashed": false
			},
			{
				"a": "fw",
				"ia": 6,
				"b": "router",
				"ib": 12,
				"color": "koke",
				"preset": "bentConnector3",
				"overlay": false,
				"dashed": false
			},
			{
				"a": "router",
				"ia": 9,
				"b": "vpn",
				"ib": 1,
				"color": "ai",
				"preset": "bentConnector3",
				"overlay": false,
				"dashed": false
			},
			{
				"a": "vpn",
				"ia": 7,
				"b": "alb",
				"ib": 12,
				"color": "ai",
				"preset": "bentConnector3",
				"overlay": false,
				"dashed": false
			},
			{
				"a": "alb",
				"ia": 9,
				"b": "web",
				"ib": 1,
				"color": "ai",
				"preset": "bentConnector3",
				"overlay": false,
				"dashed": false
			},
			{
				"a": "web",
				"ia": 6,
				"b": "api",
				"ib": 13,
				"color": "ai",
				"preset": "bentConnector3",
				"overlay": false,
				"dashed": false
			},
			{
				"a": "api",
				"ia": 10,
				"b": "rds",
				"ib": 2,
				"color": "asagi",
				"preset": "bentConnector3",
				"overlay": false,
				"dashed": false
			},
			{
				"a": "api",
				"ia": 11,
				"b": "s3",
				"ib": 1,
				"color": "asagi",
				"preset": "bentConnector3",
				"overlay": false,
				"dashed": false
			},
			{
				"a": "api",
				"ia": 5,
				"b": "sfdc",
				"ib": 15,
				"color": "kincha",
				"preset": "bentConnector3",
				"overlay": false,
				"dashed": false
			},
			{
				"a": "user",
				"ia": 8,
				"b": "igw",
				"ib": 7,
				"color": "suoh",
				"preset": "bentConnector3",
				"overlay": false,
				"dashed": false
			},
			{
				"a": "igw",
				"ia": 12,
				"b": "alb",
				"ib": 7,
				"color": "suoh",
				"preset": "bentConnector3",
				"overlay": false,
				"dashed": false
			},
			{
				"a": "net",
				"ia": 8,
				"b": "igw",
				"ib": 5,
				"color": "suoh",
				"preset": "bentConnector3",
				"overlay": false,
				"dashed": false
			},
			{
				"a": "mon",
				"ia": 7,
				"b": "web",
				"ib": 12,
				"color": "murasaki",
				"preset": "bentConnector3",
				"overlay": false,
				"dashed": true
			},
			{
				"a": "term",
				"ia": 7,
				"b": "sfdc",
				"ib": 13,
				"color": "kincha",
				"preset": "bentConnector5",
				"overlay": true,
				"dashed": false
			},
			{
				"a": "api",
				"ia": 9,
				"b": "rds",
				"ib": 3,
				"color": "asagi",
				"preset": "curvedConnector3",
				"overlay": true,
				"dashed": false
			}
		]
	},
	"detail": {
		"cols": 132,
		"rows": 62,
		"title": "03  詳細図    VPC・現場機器の単位    Alt+ドラッグで吸着    部品は05    上書きの太線は下の線を消さない",
		"shapes": [
			{
				"key": "dz_site",
				"title": "現場セグメント",
				"sub": "工場LAN",
				"kicker": "OT",
				"color": "koke",
				"x": 1,
				"y": 2,
				"w": 28,
				"h": 46,
				"dash": "dash",
				"form": "zone"
			},
			{
				"key": "dz_wan",
				"title": "閉域・DC",
				"sub": "専用線",
				"kicker": "WAN",
				"color": "ai",
				"x": 30,
				"y": 2,
				"w": 16,
				"h": 46,
				"dash": "dash",
				"form": "zone"
			},
			{
				"key": "dz_aws",
				"title": "AWS ap-northeast-1",
				"sub": "本番アカウント",
				"kicker": "ACCT",
				"color": "sumi",
				"x": 47,
				"y": 2,
				"w": 64,
				"h": 56,
				"dash": "dash",
				"form": "zone"
			},
			{
				"key": "dz_vpc",
				"title": "VPC prod",
				"sub": "10.20.0.0/16",
				"kicker": "VPC",
				"color": "ai",
				"x": 49,
				"y": 6,
				"w": 42,
				"h": 40,
				"dash": "solid",
				"form": "zone"
			},
			{
				"key": "dz_pub",
				"title": "public-a",
				"sub": "10.20.0.0/24",
				"kicker": "SUB",
				"color": "suoh",
				"x": 51,
				"y": 9,
				"w": 38,
				"h": 9,
				"dash": "sysDash",
				"form": "zone"
			},
			{
				"key": "dz_app",
				"title": "app-a",
				"sub": "10.20.1.0/24",
				"kicker": "SUB",
				"color": "ai",
				"x": 51,
				"y": 19,
				"w": 38,
				"h": 12,
				"dash": "sysDash",
				"form": "zone"
			},
			{
				"key": "dz_data",
				"title": "data-a",
				"sub": "10.20.2.0/24",
				"kicker": "SUB",
				"color": "asagi",
				"x": 51,
				"y": 32,
				"w": 38,
				"h": 11,
				"dash": "sysDash",
				"form": "zone"
			},
			{
				"key": "dz_ops",
				"title": "共通サービス",
				"sub": "アカウント共通",
				"kicker": "OPS",
				"color": "murasaki",
				"x": 92,
				"y": 8,
				"w": 16,
				"h": 36,
				"dash": "sysDash",
				"form": "zone"
			},
			{
				"key": "dz_saas",
				"title": "SaaS",
				"sub": "業務",
				"kicker": "SAAS",
				"color": "kincha",
				"x": 112,
				"y": 2,
				"w": 18,
				"h": 20,
				"dash": "dash",
				"form": "zone"
			},
			{
				"key": "dz_ext",
				"title": "外部",
				"sub": "インターネット",
				"kicker": "EXT",
				"color": "suoh",
				"x": 112,
				"y": 24,
				"w": 18,
				"h": 22,
				"dash": "dash",
				"form": "zone"
			},
			{
				"key": "plc",
				"title": "PLC",
				"kicker": "OT",
				"sub": "",
				"color": "koke",
				"x": 3,
				"y": 6,
				"w": 10,
				"h": 3,
				"form": "node",
				"large": false
			},
			{
				"key": "sensor",
				"title": "センサ",
				"kicker": "OT",
				"sub": "",
				"color": "koke",
				"x": 15,
				"y": 6,
				"w": 10,
				"h": 3,
				"form": "node",
				"large": false
			},
			{
				"key": "hist",
				"title": "ヒストリアン",
				"kicker": "SRV",
				"sub": "",
				"color": "koke",
				"x": 3,
				"y": 12,
				"w": 10,
				"h": 3,
				"form": "node",
				"large": false
			},
			{
				"key": "scada",
				"title": "SCADA",
				"kicker": "SRV",
				"sub": "",
				"color": "koke",
				"x": 15,
				"y": 12,
				"w": 10,
				"h": 3,
				"form": "node",
				"large": false
			},
			{
				"key": "sfw",
				"title": "現場FW",
				"kicker": "FW",
				"sub": "",
				"color": "koke",
				"x": 3,
				"y": 18,
				"w": 10,
				"h": 3,
				"form": "node",
				"large": false
			},
			{
				"key": "l3",
				"title": "L3スイッチ",
				"kicker": "L3",
				"sub": "",
				"color": "koke",
				"x": 15,
				"y": 18,
				"w": 10,
				"h": 3,
				"form": "node",
				"large": false
			},
			{
				"key": "fs",
				"title": "ファイル",
				"kicker": "STR",
				"sub": "図面",
				"color": "koke",
				"x": 3,
				"y": 24,
				"w": 10,
				"h": 3,
				"form": "node",
				"large": false
			},
			{
				"key": "hmi",
				"title": "現場端末",
				"kicker": "CLT",
				"sub": "",
				"color": "koke",
				"x": 15,
				"y": 24,
				"w": 10,
				"h": 3,
				"form": "node",
				"large": false
			},
			{
				"key": "rt",
				"title": "拠点ルータ",
				"kicker": "L3",
				"sub": "",
				"color": "ai",
				"x": 32,
				"y": 8,
				"w": 12,
				"h": 3,
				"form": "node",
				"large": false
			},
			{
				"key": "vpn2",
				"title": "VPN GW",
				"kicker": "VPN",
				"sub": "",
				"color": "ai",
				"x": 32,
				"y": 16,
				"w": 12,
				"h": 3,
				"form": "node",
				"large": false
			},
			{
				"key": "dx",
				"title": "Direct Connect",
				"kicker": "DX",
				"sub": "",
				"color": "ai",
				"x": 32,
				"y": 24,
				"w": 12,
				"h": 3,
				"form": "node",
				"large": false
			},
			{
				"key": "proxy",
				"title": "Proxy",
				"kicker": "SRV",
				"sub": "",
				"color": "ai",
				"x": 32,
				"y": 32,
				"w": 12,
				"h": 3,
				"form": "node",
				"large": false
			},
			{
				"key": "igw2",
				"title": "IGW",
				"kicker": "IGW",
				"sub": "",
				"color": "suoh",
				"x": 53,
				"y": 12,
				"w": 8,
				"h": 3,
				"form": "node",
				"large": false
			},
			{
				"key": "waf",
				"title": "WAF",
				"kicker": "WAF",
				"sub": "",
				"color": "suoh",
				"x": 63,
				"y": 12,
				"w": 8,
				"h": 3,
				"form": "node",
				"large": false
			},
			{
				"key": "alb2",
				"title": "ALB",
				"kicker": "ALB",
				"sub": "",
				"color": "suoh",
				"x": 73,
				"y": 12,
				"w": 8,
				"h": 3,
				"form": "node",
				"large": false
			},
			{
				"key": "nat",
				"title": "NAT",
				"kicker": "NAT",
				"sub": "",
				"color": "ai",
				"x": 83,
				"y": 12,
				"w": 5,
				"h": 3,
				"form": "node",
				"large": false
			},
			{
				"key": "ec2w",
				"title": "Web",
				"kicker": "EC2",
				"sub": "",
				"color": "ai",
				"x": 53,
				"y": 23,
				"w": 8,
				"h": 3,
				"form": "node",
				"large": false
			},
			{
				"key": "ec2a",
				"title": "API",
				"kicker": "EC2",
				"sub": "",
				"color": "ai",
				"x": 63,
				"y": 23,
				"w": 8,
				"h": 3,
				"form": "node",
				"large": false
			},
			{
				"key": "ecs",
				"title": "Worker",
				"kicker": "ECS",
				"sub": "",
				"color": "ai",
				"x": 73,
				"y": 23,
				"w": 8,
				"h": 3,
				"form": "node",
				"large": false
			},
			{
				"key": "lam",
				"title": "Webhook",
				"kicker": "Lambda",
				"sub": "",
				"color": "asagi",
				"x": 83,
				"y": 23,
				"w": 5,
				"h": 3,
				"form": "node",
				"large": false
			},
			{
				"key": "rds2",
				"title": "Aurora",
				"kicker": "RDS",
				"sub": "",
				"color": "asagi",
				"x": 53,
				"y": 36,
				"w": 8,
				"h": 3,
				"form": "node",
				"large": false
			},
			{
				"key": "cache",
				"title": "Cache",
				"kicker": "ElastiCache",
				"sub": "",
				"color": "asagi",
				"x": 63,
				"y": 36,
				"w": 8,
				"h": 3,
				"form": "node",
				"large": false
			},
			{
				"key": "s3b",
				"title": "Bucket",
				"kicker": "S3",
				"sub": "",
				"color": "asagi",
				"x": 73,
				"y": 36,
				"w": 8,
				"h": 3,
				"form": "node",
				"large": false
			},
			{
				"key": "sqs",
				"title": "Queue",
				"kicker": "SQS",
				"sub": "",
				"color": "asagi",
				"x": 83,
				"y": 36,
				"w": 5,
				"h": 3,
				"form": "node",
				"large": false
			},
			{
				"key": "cw",
				"title": "CloudWatch",
				"kicker": "OPS",
				"sub": "",
				"color": "murasaki",
				"x": 94,
				"y": 12,
				"w": 12,
				"h": 3,
				"form": "node",
				"large": false
			},
			{
				"key": "iam",
				"title": "IAM",
				"kicker": "IAM",
				"sub": "",
				"color": "murasaki",
				"x": 94,
				"y": 18,
				"w": 12,
				"h": 3,
				"form": "node",
				"large": false
			},
			{
				"key": "trail",
				"title": "CloudTrail",
				"kicker": "OPS",
				"sub": "",
				"color": "murasaki",
				"x": 94,
				"y": 24,
				"w": 12,
				"h": 3,
				"form": "node",
				"large": false
			},
			{
				"key": "r53",
				"title": "Route 53",
				"kicker": "DNS",
				"sub": "",
				"color": "suoh",
				"x": 94,
				"y": 30,
				"w": 12,
				"h": 3,
				"form": "node",
				"large": false
			},
			{
				"key": "sfn",
				"title": "Step Functions",
				"kicker": "SFN",
				"sub": "",
				"color": "asagi",
				"x": 94,
				"y": 36,
				"w": 12,
				"h": 3,
				"form": "node",
				"large": false
			},
			{
				"key": "sfdc2",
				"title": "Salesforce",
				"kicker": "SFDC",
				"sub": "",
				"color": "kincha",
				"x": 114,
				"y": 8,
				"w": 14,
				"h": 4,
				"form": "node",
				"large": false
			},
			{
				"key": "inet",
				"title": "Internet",
				"kicker": "",
				"sub": "",
				"color": "suoh",
				"x": 115,
				"y": 28,
				"w": 12,
				"h": 8,
				"form": "ellipse",
				"large": false
			},
			{
				"key": "hq",
				"title": "本部ユーザ",
				"kicker": "",
				"sub": "",
				"color": "suoh",
				"x": 115,
				"y": 38,
				"w": 12,
				"h": 6,
				"form": "ellipse",
				"large": false
			},
			{
				"key": "dn1",
				"title": "マスタはSalesforce",
				"sub": "金茶の太線が業務の流れ",
				"kicker": "金茶",
				"color": "kincha",
				"x": 114,
				"y": 14,
				"w": 14,
				"h": 5,
				"form": "note"
			},
			{
				"key": "dn2",
				"title": "データは浅葱",
				"sub": "API・DB・キュー",
				"kicker": "浅葱",
				"color": "asagi",
				"x": 53,
				"y": 40,
				"w": 14,
				"h": 4,
				"form": "note"
			},
			{
				"key": "dn3",
				"title": "監視は紫の破線",
				"sub": "本線と混ぜない",
				"kicker": "紫",
				"color": "murasaki",
				"x": 94,
				"y": 42,
				"w": 12,
				"h": 4,
				"form": "label"
			}
		],
		"lines": [
			{
				"a": "plc",
				"ia": 9,
				"b": "hist",
				"ib": 1,
				"color": "koke",
				"preset": "bentConnector3",
				"overlay": false,
				"dashed": false
			},
			{
				"a": "sensor",
				"ia": 9,
				"b": "scada",
				"ib": 1,
				"color": "koke",
				"preset": "bentConnector3",
				"overlay": false,
				"dashed": false
			},
			{
				"a": "hist",
				"ia": 9,
				"b": "sfw",
				"ib": 1,
				"color": "koke",
				"preset": "bentConnector3",
				"overlay": false,
				"dashed": false
			},
			{
				"a": "scada",
				"ia": 9,
				"b": "l3",
				"ib": 1,
				"color": "koke",
				"preset": "bentConnector3",
				"overlay": false,
				"dashed": false
			},
			{
				"a": "sfw",
				"ia": 7,
				"b": "rt",
				"ib": 12,
				"color": "koke",
				"preset": "bentConnector3",
				"overlay": false,
				"dashed": false
			},
			{
				"a": "rt",
				"ia": 9,
				"b": "vpn2",
				"ib": 1,
				"color": "ai",
				"preset": "bentConnector3",
				"overlay": false,
				"dashed": false
			},
			{
				"a": "vpn2",
				"ia": 7,
				"b": "nat",
				"ib": 12,
				"color": "ai",
				"preset": "bentConnector3",
				"overlay": false,
				"dashed": false
			},
			{
				"a": "dx",
				"ia": 6,
				"b": "ec2a",
				"ib": 12,
				"color": "ai",
				"preset": "bentConnector3",
				"overlay": false,
				"dashed": false
			},
			{
				"a": "inet",
				"ia": 8,
				"b": "igw2",
				"ib": 4,
				"color": "suoh",
				"preset": "bentConnector3",
				"overlay": false,
				"dashed": false
			},
			{
				"a": "hq",
				"ia": 12,
				"b": "r53",
				"ib": 7,
				"color": "suoh",
				"preset": "bentConnector3",
				"overlay": false,
				"dashed": false
			},
			{
				"a": "igw2",
				"ia": 6,
				"b": "waf",
				"ib": 13,
				"color": "suoh",
				"preset": "bentConnector3",
				"overlay": false,
				"dashed": false
			},
			{
				"a": "waf",
				"ia": 6,
				"b": "alb2",
				"ib": 13,
				"color": "suoh",
				"preset": "bentConnector3",
				"overlay": false,
				"dashed": false
			},
			{
				"a": "alb2",
				"ia": 9,
				"b": "ec2w",
				"ib": 3,
				"color": "ai",
				"preset": "bentConnector3",
				"overlay": false,
				"dashed": false
			},
			{
				"a": "ec2w",
				"ia": 6,
				"b": "ec2a",
				"ib": 13,
				"color": "ai",
				"preset": "bentConnector3",
				"overlay": false,
				"dashed": false
			},
			{
				"a": "ec2a",
				"ia": 6,
				"b": "ecs",
				"ib": 13,
				"color": "ai",
				"preset": "bentConnector3",
				"overlay": false,
				"dashed": false
			},
			{
				"a": "ec2a",
				"ia": 10,
				"b": "rds2",
				"ib": 2,
				"color": "asagi",
				"preset": "bentConnector3",
				"overlay": false,
				"dashed": false
			},
			{
				"a": "ec2a",
				"ia": 11,
				"b": "cache",
				"ib": 1,
				"color": "asagi",
				"preset": "bentConnector3",
				"overlay": false,
				"dashed": false
			},
			{
				"a": "ecs",
				"ia": 10,
				"b": "sqs",
				"ib": 2,
				"color": "asagi",
				"preset": "bentConnector3",
				"overlay": false,
				"dashed": false
			},
			{
				"a": "lam",
				"ia": 7,
				"b": "sfn",
				"ib": 12,
				"color": "asagi",
				"preset": "bentConnector3",
				"overlay": false,
				"dashed": false
			},
			{
				"a": "ec2a",
				"ia": 5,
				"b": "sfdc2",
				"ib": 15,
				"color": "kincha",
				"preset": "bentConnector3",
				"overlay": false,
				"dashed": false
			},
			{
				"a": "cw",
				"ia": 12,
				"b": "ecs",
				"ib": 7,
				"color": "murasaki",
				"preset": "bentConnector3",
				"overlay": false,
				"dashed": true
			},
			{
				"a": "plc",
				"ia": 7,
				"b": "sfdc2",
				"ib": 13,
				"color": "kincha",
				"preset": "bentConnector5",
				"overlay": true,
				"dashed": false
			},
			{
				"a": "ec2a",
				"ia": 9,
				"b": "rds2",
				"ib": 3,
				"color": "asagi",
				"preset": "curvedConnector3",
				"overlay": true,
				"dashed": false
			},
			{
				"a": "inet",
				"ia": 12,
				"b": "alb2",
				"ib": 3,
				"color": "suoh",
				"preset": "bentConnector3",
				"overlay": true,
				"dashed": false
			}
		]
	}
};
var FRACS = [
	.125,
	.375,
	.625,
	.875
];
var colorOf = Object.fromEntries(catalog.colors.map((c) => [c.key, c.hex]));
function endpoint(shape, idx) {
	if (shape.form === "ellipse") {
		const rad = idx * 22.5 * Math.PI / 180;
		const cx = shape.x + shape.w / 2;
		const cy = shape.y + shape.h / 2;
		return [cx + shape.w / 2 * Math.cos(rad), cy + shape.h / 2 * Math.sin(rad)];
	}
	const side = Math.floor(idx / 4);
	const f = FRACS[idx % 4] ?? .5;
	if (side === 0) return [shape.x + shape.w * f, shape.y];
	if (side === 1) return [shape.x + shape.w, shape.y + shape.h * f];
	if (side === 2) return [shape.x + shape.w * f, shape.y + shape.h];
	return [shape.x, shape.y + shape.h * f];
}
function route(line, byKey) {
	const a = byKey.get(line.a);
	const b = byKey.get(line.b);
	if (!a || !b) return "";
	const [x1, y1] = endpoint(a, line.ia);
	const [x2, y2] = endpoint(b, line.ib);
	if (line.preset.startsWith("curved")) return `M ${x1} ${y1} Q ${x1} ${y2} ${x2} ${y2}`;
	if (line.preset === "bentConnector5") {
		const xA = x1 + (x2 - x1) * .33;
		const xB = x1 + (x2 - x1) * .66;
		return `M ${x1} ${y1} H ${xA} V ${y1 + (y2 - y1) * .5} H ${xB} V ${y2} H ${x2}`;
	}
	if (line.preset === "straightConnector1") return `M ${x1} ${y1} L ${x2} ${y2}`;
	return `M ${x1} ${y1} H ${(x1 + x2) / 2} V ${y2} H ${x2}`;
}
function SheetPreview({ board, cell = 11 }) {
	const byKey = new Map(board.shapes.map((s) => [s.key, s]));
	const width = board.cols * cell;
	const height = board.rows * cell;
	const zones = board.shapes.filter((s) => s.form === "zone");
	const nodes = board.shapes.filter((s) => s.form !== "zone" && s.form !== "note" && s.form !== "label");
	const notes = board.shapes.filter((s) => s.form === "note" || s.form === "label");
	const base = board.lines.filter((l) => !l.overlay);
	const over = board.lines.filter((l) => l.overlay);
	return /* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
		className: "min-w-0 max-w-full overflow-x-auto rounded-card border border-line bg-panel",
		children: /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("svg", {
			width,
			height,
			viewBox: `0 0 ${board.cols} ${board.rows}`,
			role: "img",
			"aria-label": board.title,
			className: "block",
			children: [
				/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("defs", { children: [
					/* @__PURE__ */ (0, import_jsx_runtime.jsx)("pattern", {
						id: "minor",
						width: "1",
						height: "1",
						patternUnits: "userSpaceOnUse",
						children: /* @__PURE__ */ (0, import_jsx_runtime.jsx)("path", {
							d: "M 1 0 L 0 0 0 1",
							fill: "none",
							stroke: "var(--color-line)",
							strokeWidth: "0.03"
						})
					}),
					/* @__PURE__ */ (0, import_jsx_runtime.jsx)("pattern", {
						id: "major",
						width: "5",
						height: "5",
						patternUnits: "userSpaceOnUse",
						children: /* @__PURE__ */ (0, import_jsx_runtime.jsx)("path", {
							d: "M 5 0 L 0 0 0 5",
							fill: "none",
							stroke: "var(--color-major)",
							strokeWidth: "0.06"
						})
					}),
					catalog.colors.map((c) => /* @__PURE__ */ (0, import_jsx_runtime.jsx)("marker", {
						id: `arrow-${c.key}`,
						viewBox: "0 0 10 10",
						refX: "9",
						refY: "5",
						markerWidth: "5",
						markerHeight: "5",
						orient: "auto-start-reverse",
						children: /* @__PURE__ */ (0, import_jsx_runtime.jsx)("path", {
							d: "M 0 0 L 10 5 L 0 10 z",
							fill: `#${c.hex}`
						})
					}, c.key))
				] }),
				/* @__PURE__ */ (0, import_jsx_runtime.jsx)("rect", {
					width: board.cols,
					height: board.rows,
					fill: "url(#minor)"
				}),
				/* @__PURE__ */ (0, import_jsx_runtime.jsx)("rect", {
					width: board.cols,
					height: board.rows,
					fill: "url(#major)"
				}),
				/* @__PURE__ */ (0, import_jsx_runtime.jsx)("rect", {
					width: board.cols,
					height: "1.15",
					fill: "var(--color-ink)"
				}),
				/* @__PURE__ */ (0, import_jsx_runtime.jsx)("text", {
					x: "0.6",
					y: "0.82",
					fill: "var(--color-panel)",
					fontSize: "0.62",
					fontFamily: "var(--font-sans)",
					children: board.title
				}),
				zones.map((s) => /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("g", { children: [
					/* @__PURE__ */ (0, import_jsx_runtime.jsx)("rect", {
						x: s.x + .08,
						y: s.y + .08,
						width: s.w - .16,
						height: s.h - .16,
						rx: "0.35",
						fill: `#${colorOf[s.color]}`,
						fillOpacity: "0.07",
						stroke: `#${colorOf[s.color]}`,
						strokeWidth: "0.08",
						strokeDasharray: s.dash === "solid" ? void 0 : "0.45 0.28"
					}),
					/* @__PURE__ */ (0, import_jsx_runtime.jsx)("text", {
						x: s.x + .7,
						y: s.y + 1.35,
						fill: `#${colorOf[s.color]}`,
						fontSize: "0.72",
						fontWeight: "700",
						fontFamily: "var(--font-sans)",
						children: s.kicker
					}),
					/* @__PURE__ */ (0, import_jsx_runtime.jsx)("text", {
						x: s.x + .7,
						y: s.y + 2.35,
						fill: "var(--color-ink)",
						fontSize: "0.95",
						fontWeight: "700",
						fontFamily: "var(--font-sans)",
						children: s.title
					})
				] }, s.key)),
				nodes.map((s) => s.form === "ellipse" ? /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("g", { children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("ellipse", {
					cx: s.x + s.w / 2,
					cy: s.y + s.h / 2,
					rx: s.w / 2 - .08,
					ry: s.h / 2 - .08,
					fill: "var(--color-panel)",
					stroke: `#${colorOf[s.color]}`,
					strokeWidth: "0.1"
				}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("text", {
					x: s.x + s.w / 2,
					y: s.y + s.h / 2 + .3,
					textAnchor: "middle",
					fill: "var(--color-ink)",
					fontSize: "0.85",
					fontWeight: "700",
					fontFamily: "var(--font-sans)",
					children: s.title
				})] }, s.key) : /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("g", { children: [
					/* @__PURE__ */ (0, import_jsx_runtime.jsx)("rect", {
						x: s.x + .06,
						y: s.y + .06,
						width: s.w - .12,
						height: s.h - .12,
						rx: "0.28",
						fill: "var(--color-panel)",
						stroke: `#${colorOf[s.color]}`,
						strokeWidth: "0.09"
					}),
					/* @__PURE__ */ (0, import_jsx_runtime.jsx)("rect", {
						x: s.x + .06,
						y: s.y + .28,
						width: "0.28",
						height: Math.max(.4, s.h - .56),
						fill: `#${colorOf[s.color]}`
					}),
					s.kicker ? /* @__PURE__ */ (0, import_jsx_runtime.jsx)("text", {
						x: s.x + .7,
						y: s.y + 1.35,
						fill: `#${colorOf[s.color]}`,
						fontSize: "0.62",
						fontWeight: "700",
						fontFamily: "var(--font-sans)",
						children: s.kicker
					}) : null,
					/* @__PURE__ */ (0, import_jsx_runtime.jsx)("text", {
						x: s.x + .7,
						y: s.y + (s.kicker ? 2.45 : 1.8),
						fill: "var(--color-ink)",
						fontSize: "0.85",
						fontWeight: "700",
						fontFamily: "var(--font-sans)",
						children: s.title
					})
				] }, s.key)),
				base.map((line, i) => /* @__PURE__ */ (0, import_jsx_runtime.jsx)("path", {
					d: route(line, byKey),
					fill: "none",
					stroke: `#${colorOf[line.color]}`,
					strokeWidth: "0.14",
					strokeLinejoin: "miter",
					strokeDasharray: line.dashed ? "0.45 0.28" : void 0,
					markerEnd: `url(#arrow-${line.color})`
				}, `b${i}`)),
				over.map((line, i) => /* @__PURE__ */ (0, import_jsx_runtime.jsx)("path", {
					d: route(line, byKey),
					fill: "none",
					stroke: `#${colorOf[line.color]}`,
					strokeWidth: "0.55",
					strokeOpacity: "0.42",
					strokeLinecap: "round",
					strokeLinejoin: "round",
					markerEnd: `url(#arrow-${line.color})`
				}, `o${i}`)),
				notes.map((s) => /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("g", { children: [
					/* @__PURE__ */ (0, import_jsx_runtime.jsx)("rect", {
						x: s.x + .06,
						y: s.y + .06,
						width: s.w - .12,
						height: s.h - .12,
						rx: "0.25",
						fill: "var(--color-panel)",
						stroke: `#${colorOf[s.color]}`,
						strokeWidth: "0.08"
					}),
					/* @__PURE__ */ (0, import_jsx_runtime.jsx)("rect", {
						x: s.x + .06,
						y: s.y + .06,
						width: s.w - .12,
						height: "0.36",
						fill: `#${colorOf[s.color]}`
					}),
					/* @__PURE__ */ (0, import_jsx_runtime.jsx)("text", {
						x: s.x + .5,
						y: s.y + 1.5,
						fill: "var(--color-ink)",
						fontSize: "0.78",
						fontWeight: "700",
						fontFamily: "var(--font-sans)",
						children: s.title
					}),
					s.sub ? /* @__PURE__ */ (0, import_jsx_runtime.jsx)("text", {
						x: s.x + .5,
						y: s.y + 2.45,
						fill: "var(--color-muted)",
						fontSize: "0.62",
						fontFamily: "var(--font-sans)",
						children: s.sub
					}) : null
				] }, s.key))
			]
		})
	});
}
function AnchorMap() {
	const dots = FRACS.flatMap((f, i) => [
		{
			x: 10 + 60 * f,
			y: 8,
			id: `t${i}`
		},
		{
			x: 70,
			y: 8 + 28 * f,
			id: `r${i}`
		},
		{
			x: 10 + 60 * f,
			y: 36,
			id: `b${i}`
		},
		{
			x: 10,
			y: 8 + 28 * f,
			id: `l${i}`
		}
	]);
	return /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("svg", {
		viewBox: "0 0 80 46",
		className: "h-36 w-full max-w-64",
		"aria-hidden": "true",
		children: [
			/* @__PURE__ */ (0, import_jsx_runtime.jsx)("rect", {
				x: "10",
				y: "8",
				width: "60",
				height: "28",
				rx: "2",
				fill: "var(--color-panel)",
				stroke: "var(--color-ink)",
				strokeWidth: "0.8"
			}),
			/* @__PURE__ */ (0, import_jsx_runtime.jsx)("rect", {
				x: "10",
				y: "10",
				width: "2.2",
				height: "24",
				fill: "var(--color-ink)"
			}),
			dots.map((d) => /* @__PURE__ */ (0, import_jsx_runtime.jsx)("circle", {
				cx: d.x,
				cy: d.y,
				r: "1.15",
				fill: "var(--color-ink)"
			}, d.id))
		]
	});
}
function Home() {
	const [which, setWhich] = (0, import_react.useState)("overview");
	const board = which === "overview" ? catalog.overview : catalog.detail;
	return /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("main", {
		className: "mx-auto w-full max-w-6xl overflow-x-hidden px-4 py-8 sm:px-6 sm:py-12",
		children: [
			/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("header", {
				className: "border-b border-ink pb-6",
				children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("p", {
					className: "text-sm tracking-widest text-muted",
					children: "EXCEL TEMPLATE"
				}), /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
					className: "mt-3 flex flex-col gap-6 lg:flex-row lg:items-end lg:justify-between",
					children: [/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
						className: "max-w-2xl",
						children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("h1", {
							className: "text-3xl font-semibold tracking-tight sm:text-4xl",
							children: "システム構成図"
						}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("p", {
							className: "mt-3 text-base leading-relaxed text-muted",
							children: "現場、社内、AWS、外部SaaSを一枚に置くための方眼テンプレートです。図形は升目に吸着し、四角の接続点は各辺4つ、計16。経路は墨を含む7色で揃えます。"
						})]
					}), /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("a", {
						href: "/system-architecture-template.xlsx",
						download: "システム構成図テンプレート.xlsx",
						className: "inline-flex min-h-11 items-center justify-center gap-2 bg-ink px-5 py-3 text-sm font-semibold text-panel",
						children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)(Download, {
							className: "size-4",
							"aria-hidden": "true"
						}), "Excelをダウンロード"]
					})]
				})]
			}),
			/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("section", {
				className: "mt-8 grid gap-8 lg:grid-cols-[16rem_minmax(0,1fr)]",
				children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("ol", {
					className: "space-y-3 text-sm leading-relaxed",
					children: catalog.steps.map((step, i) => /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("li", {
						className: "flex gap-3",
						children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", {
							className: "mt-0.5 flex size-6 shrink-0 items-center justify-center bg-ink text-xs font-semibold text-panel",
							children: i + 1
						}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", { children: step })]
					}, step))
				}), /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
					className: "min-w-0",
					children: [/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
						className: "mb-3 flex flex-wrap gap-2",
						children: [
							/* @__PURE__ */ (0, import_jsx_runtime.jsx)(SheetButton, {
								active: which === "overview",
								onClick: () => setWhich("overview"),
								children: "概要図"
							}),
							/* @__PURE__ */ (0, import_jsx_runtime.jsx)(SheetButton, {
								active: which === "detail",
								onClick: () => setWhich("detail"),
								children: "詳細図"
							}),
							/* @__PURE__ */ (0, import_jsx_runtime.jsx)("p", {
								className: "self-center text-xs text-muted",
								children: "横にスクロールできます。太い半透明が上書き線です。"
							})
						]
					}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)(SheetPreview, { board })]
				})]
			}),
			/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("section", {
				className: "mt-12",
				children: [
					/* @__PURE__ */ (0, import_jsx_runtime.jsx)("h2", {
						className: "text-xl font-semibold",
						children: "経路は7色だけ"
					}),
					/* @__PURE__ */ (0, import_jsx_runtime.jsx)("p", {
						className: "mt-2 max-w-3xl text-sm leading-relaxed text-muted",
						children: "基調は墨。従来の藍・蘇芳・苔に、金茶・江戸紫・浅葱を足しています。図形の左帯、本線、上書き線、付記を同じ色にします。上書き線は白を混ぜた半透明の太線で、すでに引いてある線を消しません。"
					}),
					/* @__PURE__ */ (0, import_jsx_runtime.jsx)("ul", {
						className: "mt-5 grid gap-3 sm:grid-cols-2",
						children: catalog.colors.map((c) => /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("li", {
							className: "flex gap-3 border border-line bg-panel p-3",
							children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", {
								className: "mt-0.5 h-12 w-2 shrink-0",
								style: { backgroundColor: `#${c.hex}` }
							}), /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("span", {
								className: "min-w-0",
								children: [
									/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("span", {
										className: "flex flex-wrap items-baseline gap-x-2",
										children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", {
											className: "font-semibold",
											children: c.name
										}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", {
											className: "text-xs text-muted",
											children: c.group === "基調" ? "基調" : c.group === "従来" ? "従来" : "追加"
										})]
									}),
									/* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", {
										className: "mt-1 block text-sm",
										children: c.role
									}),
									/* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", {
										className: "mt-1 block text-xs leading-relaxed text-muted",
										children: c.hint
									}),
									/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("svg", {
										viewBox: "0 0 120 18",
										className: "mt-2 h-5 w-full max-w-48",
										"aria-hidden": "true",
										children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("path", {
											d: "M 2 5 H 40 V 13 H 78",
											fill: "none",
											stroke: `#${c.hex}`,
											strokeWidth: "1.4"
										}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("path", {
											d: "M 2 9 H 36 V 14 H 78",
											fill: "none",
											stroke: `#${c.hex}`,
											strokeWidth: "4.5",
											strokeOpacity: "0.4",
											strokeLinecap: "round"
										})]
									})
								]
							})]
						}, c.key))
					})
				]
			}),
			/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("section", {
				className: "mt-12 grid gap-8 border-t border-line pt-8 md:grid-cols-[14rem_1fr]",
				children: [/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", { children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("h2", {
					className: "text-xl font-semibold",
					children: "接続点"
				}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)(AnchorMap, {})] }), /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
					className: "max-w-3xl text-sm leading-relaxed text-muted",
					children: [
						/* @__PURE__ */ (0, import_jsx_runtime.jsx)("p", { children: "四角は各辺を、端から 12.5%、37.5%、62.5%、87.5% の位置で受けます。角には点を置かないので、線が角で重なりません。円は 22.5 度ごと、計16点です。" }),
						/* @__PURE__ */ (0, import_jsx_runtime.jsx)("p", {
							className: "mt-3",
							children: "Excelでは図形を Alt を押しながら動かすと升目に吸着します。線の端を図形へ近づけると接続点が青く光ります。曲げは線を選択して黄色いハンドルです。直角はカギ線、なめらかに曲げるときは曲線、回り込みは「直角・迂回」を使います。"
						}),
						/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("p", {
							className: "mt-3",
							children: [
								"升目は行高 15pt、列幅 ",
								catalog.colWidth,
								"。表示 100% でほぼ正方形です。フォントは Meiryo UI です。"
							]
						})
					]
				})]
			}),
			/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("section", {
				className: "mt-12",
				children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("h2", {
					className: "text-xl font-semibold",
					children: "シート"
				}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("ul", {
					className: "mt-4 divide-y divide-line border-y border-line",
					children: catalog.sheets.map((sheet) => /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("li", {
						className: "grid gap-1 py-3 sm:grid-cols-[11rem_1fr] sm:gap-4",
						children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", {
							className: "font-semibold",
							children: sheet.name
						}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", {
							className: "text-sm text-muted",
							children: sheet.text
						})]
					}, sheet.name))
				})]
			})
		]
	});
}
function SheetButton({ active, onClick, children }) {
	return /* @__PURE__ */ (0, import_jsx_runtime.jsx)("button", {
		type: "button",
		onClick,
		"aria-pressed": active,
		className: active ? "min-h-11 bg-ink px-4 text-sm font-semibold text-panel" : "min-h-11 border border-line bg-panel px-4 text-sm font-semibold text-ink",
		children
	});
}
//#endregion
export { Home as component };
