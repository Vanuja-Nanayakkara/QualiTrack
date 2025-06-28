package iit.qualitrack.frontend.data.model

data class NotificationsResponse(
    val notifications: List<NotificationItem>,
    val unread_count: Int,
    val total_count: Int,
    val page: Int,
    val page_size: Int,
    val total_pages: Int
)
