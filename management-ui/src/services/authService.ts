/**
 * OAuth2 Authentication Service for Management UI
 * 
 * This service handles OAuth2 authentication flow with Hydra:
 * 1. Redirects users to Hydra for authentication
 * 2. Handles the callback with authorization code
 * 3. Exchanges code for access token
 * 4. Manages token storage and refresh
 */

export interface AuthTokens {
  access_token: string;
  refresh_token?: string;
  id_token?: string;
  token_type: string;
  expires_in: number;
  scope: string;
}

export interface UserInfo {
  sub: string;
  email: string;
  email_verified?: boolean;
  name?: string;
  given_name?: string;
  family_name?: string;
  roles?: string[];
}

class OAuth2Service {
  private readonly clientId = 'management-ui';
  private readonly redirectUri = `${window.location.origin}/auth/callback`;
  private readonly scope = 'openid email profile admin';
  private readonly hydraPublicUrl = 'http://localhost:4444'; // Hydra public URL
  private isProcessingCallback = false; // Flag to prevent duplicate callback processing
  
  /**
   * Check if user is currently authenticated
   */
  isAuthenticated(): boolean {
    const token = this.getAccessToken();
    if (!token) return false;
    
    // Check if token is expired
    const expiresAt = localStorage.getItem('token_expires_at');
    if (!expiresAt) return false;
    
    const now = Date.now();
    const expires = parseInt(expiresAt, 10);
    
    return now < expires;
  }

  /**
   * Get the current access token
   */
  getAccessToken(): string | null {
    return localStorage.getItem('access_token');
  }

  /**
   * Get the current user info from ID token
   */
  getUserInfo(): UserInfo | null {
    const idToken = localStorage.getItem('id_token');
    if (!idToken) return null;

    try {
      // Decode JWT (without verification - we trust Hydra)
      const payload = JSON.parse(atob(idToken.split('.')[1]));
      return payload as UserInfo;
    } catch (error) {
      console.error('Failed to decode ID token:', error);
      return null;
    }
  }

  /**
   * Start the OAuth2 authorization flow
   */
  async login(): Promise<void> {
    const state = this.generateRandomString();
    const codeVerifier = this.generateRandomString();
    const codeChallenge = await this.generateCodeChallenge(codeVerifier);
    
    // Store state and code verifier for PKCE
    sessionStorage.setItem('oauth_state', state);
    sessionStorage.setItem('code_verifier', codeVerifier);
    
    const params = new URLSearchParams({
      response_type: 'code',
      client_id: this.clientId,
      redirect_uri: this.redirectUri,
      scope: this.scope,
      state: state,
      code_challenge: codeChallenge,
      code_challenge_method: 'S256',
    });

    const authUrl = `${this.hydraPublicUrl}/oauth2/auth?${params.toString()}`;
    window.location.href = authUrl;
  }

  /**
   * Handle the OAuth2 callback with authorization code
   */
  async handleCallback(): Promise<boolean> {
    // Prevent duplicate processing
    if (this.isProcessingCallback) {
      console.log('Callback already being processed, skipping duplicate call');
      return false;
    }

    this.isProcessingCallback = true;

    try {
      const urlParams = new URLSearchParams(window.location.search);
      const code = urlParams.get('code');
      const state = urlParams.get('state');
      const error = urlParams.get('error');

      if (error) {
        console.error('OAuth2 error:', error, urlParams.get('error_description'));
        this.clearStoredTokens();
        return false;
      }

      if (!code || !state) {
        console.error('Missing code or state parameter');
        return false;
      }

      // Verify state
      const storedState = sessionStorage.getItem('oauth_state');
      if (state !== storedState) {
        console.error('Invalid state parameter');
        this.clearStoredTokens();
        return false;
      }

      // Get code verifier for PKCE
      const codeVerifier = sessionStorage.getItem('code_verifier');
      if (!codeVerifier) {
        console.error('Missing code verifier');
        return false;
      }

      // Exchange authorization code for tokens
      const tokens = await this.exchangeCodeForTokens(code, codeVerifier);
      this.storeTokens(tokens);
      
      // Clean up session storage
      sessionStorage.removeItem('oauth_state');
      sessionStorage.removeItem('code_verifier');
      
      return true;
    } catch (error) {
      console.error('Failed to exchange code for tokens:', error);
      this.clearStoredTokens();
      return false;
    } finally {
      this.isProcessingCallback = false;
    }
  }

