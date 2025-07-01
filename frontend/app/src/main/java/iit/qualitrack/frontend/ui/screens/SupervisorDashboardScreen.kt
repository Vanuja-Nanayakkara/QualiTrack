package iit.qualitrack.frontend.ui.screens

import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.ExitToApp
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.runtime.collectAsState
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.lifecycle.viewmodel.compose.viewModel
import androidx.navigation.NavController
import iit.qualitrack.frontend.data.model.Inspection
import iit.qualitrack.frontend.data.model.PaginatedResponse
import iit.qualitrack.frontend.data.model.SupervisorDashboard
import iit.qualitrack.frontend.ui.components.InspectionCard
import iit.qualitrack.frontend.util.NetworkResult
import iit.qualitrack.frontend.viewmodel.SharedViewModel
import iit.qualitrack.frontend.viewmodel.SupervisorViewModel
import java.text.SimpleDateFormat
import java.util.*

@Composable
fun SupervisorDashboardScreen(
    navController: NavController,
    sharedVm: SharedViewModel,
    supVm: SupervisorViewModel = viewModel()
) {
    // 1) get role safely
    val roleState by sharedVm.userRole.collectAsState(initial = null)
    val role = roleState ?: return
    val supId = (role.details["id"] as Double).toInt()

    // 2) today's date & load dashboard
    val today = SimpleDateFormat("yyyy-MM-dd", Locale.getDefault()).format(Date())
    LaunchedEffect(supId) { supVm.loadDashboard(supId, today) }
    val dashboardResult by supVm.dashboard.collectAsState(initial = NetworkResult.Idle)

    // 3) load pending inspections
    var pending by remember { mutableStateOf<List<Inspection>>(emptyList()) }
    LaunchedEffect(Unit) {
        sharedVm.listInspections().collect { res ->
            if (res is NetworkResult.Success<*>) {
                val all = (res.data as PaginatedResponse<Inspection>).results
                pending = all.filter { it.supervisor == supId && it.status == "Pending" }
            }
        }
    }

    Scaffold(
        topBar = {
            TopAppBar(title = { Text("Supervisor Dashboard") }, actions = {
                IconButton(onClick = {
                    sharedVm.logout()
                    navController.navigate("login") { popUpTo("login") { inclusive = true } }
                }) {
                    Icon(Icons.Filled.ExitToApp, contentDescription = "Logout")
                }
            })
        }
    ) { padding ->
        Column(
            Modifier
                .fillMaxSize()
                .padding(padding)
                .padding(16.dp)
        ) {
            // — SUMMARY —
            when (dashboardResult) {
                NetworkResult.Loading -> Box(Modifier.fillMaxWidth(), Alignment.Center) {
                    CircularProgressIndicator()
                }
                is NetworkResult.Success -> {
                    val d = (dashboardResult as NetworkResult.Success<SupervisorDashboard>).data
                    Text("Pending Inspections: ${pending.size}", style = MaterialTheme.typography.bodyLarge)
                    Text("Total Flags:         ${d.total_flags}", style = MaterialTheme.typography.bodyLarge)
                    Spacer(Modifier.height(16.dp))
                }
                is NetworkResult.Error -> Text(
                    "Error: ${(dashboardResult as NetworkResult.Error).message}",
                    color = MaterialTheme.colorScheme.error
                )
                else -> Text("No data available", style = MaterialTheme.typography.bodyLarge)
            }

            // — LISTING —
            Text("Pending List", style = MaterialTheme.typography.titleMedium)
            LazyColumn(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                items(pending) { insp ->
                    Box(
                        Modifier
                            .fillMaxWidth()
                            .clickable {
                                navController.navigate("inspection/detail/${insp.id}")
                            }
                    ) {
                        InspectionCard(
                            inspection = insp,
                            supervisorName = role.details["name"] as String,
                            defectCategory = insp.fabric_defect.toString()
                        )
                    }
                }
            }
        }
    }
}
