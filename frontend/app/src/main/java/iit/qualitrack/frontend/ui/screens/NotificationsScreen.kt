package iit.qualitrack.frontend.ui.screens

import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.lifecycle.viewmodel.compose.viewModel
import androidx.navigation.NavController
import iit.qualitrack.frontend.data.model.NotificationItem
import iit.qualitrack.frontend.data.model.NotificationsResponse
import iit.qualitrack.frontend.ui.components.NotificationItem as NotificationCard
import iit.qualitrack.frontend.util.NetworkResult
import iit.qualitrack.frontend.viewmodel.SharedViewModel

@Composable
fun NotificationsScreen(
    navController: NavController,
    sharedVm: SharedViewModel = viewModel()
) {
    // 1) observe userRole as a State<Value?>
    val roleState = sharedVm.userRole.collectAsState(initial = null).value
    if (roleState == null) return

    // 2) supervisor ID from details
    val supId = (roleState.details["id"] as Double).toInt()

    // 3) UI state
    var notificationsList by remember { mutableStateOf<List<NotificationItem>>(emptyList()) }
    var loading by remember { mutableStateOf(false) }
    var error by remember { mutableStateOf<String?>(null) }

    // 4) collect notifications
    LaunchedEffect(supId) {
        sharedVm.listNotifications(supId).collect { result ->
            when (result) {
                NetworkResult.Loading -> {
                    loading = true
                    error = null
                }
                is NetworkResult.Success<NotificationsResponse> -> {
                    notificationsList = result.data.notifications
                    loading = false
                }
                is NetworkResult.Error -> {
                    error = result.message
                    loading = false
                }
                else -> { /* Idle */ }
            }
        }
    }

    // 5) UI
    Scaffold(topBar = {
        TopAppBar(title = { Text("Notifications") })
    }) { padding ->
        Box(Modifier.padding(padding)) {
            when {
                loading -> CircularProgressIndicator(Modifier.padding(16.dp))
                error != null -> Text("Error: $error", Modifier.padding(16.dp))
                else -> LazyColumn {
                    items(notificationsList) { notif ->
                        NotificationCard(notif)
                    }
                }
            }
        }
    }
}
