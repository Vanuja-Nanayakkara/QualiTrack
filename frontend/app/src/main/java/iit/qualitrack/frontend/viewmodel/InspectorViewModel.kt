package iit.qualitrack.frontend.viewmodel

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import iit.qualitrack.frontend.data.api.ServiceLocator
import iit.qualitrack.frontend.data.model.CreateInspectionRequest
import iit.qualitrack.frontend.data.model.Defect
import iit.qualitrack.frontend.data.model.Inspection
import iit.qualitrack.frontend.data.model.InspectorDashboard
import iit.qualitrack.frontend.util.NetworkResult
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.launch
import okhttp3.MultipartBody

class InspectorViewModel : ViewModel() {
    private val repo = ServiceLocator.repository

    private val _dashboard = MutableStateFlow<NetworkResult<InspectorDashboard>>(NetworkResult.Idle)
    val dashboard: StateFlow<NetworkResult<InspectorDashboard>> = _dashboard

    private val _analyzeResult = MutableStateFlow<NetworkResult<Defect>>(NetworkResult.Idle)
    val analyzeResult: StateFlow<NetworkResult<Defect>> = _analyzeResult

    private val _createInspectionResult =
        MutableStateFlow<NetworkResult<Inspection>>(NetworkResult.Idle)
    val createInspectionResult: StateFlow<NetworkResult<Inspection>> = _createInspectionResult

    fun analyzeImage(imagePart: MultipartBody.Part) = viewModelScope.launch(Dispatchers.IO) {
        _analyzeResult.value = NetworkResult.Loading
        try {
            val resp = repo.analyzeDefectImage(imagePart)
            if (resp.isSuccessful) {
                _analyzeResult.value = NetworkResult.Success(resp.body()!!)
            } else {
                _analyzeResult.value =
                    NetworkResult.Error("HTTP ${resp.code()}: ${resp.errorBody()?.string()}")
            }
        } catch (e: Exception) {
            _analyzeResult.value = NetworkResult.Error(e.localizedMessage ?: "Error")
        }
    }

    fun resetAnalyze() {
        _analyzeResult.value = NetworkResult.Idle
    }

    fun loadDashboard(inspectorId: Int, date: String) = viewModelScope.launch {
        _dashboard.value = NetworkResult.Loading
        val resp = repo.inspectorDashboard(inspectorId, date)
        _dashboard.value = if (resp.isSuccessful) {
            NetworkResult.Success(resp.body()!!)
        } else {
            NetworkResult.Error("HTTP ${resp.code()}: ${resp.errorBody()?.string()}")
        }
    }

    fun createInspection(req: CreateInspectionRequest) = viewModelScope.launch(Dispatchers.IO) {
        _createInspectionResult.value = NetworkResult.Loading
        try {
            val resp = repo.createInspection(req)
            if (resp.isSuccessful) {
                _createInspectionResult.value = NetworkResult.Success(resp.body()!!)
            } else {
                _createInspectionResult.value =
                    NetworkResult.Error("HTTP ${resp.code()}: ${resp.errorBody()?.string()}")
            }
        } catch (e: Exception) {
            _createInspectionResult.value = NetworkResult.Error(e.localizedMessage ?: "Error")
        }
    }
}