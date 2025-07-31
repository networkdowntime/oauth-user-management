"""API endpoints for authentication operations."""

from fastapi import APIRouter, Depends, HTTPException, Request, Form, Query, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from ...core.database import get_db
from ...schemas.common import SuccessResponse
from ...services.hydra_client import HydraAdminClient
from ...services.user_service import UserService
from ...repositories.user import UserRepository
from ...repositories.role import RoleRepository
from ...repositories.audit_log import AuditLogRepository
from ...core.config import settings

router = APIRouter()
templates = Jinja2Templates(directory="src/templates")
hydra_client = HydraAdminClient()


async def get_user_service(db: AsyncSession = Depends(get_db)) -> UserService:
    """Create UserService with all required dependencies."""
    user_repo = UserRepository(db)
    role_repo = RoleRepository(db)
    audit_repo = AuditLogRepository(db)
    return UserService(user_repo, role_repo, audit_repo)


# Login Flow Endpoints

@router.get("/login", response_class=HTMLResponse)
async def login_page(
    request: Request,
    login_challenge: str = Query(...),
    error: Optional[str] = Query(None)
):
    """Display the login page."""
    try:
        # Get login request info from Hydra
        login_request = await hydra_client.get_login_request(login_challenge)
        
        # Check if user is already authenticated
        if login_request.get("skip"):
            # User is already authenticated, accept the login request
            accept_response = await hydra_client.accept_login_request(
                login_challenge=login_challenge,
                subject=login_request["subject"]
            )
            return RedirectResponse(url=accept_response["redirect_to"], status_code=303)
        
        # Render login page
        return templates.TemplateResponse("login.html", {
            "request": request,
            "login_challenge": login_challenge,
            "client": login_request.get("client", {}),
            "error": error
        })
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid login challenge: {str(e)}"
        )


@router.post("/login")
async def login_submit(
    request: Request,
    login_challenge: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    remember: Optional[bool] = Form(False),
    user_service: UserService = Depends(get_user_service)
):
    """Handle login form submission."""
    try:
        # Get login request info from Hydra
        login_request = await hydra_client.get_login_request(login_challenge)
        
        # Authenticate user
        user = await user_service.authenticate_user(email, password)
        
        if not user:
            # Authentication failed, show error
            return templates.TemplateResponse("login.html", {
                "request": request,
                "login_challenge": login_challenge,
                "client": login_request.get("client", {}),
                "email": email,
                "error": "Invalid email or password"
            })
        
        # Check if user is active
        if not user.is_active:
            return templates.TemplateResponse("login.html", {
                "request": request,
                "login_challenge": login_challenge,
                "client": login_request.get("client", {}),
                "email": email,
                "error": "Account is disabled"
            })
        
        # Accept login request
        remember_bool = remember or False
        accept_response = await hydra_client.accept_login_request(
            login_challenge=login_challenge,
            subject=str(user.id),
            remember=remember_bool,
            remember_for=86400 if remember_bool else 3600,  # 24h if remember, 1h otherwise
            context={
                "user_id": user.id,
                "email": user.email,
                "username": getattr(user, 'username', user.email)  # Fallback to email if no username
            }
        )
        
        return RedirectResponse(url=accept_response["redirect_to"], status_code=303)
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Login failed: {str(e)}"
        )


# Consent Flow Endpoints

@router.get("/consent", response_class=HTMLResponse)
async def consent_page(
    request: Request,
    consent_challenge: str = Query(...)
):
    """Display the consent page."""
    try:
        # Get consent request info from Hydra
        consent_request = await hydra_client.get_consent_request(consent_challenge)
        
        # Check if consent can be skipped
        if consent_request.get("skip"):
            # Consent can be skipped, accept automatically
            accept_response = await hydra_client.accept_consent_request(
                consent_challenge=consent_challenge,
                grant_scope=consent_request["requested_scope"]
            )
            return RedirectResponse(url=accept_response["redirect_to"], status_code=303)
        
        # Render consent page
        return templates.TemplateResponse("consent.html", {
            "request": request,
            "consent_challenge": consent_challenge,
            "client": consent_request.get("client", {}),
            "user": consent_request.get("subject", {}),
            "requested_scope": consent_request.get("requested_scope", []),
            "requested_access_token_audience": consent_request.get("requested_access_token_audience", [])
        })
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid consent challenge: {str(e)}"
        )


