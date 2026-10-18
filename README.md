# hazim-reseller-agent

Hazim Reseller Agent is a production-grade Python CLI designed for high-volume side-hustle resellers on marketplaces like eBay and Etsy. It focuses on local inference, data sovereignty, and deterministic template processing to generate SEO-optimized, high-conversion product descriptions ready for immediate use in listing fields.

Features
- CLI with `--product`, `--specs` (JSON file or inline JSON string), and `--local-engine` flag.
- Inference Pipeline (Local Engine) that produces structured JSON and marketplace-ready markdown descriptions.
- Deterministic Template Processing fallback and explicit JSON validation hooks.
- Robust logging, error handling, and defensive file ingestion for production use.

Installation
1. Clone the repository:
   git clone https://github.com/HazemAbabneh/open-claw-reseller-agent.git
2. Create a virtual environment (recommended):
   python -m venv .venv
   source .venv/bin/activate   # macOS/Linux
   .\.venv\Scripts\activate    # Windows
3. Install dependencies:
   pip install -r requirements.txt

Usage
- Inline specs example:
  python hazim_reseller_agent.py --product "Samsung S9 Custom ROM" --specs '{"condition":"Used","features":["Custom ROM","Rooted"],"keywords":["Android","Samsung","Custom ROM"]}'

- From specs file, using local engine:
  python hazim_reseller_agent.py --product "Raspberry Pi Zero w/Case" --specs specs.json --local-engine

Architectural advantages
- Data Sovereignty & Enterprise Privacy: All processing is designed to run locally. No product data is transmitted to third-party APIs, ensuring compliance with enterprise privacy requirements.
- Zero Operational Ingestion Fees: Deterministic Template Processing and local inference remove ongoing API usage costs, improving margins for small resellers.
- Elimination of Closed API Vendor Lock-in: The pipeline is model-agnostic and accepts local engines; migrate to any compatible open-weight runtime without migration costs.

CLI
- --product (-p): Product title/name (required)
- --specs (-s): Path to a JSON file containing specs or an inline JSON string
- --local-engine (-l): Use the local inference engine for generation

Testing
Run the unit tests:
  python -m unittest discover -v

License
MIT
