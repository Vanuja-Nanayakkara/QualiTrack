package iit.qualitrack.frontend.ui.screens

import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.navigation.NavController
import iit.qualitrack.frontend.data.api.ServiceLocator
import iit.qualitrack.frontend.viewmodel.SharedViewModel
import iit.qualitrack.frontend.viewmodel.SupervisorViewModel
import kotlinx.coroutines.launch
import okhttp3.MediaType.Companion.toMediaTypeOrNull
import okhttp3.RequestBody.Companion.toRequestBody
import org.json.JSONObject

@Composable
fun PendingInspectionDetailScreen(
    inspId: Int,
    sharedVm: SharedViewModel,
    supVm: SupervisorViewModel,
    navController: NavController
) {
    val scope = rememberCoroutineScope()
    var loading by remember { mutableStateOf(false) }
    var error by remember { mutableStateOf<String?>(null) }

    Column(
        Modifier
            .fillMaxSize()
            .padding(16.dp),
        verticalArrangement = Arrangement.spacedBy(24.dp)
    ) {
        Text("Inspection #$inspId", style = MaterialTheme.typography.headlineSmall)

        error?.let {
            Text("Error: $it", color = MaterialTheme.colorScheme.error)
        }

        if (loading) {
            CircularProgressIndicator()
        } else {
            Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(16.dp)) {
                Button(onClick = {
                    scope.launch {
                        loading = true
                        error = null

                        try {
                            val body = JSONObject().apply {
                                put("status", "Resolved")
                            }.toString().toRequestBody("application/json".toMediaTypeOrNull())

                            val response = ServiceLocator.apiService.updateInspectionStatus(inspId, body)
                            if (response.isSuccessful) {
                                navController.popBackStack()
                            } else {
                                error = response.errorBody()?.string() ?: "Failed to update"
                            }
                        } catch (e: Exception) {
                            error = e.localizedMessage ?: "Unexpected error"
                        }

                        loading = false
                    }
                }, Modifier.weight(1f)) {
                    Text("Done")
                }

                Button(onClick = { navController.popBackStack() }, Modifier.weight(1f)) {
                    Text("Later")
                }
            }
        }
    }
}