  /**
   * Exchange authorization code for access token
   */
  private async exchangeCodeForTokens(code: string, codeVerifier: string): Promise<AuthTokens> {
    const params = new URLSearchParams({
      grant_type: 'authorization_code',
      client_id: this.clientId,
      code: code,
      redirect_uri: this.redirectUri,
      code_verifier: codeVerifier,
    });

    const response = await fetch(`${this.hydraPublicUrl}/oauth2/token`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: params.toString(),
    });

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`Token exchange failed: ${response.status} ${errorText}`);
    }

    return response.json();
  }

  /**
   * Store tokens in localStorage
   */
  private storeTokens(tokens: AuthTokens): void {
    localStorage.setItem('access_token', tokens.access_token);
    localStorage.setItem('token_type', tokens.token_type);
    localStorage.setItem('scope', tokens.scope);
    
    if (tokens.refresh_token) {
      localStorage.setItem('refresh_token', tokens.refresh_token);
    }
    
    if (tokens.id_token) {
      localStorage.setItem('id_token', tokens.id_token);
    }
    
    // Calculate expiration time
    const expiresAt = Date.now() + (tokens.expires_in * 1000);
    localStorage.setItem('token_expires_at', expiresAt.toString());
  }

  /**
   * Refresh the access token using refresh token
   */
  async refreshToken(): Promise<boolean> {
    const refreshToken = localStorage.getItem('refresh_token');
    if (!refreshToken) {
      return false;
    }

    try {
      const params = new URLSearchParams({
        grant_type: 'refresh_token',
        client_id: this.clientId,
        refresh_token: refreshToken,
      });

      const response = await fetch(`${this.hydraPublicUrl}/oauth2/token`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: params.toString(),
      });

      if (!response.ok) {
        throw new Error(`Token refresh failed: ${response.status}`);
      }

      const tokens: AuthTokens = await response.json();
      this.storeTokens(tokens);
      return true;
    } catch (error) {
      console.error('Failed to refresh token:', error);
      this.clearStoredTokens();
      return false;
    }
  }

  /**
   * Logout the user
   */
  async logout(): Promise<void> {
    const idToken = localStorage.getItem('id_token');
    
    // Clear stored tokens
    this.clearStoredTokens();
    
    // Redirect to Hydra logout endpoint
    const params = new URLSearchParams({
      post_logout_redirect_uri: window.location.origin,
    });
    
    if (idToken) {
      params.set('id_token_hint', idToken);
    }
    
    const logoutUrl = `${this.hydraPublicUrl}/oauth2/sessions/logout?${params.toString()}`;
    window.location.href = logoutUrl;
  }

  /**
   * Clear all stored tokens
   */
  private clearStoredTokens(): void {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('id_token');
    localStorage.removeItem('token_type');
    localStorage.removeItem('scope');
    localStorage.removeItem('token_expires_at');
  }

  /**
   * Generate a random string for state and code verifier
   */
  private generateRandomString(): string {
    const array = new Uint8Array(32);
    crypto.getRandomValues(array);
    return Array.from(array, byte => byte.toString(16).padStart(2, '0')).join('');
  }

  /**
   * Generate code challenge for PKCE using SHA256
   */
  private async generateCodeChallenge(codeVerifier: string): Promise<string> {
    // Use SHA256 method for security
    const encoder = new TextEncoder();
    const data = encoder.encode(codeVerifier);
    const digest = await crypto.subtle.digest('SHA-256', data);
    
    // Convert to base64url
    const digestArray = Array.from(new Uint8Array(digest));
    const base64 = btoa(String.fromCharCode.apply(null, digestArray));
    return base64.replace(/\+/g, '-').replace(/\//g, '_').replace(/=/g, '');
  }

  /**
   * Get authorization header for API requests
   */
  getAuthHeader(): { Authorization: string } | {} {
    const token = this.getAccessToken();
    if (!token) return {};
    
    const tokenType = localStorage.getItem('token_type') || 'Bearer';
    return {
      Authorization: `${tokenType} ${token}`,
    };
  }
}

export const authService = new OAuth2Service();
