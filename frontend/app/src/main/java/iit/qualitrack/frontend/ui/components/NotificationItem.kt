package iit.qualitrack.frontend.ui.components

import androidx.compose.foundation.layout.*
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import iit.qualitrack.frontend.data.model.NotificationItem

@Composable
fun NotificationItem(notification: NotificationItem) {
    Card(
        modifier = Modifier
            .fillMaxWidth()
            .padding(8.dp),
        elevation = CardDefaults.cardElevation(4.dp)
    ) {
        Column(modifier = Modifier.padding(16.dp)) {
            Text(text = notification.title)
            Spacer(modifier = Modifier.height(4.dp))
            Text(text = notification.message)
            Spacer(modifier = Modifier.height(8.dp))
            Text(text = "At: ${notification.created_at}")
        }
    }
}
