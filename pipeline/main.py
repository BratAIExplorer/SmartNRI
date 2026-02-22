"""
main.py — SmartNRI Pipeline Orchestrator
Runs: scraper → summarizer → publisher → watchdog

Usage:
  python main.py              # Full run
  python main.py --dry-run    # Scrape only, no HTML injection or alerts
"""

import sys
import logging
from pathlib import Path

LOG_DIR = Path(__file__).resolve().parent.parent / "logs"
LOG_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / "pipeline.log"),
        logging.StreamHandler()
    ]
)
log = logging.getLogger("main")

DRY_RUN = "--dry-run" in sys.argv


def main():
    log.info("=" * 60)
    log.info(f"SmartNRI Pipeline starting {'(DRY RUN)' if DRY_RUN else ''}")
    log.info("=" * 60)

    pipeline_failed = False

    try:
        # Step 1: Scrape
        log.info("STEP 1/3 — Scraper")
        from scraper import run as scrape
        raw_items = scrape()
        log.info(f"  → {len(raw_items)} new items fetched")

        if DRY_RUN:
            log.info("Dry run — stopping after scrape.")
            return

        if not raw_items:
            log.info("No new items — skipping summariser and publisher.")
            from watchdog import run as watchdog
            watchdog(pipeline_failed=False)
            return

        # Step 2: Summarise
        log.info("STEP 2/3 — Summariser")
        from summarizer import run as summarise
        summaries = summarise()
        log.info(f"  → {len(summaries)} summaries produced")

        # Step 3: Publish
        log.info("STEP 3/3 — Publisher")
        from publisher import run as publish
        publish()

    except Exception as e:
        log.error(f"Pipeline FAILED: {e}", exc_info=True)
        pipeline_failed = True

    finally:
        # Watchdog always runs
        log.info("WATCHDOG — Health check")
        from watchdog import run as watchdog
        healthy = watchdog(pipeline_failed=pipeline_failed)
        log.info(f"  → {'✅ Healthy' if healthy else '⚠️ Issues detected'}")
        log.info("Pipeline run complete.")
        sys.exit(1 if pipeline_failed else 0)


if __name__ == "__main__":
    main()
