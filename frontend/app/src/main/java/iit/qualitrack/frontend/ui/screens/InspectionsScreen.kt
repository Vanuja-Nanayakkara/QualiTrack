package iit.qualitrack.frontend.ui.screens

import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Add
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.FloatingActionButton
import androidx.compose.material3.Icon
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.lifecycle.viewmodel.compose.viewModel
import androidx.navigation.NavController
import iit.qualitrack.frontend.data.model.Defect
import iit.qualitrack.frontend.data.model.Inspection
import iit.qualitrack.frontend.ui.components.InspectionCard
import iit.qualitrack.frontend.util.NetworkResult
import iit.qualitrack.frontend.viewmodel.SharedViewModel

@Composable
fun InspectionsScreen(
    navController: NavController, sharedVm: SharedViewModel = viewModel()
) {
    var inspections by remember { mutableStateOf<List<Inspection>>(emptyList()) }
    var loading by remember { mutableStateOf(false) }
    var error by remember { mutableStateOf<String?>(null) }

    // 1) load inspections
    LaunchedEffect(Unit) {
        sharedVm.listInspections().collect { result ->
            when (result) {
                is NetworkResult.Loading -> {
                    loading = true; error = null
                }

                is NetworkResult.Success -> {
                    inspections = result.data.results
                    loading = false
                }

                is NetworkResult.Error -> {
                    error = result.message
                    loading = false
                }

                else -> Unit
            }
        }
    }

    // 2) load supervisors
    LaunchedEffect(Unit) { sharedVm.loadSupervisors() }
    val supervisors by sharedVm.supervisors.collectAsState()
    val supMap = remember(supervisors) { supervisors.associateBy { it.id } }

    // 3) load defects
    var defects by remember { mutableStateOf<List<Defect>>(emptyList()) }
    LaunchedEffect(Unit) {
        sharedVm.listDefects().collect { result ->
            if (result is NetworkResult.Success) {
                defects = result.data.results
            }
        }
    }
    val defMap = remember(defects) { defects.associateBy { it.id } }

    Scaffold(topBar = { TopAppBar(title = { Text("Inspections") }) }, floatingActionButton = {
        FloatingActionButton(onClick = { navController.navigate("inspections/new") }) {
            Icon(Icons.Filled.Add, contentDescription = "New Inspection")
        }
    }) { padding ->
        Box(Modifier.padding(padding)) {
            when {
                loading -> CircularProgressIndicator(Modifier.padding(16.dp))
                error != null -> Text("Error: $error", Modifier.padding(16.dp))
                else -> LazyColumn {
                    items(inspections) { insp ->
                        // **Use camelCase** here:
                        val supName = supMap[insp.supervisor]?.name.orEmpty()
                        val defCat = defMap[insp.fabric_defect]?.defect_type.orEmpty()
                        InspectionCard(
                            inspection = insp, supervisorName = supName, defectCategory = defCat
                        )
                    }
                }
            }
        }
    }
}