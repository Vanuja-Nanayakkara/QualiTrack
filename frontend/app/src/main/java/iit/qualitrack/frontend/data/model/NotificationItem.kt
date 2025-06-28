package iit.qualitrack.frontend.data.model

data class NotificationItem(
    val id: Int,
    val notification_type: String,
    val title: String,
    val message: String,
    val is_read: Boolean,
    val created_at: String
)
