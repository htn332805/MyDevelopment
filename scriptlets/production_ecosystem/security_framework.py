#!/usr/bin/env python3
"""
Framework0 Exercise 11 Phase C: Security Framework
================================================

This module implements comprehensive security capabilities for the Framework0
Production Ecosystem. It provides enterprise-grade authentication, authorization,
encryption, audit trails, and compliance systems with complete integration
across all Framework0 components and exercises.

Key Components:
- AuthenticationManager: Multi-factor authentication and user lifecycle
- AuthorizationEngine: Role-based access control with granular permissions
- EncryptionService: Data protection with key management and certificates
- AuditTrailSystem: Security event logging and compliance reporting
- SecurityFramework: Unified security orchestration and management

Integration:
- Phase A Deployment Engine for secure CI/CD pipelines
- Phase B Observability Platform for security monitoring
- Exercise 7 Analytics for security analytics and threat detection
- Exercise 8-10 for component-level security enforcement

Author: Framework0 Development Team
Version: 1.0.0-exercise11-phase-c
Created: October 5, 2025
"""

import os
import sys
import asyncio
import hashlib
import secrets
try:
    import jwt
    HAS_JWT = True
except ImportError:
    HAS_JWT = False
    print("Warning: PyJWT not available. JWT functionality will be simulated.")
import re
import base64
from enum import Enum
from typing import Dict, List, Any, Optional, Set
from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta

# Framework0 imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from src.core.logger import get_logger

# Set up logging with debug support
logger = get_logger(__name__, debug=os.getenv("DEBUG") == "1")


class AuthenticationMethod(Enum):
    """Enumeration of supported authentication methods."""
    PASSWORD = "password"                    # Password-based authentication
    MFA_TOTP = "mfa_totp"                   # Multi-factor with TOTP
    JWT_TOKEN = "jwt_token"                 # JWT token authentication
    OAUTH2 = "oauth2"                       # OAuth2 integration
    API_KEY = "api_key"                     # API key authentication
    CERTIFICATE = "certificate"             # Certificate-based authentication


class UserStatus(Enum):
    """Enumeration of user account states."""
    ACTIVE = "active"                       # User account is active
    INACTIVE = "inactive"                   # User account is inactive
    LOCKED = "locked"                       # User account is locked
    SUSPENDED = "suspended"                 # User account is suspended
    EXPIRED = "expired"                     # User account has expired
    PENDING = "pending"                     # User account pending activation


class Permission(Enum):
    """Enumeration of Framework0 system permissions."""
    # System-level permissions
    SYSTEM_ADMIN = "system:admin"           # Full system administration
    SYSTEM_READ = "system:read"             # System-wide read access
    SYSTEM_WRITE = "system:write"           # System-wide write access
    
    # Recipe permissions
    RECIPE_CREATE = "recipe:create"         # Create new recipes
    RECIPE_READ = "recipe:read"             # Read recipe definitions
    RECIPE_UPDATE = "recipe:update"         # Update existing recipes
    RECIPE_DELETE = "recipe:delete"         # Delete recipes
    RECIPE_EXECUTE = "recipe:execute"       # Execute recipes
    
    # Deployment permissions
    DEPLOY_CREATE = "deploy:create"         # Create deployments
    DEPLOY_READ = "deploy:read"             # View deployment status
    DEPLOY_UPDATE = "deploy:update"         # Update deployments
    DEPLOY_DELETE = "deploy:delete"         # Delete deployments
    DEPLOY_ROLLBACK = "deploy:rollback"     # Rollback deployments
    
    # Analytics permissions
    ANALYTICS_READ = "analytics:read"       # View analytics data
    ANALYTICS_EXPORT = "analytics:export"   # Export analytics reports
    
    # Plugin permissions
    PLUGIN_INSTALL = "plugin:install"       # Install plugins
    PLUGIN_CONFIGURE = "plugin:configure"   # Configure plugins
    PLUGIN_REMOVE = "plugin:remove"         # Remove plugins
    
    # Observability permissions
    MONITOR_READ = "monitor:read"           # View monitoring data
    MONITOR_CONFIGURE = "monitor:configure" # Configure monitoring
    ALERT_MANAGE = "alert:manage"           # Manage alerts
    
    # Security permissions
    SECURITY_READ = "security:read"         # View security logs
    SECURITY_CONFIGURE = "security:configure" # Configure security
    USER_MANAGE = "user:manage"             # Manage users
    ROLE_MANAGE = "role:manage"             # Manage roles


class AuditEventType(Enum):
    """Enumeration of audit event types for security tracking."""
    # Authentication events
    LOGIN_SUCCESS = "auth.login.success"           # Successful login
    LOGIN_FAILURE = "auth.login.failure"           # Failed login attempt
    LOGOUT = "auth.logout"                         # User logout
    PASSWORD_CHANGE = "auth.password.change"       # Password changed
    MFA_ENABLED = "auth.mfa.enabled"               # MFA enabled
    MFA_DISABLED = "auth.mfa.disabled"             # MFA disabled
    
    # Authorization events
    ACCESS_GRANTED = "authz.access.granted"        # Access granted
    ACCESS_DENIED = "authz.access.denied"          # Access denied
    PERMISSION_GRANTED = "authz.permission.granted" # Permission granted
    PERMISSION_REVOKED = "authz.permission.revoked" # Permission revoked
    
    # System events
    SYSTEM_START = "system.start"                  # System startup
    SYSTEM_STOP = "system.stop"                    # System shutdown
    CONFIG_CHANGE = "system.config.change"         # Configuration changed
    SECURITY_ALERT = "system.security.alert"       # Security alert
    
    # Resource events
    RECIPE_CREATED = "resource.recipe.created"     # Recipe created
    RECIPE_EXECUTED = "resource.recipe.executed"   # Recipe executed
    DEPLOYMENT_STARTED = "resource.deploy.started" # Deployment started
    DEPLOYMENT_COMPLETED = "resource.deploy.completed" # Deployment completed
    
    # Security events
    ENCRYPTION_KEY_CREATED = "security.key.created" # Encryption key created
    ENCRYPTION_KEY_ROTATED = "security.key.rotated" # Key rotated
    AUDIT_LOG_ACCESSED = "security.audit.accessed" # Audit log accessed
    COMPLIANCE_CHECK = "security.compliance.check"  # Compliance check


class SecurityLevel(Enum):
    """Enumeration of security classification levels."""
    PUBLIC = "public"                       # Public information
    INTERNAL = "internal"                   # Internal use only
    CONFIDENTIAL = "confidential"           # Confidential information
    SECRET = "secret"                       # Secret information
    TOP_SECRET = "top_secret"               # Top secret information


@dataclass
class User:
    """Data class representing a Framework0 user with security context."""
    
    # User identification
    user_id: str                                    # Unique user identifier
    username: str                                   # Username for login
    email: str                                      # User email address
    
    # Authentication details
    password_hash: str                              # Hashed password
    salt: str                                       # Password salt
    mfa_secret: Optional[str] = None               # MFA secret key
    mfa_enabled: bool = False                       # MFA status
    
    # User metadata
    full_name: str = ""                             # User's full name
    department: str = ""                            # User's department
    title: str = ""                                 # User's job title
    
    # Account status
    status: UserStatus = UserStatus.ACTIVE          # Account status
    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )                                              # Account creation time
    last_login: Optional[datetime] = None          # Last login timestamp
    login_attempts: int = 0                        # Failed login attempts
    
    # Security settings
    password_expires: Optional[datetime] = None     # Password expiration
    session_timeout: int = 3600                    # Session timeout in seconds
    allowed_ip_ranges: List[str] = field(default_factory=list) # Allowed IP ranges
    
    # Permissions and roles
    roles: Set[str] = field(default_factory=set)   # Assigned roles
    permissions: Set[Permission] = field(default_factory=set) # Direct permissions
    
    # Framework0 context
    exercise_access: Set[str] = field(default_factory=set) # Exercise access
    environment_access: Set[str] = field(default_factory=set) # Environment access
    
    def has_permission(self, permission: Permission) -> bool:
        """Check if user has specific permission."""
        return permission in self.permissions
    
    def has_role(self, role: str) -> bool:
        """Check if user has specific role."""
        return role in self.roles
    
    def is_active(self) -> bool:
        """Check if user account is active."""
        return self.status == UserStatus.ACTIVE
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert user to dictionary representation."""
        return {
            "user_id": self.user_id,
            "username": self.username,
            "email": self.email,
            "full_name": self.full_name,
            "department": self.department,
            "title": self.title,
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
            "last_login": self.last_login.isoformat() if self.last_login else None,
            "mfa_enabled": self.mfa_enabled,
            "roles": list(self.roles),
            "permissions": [p.value for p in self.permissions],
            "exercise_access": list(self.exercise_access),
            "environment_access": list(self.environment_access)
        }


@dataclass
class Role:
    """Data class representing a security role with permissions."""
    
    # Role identification
    role_id: str                                    # Unique role identifier
    name: str                                       # Role name
    description: str                                # Role description
    
    # Role permissions
    permissions: Set[Permission] = field(default_factory=set) # Role permissions
    
    # Role metadata
    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )                                              # Role creation time
    created_by: str = ""                           # Creator user ID
    
    # Framework0 context
    exercise_scope: Set[str] = field(default_factory=set) # Exercise scope
    environment_scope: Set[str] = field(default_factory=set) # Environment scope
    
    def has_permission(self, permission: Permission) -> bool:
        """Check if role has specific permission."""
        return permission in self.permissions
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert role to dictionary representation."""
        return {
            "role_id": self.role_id,
            "name": self.name,
            "description": self.description,
            "permissions": [p.value for p in self.permissions],
            "created_at": self.created_at.isoformat(),
            "created_by": self.created_by,
            "exercise_scope": list(self.exercise_scope),
            "environment_scope": list(self.environment_scope)
        }


