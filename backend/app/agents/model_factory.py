import os
import logging
from strands.models import BedrockModel
from app.config import settings

logger = logging.getLogger("krishisathi.model_factory")


def get_bedrock_model() -> BedrockModel:
    """
    Get configured Amazon Bedrock foundation model instance for Strands Agents.
    Uses AWS credential provider chain and specified region.
    """
    try:
        return BedrockModel(
            model_id=settings.BEDROCK_MODEL_ID,
            region_name=settings.AWS_REGION
        )
    except Exception as e:
        logger.warning(f"Notice during BedrockModel creation: {e}. Model will use available default credentials.")
        return BedrockModel()

