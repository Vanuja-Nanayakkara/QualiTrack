package iit.qualitrack.frontend.ui.components

import androidx.compose.foundation.layout.*
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import iit.qualitrack.frontend.data.model.Flag
import iit.qualitrack.frontend.data.model.Inspection

@Composable
fun InspectionCard(
    inspection: Inspection,
    supervisorName: String,
    defectCategory: String,
    flagDetails: Flag? = null
) {
    Card(
        modifier = Modifier
            .fillMaxWidth()
            .padding(horizontal = 16.dp, vertical = 8.dp),
        elevation = CardDefaults.cardElevation(4.dp)
    ) {
        Column(
            modifier = Modifier.padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(4.dp)
        ) {
            Text("Inspection #${inspection.id}", style = MaterialTheme.typography.titleMedium)
            Text("Status: ${inspection.status}")
            Text("Date:   ${inspection.inspection_date}")
            Text("Supervisor: $supervisorName")
            Text("Defect: $defectCategory")

            // Optional flag info
            flagDetails?.let { flag ->
                Spacer(modifier = Modifier.height(8.dp))
                Text("🚩 Flag Info", style = MaterialTheme.typography.titleSmall)
                Text("Type: ${flag.flag_type}")
                flag.issue_type?.let { Text("Issue: $it") }
                flag.custom_reason?.let { Text("Reason: $it") }
            }
        }
    }
}
