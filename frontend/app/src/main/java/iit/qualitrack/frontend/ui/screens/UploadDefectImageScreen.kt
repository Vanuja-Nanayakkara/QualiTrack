package iit.qualitrack.frontend.ui.screens

import android.net.Uri
import android.provider.OpenableColumns
import android.widget.Toast
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts.OpenDocument
import androidx.compose.foundation.Image
import androidx.compose.foundation.layout.*
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.ArrowBack
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.unit.dp
import androidx.navigation.NavController
import coil.compose.rememberAsyncImagePainter
import iit.qualitrack.frontend.data.model.CreateFlagRequest
import iit.qualitrack.frontend.util.NetworkResult
import iit.qualitrack.frontend.viewmodel.SharedViewModel
import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.firstOrNull
import kotlinx.coroutines.launch
import java.text.SimpleDateFormat
import java.util.*

@Composable
fun UploadDefectImageScreen(
    navController: NavController, sharedVm: SharedViewModel
) {
    val context = LocalContext.current
    val scope = rememberCoroutineScope()
    var selectedUri by remember { mutableStateOf<Uri?>(null) }

    val role = sharedVm.userRole.collectAsState(null).value
    val inspectorName = role?.details?.get("name") as? String ?: ""

    val launcher = rememberLauncherForActivityResult(OpenDocument()) { uri ->
        selectedUri = uri
    }

    Scaffold(topBar = {
        TopAppBar(title = { Text("Upload Defect Image") }, navigationIcon = {
            IconButton(onClick = {
                navController.popBackStack("inspector_dashboard", inclusive = false)
            }) {
                Icon(Icons.Filled.ArrowBack, contentDescription = "Back")
            }
        })
    }) { innerPadding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(innerPadding)
                .padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            Button(onClick = { launcher.launch(arrayOf("image/*")) }, Modifier.fillMaxWidth()) {
                Text("Pick / Snap Image")
            }

            selectedUri?.let { uri ->
                Image(
                    painter = rememberAsyncImagePainter(uri),
                    contentDescription = null,
                    modifier = Modifier
                        .fillMaxWidth()
                        .height(200.dp)
                )

                Spacer(Modifier.height(8.dp))

                Button(
                    onClick = {
                        val name = context.contentResolver.query(
                            uri, arrayOf(OpenableColumns.DISPLAY_NAME), null, null, null
                        )?.use { cursor ->
                            if (cursor.moveToFirst()) {
                                cursor.getString(cursor.getColumnIndexOrThrow(OpenableColumns.DISPLAY_NAME))
                            } else null
                        } ?: ""

                        if (name.contains("bad", ignoreCase = true)) {
                            // BAD IMAGE → Go to inspection form
                            scope.launch {
                                val resp = sharedVm.listDefects().firstOrNull {
                                    it is NetworkResult.Success
                                } as? NetworkResult.Success

                                val defects = resp?.data?.results.orEmpty()
                                val chosen = defects.randomOrNull()

                                if (chosen != null) {
                                    navController.navigate("inspections/new?defectId=${chosen.id}&defectType=${chosen.defect_type}")
                                } else {
                                    Toast.makeText(
                                        context, "No defects available", Toast.LENGTH_SHORT
                                    ).show()
                                }
                            }
                        } else {
                            // GOOD IMAGE → Submit GREEN flag
                            scope.launch {
                                val supervisors = sharedVm.supervisors.value
                                val supervisor = supervisors.firstOrNull()

                                if (supervisor == null) {
                                    Toast.makeText(
                                        context, "No supervisor found", Toast.LENGTH_SHORT
                                    ).show()
                                    return@launch
                                }

                                val now = Calendar.getInstance()
                                val date = SimpleDateFormat(
                                    "yyyy-MM-dd", Locale.getDefault()
                                ).format(now.time)
                                val time =
                                    SimpleDateFormat("HH:mm", Locale.getDefault()).format(now.time)

                                sharedVm.createFlag(
                                    CreateFlagRequest(
                                        operator_id = "AUTO_OP",
                                        machine_no = "AUTO_MACH",
                                        defect = "No Defect",
                                        flag_type = "GREEN",
                                        inspected_by = inspectorName,
                                        supervisor_in_charge = supervisor.name,
                                        date_of_inspection = date,
                                        time_of_inspection = time,
                                        issue_type = null,
                                        custom_reason = null
                                    )
                                )

                                delay(1000) // optional wait for result

                                when (val result = sharedVm.createFlagResult.value) {
                                    is NetworkResult.Success -> {
                                        Toast.makeText(
                                            context,
                                            "✅ Flag submitted: ${result.data.message}",
                                            Toast.LENGTH_LONG
                                        ).show()
                                        selectedUri = null
                                        navController.popBackStack(
                                            "inspector_dashboard", inclusive = false
                                        )
                                    }

                                    is NetworkResult.Error -> {
                                        Toast.makeText(
                                            context,
                                            "❌ Flag failed: ${result.message}",
                                            Toast.LENGTH_LONG
                                        ).show()
                                    }

                                    is NetworkResult.Loading -> {
                                        Toast.makeText(
                                            context, "Submitting flag...", Toast.LENGTH_SHORT
                                        ).show()
                                    }

                                    else -> Unit
                                }
                            }
                        }
                    }, modifier = Modifier.fillMaxWidth()
                ) {
                    Text("Analyze Image")
                }
            }
        }
    }
}
