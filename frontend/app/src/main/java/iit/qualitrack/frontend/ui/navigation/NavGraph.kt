package iit.qualitrack.frontend.ui.navigation

import androidx.compose.runtime.Composable
import androidx.lifecycle.viewmodel.compose.viewModel
import androidx.navigation.NavType
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.rememberNavController
import androidx.navigation.navArgument
import iit.qualitrack.frontend.viewmodel.SharedViewModel
import iit.qualitrack.frontend.viewmodel.SupervisorViewModel
import iit.qualitrack.frontend.ui.screens.*

@Composable
fun NavGraph(sharedVm: SharedViewModel) {
    val navController = rememberNavController()
    val supVm: SupervisorViewModel = viewModel()

    NavHost(navController = navController, startDestination = "login") {
        composable("login") {
            LoginScreen(navController, sharedVm)
        }
        composable("register") {
            RegisterScreen(navController, sharedVm)
        }
        composable("inspector_dashboard") {
            CombinedDashboardScreen(navController, sharedVm)
        }
        composable("supervisor_dashboard") {
            SupervisorDashboardScreen(navController, sharedVm, supVm)
        }
        composable("defects") {
            DefectsScreen(navController, sharedVm)
        }
        composable("defects/new") {
            CreateDefectScreen(navController, sharedVm)
        }
        composable("flags") {
            FlagsScreen(navController, sharedVm)
        }
        composable("notifications") {
            NotificationsScreen(navController, sharedVm)
        }
        composable("upload_defect") {
            UploadDefectImageScreen(navController, sharedVm)
        }
        composable(
            "inspections/new?defectId={defectId}&defectType={defectType}", arguments = listOf(
                navArgument("defectId") { type = NavType.IntType; defaultValue = -1 },
                navArgument("defectType") {
                    type = NavType.StringType; defaultValue = ""
                })) { backStack ->
            val defectId = backStack.arguments?.getInt("defectId") ?: -1
            val defectType = backStack.arguments?.getString("defectType") ?: ""
            CreateInspectionScreen(navController, defectId, defectType, sharedVm)
        }
        composable("inspections") {
            InspectionsScreen(navController, sharedVm)
        }
        composable(
            "inspection/detail/{inspId}",
            arguments = listOf(navArgument("inspId") { type = NavType.IntType })
        ) { back ->
            val inspId = back.arguments!!.getInt("inspId")
            PendingInspectionDetailScreen(inspId, sharedVm, supVm, navController)
        }
    }
}
