package iit.qualitrack.frontend.ui.screens

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Add
import androidx.compose.material.icons.filled.ExitToApp
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.lifecycle.viewmodel.compose.viewModel
import androidx.navigation.NavController
import iit.qualitrack.frontend.data.model.*
import iit.qualitrack.frontend.ui.components.InspectionCard
import iit.qualitrack.frontend.util.NetworkResult
import iit.qualitrack.frontend.viewmodel.InspectorViewModel
import iit.qualitrack.frontend.viewmodel.SharedViewModel
import kotlinx.coroutines.launch
import java.text.SimpleDateFormat
import java.util.*

@Composable
fun CombinedDashboardScreen(
    navController: NavController,
    sharedVm: SharedViewModel = viewModel(),
    inspVm: InspectorViewModel = viewModel()
) {
    val roleState by sharedVm.userRole.collectAsState(initial = null)
    if (roleState == null) {
        Box(Modifier.fillMaxSize(), Alignment.Center) { CircularProgressIndicator() }
        return
    }

    val inspId = (roleState!!.details["id"] as Double).toInt()
    val inspName = roleState!!.details["name"] as? String ?: ""

    val today = remember {
        SimpleDateFormat("yyyy-MM-dd", Locale.getDefault()).format(Date())
    }

    LaunchedEffect(inspId, today) {
        inspVm.loadDashboard(inspId, today)
        sharedVm.loadSupervisors()
    }
    val dashResult by inspVm.dashboard.collectAsState(initial = NetworkResult.Idle)

    var inspections by remember { mutableStateOf<List<Inspection>>(emptyList()) }
    var loadingIns by remember { mutableStateOf(false) }
    var errorIns by remember { mutableStateOf<String?>(null) }

    LaunchedEffect(Unit) {
        sharedVm.listInspections().collect { res ->
            when (res) {
                is NetworkResult.Loading -> {
                    loadingIns = true
                    errorIns = null
                }

                is NetworkResult.Success<*> -> {
                    val data = res.data
                    inspections = if (data is PaginatedResponse<*>) {
                        data.results.filterIsInstance<Inspection>()
                    } else {
                        emptyList()
                    }
                    loadingIns = false
                }

                is NetworkResult.Error -> {
                    errorIns = res.message
                    loadingIns = false
                }

                else -> Unit
            }
        }
    }

    LaunchedEffect(Unit) { sharedVm.loadSupervisors() }
    val supMap = sharedVm.supervisors.collectAsState().value.associateBy { it.id }

    var defectMap by remember { mutableStateOf<Map<Int, String>>(emptyMap()) }
    LaunchedEffect(Unit) {
        sharedVm.listDefects().collect { res ->
            if (res is NetworkResult.Success<*>) {
                val data = res.data
                val list = if (data is PaginatedResponse<*>) {
                    data.results.filterIsInstance<Defect>()
                } else emptyList()
                defectMap = list.associate { it.id to it.defect_type }
            }
        }
    }

    var flags by remember { mutableStateOf<List<Flag>>(emptyList()) }
    LaunchedEffect(Unit) {
        sharedVm.listFlags().collect { res ->
            if (res is NetworkResult.Success<*>) {
                val data = res.data
                val list = if (data is PaginatedResponse<*>) {
                    data.results.filterIsInstance<Flag>()
                } else emptyList()
                flags = list
            }
        }
    }

    Scaffold(topBar = {
        TopAppBar(title = { Text("Today's Analysis") }, actions = {
            IconButton(onClick = {
                sharedVm.logout()
                navController.navigate("login") {
                    popUpTo("login") { inclusive = true }
                }
            }) {
                Icon(Icons.Filled.ExitToApp, contentDescription = "Logout")
            }
        })
    }, floatingActionButton = {
        FloatingActionButton(onClick = { navController.navigate("upload_defect") }) {
            Icon(Icons.Filled.Add, contentDescription = "New")
        }
    }) { padding ->
        Column(
            Modifier
                .fillMaxSize()
                .padding(padding)
                .padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            when (dashResult) {
                is NetworkResult.Loading -> CircularProgressIndicator()
                is NetworkResult.Success<*> -> {
                    val d = (dashResult as NetworkResult.Success<InspectorDashboard>).data
                    val apiTotal = d.total_inspections
                    val greenFlagCount = d.green_flags
                    val allTotal = apiTotal + greenFlagCount
                    val pct = if (allTotal > 0) apiTotal * 100 / allTotal else 0

                    Text("Total Analyses:  $allTotal", style = MaterialTheme.typography.bodyLarge)
                    Text("Defects Found:   $apiTotal", style = MaterialTheme.typography.bodyLarge)
                    Text(
                        "Green Flags:     $greenFlagCount",
                        style = MaterialTheme.typography.bodyLarge
                    )
                    Text("Defect %:        $pct%", style = MaterialTheme.typography.bodyLarge)
                }

                is NetworkResult.Error -> Text(
                    "Error: ${(dashResult as NetworkResult.Error).message}",
                    color = MaterialTheme.colorScheme.error
                )

                else -> Text("No data available", style = MaterialTheme.typography.bodyLarge)
            }

            Spacer(Modifier.height(24.dp))
            Text("All Inspections", style = MaterialTheme.typography.titleMedium)

            if (loadingIns) {
                Box(Modifier.fillMaxSize(), Alignment.Center) { CircularProgressIndicator() }
            } else if (errorIns != null) {
                Text("Error: $errorIns", color = MaterialTheme.colorScheme.error)
            } else {
                LazyColumn(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                    items(inspections.filter { it.cli_inspector == inspId }) { insp ->
                        val supName = supMap[insp.supervisor]?.name.orEmpty()
                        val defCat = defectMap[insp.fabric_defect] ?: ""

                        val relatedFlag = flags.find { flag ->
                            flag.date_of_inspection == insp.inspection_date.take(10) && flag.inspector_name == inspName
                        }


                        InspectionCard(
                            inspection = insp,
                            supervisorName = supName,
                            defectCategory = defCat,
                            flagDetails = relatedFlag
                        )
                    }
                }
            }
        }
    }
}