@router.post("/consent")
async def consent_submit(
    request: Request,
    consent_challenge: str = Form(...),
    action: str = Form(...)
):
    """Handle consent form submission."""
    try:
        # Get consent request info from Hydra
        consent_request = await hydra_client.get_consent_request(consent_challenge)
        
        if action == "accept":
            # User granted consent
            accept_response = await hydra_client.accept_consent_request(
                consent_challenge=consent_challenge,
                grant_scope=consent_request["requested_scope"],
                grant_access_token_audience=consent_request.get("requested_access_token_audience", []),
                remember=True,
                remember_for=86400,  # Remember for 24 hours
                session={
                    "access_token": {
                        "user_id": consent_request["subject"],
                        "email": consent_request.get("context", {}).get("email"),
                        "username": consent_request.get("context", {}).get("username")
                    },
                    "id_token": {
                        "user_id": consent_request["subject"],
                        "email": consent_request.get("context", {}).get("email"),
                        "username": consent_request.get("context", {}).get("username")
                    }
                }
            )
            return RedirectResponse(url=accept_response["redirect_to"], status_code=303)
        
        elif action == "deny":
            # User denied consent
            reject_response = await hydra_client.reject_consent_request(
                consent_challenge=consent_challenge,
                error="access_denied",
                error_description="The user denied the consent request"
            )
            return RedirectResponse(url=reject_response["redirect_to"], status_code=303)
        
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid action"
            )
            
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Consent failed: {str(e)}"
        )


# Logout Flow Endpoints

@router.get("/logout", response_class=HTMLResponse)
async def logout_page(
    request: Request,
    logout_challenge: str = Query(...)
):
    """Display the logout page."""
    try:
        # Get logout request info from Hydra
        logout_request = await hydra_client.get_logout_request(logout_challenge)
        
        # Render logout page
        return templates.TemplateResponse("logout.html", {
            "request": request,
            "logout_challenge": logout_challenge,
            "client": logout_request.get("client"),
            "user": logout_request.get("subject")
        })
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid logout challenge: {str(e)}"
        )


@router.post("/logout")
async def logout_submit(
    request: Request,
    logout_challenge: str = Form(...),
    action: str = Form(...)
):
    """Handle logout form submission."""
    try:
        if action == "accept":
            # User confirmed logout
            accept_response = await hydra_client.accept_logout_request(logout_challenge)
            return RedirectResponse(url=accept_response["redirect_to"], status_code=303)
        
        elif action == "reject":
            # User cancelled logout
            reject_response = await hydra_client.reject_logout_request(logout_challenge)
            return RedirectResponse(url=reject_response["redirect_to"], status_code=303)
        
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid action"
            )
            
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Logout failed: {str(e)}"
        )


# Social Authentication Endpoints (Federated Login)

@router.get("/auth/google")
async def google_auth(
    request: Request,
    login_challenge: str = Query(...)
):
    """Initiate Google OAuth flow."""
    # This would integrate with Google OAuth2
    # For now, return not implemented
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Google OAuth integration not implemented yet"
    )


@router.get("/auth/github")
async def github_auth(
    request: Request,
    login_challenge: str = Query(...)
):
    """Initiate GitHub OAuth flow."""
    # This would integrate with GitHub OAuth
    # For now, return not implemented
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="GitHub OAuth integration not implemented yet"
    )


@router.get("/auth/callback/google")
async def google_callback(
    request: Request,
    code: str = Query(...),
    state: str = Query(...)
):
    """Handle Google OAuth callback."""
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Google OAuth callback not implemented yet"
    )


@router.get("/auth/callback/github")
async def github_callback(
    request: Request,
    code: str = Query(...),
    state: str = Query(...)
):
    """Handle GitHub OAuth callback."""
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="GitHub OAuth callback not implemented yet"
    )
