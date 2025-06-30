package iit.qualitrack.frontend.ui.components

import androidx.compose.foundation.layout.*
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import iit.qualitrack.frontend.data.model.Flag

@Composable
fun FlagCard(flag: Flag) {
    Card(
        modifier = Modifier
            .fillMaxWidth()
            .padding(8.dp),
        elevation = CardDefaults.cardElevation(4.dp)
    ) {
        Column(modifier = Modifier.padding(16.dp)) {
            Text(text = "Operator: ${flag.operator_id}")
            Text(text = "Machine: ${flag.machine_no}")
            Text(text = "Flag Type: ${flag.flag_type}")
            flag.issue_type?.let { Text(text = "Issue Type: $it") }
            flag.custom_reason?.let { Text(text = "Reason: $it") }
            Text(text = "Date: ${flag.date_of_inspection}")
            Text(text = "Time: ${flag.time_of_inspection}")
        }
    }
}