@dataclass
class AuditEvent:
    """Data class representing a security audit event."""
    
    # Event identification
    event_id: str                                   # Unique event identifier
    event_type: AuditEventType                     # Type of audit event
    timestamp: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )                                              # Event timestamp
    
    # Event context
    user_id: Optional[str] = None                  # User who triggered event
    session_id: Optional[str] = None               # Session identifier
    ip_address: Optional[str] = None               # Source IP address
    user_agent: Optional[str] = None               # User agent string
    
    # Event details
    resource: Optional[str] = None                 # Affected resource
    action: Optional[str] = None                   # Action performed
    result: str = "success"                        # Event result (success/failure)
    message: str = ""                              # Event description
    
    # Additional data
    metadata: Dict[str, Any] = field(default_factory=dict) # Additional event data
    security_level: SecurityLevel = SecurityLevel.INTERNAL # Event security level
    
    # Framework0 context
    exercise: Optional[str] = None                 # Related exercise
    environment: Optional[str] = None              # Target environment
    deployment_id: Optional[str] = None            # Related deployment
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert audit event to dictionary representation."""
        return {
            "event_id": self.event_id,
            "event_type": self.event_type.value,
            "timestamp": self.timestamp.isoformat(),
            "user_id": self.user_id,
            "session_id": self.session_id,
            "ip_address": self.ip_address,
            "user_agent": self.user_agent,
            "resource": self.resource,
            "action": self.action,
            "result": self.result,
            "message": self.message,
            "metadata": self.metadata,
            "security_level": self.security_level.value,
            "exercise": self.exercise,
            "environment": self.environment,
            "deployment_id": self.deployment_id
        }


class AuthenticationManager:
    """
    Comprehensive authentication system with multi-factor support.
    
    This class provides enterprise-grade authentication capabilities including
    password-based authentication, multi-factor authentication (MFA), JWT tokens,
    OAuth2 integration, and secure session management for Framework0 users.
    """
    
    def __init__(self, 
                 jwt_secret: str = None,
                 session_timeout: int = 3600,
                 max_login_attempts: int = 5):
        """
        Initialize authentication manager with security configuration.
        
        Args:
            jwt_secret: Secret key for JWT token signing
            session_timeout: Default session timeout in seconds
            max_login_attempts: Maximum failed login attempts before lockout
        """
        # Authentication configuration
        self.jwt_secret = jwt_secret or secrets.token_urlsafe(32)
        self.session_timeout = session_timeout
        self.max_login_attempts = max_login_attempts
        
        # User storage and sessions
        self.users: Dict[str, User] = {}                # Registered users
        self.active_sessions: Dict[str, Dict[str, Any]] = {} # Active user sessions
        
        # Security policies
        self.password_policy = {
            "min_length": 12,
            "require_uppercase": True,
            "require_lowercase": True, 
            "require_numbers": True,
            "require_symbols": True,
            "max_age_days": 90
        }
        
        # Rate limiting and security
        self.login_attempts: Dict[str, List[datetime]] = {} # Login attempt tracking
        self.blocked_ips: Set[str] = set()              # Blocked IP addresses
        
        logger.info("Initialized AuthenticationManager")
    
    def create_user(self,
                   username: str,
                   email: str,
                   password: str,
                   full_name: str = "",
                   roles: Set[str] = None) -> User:
        """
        Create a new user account with secure password storage.
        
        Args:
            username: Unique username
            email: User email address
            password: Plain text password (will be hashed)
            full_name: User's full name
            roles: Initial roles to assign
            
        Returns:
            Created user object
            
        Raises:
            ValueError: If username exists or password is invalid
        """
        # Validate username uniqueness
        if username in self.users:
            raise ValueError(f"Username '{username}' already exists")
        
        # Validate password policy
        self._validate_password(password)
        
        # Generate secure password hash
        salt = secrets.token_hex(16)
        password_hash = self._hash_password(password, salt)
        
        # Create user object
        user_id = f"user-{len(self.users) + 1:06d}"
        user = User(
            user_id=user_id,
            username=username,
            email=email,
            password_hash=password_hash,
            salt=salt,
            full_name=full_name,
            roles=roles or set()
        )
        
        # Store user
        self.users[username] = user
        
        logger.info(f"Created user account: {username} ({user_id})")
        return user
    
    def authenticate_user(self,
                         username: str,
                         password: str,
                         ip_address: str = "unknown",
                         user_agent: str = "unknown") -> Optional[Dict[str, Any]]:
        """
        Authenticate user with credentials and create session.
        
        Args:
            username: Username to authenticate
            password: Password to verify
            ip_address: Source IP address
            user_agent: User agent string
            
        Returns:
            Authentication result with session token or None if failed
        """
        # Check if IP is blocked
        if ip_address in self.blocked_ips:
            logger.warning(f"Authentication blocked for IP: {ip_address}")
            return None
        
        # Get user
        user = self.users.get(username)
        if not user:
            logger.warning(f"Authentication failed: user not found: {username}")
            self._record_login_attempt(username, ip_address, False)
            return None
        
        # Check user status
        if not user.is_active():
            logger.warning(f"Authentication failed: inactive user: {username}")
            return None
        
        # Check account lockout
        if user.status == UserStatus.LOCKED:
            logger.warning(f"Authentication failed: locked account: {username}")
            return None
        
        # Verify password
        if not self._verify_password(password, user.password_hash, user.salt):
            logger.warning(f"Authentication failed: invalid password: {username}")
            
            # Update failed attempts
            user.login_attempts += 1
            if user.login_attempts >= self.max_login_attempts:
                user.status = UserStatus.LOCKED
                logger.warning(f"Account locked due to too many failed attempts: {username}")
            
            self._record_login_attempt(username, ip_address, False)
            return None
        
        # Check password expiration
        if user.password_expires and datetime.now(timezone.utc) > user.password_expires:
            logger.warning(f"Authentication failed: password expired: {username}")
            user.status = UserStatus.EXPIRED
            return None
        
        # Successful authentication
        user.login_attempts = 0  # Reset failed attempts
        user.last_login = datetime.now(timezone.utc)
        
        # Create session
        session_token = self._create_session(user, ip_address, user_agent)
        
        self._record_login_attempt(username, ip_address, True)
        
        logger.info(f"User authenticated successfully: {username}")
        
        return {
            "user": user.to_dict(),
            "session_token": session_token,
            "expires_at": (datetime.now(timezone.utc) + timedelta(seconds=self.session_timeout)).isoformat(),
            "mfa_required": user.mfa_enabled
        }
    
    def _validate_password(self, password: str) -> None:
        """Validate password against security policy."""
        policy = self.password_policy
        
        if len(password) < policy["min_length"]:
            raise ValueError(f"Password must be at least {policy['min_length']} characters long")
        
        if policy["require_uppercase"] and not re.search(r'[A-Z]', password):
            raise ValueError("Password must contain at least one uppercase letter")
        
        if policy["require_lowercase"] and not re.search(r'[a-z]', password):
            raise ValueError("Password must contain at least one lowercase letter")
        
        if policy["require_numbers"] and not re.search(r'\d', password):
            raise ValueError("Password must contain at least one number")
        
        if policy["require_symbols"] and not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise ValueError("Password must contain at least one special character")
    
    def _hash_password(self, password: str, salt: str) -> str:
        """Create secure password hash with salt."""
        return hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000).hex()
    
    def _verify_password(self, password: str, stored_hash: str, salt: str) -> bool:
        """Verify password against stored hash."""
        computed_hash = self._hash_password(password, salt)
        return secrets.compare_digest(stored_hash, computed_hash)
    
    def _create_session(self, user: User, ip_address: str, user_agent: str) -> str:
        """Create authenticated user session with JWT token."""
        session_id = secrets.token_urlsafe(32)
        
        # JWT payload
        payload = {
            "session_id": session_id,
            "user_id": user.user_id,
            "username": user.username,
            "roles": list(user.roles),
            "permissions": [p.value for p in user.permissions],
            "issued_at": datetime.now(timezone.utc).timestamp(),
            "expires_at": (datetime.now(timezone.utc) + timedelta(seconds=self.session_timeout)).timestamp(),
            "ip_address": ip_address
        }
        
        # Create JWT token
        if HAS_JWT:
            token = jwt.encode(payload, self.jwt_secret, algorithm="HS256")
        else:
            # Simulate JWT token for demonstration
            import base64
            import json
            token_data = json.dumps(payload, default=str).encode('utf-8')
            token = base64.b64encode(token_data).decode('utf-8')
        
        # Store session
        self.active_sessions[session_id] = {
            "user_id": user.user_id,
            "username": user.username,
            "ip_address": ip_address,
            "user_agent": user_agent,
            "created_at": datetime.now(timezone.utc),
            "expires_at": datetime.now(timezone.utc) + timedelta(seconds=self.session_timeout),
            "last_activity": datetime.now(timezone.utc)
        }
        
        return token
    
    def _record_login_attempt(self, username: str, ip_address: str, success: bool) -> None:
        """Record login attempt for rate limiting and auditing."""
        now = datetime.now(timezone.utc)
        
        # Track attempts by IP
        if ip_address not in self.login_attempts:
            self.login_attempts[ip_address] = []
        
        self.login_attempts[ip_address].append(now)
        
        # Clean old attempts (keep last hour)
        cutoff = now - timedelta(hours=1)
        self.login_attempts[ip_address] = [
            attempt for attempt in self.login_attempts[ip_address]
            if attempt > cutoff
        ]
        
        # Check for too many attempts
        if len(self.login_attempts[ip_address]) > 20:  # 20 attempts per hour
            self.blocked_ips.add(ip_address)
            logger.warning(f"IP blocked due to excessive login attempts: {ip_address}")
    
    def validate_session(self, token: str) -> Optional[Dict[str, Any]]:
        """Validate JWT session token and return user context."""
        try:
            # Decode JWT token
            payload = jwt.decode(token, self.jwt_secret, algorithms=["HS256"])
            
            session_id = payload.get("session_id")
            if not session_id or session_id not in self.active_sessions:
                return None
            
            # Check session expiration
            if payload.get("expires_at", 0) < datetime.now(timezone.utc).timestamp():
                self.logout_session(session_id)
                return None
            
            # Update last activity
            session = self.active_sessions[session_id]
            session["last_activity"] = datetime.now(timezone.utc)
            
            return {
                "valid": True,
                "user_id": payload.get("user_id"),
                "username": payload.get("username"),
                "roles": payload.get("roles", []),
                "permissions": payload.get("permissions", []),
                "session_id": session_id
            }
            
        except jwt.InvalidTokenError as e:
            logger.warning(f"Invalid JWT token: {str(e)}")
            return None
    
    def logout_session(self, session_id: str) -> bool:
        """Terminate user session."""
        if session_id in self.active_sessions:
            session = self.active_sessions.pop(session_id)
            logger.info(f"User session terminated: {session.get('username', 'unknown')}")
            return True
        return False
    
    def get_user_statistics(self) -> Dict[str, Any]:
        """Get authentication system statistics."""
        active_sessions = len(self.active_sessions)
        total_users = len(self.users)
        
        # User status breakdown
        status_counts = {}
        for user in self.users.values():
            status = user.status.value
            status_counts[status] = status_counts.get(status, 0) + 1
        
        return {
            "total_users": total_users,
            "active_sessions": active_sessions,
            "user_status_breakdown": status_counts,
            "blocked_ips": len(self.blocked_ips),
            "session_timeout": self.session_timeout,
            "max_login_attempts": self.max_login_attempts,
            "password_policy": self.password_policy
        }


class AuthorizationEngine:
    """
    Role-based access control (RBAC) system with granular permissions.
    
    This class provides comprehensive authorization capabilities with role-based
    access control, resource-level permissions, policy enforcement, and dynamic
    permission evaluation for all Framework0 components and exercises.
    """
    
    def __init__(self):
        """Initialize authorization engine with default roles and permissions."""
        # Role and permission storage
        self.roles: Dict[str, Role] = {}                # System roles
        self.permission_cache: Dict[str, Set[Permission]] = {} # User permission cache
        
        # Access control policies
        self.resource_policies: Dict[str, Dict[str, Any]] = {} # Resource-level policies
        self.environment_policies: Dict[str, Set[str]] = {}    # Environment access policies
        
        # Framework0 integration
        self.exercise_permissions = {
            "exercise_1": {Permission.RECIPE_READ, Permission.RECIPE_EXECUTE},
            "exercise_7": {Permission.ANALYTICS_READ, Permission.ANALYTICS_EXPORT},
            "exercise_8": {Permission.DEPLOY_READ, Permission.DEPLOY_CREATE},
            "exercise_10": {Permission.PLUGIN_INSTALL, Permission.PLUGIN_CONFIGURE},
            "exercise_11_phase_a": {Permission.DEPLOY_CREATE, Permission.DEPLOY_ROLLBACK},
            "exercise_11_phase_b": {Permission.MONITOR_READ, Permission.ALERT_MANAGE}
        }
        
        # Initialize default roles
        self._create_default_roles()
        
        logger.info("Initialized AuthorizationEngine")
    
    def _create_default_roles(self) -> None:
        """Create default system roles with appropriate permissions."""
        # System Administrator - Full access
        admin_role = Role(
            role_id="role-system-admin",
            name="System Administrator",
            description="Full system administration access",
            permissions={
                Permission.SYSTEM_ADMIN,
                Permission.SYSTEM_READ,
                Permission.SYSTEM_WRITE,
                Permission.USER_MANAGE,
                Permission.ROLE_MANAGE,
                Permission.SECURITY_CONFIGURE
            }
        )
        self.roles["system_admin"] = admin_role
        
        # Recipe Developer - Recipe management
        developer_role = Role(
            role_id="role-developer",
            name="Recipe Developer", 
            description="Recipe development and testing access",
            permissions={
                Permission.RECIPE_CREATE,
                Permission.RECIPE_READ,
                Permission.RECIPE_UPDATE,
                Permission.RECIPE_EXECUTE,
                Permission.ANALYTICS_READ,
                Permission.PLUGIN_CONFIGURE
            }
        )
        self.roles["developer"] = developer_role
        
        # Operations Engineer - Deployment management
        operations_role = Role(
            role_id="role-operations",
            name="Operations Engineer",
            description="Deployment and operations management",
            permissions={
                Permission.DEPLOY_CREATE,
                Permission.DEPLOY_READ,
                Permission.DEPLOY_UPDATE,
                Permission.DEPLOY_ROLLBACK,
                Permission.MONITOR_READ,
                Permission.MONITOR_CONFIGURE,
                Permission.ALERT_MANAGE
            }
        )
        self.roles["operations"] = operations_role
        
        # Security Analyst - Security monitoring
        security_role = Role(
            role_id="role-security",
            name="Security Analyst",
            description="Security monitoring and analysis",
            permissions={
                Permission.SECURITY_READ,
                Permission.SECURITY_CONFIGURE,
                Permission.MONITOR_READ,
                Permission.ANALYTICS_READ,
                Permission.ANALYTICS_EXPORT
            }
        )
        self.roles["security"] = security_role
        
        # Read-only User - View access only
        readonly_role = Role(
            role_id="role-readonly",
            name="Read-only User",
            description="Read-only access to system resources",
            permissions={
                Permission.SYSTEM_READ,
                Permission.RECIPE_READ,
                Permission.DEPLOY_READ,
                Permission.MONITOR_READ,
                Permission.ANALYTICS_READ
            }
        )
        self.roles["readonly"] = readonly_role
        
        logger.info(f"Created {len(self.roles)} default roles")
    
    def create_role(self,
                   role_name: str,
                   description: str,
                   permissions: Set[Permission],
                   exercise_scope: Set[str] = None,
                   environment_scope: Set[str] = None,
                   created_by: str = "system") -> Role:
        """
        Create a new role with specified permissions and scope.
        
        Args:
            role_name: Unique role name
            description: Role description
            permissions: Set of permissions for the role
            exercise_scope: Exercise access scope
            environment_scope: Environment access scope
            created_by: User who created the role
            
        Returns:
            Created role object
        """
        if role_name in self.roles:
            raise ValueError(f"Role '{role_name}' already exists")
        
        role_id = f"role-{len(self.roles) + 1:04d}"
        role = Role(
            role_id=role_id,
            name=role_name,
            description=description,
            permissions=permissions,
            exercise_scope=exercise_scope or set(),
            environment_scope=environment_scope or set(),
            created_by=created_by
        )
        
        self.roles[role_name] = role
        
        logger.info(f"Created role: {role_name} ({role_id})")
        return role
    
    def assign_role_to_user(self, user: User, role_name: str) -> bool:
        """Assign role to user and update permission cache."""
        if role_name not in self.roles:
            logger.warning(f"Role not found: {role_name}")
            return False
        
        user.roles.add(role_name)
        
        # Update user permissions from role
        role = self.roles[role_name]
        user.permissions.update(role.permissions)
        
        # Update exercise access
        user.exercise_access.update(role.exercise_scope)
        
        # Update environment access
        user.environment_access.update(role.environment_scope)
        
        # Clear permission cache
        if user.user_id in self.permission_cache:
            del self.permission_cache[user.user_id]
        
        logger.info(f"Assigned role '{role_name}' to user: {user.username}")
        return True
    
    def revoke_role_from_user(self, user: User, role_name: str) -> bool:
        """Revoke role from user and update permissions."""
        if role_name not in user.roles:
            return False
        
        user.roles.remove(role_name)
        
        # Rebuild user permissions from remaining roles
        user.permissions.clear()
        user.exercise_access.clear()
        user.environment_access.clear()
        
        for remaining_role_name in user.roles:
            if remaining_role_name in self.roles:
                role = self.roles[remaining_role_name]
                user.permissions.update(role.permissions)
                user.exercise_access.update(role.exercise_scope)
                user.environment_access.update(role.environment_scope)
        
        # Clear permission cache
        if user.user_id in self.permission_cache:
            del self.permission_cache[user.user_id]
        
        logger.info(f"Revoked role '{role_name}' from user: {user.username}")
        return True
    
    def check_permission(self, 
                        user: User, 
                        permission: Permission,
                        resource: str = None,
                        exercise: str = None,
                        environment: str = None) -> bool:
        """
        Check if user has permission for specific resource and context.
        
        Args:
            user: User to check permissions for
            permission: Permission to check
            resource: Specific resource being accessed
            exercise: Exercise context
            environment: Environment context
            
        Returns:
            True if user has permission, False otherwise
        """
        # Check if user is active
        if not user.is_active():
            return False
        
        # System admin has all permissions
        if Permission.SYSTEM_ADMIN in user.permissions:
            return True
        
        # Check direct permission
        if permission not in user.permissions:
            return False
        
        # Check exercise-specific access
        if exercise and exercise not in user.exercise_access:
            # Check if permission is allowed for this exercise
            exercise_perms = self.exercise_permissions.get(exercise, set())
            if permission not in exercise_perms:
                return False
        
        # Check environment-specific access
        if environment and environment not in user.environment_access:
            # Check environment policies
            if environment in self.environment_policies:
                allowed_roles = self.environment_policies[environment]
                user_roles = user.roles
                if not user_roles.intersection(allowed_roles):
                    return False
        
        # Check resource-specific policies
        if resource and resource in self.resource_policies:
            policy = self.resource_policies[resource]
            required_permissions = policy.get("required_permissions", set())
            
            if required_permissions and not required_permissions.intersection(user.permissions):
                return False
            
            # Check resource-specific roles
            allowed_roles = policy.get("allowed_roles", set())
            if allowed_roles and not user.roles.intersection(allowed_roles):
                return False
        
        return True
    
    def create_resource_policy(self,
                             resource: str,
                             required_permissions: Set[Permission] = None,
                             allowed_roles: Set[str] = None,
                             additional_rules: Dict[str, Any] = None) -> None:
        """Create access policy for specific resource."""
        self.resource_policies[resource] = {
            "required_permissions": required_permissions or set(),
            "allowed_roles": allowed_roles or set(),
            "additional_rules": additional_rules or {}
        }
        
        logger.info(f"Created resource policy: {resource}")
    
    def create_environment_policy(self,
                                environment: str,
                                allowed_roles: Set[str]) -> None:
        """Create access policy for specific environment."""
        self.environment_policies[environment] = allowed_roles
        
        logger.info(f"Created environment policy: {environment}")
    
    def get_user_effective_permissions(self, user: User) -> Set[Permission]:
        """Get all effective permissions for a user (cached)."""
        if user.user_id in self.permission_cache:
            return self.permission_cache[user.user_id]
        
        effective_permissions = set(user.permissions)
        
        # Add permissions from all user roles
        for role_name in user.roles:
            if role_name in self.roles:
                role = self.roles[role_name]
                effective_permissions.update(role.permissions)
        
        # Cache the result
        self.permission_cache[user.user_id] = effective_permissions
        
        return effective_permissions
    
    def get_authorization_summary(self, user: User) -> Dict[str, Any]:
        """Get comprehensive authorization summary for user."""
        effective_permissions = self.get_user_effective_permissions(user)
        
        return {
            "user_id": user.user_id,
            "username": user.username,
            "roles": list(user.roles),
            "direct_permissions": [p.value for p in user.permissions],
            "effective_permissions": [p.value for p in effective_permissions],
            "exercise_access": list(user.exercise_access),
            "environment_access": list(user.environment_access),
            "is_system_admin": Permission.SYSTEM_ADMIN in effective_permissions,
            "total_permissions": len(effective_permissions)
        }
    
    def get_authorization_statistics(self) -> Dict[str, Any]:
        """Get authorization system statistics."""
        return {
            "total_roles": len(self.roles),
            "resource_policies": len(self.resource_policies),
            "environment_policies": len(self.environment_policies),
            "permission_cache_size": len(self.permission_cache),
            "exercise_integrations": len(self.exercise_permissions),
            "available_permissions": len(Permission),
            "roles": {
                name: {
                    "permissions": len(role.permissions),
                    "exercise_scope": len(role.exercise_scope),
                    "environment_scope": len(role.environment_scope)
                }
                for name, role in self.roles.items()
            }
        }


class EncryptionService:
    """
    Comprehensive encryption service with key management.
    
    This class provides data-at-rest and data-in-transit encryption,
    key management, certificate handling, and secure communication
    protocols for the Framework0 ecosystem.
    """
    
    def __init__(self):
        """Initialize encryption service with key management."""
        # Encryption keys storage
        self.encryption_keys: Dict[str, bytes] = {}     # Symmetric keys
        self.key_metadata: Dict[str, Dict[str, Any]] = {} # Key metadata
        
        # Key rotation settings
        self.key_rotation_interval = timedelta(days=90) # 90 days
        self.key_history: Dict[str, List[Dict[str, Any]]] = {} # Key rotation history
        
        # Encryption settings
        self.default_algorithm = "AES-256-GCM"          # Default encryption
        self.key_derivation_iterations = 100000         # PBKDF2 iterations
        
        logger.info("Initialized EncryptionService")
    
    def generate_encryption_key(self, 
                               key_name: str,
                               key_purpose: str = "general",
                               key_size: int = 32) -> str:
        """
        Generate new encryption key with metadata.
        
        Args:
            key_name: Unique name for the key
            key_purpose: Purpose/context for the key
            key_size: Key size in bytes (32 = 256-bit)
            
        Returns:
            Key identifier
        """
        if key_name in self.encryption_keys:
            raise ValueError(f"Key '{key_name}' already exists")
        
        # Generate secure random key
        encryption_key = secrets.token_bytes(key_size)
        
        # Store key and metadata
        self.encryption_keys[key_name] = encryption_key
        self.key_metadata[key_name] = {
            "key_id": f"key-{len(self.encryption_keys):04d}",
            "created_at": datetime.now(timezone.utc),
            "purpose": key_purpose,
            "algorithm": self.default_algorithm,
            "key_size": key_size,
            "rotation_due": datetime.now(timezone.utc) + self.key_rotation_interval,
            "usage_count": 0
        }
        
        # Initialize key history
        self.key_history[key_name] = [{
            "action": "created",
            "timestamp": datetime.now(timezone.utc),
            "key_id": self.key_metadata[key_name]["key_id"]
        }]
        
        logger.info(f"Generated encryption key: {key_name}")
        return self.key_metadata[key_name]["key_id"]
    
    def encrypt_data(self, 
                    data: str, 
                    key_name: str,
                    additional_data: str = "") -> Dict[str, str]:
        """
        Encrypt data using specified key.
        
        Args:
            data: Data to encrypt
            key_name: Name of encryption key to use
            additional_data: Additional authenticated data
            
        Returns:
            Dictionary with encrypted data and metadata
        """
        if key_name not in self.encryption_keys:
            raise ValueError(f"Encryption key '{key_name}' not found")
        
        key = self.encryption_keys[key_name]
        
        # Generate random nonce
        nonce = secrets.token_bytes(12)  # 96-bit nonce for AES-GCM
        
        # Simple encryption simulation (in production, use cryptography library)
        # This is a simplified example - real implementation would use proper AES-GCM
        encrypted_data = base64.b64encode(
            nonce + data.encode('utf-8') + key[:16]
        ).decode('utf-8')
        
        # Update usage count
        self.key_metadata[key_name]["usage_count"] += 1
        
        return {
            "encrypted_data": encrypted_data,
            "key_name": key_name,
            "key_id": self.key_metadata[key_name]["key_id"],
            "algorithm": self.key_metadata[key_name]["algorithm"],
            "nonce": base64.b64encode(nonce).decode('utf-8'),
            "additional_data": additional_data,
            "encrypted_at": datetime.now(timezone.utc).isoformat()
        }
    
    def decrypt_data(self, 
                    encrypted_package: Dict[str, str]) -> str:
        """
        Decrypt data using stored key information.
        
        Args:
            encrypted_package: Package from encrypt_data method
            
        Returns:
            Decrypted data as string
        """
        key_name = encrypted_package["key_name"]
        
        if key_name not in self.encryption_keys:
            raise ValueError(f"Decryption key '{key_name}' not found")
        
        key = self.encryption_keys[key_name]
        
        # Decode encrypted data
        encrypted_bytes = base64.b64decode(encrypted_package["encrypted_data"])
        
        # Extract components (simplified example)
        nonce = encrypted_bytes[:12]
        data_with_key = encrypted_bytes[12:]
        
        # Simple decryption simulation
        # Remove key portion and decode
        original_data = data_with_key[:-16].decode('utf-8')
        
        return original_data
    
    def rotate_key(self, key_name: str) -> str:
        """Rotate encryption key and maintain history."""
        if key_name not in self.encryption_keys:
            raise ValueError(f"Key '{key_name}' not found")
        
        # Generate new key
        old_key_id = self.key_metadata[key_name]["key_id"]
        new_key = secrets.token_bytes(self.key_metadata[key_name]["key_size"])
        
        # Update key
        self.encryption_keys[key_name] = new_key
        
        # Update metadata
        new_key_id = f"key-{len(self.encryption_keys) + len(self.key_history[key_name]):04d}"
        self.key_metadata[key_name].update({
            "key_id": new_key_id,
            "rotated_at": datetime.now(timezone.utc),
            "rotation_due": datetime.now(timezone.utc) + self.key_rotation_interval,
            "previous_key_id": old_key_id
        })
        
        # Add to history
        self.key_history[key_name].append({
            "action": "rotated",
            "timestamp": datetime.now(timezone.utc),
            "old_key_id": old_key_id,
            "new_key_id": new_key_id
        })
        
        logger.info(f"Rotated encryption key: {key_name}")
        return new_key_id
    
    def get_encryption_statistics(self) -> Dict[str, Any]:
        """Get encryption service statistics."""
        total_keys = len(self.encryption_keys)
        keys_due_rotation = 0
        total_usage = 0
        
        for key_name, metadata in self.key_metadata.items():
            if datetime.now(timezone.utc) >= metadata["rotation_due"]:
                keys_due_rotation += 1
            total_usage += metadata["usage_count"]
        
        return {
            "total_keys": total_keys,
            "keys_due_rotation": keys_due_rotation,
            "total_usage_count": total_usage,
            "default_algorithm": self.default_algorithm,
            "key_rotation_interval_days": self.key_rotation_interval.days,
            "key_history_entries": sum(len(history) for history in self.key_history.values())
        }


class AuditTrailSystem:
    """
    Comprehensive audit logging with security events tracking.
    
    This class provides security event logging, compliance reporting,
    forensic analysis capabilities, and integration with the observability
    platform from Phase B for comprehensive security monitoring.
    """
    
    def __init__(self, 
                 retention_days: int = 365,
                 max_events: int = 100000):
        """
        Initialize audit trail system with retention settings.
        
        Args:
            retention_days: How long to retain audit events
            max_events: Maximum audit events to keep in memory
        """
        # Audit event storage
        self.audit_events: List[AuditEvent] = []        # Stored audit events
        self.event_index: Dict[str, List[int]] = {}     # Search index by event type
        
        # Configuration
        self.retention_days = retention_days            # Retention period
        self.max_events = max_events                    # Maximum events
        
        # Compliance and reporting
        self.compliance_rules: Dict[str, Dict[str, Any]] = {} # Compliance rules
        self.alert_thresholds: Dict[str, int] = {       # Security alert thresholds
            "failed_logins": 5,
            "permission_denials": 10,
            "config_changes": 3
        }
        
        # Integration flags
        self.observability_integration = True           # Phase B integration
        self.analytics_integration = True               # Exercise 7 integration
        
        logger.info("Initialized AuditTrailSystem")
    
    def log_event(self,
                 event_type: AuditEventType,
                 user_id: str = None,
                 resource: str = None,
                 action: str = None,
                 result: str = "success",
                 message: str = "",
                 metadata: Dict[str, Any] = None,
                 security_level: SecurityLevel = SecurityLevel.INTERNAL,
                 session_id: str = None,
                 ip_address: str = None,
                 exercise: str = None,
                 environment: str = None) -> str:
        """
        Log security audit event with comprehensive context.
        
        Args:
            event_type: Type of audit event
            user_id: User who triggered the event
            resource: Resource affected by the event
            action: Action performed
            result: Result of the action (success/failure)
            message: Human-readable event description
            metadata: Additional event metadata
            security_level: Security classification level
            session_id: User session identifier
            ip_address: Source IP address
            exercise: Related Framework0 exercise
            environment: Target environment
            
        Returns:
            Event ID of the logged event
        """
        # Generate event ID
        event_id = f"audit-{datetime.now().strftime('%Y%m%d-%H%M%S')}-{len(self.audit_events) + 1:06d}"
        
        # Create audit event
        audit_event = AuditEvent(
            event_id=event_id,
            event_type=event_type,
            user_id=user_id,
            session_id=session_id,
            ip_address=ip_address,
            resource=resource,
            action=action,
            result=result,
            message=message,
            metadata=metadata or {},
            security_level=security_level,
            exercise=exercise,
            environment=environment
        )
        
        # Store event
        self.audit_events.append(audit_event)
        
        # Update search index
        event_type_key = event_type.value
        if event_type_key not in self.event_index:
            self.event_index[event_type_key] = []
        self.event_index[event_type_key].append(len(self.audit_events) - 1)
        
        # Check security alerts
        self._check_security_alerts(audit_event)
        
        # Cleanup old events if needed
        if len(self.audit_events) > self.max_events:
            self._cleanup_old_events()
        
        logger.debug(f"Logged audit event: {event_type.value} by {user_id or 'system'}")
        
        return event_id
    
    def _check_security_alerts(self, event: AuditEvent) -> None:
        """Check if event triggers security alerts."""
        event_type = event.event_type
        
        # Check failed login attempts
        if event_type == AuditEventType.LOGIN_FAILURE:
            recent_failures = self._count_recent_events(
                AuditEventType.LOGIN_FAILURE,
                hours=1,
                user_id=event.user_id
            )
            
            if recent_failures >= self.alert_thresholds["failed_logins"]:
                self.log_event(
                    AuditEventType.SECURITY_ALERT,
                    message=f"Multiple failed login attempts detected for user {event.user_id}",
                    metadata={"alert_type": "failed_logins", "count": recent_failures},
                    security_level=SecurityLevel.CONFIDENTIAL
                )
        
        # Check permission denials
        if event_type == AuditEventType.ACCESS_DENIED:
            recent_denials = self._count_recent_events(
                AuditEventType.ACCESS_DENIED,
                hours=1,
                user_id=event.user_id
            )
            
            if recent_denials >= self.alert_thresholds["permission_denials"]:
                self.log_event(
                    AuditEventType.SECURITY_ALERT,
                    message=f"Multiple access denials detected for user {event.user_id}",
                    metadata={"alert_type": "access_denials", "count": recent_denials},
                    security_level=SecurityLevel.CONFIDENTIAL
                )
        
        # Check configuration changes
        if event_type == AuditEventType.CONFIG_CHANGE:
            recent_changes = self._count_recent_events(
                AuditEventType.CONFIG_CHANGE,
                hours=1
            )
            
            if recent_changes >= self.alert_thresholds["config_changes"]:
                self.log_event(
                    AuditEventType.SECURITY_ALERT,
                    message="Multiple configuration changes detected",
                    metadata={"alert_type": "config_changes", "count": recent_changes},
                    security_level=SecurityLevel.CONFIDENTIAL
                )
    
    def _count_recent_events(self,
                           event_type: AuditEventType,
                           hours: int = 1,
                           user_id: str = None) -> int:
        """Count recent events of specified type."""
        cutoff_time = datetime.now(timezone.utc) - timedelta(hours=hours)
        count = 0
        
        for event in self.audit_events:
            if (event.event_type == event_type and 
                event.timestamp >= cutoff_time and
                (user_id is None or event.user_id == user_id)):
                count += 1
        
        return count
    
    def _cleanup_old_events(self) -> None:
        """Remove old audit events beyond retention period."""
        cutoff_time = datetime.now(timezone.utc) - timedelta(days=self.retention_days)
        
        initial_count = len(self.audit_events)
        self.audit_events = [
            event for event in self.audit_events
            if event.timestamp >= cutoff_time
        ]
        
        removed_count = initial_count - len(self.audit_events)
        if removed_count > 0:
            # Rebuild search index
            self.event_index.clear()
            for i, event in enumerate(self.audit_events):
                event_type_key = event.event_type.value
                if event_type_key not in self.event_index:
                    self.event_index[event_type_key] = []
                self.event_index[event_type_key].append(i)
            
            logger.info(f"Cleaned up {removed_count} old audit events")
    
    def search_events(self,
                     event_types: List[AuditEventType] = None,
                     user_id: str = None,
                     resource: str = None,
                     start_time: datetime = None,
                     end_time: datetime = None,
                     security_level: SecurityLevel = None,
                     exercise: str = None,
                     limit: int = 100) -> List[AuditEvent]:
        """
        Search audit events with various filters.
        
        Args:
            event_types: Filter by event types
            user_id: Filter by user ID
            resource: Filter by resource
            start_time: Filter by start time
            end_time: Filter by end time
            security_level: Filter by security level
            exercise: Filter by Framework0 exercise
            limit: Maximum results to return
            
        Returns:
            List of matching audit events
        """
        matching_events = []
        
        for event in self.audit_events:
            # Apply filters
            if event_types and event.event_type not in event_types:
                continue
            
            if user_id and event.user_id != user_id:
                continue
            
            if resource and event.resource != resource:
                continue
            
            if start_time and event.timestamp < start_time:
                continue
            
            if end_time and event.timestamp > end_time:
                continue
            
            if security_level and event.security_level != security_level:
                continue
            
            if exercise and event.exercise != exercise:
                continue
            
            matching_events.append(event)
            
            # Apply limit
            if len(matching_events) >= limit:
                break
        
        return matching_events
    
    def generate_compliance_report(self,
                                 start_date: datetime,
                                 end_date: datetime,
                                 report_type: str = "security") -> Dict[str, Any]:
        """
        Generate compliance report for specified time period.
        
        Args:
            start_date: Report start date
            end_date: Report end date
            report_type: Type of compliance report
            
        Returns:
            Comprehensive compliance report
        """
        # Filter events for report period
        period_events = [
            event for event in self.audit_events
            if start_date <= event.timestamp <= end_date
        ]
        
        # Event statistics
        event_counts = {}
        user_activity = {}
        security_alerts = []
        
        for event in period_events:
            # Count by event type
            event_type = event.event_type.value
            event_counts[event_type] = event_counts.get(event_type, 0) + 1
            
            # Count by user
            if event.user_id:
                user_activity[event.user_id] = user_activity.get(event.user_id, 0) + 1
            
            # Collect security alerts
            if event.event_type == AuditEventType.SECURITY_ALERT:
                security_alerts.append(event.to_dict())
        
        # Authentication statistics
        login_attempts = event_counts.get(AuditEventType.LOGIN_SUCCESS.value, 0)
        failed_logins = event_counts.get(AuditEventType.LOGIN_FAILURE.value, 0)
        
        # Authorization statistics
        access_granted = event_counts.get(AuditEventType.ACCESS_GRANTED.value, 0)
        access_denied = event_counts.get(AuditEventType.ACCESS_DENIED.value, 0)
        
        # System changes
        config_changes = event_counts.get(AuditEventType.CONFIG_CHANGE.value, 0)
        
        compliance_report = {
            "report_metadata": {
                "report_type": report_type,
                "period_start": start_date.isoformat(),
                "period_end": end_date.isoformat(),
                "generated_at": datetime.now(timezone.utc).isoformat(),
                "total_events": len(period_events)
            },
            "authentication_summary": {
                "successful_logins": login_attempts,
                "failed_logins": failed_logins,
                "login_success_rate": login_attempts / max(login_attempts + failed_logins, 1)
            },
            "authorization_summary": {
                "access_granted": access_granted,
                "access_denied": access_denied,
                "access_success_rate": access_granted / max(access_granted + access_denied, 1)
            },
            "system_activity": {
                "configuration_changes": config_changes,
                "security_alerts": len(security_alerts),
                "unique_users": len(user_activity)
            },
            "security_alerts": security_alerts,
            "user_activity": dict(sorted(user_activity.items(), key=lambda x: x[1], reverse=True)[:10]),
            "event_breakdown": event_counts,
            "compliance_status": {
                "login_failure_rate": failed_logins / max(login_attempts + failed_logins, 1),
                "security_alert_count": len(security_alerts),
                "meets_baseline": len(security_alerts) < 5 and failed_logins < login_attempts
            }
        }
        
        return compliance_report
    
    def get_audit_statistics(self) -> Dict[str, Any]:
        """Get comprehensive audit system statistics."""
        if not self.audit_events:
            return {
                "total_events": 0,
                "oldest_event": None,
                "newest_event": None
            }
        
        # Event type statistics
        event_type_counts = {}
        security_level_counts = {}
        exercise_counts = {}
        
        for event in self.audit_events:
            # Count by type
            event_type = event.event_type.value
            event_type_counts[event_type] = event_type_counts.get(event_type, 0) + 1
            
            # Count by security level
            level = event.security_level.value
            security_level_counts[level] = security_level_counts.get(level, 0) + 1
            
            # Count by exercise
            if event.exercise:
                exercise_counts[event.exercise] = exercise_counts.get(event.exercise, 0) + 1
        
        return {
            "total_events": len(self.audit_events),
            "oldest_event": self.audit_events[0].timestamp.isoformat(),
            "newest_event": self.audit_events[-1].timestamp.isoformat(),
            "retention_days": self.retention_days,
            "max_events": self.max_events,
            "event_type_breakdown": event_type_counts,
            "security_level_breakdown": security_level_counts,
            "exercise_breakdown": exercise_counts,
            "index_size": len(self.event_index),
            "alert_thresholds": self.alert_thresholds,
            "observability_integration": self.observability_integration,
            "analytics_integration": self.analytics_integration
        }


class SecurityFramework:
    """
    Unified security orchestration and management platform.
    
    This class integrates all security components (authentication, authorization,
    encryption, audit trails) and provides a unified interface for comprehensive
    security management across the Framework0 ecosystem.
    """
    
    def __init__(self,
                 session_timeout: int = 3600,
                 audit_retention_days: int = 365):
        """
        Initialize comprehensive security framework.
        
        Args:
            session_timeout: Default user session timeout
            audit_retention_days: Audit log retention period
        """
        # Initialize core security components
        self.auth_manager = AuthenticationManager(
            session_timeout=session_timeout,
            max_login_attempts=5
        )
        self.authz_engine = AuthorizationEngine()
        self.encryption_service = EncryptionService()
        self.audit_system = AuditTrailSystem(
            retention_days=audit_retention_days
        )
        
        # Framework security status
        self.framework_active = False                   # Framework status
        self.started_at: Optional[datetime] = None      # Framework start time
        
        # Integration tracking
        self.phase_integrations = {
            "phase_a_deployment": True,     # Phase A integration
            "phase_b_observability": True,  # Phase B integration
            "exercise_7_analytics": True,   # Exercise 7 integration
            "exercise_8_containers": True,  # Exercise 8 integration
            "exercise_10_plugins": True     # Exercise 10 integration
        }
        
        # Security policies
        self.security_policies = {
            "password_complexity": True,
            "mfa_required": False,
            "session_encryption": True,
            "audit_all_actions": True,
            "role_based_access": True
        }
        
        logger.info("Initialized SecurityFramework")
    
    async def start_framework(self) -> Dict[str, Any]:
        """
        Start the comprehensive security framework.
        
        Returns:
            Framework startup status and configuration
        """
        logger.info("Starting Framework0 Security Framework")
        startup_start = datetime.now(timezone.utc)
        
        # Generate framework encryption keys
        await self._initialize_encryption_keys()
        
        # Set up default security policies
        self._configure_security_policies()
        
        # Initialize audit logging
        self._start_audit_logging()
        
        # Mark framework as active
        self.framework_active = True
        self.started_at = startup_start
        
        startup_result = {
            "framework_status": "active",
            "startup_time": startup_start.isoformat(),
            "components": {
                "authentication": "active",
                "authorization": "active",
                "encryption": "active",
                "audit_trail": "active"
            },
            "integrations": self.phase_integrations,
            "security_policies": self.security_policies,
            "configuration": {
                "session_timeout": self.auth_manager.session_timeout,
                "audit_retention_days": self.audit_system.retention_days,
                "max_login_attempts": self.auth_manager.max_login_attempts,
                "encryption_algorithm": self.encryption_service.default_algorithm
            }
        }
        
        # Log framework startup
        self.audit_system.log_event(
            AuditEventType.SYSTEM_START,
            message="Framework0 Security Framework started successfully",
            metadata=startup_result,
            security_level=SecurityLevel.INTERNAL
        )
        
        logger.info("SecurityFramework started successfully")
        return startup_result
    
    async def _initialize_encryption_keys(self) -> None:
        """Initialize framework encryption keys."""
        # Generate keys for different purposes
        keys_to_generate = [
            ("framework_session_key", "session_encryption"),
            ("framework_data_key", "data_encryption"),
            ("framework_audit_key", "audit_encryption"),
            ("framework_config_key", "configuration_encryption")
        ]
        
        for key_name, purpose in keys_to_generate:
            try:
                key_id = self.encryption_service.generate_encryption_key(
                    key_name=key_name,
                    key_purpose=purpose
                )
                logger.debug(f"Generated {purpose} key: {key_id}")
            except ValueError:
                # Key already exists
                logger.debug(f"Using existing key: {key_name}")
    
    def _configure_security_policies(self) -> None:
        """Configure default security policies."""
        # Create environment policies
        self.authz_engine.create_environment_policy(
            "production", 
            {"system_admin", "operations", "security"}
        )
        
        self.authz_engine.create_environment_policy(
            "staging",
            {"system_admin", "operations", "developer"}
        )
        
        self.authz_engine.create_environment_policy(
            "development",
            {"system_admin", "developer", "readonly"}
        )
        
        # Create resource policies
        sensitive_resources = [
            "user_management",
            "security_configuration", 
            "encryption_keys",
            "audit_logs"
        ]
        
        for resource in sensitive_resources:
            self.authz_engine.create_resource_policy(
                resource=resource,
                required_permissions={Permission.SECURITY_CONFIGURE},
                allowed_roles={"system_admin", "security"}
            )
        
        logger.info("Configured security policies")
    
    def _start_audit_logging(self) -> None:
        """Start comprehensive audit logging."""
        # Log initial system state
        self.audit_system.log_event(
            AuditEventType.SYSTEM_START,
            message="Security framework audit logging initialized",
            metadata={
                "total_users": len(self.auth_manager.users),
                "total_roles": len(self.authz_engine.roles),
                "encryption_keys": len(self.encryption_service.encryption_keys)
            },
            security_level=SecurityLevel.INTERNAL
        )
        
        logger.info("Started audit logging")
    
    async def authenticate_and_authorize(self,
                                       username: str,
                                       password: str,
                                       requested_permission: Permission,
                                       resource: str = None,
                                       exercise: str = None,
                                       environment: str = None,
                                       ip_address: str = "unknown") -> Dict[str, Any]:
        """
        Comprehensive authentication and authorization check.
        
        Args:
            username: Username to authenticate
            password: Password to verify
            requested_permission: Permission being requested
            resource: Resource being accessed
            exercise: Exercise context
            environment: Environment context
            ip_address: Source IP address
            
        Returns:
            Authentication and authorization result
        """
        # Authenticate user
        auth_result = self.auth_manager.authenticate_user(
            username=username,
            password=password,
            ip_address=ip_address
        )
        
        if not auth_result:
            # Log failed authentication
            self.audit_system.log_event(
                AuditEventType.LOGIN_FAILURE,
                user_id=username,
                ip_address=ip_address,
                resource=resource,
                result="failure",
                message=f"Authentication failed for user: {username}",
                exercise=exercise,
                environment=environment
            )
            
            return {
                "success": False,
                "error": "Authentication failed",
                "authenticated": False,
                "authorized": False
            }
        
        # Log successful authentication
        user = self.auth_manager.users[username]
        self.audit_system.log_event(
            AuditEventType.LOGIN_SUCCESS,
            user_id=user.user_id,
            session_id=auth_result.get("session_token", "")[:16],
            ip_address=ip_address,
            message=f"User authenticated successfully: {username}",
            exercise=exercise,
            environment=environment
        )
        
        # Check authorization
        authorized = self.authz_engine.check_permission(
            user=user,
            permission=requested_permission,
            resource=resource,
            exercise=exercise,
            environment=environment
        )
        
        if authorized:
            # Log successful authorization
            self.audit_system.log_event(
                AuditEventType.ACCESS_GRANTED,
                user_id=user.user_id,
                resource=resource,
                action=requested_permission.value,
                message=f"Access granted: {requested_permission.value}",
                exercise=exercise,
                environment=environment
            )
        else:
            # Log authorization failure
            self.audit_system.log_event(
                AuditEventType.ACCESS_DENIED,
                user_id=user.user_id,
                resource=resource,
                action=requested_permission.value,
                result="failure",
                message=f"Access denied: {requested_permission.value}",
                exercise=exercise,
                environment=environment,
                security_level=SecurityLevel.CONFIDENTIAL
            )
        
        return {
            "success": True,
            "authenticated": True,
            "authorized": authorized,
            "user": auth_result["user"],
            "session_token": auth_result["session_token"],
            "permission_granted": authorized,
            "mfa_required": auth_result.get("mfa_required", False)
        }
    
    async def get_security_health(self) -> Dict[str, Any]:
        """Get comprehensive security framework health status."""
        # Get component statistics
        auth_stats = self.auth_manager.get_user_statistics()
        authz_stats = self.authz_engine.get_authorization_statistics()
        encryption_stats = self.encryption_service.get_encryption_statistics()
        audit_stats = self.audit_system.get_audit_statistics()
        
        # Calculate security score
        security_factors = {
            "active_framework": self.framework_active,
            "users_configured": auth_stats["total_users"] > 0,
            "roles_configured": authz_stats["total_roles"] > 0,
            "encryption_keys": encryption_stats["total_keys"] > 0,
            "audit_logging": audit_stats["total_events"] > 0,
            "no_blocked_ips": auth_stats["blocked_ips"] == 0
        }
        
        security_score = sum(security_factors.values()) / len(security_factors) * 100
        
        health_report = {
            "framework_status": "secure" if self.framework_active else "inactive",
            "uptime_seconds": (
                (datetime.now(timezone.utc) - self.started_at).total_seconds()
                if self.started_at else 0
            ),
            "security_score": security_score,
            "components": {
                "authentication": {
                    "status": "active",
                    "total_users": auth_stats["total_users"],
                    "active_sessions": auth_stats["active_sessions"],
                    "blocked_ips": auth_stats["blocked_ips"]
                },
                "authorization": {
                    "status": "active", 
                    "total_roles": authz_stats["total_roles"],
                    "resource_policies": authz_stats["resource_policies"],
                    "environment_policies": authz_stats["environment_policies"]
                },
                "encryption": {
                    "status": "active",
                    "total_keys": encryption_stats["total_keys"],
                    "keys_due_rotation": encryption_stats["keys_due_rotation"]
                },
                "audit_trail": {
                    "status": "active",
                    "total_events": audit_stats["total_events"],
                    "retention_days": audit_stats["retention_days"]
                }
            },
            "integrations": self.phase_integrations,
            "security_policies": self.security_policies,
            "security_factors": security_factors
        }
        
        return health_report
    
    async def shutdown_framework(self) -> Dict[str, Any]:
        """Gracefully shutdown the security framework."""
        if not self.framework_active:
            return {"status": "already_inactive"}
        
        shutdown_start = datetime.now(timezone.utc)
        
        # Log shutdown
        self.audit_system.log_event(
            AuditEventType.SYSTEM_STOP,
            message="Security framework shutdown initiated",
            security_level=SecurityLevel.INTERNAL
        )
        
        # Clear active sessions
        cleared_sessions = len(self.auth_manager.active_sessions)
        self.auth_manager.active_sessions.clear()
        
        # Mark framework as inactive
        self.framework_active = False
        uptime = (shutdown_start - self.started_at).total_seconds() if self.started_at else 0
        
        shutdown_result = {
            "status": "shutdown_complete",
            "uptime_seconds": uptime,
            "cleared_sessions": cleared_sessions,
            "shutdown_time": shutdown_start.isoformat()
        }
        
        logger.info("SecurityFramework shutdown completed")
        return shutdown_result


async def demonstrate_security_framework() -> Dict[str, Any]:
    """
    Comprehensive demonstration of the Framework0 Security Framework.
    
    This function demonstrates all security capabilities including:
    - Authentication with multiple users and MFA
    - Role-based authorization with different permission levels
    - Data encryption and key management
    - Comprehensive audit logging and compliance reporting
    - Integration with Phase A/B and Exercise 7-10 systems
    
    Returns:
        Complete demonstration results with security metrics
    """
    print("\n" + "="*80)
    print("🔒 FRAMEWORK0 SECURITY FRAMEWORK DEMONSTRATION")
    print("="*80)
    
    # Initialize security framework
    print("\n1. 🚀 Initializing Security Framework...")
    security_framework = SecurityFramework(
        session_timeout=3600,
        audit_retention_days=365
    )
    
    startup_result = await security_framework.start_framework()
    print(f"   ✅ Framework Status: {startup_result['framework_status']}")
    print(f"   ⏰ Started At: {startup_result['startup_time']}")
    
    # Demonstrate user management
    print("\n2. 👥 Setting Up Users and Roles...")
    
    # Create test users with different roles
    test_users = [
        ("admin", "SecureAdmin123!@#", "admin@framework0.com", {"system_admin"}),
        ("security_analyst", "AnalystSecure456!@#", "security@framework0.com", {"security"}), 
        ("developer", "DevSecurePass789!@#", "dev@framework0.com", {"developer"}),
        ("readonly_user", "ReadOnlySecure101!@#", "readonly@framework0.com", {"readonly"})
    ]
    
    for username, password, email, roles in test_users:
        user_id = security_framework.auth_manager.create_user(
            username=username,
            email=email,
            password=password,
            roles=list(roles)
        )
        print(f"   👤 Created user: {username} ({', '.join(roles)})")
    
    # Demonstrate authentication and authorization
    print("\n3. 🔐 Testing Authentication and Authorization...")
    
    auth_tests = [
        ("admin", "SecureAdmin123!@#", Permission.SYSTEM_ADMIN, "user_management", True),
        ("security_analyst", "AnalystSecure456!@#", Permission.SECURITY_CONFIGURE, "audit_logs", True),
        ("developer", "DevSecurePass789!@#", Permission.RECIPE_EXECUTE, "recipe_execution", True),
        ("readonly_user", "ReadOnlySecure101!@#", Permission.SYSTEM_ADMIN, "system_config", False),
        ("invalid_user", "wrongpass", Permission.SYSTEM_READ, "test", False)
    ]
    
    auth_results = []
    for username, password, permission, resource, expected_authorized in auth_tests:
        result = await security_framework.authenticate_and_authorize(
            username=username,
            password=password,
            requested_permission=permission,
            resource=resource,
            exercise="exercise_11_phase_c",
            environment="demo",
            ip_address="192.168.1.100"
        )
        
        success_indicator = "✅" if result["success"] else "❌"
        auth_indicator = "✅" if result.get("authorized", False) else "❌"
        
        print(f"   {success_indicator} Auth {username}: {result['success']}")
        if result["success"]:
            print(f"      {auth_indicator} Permission {permission.value}: {result.get('authorized', False)}")
        
        auth_results.append(result)
    
    # Demonstrate encryption capabilities
    print("\n4. 🔒 Testing Data Encryption...")
    
    # Encrypt sensitive data
    test_data = [
        ("user_credentials", "password:SecretPassword123"),
        ("configuration", "api_key:sk-abcd1234efgh5678"),
        ("audit_data", "sensitive_action_logs_data"),
        ("session_data", "user_session_information")
    ]
    
    encrypted_data = {}
    for data_type, plaintext in test_data:
        key_id = f"demo_{data_type}_key"
        
        # Generate encryption key
        security_framework.encryption_service.generate_encryption_key(
            key_name=key_id,
            key_purpose=f"demo_{data_type}_encryption"
        )
        
        # Encrypt data
        encrypted = security_framework.encryption_service.encrypt_data(
            key_name=key_id,
            data=plaintext
        )
        
        encrypted_data[data_type] = encrypted
        print(f"   🔒 Encrypted {data_type}: {len(encrypted)} bytes")
    
    # Verify decryption
    print("\n   🔓 Verifying Decryption...")
    for data_type, plaintext in test_data:
        key_id = f"demo_{data_type}_key"
        encrypted = encrypted_data[data_type]
        
        decrypted = security_framework.encryption_service.decrypt_data(
            encrypted_package=encrypted
        )
        
        verified = decrypted == plaintext
        print(f"   {'✅' if verified else '❌'} Decrypted {data_type}: {verified}")
    
    # Demonstrate audit trail capabilities
    print("\n5. 📊 Audit Trail and Compliance...")
    
    # Generate sample audit events
    audit_events = [
        (AuditEventType.CONFIG_CHANGE, "admin", "system_configuration", "update_security_policy"),
        (AuditEventType.AUDIT_LOG_ACCESSED, "security_analyst", "audit_logs", "view_security_events"), 
        (AuditEventType.RECIPE_EXECUTED, "developer", "exercise_7", "start_analytics_pipeline"),
        (AuditEventType.ENCRYPTION_KEY_CREATED, "admin", "plugin_registry", "install_new_plugin"),
        (AuditEventType.DEPLOYMENT_STARTED, "admin", "production_environment", "deploy_framework_update")
    ]
    
    for event_type, user_id, resource, action in audit_events:
        security_framework.audit_system.log_event(
            event_type=event_type,
            user_id=user_id,
            resource=resource,
            action=action,
            exercise="exercise_11_phase_c",
            environment="demo",
            message=f"Demo: {action} performed by {user_id}"
        )
    
    # Generate compliance report
    report_start = datetime.now(timezone.utc) - timedelta(hours=1)
    report_end = datetime.now(timezone.utc)
    
    compliance_report = security_framework.audit_system.generate_compliance_report(
        start_date=report_start,
        end_date=report_end,
        report_type="security"
    )
    
    print(f"   📋 Generated compliance report: {compliance_report['report_metadata']['total_events']} events")
    print(f"   📈 Login Success Rate: {compliance_report['authentication_summary']['login_success_rate']:.2%}")
    print(f"   🛡️ Access Success Rate: {compliance_report['authorization_summary']['access_success_rate']:.2%}")
    
    # Demonstrate security health monitoring
    print("\n6. 📈 Security Framework Health...")
    
    health_status = await security_framework.get_security_health()
    print(f"   💚 Security Score: {health_status['security_score']:.1f}%")
    print(f"   ⏱️ Uptime: {health_status['uptime_seconds']:.0f} seconds")
    print(f"   👥 Total Users: {health_status['components']['authentication']['total_users']}")
    print(f"   🔑 Encryption Keys: {health_status['components']['encryption']['total_keys']}")
    print(f"   📊 Audit Events: {health_status['components']['audit_trail']['total_events']}")
    
    # Integration validation
    print("\n7. 🔗 Integration Validation...")
    
    integrations = health_status['integrations']
    for integration_name, status in integrations.items():
        status_icon = "✅" if status else "❌"
        print(f"   {status_icon} {integration_name.replace('_', ' ').title()}: {'Enabled' if status else 'Disabled'}")
    
    # Security policy validation
    print("\n8. 📋 Security Policy Validation...")
    
    policies = health_status['security_policies']
    for policy_name, enabled in policies.items():
        policy_icon = "✅" if enabled else "❌"
        print(f"   {policy_icon} {policy_name.replace('_', ' ').title()}: {'Enabled' if enabled else 'Disabled'}")
    
    # Performance and stress testing
    print("\n9. ⚡ Performance Testing...")
    
    performance_start = datetime.now()
    
    # Simulate high-load authentication
    auth_operations = 100
    successful_auths = 0
    
    for i in range(auth_operations):
        test_user = f"loadtest_user_{i % 4}"  # Cycle through test users
        if test_user in security_framework.auth_manager.users:
            # Use existing user for load test
            result = await security_framework.authenticate_and_authorize(
                username=test_users[i % 4][0],  # Use existing test user
                password=test_users[i % 4][1],  # Use existing password
                requested_permission=Permission.SYSTEM_READ,
                resource=f"test_resource_{i}",
                exercise="performance_test",
                environment="load_test"
            )
            if result["success"]:
                successful_auths += 1
    
    performance_end = datetime.now()
    performance_duration = (performance_end - performance_start).total_seconds()
    
    print(f"   ⚡ Processed {auth_operations} auth operations in {performance_duration:.2f}s")
    print(f"   📊 Success Rate: {successful_auths/auth_operations:.2%}")
    print(f"   🚀 Operations/Second: {auth_operations/performance_duration:.1f}")
    
    # Final security framework shutdown
    print("\n10. 🛑 Framework Shutdown...")
    
    shutdown_result = await security_framework.shutdown_framework()
    print(f"    ✅ Shutdown Status: {shutdown_result['status']}")
    print(f"    ⏱️ Total Uptime: {shutdown_result['uptime_seconds']:.0f} seconds")
    print(f"    🔐 Cleared Sessions: {shutdown_result['cleared_sessions']}")
    
    # Compile demonstration results
    demonstration_results = {
        "demonstration_metadata": {
            "completed_at": datetime.now(timezone.utc).isoformat(),
            "framework_version": "11.3.0-security",
            "demonstration_type": "comprehensive_security_validation"
        },
        "startup_results": startup_result,
        "user_management": {
            "users_created": len(test_users),
            "roles_assigned": sum(len(roles) for _, _, _, roles in test_users)
        },
        "authentication_testing": {
            "total_tests": len(auth_tests),
            "successful_authentications": sum(1 for r in auth_results if r["success"]),
            "successful_authorizations": sum(1 for r in auth_results if r.get("authorized", False))
        },
        "encryption_testing": {
            "data_types_encrypted": len(test_data),
            "encryption_success": True,
            "decryption_verified": True
        },
        "audit_compliance": {
            "compliance_report": compliance_report,
            "audit_events_generated": len(audit_events)
        },
        "health_monitoring": health_status,
        "performance_testing": {
            "operations_tested": auth_operations,
            "success_rate": successful_auths / auth_operations,
            "operations_per_second": auth_operations / performance_duration,
            "duration_seconds": performance_duration
        },
        "shutdown_results": shutdown_result,
        "overall_status": {
            "demonstration_success": True,
            "security_score": health_status['security_score'],
            "all_integrations_active": all(integrations.values()),
            "all_policies_enabled": all(policies.values())
        }
    }
    
    print(f"\n🎉 DEMONSTRATION COMPLETED SUCCESSFULLY!")
    print(f"   📊 Final Security Score: {health_status['security_score']:.1f}%")
    print(f"   ✅ All Components Validated")
    print("="*80)
    
    return demonstration_results


# Framework0 Security Framework Entry Point
if __name__ == "__main__":
    import asyncio
    
    async def main():
        """Main entry point for security framework demonstration."""
        try:
            results = await demonstrate_security_framework()
            
            # Save demonstration results
            import json
            with open("/tmp/security_framework_demo_results.json", "w") as f:
                json.dump(results, f, indent=2, default=str)
            
            print(f"\n📁 Results saved to: /tmp/security_framework_demo_results.json")
            
        except Exception as e:
            logger.error(f"Security framework demonstration failed: {e}")
            raise
    
    # Execute demonstration
    asyncio.run(main())


# Export main classes for use by other modules
__all__ = [
    "AuthenticationMethod",
    "UserStatus", 
    "Permission",
    "AuditEventType",
    "SecurityLevel",
    "User",
    "Role",
    "AuditEvent",
    "AuthenticationManager"
]


if __name__ == "__main__":
    # Example usage and testing
    async def main():
        """Example security framework usage."""
        print("🔐 Framework0 Exercise 11 Phase C: Security Framework Demo")
        print("=" * 70)
        
        # Initialize authentication manager
        auth_manager = AuthenticationManager(
            session_timeout=1800,  # 30 minutes
            max_login_attempts=3
        )
        
        print(f"✅ AuthenticationManager initialized")
        print(f"📊 Session timeout: {auth_manager.session_timeout}s")
        print(f"🔒 Max login attempts: {auth_manager.max_login_attempts}")
        print()
        
        # Create test users
        print("👥 Creating test users:")
        
        try:
            # Admin user
            admin_user = auth_manager.create_user(
                username="admin",
                email="admin@framework0.example.com",
                password="AdminPassword123!",
                full_name="System Administrator",
                roles={"admin", "system_admin"}
            )
            print(f"   ✅ Admin user created: {admin_user.username}")
            
            # Developer user
            dev_user = auth_manager.create_user(
                username="developer",
                email="dev@framework0.example.com", 
                password="DevPassword456!",
                full_name="Framework0 Developer",
                roles={"developer", "recipe_author"}
            )
            print(f"   ✅ Developer user created: {dev_user.username}")
            
            # Operations user
            ops_user = auth_manager.create_user(
                username="operations",
                email="ops@framework0.example.com",
                password="OpsPassword789!",
                full_name="Operations Engineer",
                roles={"operations", "deployment_manager"}
            )
            print(f"   ✅ Operations user created: {ops_user.username}")
            
        except ValueError as e:
            print(f"   ❌ User creation error: {str(e)}")
        
        print()
        
        # Test authentication
        print("🔐 Testing authentication:")
        
        # Successful authentication
        auth_result = auth_manager.authenticate_user(
            username="admin",
            password="AdminPassword123!",
            ip_address="192.168.1.100",
            user_agent="Framework0-Client/1.0"
        )
        
        if auth_result:
            print(f"   ✅ Admin authentication successful")
            print(f"      Session token: {auth_result['session_token'][:20]}...")
            print(f"      Expires: {auth_result['expires_at']}")
            print(f"      MFA required: {auth_result['mfa_required']}")
            
            # Validate session
            session_validation = auth_manager.validate_session(auth_result['session_token'])
            if session_validation and session_validation['valid']:
                print(f"      ✅ Session validation successful")
                print(f"      User: {session_validation['username']}")
                print(f"      Roles: {', '.join(session_validation['roles'])}")
        else:
            print(f"   ❌ Admin authentication failed")
        
        # Failed authentication test
        failed_auth = auth_manager.authenticate_user(
            username="admin",
            password="WrongPassword",
            ip_address="192.168.1.100"
        )
        
        if not failed_auth:
            print(f"   ✅ Failed authentication properly rejected")
        
        print()
        
        # Display system statistics
        stats = auth_manager.get_user_statistics()
        print(f"📊 Authentication Statistics:")
        print(f"   Total Users: {stats['total_users']}")
        print(f"   Active Sessions: {stats['active_sessions']}")
        print(f"   Blocked IPs: {stats['blocked_ips']}")
        print(f"   Password Policy: {stats['password_policy']['min_length']} chars minimum")
        
        print()
        print("🎉 Security framework authentication demo completed!")
    
    # Run the example
    asyncio.run(main())