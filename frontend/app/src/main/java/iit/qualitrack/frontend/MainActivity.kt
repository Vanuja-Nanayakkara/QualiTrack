package iit.qualitrack.frontend

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.lifecycle.viewmodel.compose.viewModel
import iit.qualitrack.frontend.ui.navigation.NavGraph
import iit.qualitrack.frontend.ui.theme.GarmentInspectionAppTheme
import iit.qualitrack.frontend.viewmodel.SharedViewModel

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            GarmentInspectionAppTheme {
                val sharedVm: SharedViewModel = viewModel()
                NavGraph(sharedVm = sharedVm)
            }
        }
    }
}
