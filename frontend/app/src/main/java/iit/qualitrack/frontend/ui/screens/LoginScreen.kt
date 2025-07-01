package iit.qualitrack.frontend.ui.screens

import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.runtime.collectAsState
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.input.PasswordVisualTransformation
import androidx.compose.ui.unit.dp
import androidx.lifecycle.viewmodel.compose.viewModel
import androidx.navigation.NavController
import iit.qualitrack.frontend.util.NetworkResult
import iit.qualitrack.frontend.viewmodel.AuthViewModel
import iit.qualitrack.frontend.viewmodel.SharedViewModel

@Composable
fun LoginScreen(
    navController: NavController, sharedVm: SharedViewModel, authVm: AuthViewModel = viewModel()
) {
    var username by remember { mutableStateOf("") }
    var password by remember { mutableStateOf("") }

    val loginResult by authVm.loginResult.collectAsState(initial = NetworkResult.Idle)
    val role = sharedVm.userRole.collectAsState(initial = null).value?.role

    LaunchedEffect(loginResult) {
        if (loginResult is NetworkResult.Success) {
            sharedVm.setToken((loginResult as NetworkResult.Success<String>).data)
            sharedVm.loadUserRole()
        }
    }

    LaunchedEffect(role) {
        role?.let {
            val dest = if (it == "supervisor") "supervisor_dashboard" else "inspector_dashboard"
            navController.navigate(dest) { popUpTo("login") { inclusive = true } }
        }
    }

    Scaffold(topBar = { TopAppBar(title = { Text("Login") }) }) { padding ->
        Column(
            Modifier
                .padding(padding)
                .padding(16.dp),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            TextField(username,
                { username = it },
                Modifier.fillMaxWidth(),
                label = { Text("Username") })
            Spacer(Modifier.height(8.dp))
            TextField(password,
                { password = it },
                Modifier.fillMaxWidth(),
                label = { Text("Password") },
                visualTransformation = PasswordVisualTransformation()
            )
            Spacer(Modifier.height(16.dp))
            Button({ authVm.login(username, password) }, Modifier.fillMaxWidth()) {
                Text("Login")
            }
            Spacer(Modifier.height(8.dp))
            TextButton({ navController.navigate("register") }) { Text("Don't have an account? Sign up") }
            Spacer(Modifier.height(16.dp))

            when (loginResult) {
                NetworkResult.Loading -> CircularProgressIndicator()
                is NetworkResult.Error -> Text(
                    "Error: ${(loginResult as NetworkResult.Error).message}",
                    color = MaterialTheme.colorScheme.error
                )

                else -> {}
            }
        }
    }
}