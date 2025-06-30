package iit.qualitrack.frontend.ui.components

import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import iit.qualitrack.frontend.data.model.Defect

@Composable
fun DefectCard(defect: Defect) {
    Card(
        modifier = Modifier
            .fillMaxWidth()
            .padding(8.dp),
        elevation = CardDefaults.cardElevation(4.dp)
    ) {
        Column(modifier = Modifier.padding(16.dp)) {
            Text(text = "Type: ${defect.defect_type}")
            Text(text = "Severity: ${defect.severity}")
            Text(text = "Detected At: ${defect.detected_at}")
            Text(text = "Reviewed: ${if (defect.reviewed) "Yes" else "No"}")
        }
    }
}