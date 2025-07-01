package iit.qualitrack.frontend.ui.screens

import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.navigation.NavController
import iit.qualitrack.frontend.data.model.CreateDefectRequest
import iit.qualitrack.frontend.util.NetworkResult
import iit.qualitrack.frontend.viewmodel.SharedViewModel
import kotlinx.coroutines.launch

@Composable
fun CreateDefectScreen(
    navController: NavController, sharedVm: SharedViewModel
) {
    var type by remember { mutableStateOf("") }
    var severity by remember { mutableStateOf("") }
    val result by sharedVm.createDefectResult.collectAsState()

    val scope = rememberCoroutineScope()

    Scaffold(topBar = { TopAppBar(title = { Text("New Defect") }) }) { padding ->
        Column(
            Modifier
                .padding(padding)
                .padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            OutlinedTextField(type,
                { type = it },
                Modifier.fillMaxWidth(),
                label = { Text("Defect Type") })
            OutlinedTextField(severity,
                { severity = it },
                Modifier.fillMaxWidth(),
                label = { Text("Severity") })

            Button(onClick = {
                scope.launch {
                    sharedVm.createDefect(
                        CreateDefectRequest(
                            defect_type = type, severity = severity
                        )
                    )
                }
            }) {
                Text("Submit")
            }

            when (result) {
                NetworkResult.Loading -> CircularProgressIndicator()
                is NetworkResult.Success -> LaunchedEffect(result) {
                    navController.popBackStack("defects", false)
                }

                is NetworkResult.Error -> Text(
                    "Error: ${(result as NetworkResult.Error).message}",
                    color = MaterialTheme.colorScheme.error
                )

                else -> {}
            }
        }
    }
}