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
import iit.qualitrack.frontend.data.model.AssignRoleRequest
import iit.qualitrack.frontend.util.NetworkResult
import iit.qualitrack.frontend.viewmodel.AuthViewModel
import iit.qualitrack.frontend.viewmodel.SharedViewModel

@Composable
fun RegisterScreen(
    navController: NavController, sharedVm: SharedViewModel, authVm: AuthViewModel = viewModel()
) {
    var username by remember { mutableStateOf("") }
    var email by remember { mutableStateOf("") }
    var password by remember { mutableStateOf("") }
    var confirmPw by remember { mutableStateOf("") }
    var name by remember { mutableStateOf("") }
    var phone by remember { mutableStateOf("") }
    var dept by remember { mutableStateOf("") }
    var roleType by remember { mutableStateOf("inspector") }

    val regResult by authVm.registerResult.collectAsState(initial = NetworkResult.Idle)
    val loginResult by authVm.loginResult.collectAsState(initial = NetworkResult.Idle)
    val assignResult by sharedVm.assignRoleResult.collectAsState(initial = NetworkResult.Idle)

    LaunchedEffect(regResult) {
        if (regResult is NetworkResult.Success) authVm.login(username, password)
    }
    LaunchedEffect(loginResult) {
        if (loginResult is NetworkResult.Success) {
            sharedVm.setToken((loginResult as NetworkResult.Success<String>).data)
            sharedVm.assignRole(
                AssignRoleRequest(
                    role_type = roleType,
                    name = name,
                    phone = phone,
                    department = if (roleType == "supervisor") dept else null
                )
            )
        }
    }
    LaunchedEffect(assignResult) {
        if (assignResult is NetworkResult.Success) {
            sharedVm.loadUserRole()
            val dest =
                if (roleType == "supervisor") "supervisor_dashboard" else "inspector_dashboard"
            navController.navigate(dest) { popUpTo("register") { inclusive = true } }
        }
    }

    Scaffold(topBar = { TopAppBar(title = { Text("Register") }) }) { padding ->
        Column(
            Modifier
                .padding(padding)
                .padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(8.dp),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            Text("Select Role:")
            Row {
                RadioButton(roleType == "inspector", { roleType = "inspector" }); Text("Inspector")
                Spacer(Modifier.width(16.dp))
                RadioButton(roleType == "supervisor",
                    { roleType = "supervisor" }); Text("Supervisor")
            }
            TextField(name, { name = it }, Modifier.fillMaxWidth(), label = { Text("Full Name") })
            TextField(username,
                { username = it },
                Modifier.fillMaxWidth(),
                label = { Text("Username") })
            TextField(email, { email = it }, Modifier.fillMaxWidth(), label = { Text("Email") })
            TextField(password,
                { password = it },
                Modifier.fillMaxWidth(),
                label = { Text("Password") },
                visualTransformation = PasswordVisualTransformation()
            )
            TextField(confirmPw,
                { confirmPw = it },
                Modifier.fillMaxWidth(),
                label = { Text("Confirm Password") },
                visualTransformation = PasswordVisualTransformation()
            )
            if (roleType == "supervisor") {
                TextField(phone, { phone = it }, Modifier.fillMaxWidth(), label = { Text("Phone") })
                TextField(dept,
                    { dept = it },
                    Modifier.fillMaxWidth(),
                    label = { Text("Department") })
            }
            Spacer(Modifier.height(16.dp))
            Button(
                { authVm.register(username, email, password, confirmPw) }, Modifier.fillMaxWidth()
            ) { Text("Sign Up") }

            if (regResult is NetworkResult.Loading) CircularProgressIndicator()
            if (regResult is NetworkResult.Error) Text(
                "Registration failed: ${(regResult as NetworkResult.Error).message}",
                color = MaterialTheme.colorScheme.error
            )
            if (assignResult is NetworkResult.Loading) Text("Assigning role…")
            if (assignResult is NetworkResult.Error) Text(
                "Role assignment failed: ${(assignResult as NetworkResult.Error).message}",
                color = MaterialTheme.colorScheme.error
            )
        }
    }
}