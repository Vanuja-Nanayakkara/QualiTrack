package iit.qualitrack.frontend.viewmodel

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import iit.qualitrack.frontend.data.api.ServiceLocator
import iit.qualitrack.frontend.util.NetworkResult
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext

class SupervisorViewModel : ViewModel() {
    private val repo = ServiceLocator.repository

    private val _dashboard = MutableStateFlow<NetworkResult<Any>>(NetworkResult.Idle)
    val dashboard: StateFlow<NetworkResult<Any>> = _dashboard.asStateFlow()

    /**
     * Load the supervisor dashboard.
     * Wraps the network call in IO dispatcher and catches any exception
     * to prevent the app from crashing.
     */
    fun loadDashboard(supervisorId: Int, date: String) = viewModelScope.launch {
        _dashboard.value = NetworkResult.Loading

        try {
            val resp = withContext(Dispatchers.IO) {
                repo.supervisorDashboard(supervisorId, date)
            }

            if (resp.isSuccessful) {
                _dashboard.value = NetworkResult.Success(resp.body()!!)
            } else {
                val errorText = resp.errorBody()?.string()
                _dashboard.value = NetworkResult.Error("HTTP ${resp.code()}: $errorText")
            }
        } catch (e: Exception) {
            _dashboard.value = NetworkResult.Error(e.localizedMessage ?: "Unknown error")
        }
    }
}