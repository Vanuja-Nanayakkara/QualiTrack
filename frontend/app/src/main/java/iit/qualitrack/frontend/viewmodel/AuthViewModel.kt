package iit.qualitrack.frontend.viewmodel

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import iit.qualitrack.frontend.data.api.ServiceLocator
import iit.qualitrack.frontend.data.model.LoginRequest
import iit.qualitrack.frontend.data.model.RegisterRequest
import iit.qualitrack.frontend.util.NetworkResult
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch

class AuthViewModel : ViewModel() {
    private val repo = ServiceLocator.repository

    // LOGIN
    private val _loginResult = MutableStateFlow<NetworkResult<String>>(NetworkResult.Idle)
    val loginResult: StateFlow<NetworkResult<String>> = _loginResult.asStateFlow()

    // REGISTER
    private val _registerResult = MutableStateFlow<NetworkResult<String>>(NetworkResult.Idle)
    val registerResult: StateFlow<NetworkResult<String>> = _registerResult.asStateFlow()

    fun login(username: String, password: String) = viewModelScope.launch {
        _loginResult.value = NetworkResult.Loading
        try {
            val resp = repo.login(LoginRequest(username, password))
            if (resp.isSuccessful) {
                _loginResult.value = NetworkResult.Success(resp.body()!!.access)
            } else {
                _loginResult.value =
                    NetworkResult.Error(resp.errorBody()?.string() ?: "Login failed")
            }
        } catch (e: Exception) {
            _loginResult.value = NetworkResult.Error(e.localizedMessage ?: "Error")
        }
    }

    fun register(username: String, email: String, password: String, password2: String) =
        viewModelScope.launch {
            _registerResult.value = NetworkResult.Loading
            try {
                val resp = repo.register(RegisterRequest(username, email, password, password2))
                if (resp.isSuccessful) {
                    _registerResult.value = NetworkResult.Success(resp.body()!!.message)
                } else {
                    _registerResult.value =
                        NetworkResult.Error(resp.errorBody()?.string() ?: "Register failed")
                }
            } catch (e: Exception) {
                _registerResult.value = NetworkResult.Error(e.localizedMessage ?: "Error")
            }
        }
}