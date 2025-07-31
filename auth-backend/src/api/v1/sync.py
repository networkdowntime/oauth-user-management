"""
Hydra synchronization API endpoints.
"""

import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from ...core.database import get_db
from ...services.hydra_sync_service import create_hydra_sync_service


logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/hydra/sync")
async def sync_hydra(
    db: AsyncSession = Depends(get_db)
):
    """
    Synchronize all service accounts and scopes with Hydra.
    
    This endpoint will:
    1. Fetch all clients from Hydra
    2. Fetch all service accounts from the database
    3. Create/update/delete clients in Hydra to match the database
    4. Update client scopes in Hydra
    
    Returns:
        dict: Synchronization result with summary and details
    """
    try:
        sync_service = create_hydra_sync_service(db)
        result = await sync_service.sync_all()
        
        if not result.success:
            logger.warning(f"Hydra sync completed with errors: {result.errors}")
        
        return result.to_dict()
    
    except Exception as e:
        logger.error(f"Hydra sync failed: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Hydra synchronization failed: {str(e)}"
        )


@router.get("/hydra/status")
async def hydra_status():
    """
    Check Hydra connection status.
    
    Returns:
        dict: Hydra health status
    """
    try:
        from ...services.hydra_client import HydraAdminClient
        
        hydra_client = HydraAdminClient()
        is_healthy = await hydra_client.health_check()
        
        return {
            "hydra_connected": is_healthy,
            "status": "healthy" if is_healthy else "unhealthy"
        }
    
    except Exception as e:
        logger.error(f"Hydra status check failed: {str(e)}")
        return {
            "hydra_connected": False,
            "status": "error",
            "error": str(e)
        }
