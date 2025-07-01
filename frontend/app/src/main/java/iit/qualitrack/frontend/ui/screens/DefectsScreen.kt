package iit.qualitrack.frontend.ui.screens

import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Add
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.navigation.NavController
import iit.qualitrack.frontend.data.model.Defect
import iit.qualitrack.frontend.ui.components.DefectCard
import iit.qualitrack.frontend.util.NetworkResult
import iit.qualitrack.frontend.viewmodel.SharedViewModel

@Composable
fun DefectsScreen(
    navController: NavController, sharedVm: SharedViewModel
) {
    var defects by remember { mutableStateOf<List<Defect>>(emptyList()) }
    var loading by remember { mutableStateOf(false) }
    var error by remember { mutableStateOf<String?>(null) }

    LaunchedEffect(Unit) {
        sharedVm.listDefects().collect { result ->
            when (result) {
                NetworkResult.Loading -> {
                    loading = true; error = null
                }

                is NetworkResult.Success -> {
                    defects = result.data.results; loading = false
                }

                is NetworkResult.Error -> {
                    error = result.message; loading = false
                }

                else -> {}
            }
        }
    }

    Scaffold(topBar = { TopAppBar(title = { Text("Defects") }) }, floatingActionButton = {
        FloatingActionButton({ navController.navigate("defects/new") }) {
            Icon(Icons.Filled.Add, contentDescription = "New Defect")
        }
    }) { padding ->
        Box(Modifier.padding(padding)) {
            when {
                loading -> CircularProgressIndicator(Modifier.padding(16.dp))
                error != null -> Text("Error: $error", Modifier.padding(16.dp))
                else -> LazyColumn { items(defects) { DefectCard(it) } }
            }
        }
    }
}