# k8s/security/opa/tenant-policy.rego
package aegis.authz

import future.keywords.if
import future.keywords.in

default allow := false

# Allow if the user has the required permission for the action
allow if {
    input.permission in input.user_permissions
    input.tenant_id == input.target_tenant_id
}

# Admin override
allow if {
    "admin" in input.user_roles
}

# Data Loss Prevention (DLP) Rule: 
# Block if sensitive data is detected in the payload without encryption
deny_unencrypted_pii if {
    input.pii_detected == true
    input.encrypted == false
}
