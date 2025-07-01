package iit.qualitrack.frontend.ui.screens

import android.widget.Toast
import androidx.compose.foundation.layout.*
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Flag
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.unit.dp
import androidx.lifecycle.viewmodel.compose.viewModel
import androidx.navigation.NavController
import iit.qualitrack.frontend.data.model.CreateInspectionRequest
import iit.qualitrack.frontend.data.model.CreateFlagRequest
import iit.qualitrack.frontend.util.NetworkResult
import iit.qualitrack.frontend.viewmodel.InspectorViewModel
import iit.qualitrack.frontend.viewmodel.SharedViewModel
import kotlinx.coroutines.launch
import java.text.SimpleDateFormat
import java.util.*

@Composable
fun CreateInspectionScreen(
    navController: NavController,
    defectId: Int,
    defectType: String,
    sharedVm: SharedViewModel,
    inspVm: InspectorViewModel = viewModel()
) {
    val context = LocalContext.current
    val roleState by sharedVm.userRole.collectAsState(initial = null)
    val role = roleState ?: return
    val inspId = (role.details["id"] as Double).toInt()

    LaunchedEffect(Unit) { sharedVm.loadSupervisors() }
    val supervisors by sharedVm.supervisors.collectAsState()

    var expanded by remember { mutableStateOf(false) }
    var selectedSupIdx by remember { mutableStateOf(0) }
    var status by remember { mutableStateOf("Pending") }

    var addFlag by remember { mutableStateOf(false) }
    var customReason by remember { mutableStateOf("") }

    val inspRes by inspVm.createInspectionResult.collectAsState()
    val flagRes by sharedVm.createFlagResult.collectAsState()
    val scope = rememberCoroutineScope()

    if (defectId == -1) {
        Toast.makeText(context, "Cannot create inspection for good image", Toast.LENGTH_SHORT).show()
        navController.popBackStack()
        return
    }

    Scaffold(topBar = { TopAppBar(title = { Text("New Inspection") }) }) { padding ->
        Column(
            Modifier
                .padding(padding)
                .padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            Text("Defect found: $defectType", style = MaterialTheme.typography.bodyLarge)

            OutlinedTextField(
                value = inspId.toString(),
                onValueChange = {},
                label = { Text("Inspector ID") },
                readOnly = true,
                modifier = Modifier.fillMaxWidth()
            )

            ExposedDropdownMenuBox(
                expanded = expanded,
                onExpandedChange = { expanded = !expanded }
            ) {
                OutlinedTextField(
                    value = supervisors.getOrNull(selectedSupIdx)?.name.orEmpty(),
                    onValueChange = {},
                    label = { Text("Supervisor") },
                    readOnly = true,
                    trailingIcon = { ExposedDropdownMenuDefaults.TrailingIcon(expanded) },
                    modifier = Modifier
                        .fillMaxWidth()
                        .menuAnchor()
                )
                ExposedDropdownMenu(
                    expanded = expanded,
                    onDismissRequest = { expanded = false }
                ) {
                    supervisors.forEachIndexed { idx, sup ->
                        DropdownMenuItem(
                            text = { Text(sup.name) },
                            onClick = {
                                selectedSupIdx = idx
                                expanded = false
                            }
                        )
                    }
                }
            }

            OutlinedTextField(
                value = status,
                onValueChange = { status = it },
                label = { Text("Status") },
                modifier = Modifier.fillMaxWidth()
            )

            OutlinedButton(
                onClick = { addFlag = !addFlag },
                modifier = Modifier.fillMaxWidth()
            ) {
                Icon(Icons.Filled.Flag, contentDescription = null)
                Spacer(Modifier.width(6.dp))
                Text(if (addFlag) "Remove Flag" else "Add Flag")
            }

            if (addFlag) {
                OutlinedTextField(
                    value = defectType,
                    onValueChange = {},
                    label = { Text("Issue Type") },
                    readOnly = true,
                    modifier = Modifier.fillMaxWidth()
                )

                OutlinedTextField(
                    value = customReason,
                    onValueChange = { customReason = it },
                    label = { Text("Reason") },
                    modifier = Modifier.fillMaxWidth()
                )
            }

            Button(
                onClick = {
                    val supervisor = supervisors.getOrNull(selectedSupIdx)
                    if (supervisor == null) {
                        Toast.makeText(context, "Please select a supervisor", Toast.LENGTH_SHORT).show()
                        return@Button
                    }

                    scope.launch {
                        val now = Calendar.getInstance()
                        val date = SimpleDateFormat("yyyy-MM-dd", Locale.getDefault()).format(now.time)
                        val time = SimpleDateFormat("HH:mm:ss", Locale.getDefault()).format(now.time)

                        // First: create flag if enabled
                        if (addFlag) {
                            sharedVm.createFlag(
                                CreateFlagRequest(
                                    operator_id = "AUTO_OP",
                                    machine_no = "AUTO_MACH",
                                    defect = defectType,
                                    flag_type = "RED",
                                    inspected_by = inspId.toString(),
                                    supervisor_in_charge = supervisor.name,
                                    date_of_inspection = date,
                                    time_of_inspection = time,
                                    issue_type = defectType,
                                    custom_reason = customReason
                                )
                            )
                        }

                        // Then: create inspection
                        inspVm.createInspection(
                            CreateInspectionRequest(
                                cli_inspector = inspId,
                                supervisor = supervisor.id,
                                fabric_defect = defectId,
                                status = status
                            )
                        )
                    }
                },
                modifier = Modifier.fillMaxWidth()
            ) {
                Text("Submit")
            }

            if (inspRes is NetworkResult.Success) {
                LaunchedEffect(inspRes) {
                    navController.popBackStack("inspector_dashboard", false)
                }
            }

            if (inspRes is NetworkResult.Error) {
                Text(
                    "Inspection Error: ${(inspRes as NetworkResult.Error).message}",
                    color = MaterialTheme.colorScheme.error
                )
            }

            if (flagRes is NetworkResult.Error) {
                Text(
                    "Flag Error: ${(flagRes as NetworkResult.Error).message}",
                    color = MaterialTheme.colorScheme.error
                )
            }
        }
    }
}
