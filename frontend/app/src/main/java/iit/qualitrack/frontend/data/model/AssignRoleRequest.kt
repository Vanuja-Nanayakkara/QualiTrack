package iit.qualitrack.frontend.data.model

data class AssignRoleRequest(
    val role_type: String, val name: String, val phone: String, val department: String? = null
)
