package iit.qualitrack.frontend.data.model

data class LoginResponse(
    val message: String, val access: String, val refresh: String, val user_id: Int
)
