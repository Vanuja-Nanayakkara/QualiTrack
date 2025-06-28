package iit.qualitrack.frontend.data.model

data class SimpleRoleResponse(
    val message: String, val role: String, val details: Map<String, @JvmSuppressWildcards Any>
)
