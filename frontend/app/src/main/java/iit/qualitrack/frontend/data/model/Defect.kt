package iit.qualitrack.frontend.data.model

data class Defect(
    val id: Int,
    val defect_type: String,
    val severity: String,
    val image: String?,
    val detected_at: String,
    val reviewed: Boolean
)

