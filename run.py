from agents.marketing_agent import MarketingAgent
from agents.enrichment_agent import EnrichmentAgent
from agents.audit_agent import AuditAgent
from agents.sales_agent import SalesAgent
from config.logger import logger


def run_marketing_stage():


    logger.info("==============================")
    logger.info("STAGE 1: MARKETING AGENT")
    logger.info("==============================")

    agent = MarketingAgent()

    agent.run()

    logger.info("Marketing stage completed")


def run_enrichment_stage():

    logger.info("==============================")
    logger.info("STAGE 2: ENRICHMENT AGENT")
    logger.info("==============================")

    agent = EnrichmentAgent()

    agent.run()

    logger.info("Enrichment stage completed")


def run_audit_stage():

    logger.info("\n==============================")
    logger.info("STAGE 3: AUDIT AGENT")
    logger.info("==============================")

    agent = AuditAgent()

    agent.run()

    logger.info("Audit stage completed")


def run_sales_stage():

    logger.info("\n==============================")
    logger.info("STAGE 4: SALES AGENT")
    logger.info("==============================")

    agent = SalesAgent()

    agent.run()

    logger.info("Sales stage completed")


def main():

    logger.info("\n======================================")
    logger.info("STARTING AI GIG HUNTER PIPELINE")
    logger.info("======================================")


    try:

        run_marketing_stage()

    except Exception as e:

        logger.warning("Marketing stage failed")
        logger.exception(e)


    try:

        run_enrichment_stage()

    except Exception as e:

        logger.warning("Enrichment stage failed")
        logger.exception(e)

    try:

        run_audit_stage()

    except Exception as e:

        logger.warning("Audit stage failed")
        logger.exception(e)


    try:

        run_sales_stage()

    except Exception as e:

        logger.warning("\nSales stage failed")
        logger.exception(e)

    logger.info("======================================")
    logger.info("PIPELINE FINISHED")
    logger.info("======================================")


if __name__ == "__main__":

    main()