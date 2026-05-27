from agents.marketing_agent import MarketingAgent
from agents.enrichment_agent import EnrichmentAgent
from agents.audit_agent import AuditAgent
from agents.sales_agent import SalesAgent


def run_marketing_stage():

    print("\n==============================")
    print("STAGE 1: MARKETING AGENT")
    print("==============================")

    agent = MarketingAgent()

    agent.run()

    print("\nMarketing stage completed")


def run_enrichment_stage():

    print("\n==============================")
    print("STAGE 2: ENRICHMENT AGENT")
    print("==============================")

    agent = EnrichmentAgent()

    agent.run()

    print("\nEnrichment stage completed")


def run_audit_stage():

    print("\n==============================")
    print("STAGE 3: AUDIT AGENT")
    print("==============================")

    agent = AuditAgent()

    agent.run()

    print("\nAudit stage completed")


def run_sales_stage():

    print("\n==============================")
    print("STAGE 4: SALES AGENT")
    print("==============================")

    agent = SalesAgent()

    agent.run()

    print("\nSales stage completed")


def main():

    print("\n======================================")
    print("STARTING AI GIG HUNTER PIPELINE")
    print("======================================")

    # ==================================
    # STAGE 1 — SCRAPE LEADS
    # ==================================

    try:

        run_marketing_stage()

    except Exception as e:

        print("\nMarketing stage failed")
        print(str(e))

    # ==================================
    # STAGE 2 — ENRICH LEADS
    # ==================================

    try:

        run_enrichment_stage()

    except Exception as e:

        print("\nEnrichment stage failed")
        print(str(e))

    # ==================================
    # STAGE 3 — AUDIT WEBSITES
    # ==================================

    try:

        run_audit_stage()

    except Exception as e:

        print("\nAudit stage failed")
        print(str(e))

    # ==================================
    # STAGE 4 — SEND OUTREACH
    # ==================================

    try:

        run_sales_stage()

    except Exception as e:

        print("\nSales stage failed")
        print(str(e))

    print("\n======================================")
    print("PIPELINE FINISHED")
    print("======================================")


if __name__ == "__main__":

    main()