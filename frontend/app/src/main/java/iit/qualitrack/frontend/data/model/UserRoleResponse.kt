package iit.qualitrack.frontend.data.model

data class UserRoleResponse(
    val role: String,
    val user: Map<String, @JvmSuppressWildcards Any>,
    val details: Map<String, @JvmSuppressWildcards Any>
)
