# hazim-reseller-agent

Hazim Reseller Agent is a production-grade Python CLI designed for high-volume side-hustle resellers on marketplaces like eBay and Etsy. It focuses on local inference, data sovereignty, and deterministic template processing to generate SEO-optimized, high-conversion product descriptions ready for immediate use in listing fields.

## Features

- CLI with `--product`, `--specs` (JSON file or inline JSON string), and `--local-engine` flag.
- Inference Pipeline (Local Engine) that produces structured JSON and marketplace-ready markdown descriptions.
- Deterministic Template Processing fallback and explicit JSON validation hooks.
- Robust logging, error handling, and defensive file ingestion for production use.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/HazemAbabneh/hazim-reseller-agent
   ```
2. Create a virtual environment (recommended):
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # macOS/Linux
   .venv\Scripts\activate     # Windows
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

- **Inline specs example:**
  ```bash
  python hazim_reseller_agent.py --product "Enterprise Network Switch 24-Port" --specs '{"condition":"Refurbished","features":["Gigabit Ethernet","PoE+ Support"],"keywords":["Cisco","Networking","Hardware"]}' --local-engine
  ```

- **From specs file, using local engine:**
  ```bash
  python hazim_reseller_agent.py --product "Rackmount Server Chassis 2U" --specs specs.json --local-engine
  ```

## Architectural advantages

- **Data Sovereignty & Enterprise Privacy:** All processing is designed to run locally. No product data is transmitted to third-party APIs, ensuring compliance with enterprise privacy requirements.
- **Zero Operational Ingestion Fees:** Deterministic Template Processing and local inference remove ongoing API usage costs, improving margins for small resellers.
- **Elimination of Closed API Vendor Lock-in:** The pipeline is model-agnostic and accepts local engines; migrate to any compatible open-weight runtime without migration costs.

## CLI Options

- `--product` (`-p`): Product title/name (required)
- `--specs` (`-s`): Path to a JSON file containing specs or an inline JSON string
- `--local-engine` (`-l`): Use the local inference engine for generation

## Testing

Run the unit tests:
```bash
python -m unittest discover -v
```

## License

MIT
