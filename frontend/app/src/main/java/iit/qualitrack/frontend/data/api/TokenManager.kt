package iit.qualitrack.frontend.data.api

/**
 * Simple global holder for the current Bearer token.
 * Call TokenManager.token = "Bearer $rawToken" once on login.
 */
object TokenManager {
    @Volatile
    var token: String? = null
}
