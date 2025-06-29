package iit.qualitrack.frontend.viewmodel

import android.util.Log
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import iit.qualitrack.frontend.data.api.ServiceLocator
import iit.qualitrack.frontend.data.api.TokenManager
import iit.qualitrack.frontend.data.model.*
import iit.qualitrack.frontend.util.NetworkResult
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.flow.*
import kotlinx.coroutines.launch
import java.text.SimpleDateFormat
import java.util.*

class SharedViewModel : ViewModel() {
    private val repo = ServiceLocator.repository

    // 1) AUTH TOKEN
    private val _authToken = MutableStateFlow<String?>(null)
    val authToken: StateFlow<String?> = _authToken.asStateFlow()

    // 2) ROLE
    private val _userRole = MutableStateFlow<UserRoleResponse?>(null)
    val userRole: StateFlow<UserRoleResponse?> = _userRole.asStateFlow()

    // 3) ERRORS
    private val _errors = MutableSharedFlow<String>()
    val errors: SharedFlow<String> = _errors.asSharedFlow()

    // 4) ASSIGN ROLE
    private val _assignRoleResult =
        MutableStateFlow<NetworkResult<SimpleRoleResponse>>(NetworkResult.Idle)
    val assignRoleResult: StateFlow<NetworkResult<SimpleRoleResponse>> =
        _assignRoleResult.asStateFlow()

    // 5) CREATE DEFECT
    private val _createDefectResult = MutableStateFlow<NetworkResult<Defect>>(NetworkResult.Idle)
    val createDefectResult: StateFlow<NetworkResult<Defect>> = _createDefectResult.asStateFlow()

    // 6) CREATE FLAG
    private val _createFlagResult =
        MutableStateFlow<NetworkResult<SimpleMessageResponse>>(NetworkResult.Idle)
    val createFlagResult: StateFlow<NetworkResult<SimpleMessageResponse>> =
        _createFlagResult.asStateFlow()

    // 7) SUPERVISORS LIST
    private val _supervisors = MutableStateFlow<List<Supervisor>>(emptyList())
    val supervisors: StateFlow<List<Supervisor>> = _supervisors.asStateFlow()

    /** Load supervisors from server */
    fun loadSupervisors() = viewModelScope.launch(Dispatchers.IO) {
        try {
            val resp = repo.listSupervisors()
            if (resp.isSuccessful) {
                _supervisors.value = resp.body()?.results ?: emptyList()
            }
        } catch (_: Exception) {
        }
    }

    /** Assign a user role */
    fun assignRole(req: AssignRoleRequest) = viewModelScope.launch(Dispatchers.IO) {
        _assignRoleResult.value = NetworkResult.Loading
        try {
            val resp = repo.assignRole(req)
            if (resp.isSuccessful) {
                _assignRoleResult.value = NetworkResult.Success(resp.body()!!)
            } else {
                _assignRoleResult.value =
                    NetworkResult.Error(resp.errorBody()?.string() ?: "Assign role failed")
            }
        } catch (e: Exception) {
            _assignRoleResult.value = NetworkResult.Error(e.localizedMessage ?: "Error")
        }
    }

    /** Store JWT locally */
    fun setToken(rawToken: String) {
        TokenManager.token = "Bearer $rawToken"
        _authToken.value = rawToken
    }

    /** Fetch current user role */
    fun loadUserRole() = viewModelScope.launch(Dispatchers.IO) {
        try {
            val resp = repo.getRole()
            if (resp.isSuccessful) {
                resp.body()?.let { _userRole.value = it }
            } else {
                _errors.emit("Role load failed: ${resp.errorBody()?.string()}")
            }
        } catch (e: Exception) {
            _errors.emit(e.localizedMessage ?: "Unknown error")
        }
    }

    /** List defects (paginated) */
    fun listDefects(): Flow<NetworkResult<PaginatedResponse<Defect>>> = flow {
        emit(NetworkResult.Loading)
        try {
            val resp = repo.listDefects()
            if (resp.isSuccessful) {
                emit(NetworkResult.Success(resp.body()!!))
            } else {
                emit(NetworkResult.Error(resp.errorBody()?.string() ?: "Unknown error"))
            }
        } catch (e: Exception) {
            emit(NetworkResult.Error(e.localizedMessage ?: "Error fetching defects"))
        }
    }.flowOn(Dispatchers.IO)

    /** List inspections (paginated) */
    fun listInspections(): Flow<NetworkResult<PaginatedResponse<Inspection>>> = flow {
        emit(NetworkResult.Loading)

        val allResults = mutableListOf<Inspection>()
        var nextUrl: String? = null

        try {
            do {
                val response = if (nextUrl == null) {
                    repo.listInspections()
                } else {
                    repo.getFromUrl(nextUrl)
                }

                if (response.isSuccessful) {
                    val page = response.body()!!
                    allResults.addAll(page.results)
                    nextUrl = page.next
                } else {
                    emit(NetworkResult.Error(response.errorBody()?.string() ?: "Unknown error"))
                    return@flow
                }
            } while (nextUrl != null)

            emit(
                NetworkResult.Success(
                    PaginatedResponse(
                        count = allResults.size, next = null, previous = null, results = allResults
                    )
                )
            )
        } catch (e: Exception) {
            emit(NetworkResult.Error(e.localizedMessage ?: "Error fetching inspections"))
        }
    }.flowOn(Dispatchers.IO)


    /** Lists flags (paginated). */
    fun listFlags(): Flow<NetworkResult<PaginatedResponse<Flag>>> = flow {
        emit(NetworkResult.Loading)
        try {
            val resp = repo.listFlags()
            if (resp.isSuccessful) {
                emit(NetworkResult.Success(resp.body()!!))
            } else {
                emit(NetworkResult.Error(resp.errorBody()?.string() ?: "Unknown error"))
            }
        } catch (e: Exception) {
            emit(NetworkResult.Error(e.localizedMessage ?: "Error fetching flags"))
        }
    }.flowOn(Dispatchers.IO)

    /** Lists notifications for the given supervisor ID. */
    fun listNotifications(supId: Int): Flow<NetworkResult<NotificationsResponse>> = flow {
        emit(NetworkResult.Loading)
        try {
            val resp = repo.listNotifications(supId)
            if (resp.isSuccessful) {
                emit(NetworkResult.Success(resp.body()!!))
            } else {
                emit(NetworkResult.Error(resp.errorBody()?.string() ?: "Unknown error"))
            }
        } catch (e: Exception) {
            emit(NetworkResult.Error(e.localizedMessage ?: "Error fetching notifications"))
        }
    }.flowOn(Dispatchers.IO)

    /** Creates a new defect on the server. */
    fun createDefect(req: CreateDefectRequest) = viewModelScope.launch(Dispatchers.IO) {
        _createDefectResult.value = NetworkResult.Loading
        try {
            val resp = repo.createDefect(req)
            if (resp.isSuccessful) {
                _createDefectResult.value = NetworkResult.Success(resp.body()!!)
            } else {
                _createDefectResult.value =
                    NetworkResult.Error(resp.errorBody()?.string() ?: "Create defect failed")
            }
        } catch (e: Exception) {
            _createDefectResult.value = NetworkResult.Error(e.localizedMessage ?: "Error")
        }
    }

    /** Creates a new flag on the server. */
    fun createFlag(req: CreateFlagRequest) = viewModelScope.launch(Dispatchers.IO) {
        Log.d("FLAG_DEBUG", "Submitting flag: $req")   // ✅ ADD THIS

        _createFlagResult.value = NetworkResult.Loading
        try {
            val resp = repo.createFlag(req)
            Log.d("FLAG_DEBUG", "Response code: ${resp.code()}")   // ✅ AND THIS
            if (resp.isSuccessful) {
                _createFlagResult.value = NetworkResult.Success(resp.body()!!)
            } else {
                _createFlagResult.value =
                    NetworkResult.Error(resp.errorBody()?.string() ?: "Create flag failed")
            }
        } catch (e: Exception) {
            Log.e("FLAG_DEBUG", "Exception: ${e.message}", e)     // ✅ AND THIS
            _createFlagResult.value = NetworkResult.Error(e.localizedMessage ?: "Error")
        }
    }

    /** Count green flags created by inspector on current date. */
    fun countTodayGreenFlags(inspectorId: Int, date: String): Flow<Int> = flow {
        try {
            val resp = repo.listFlags()
            if (resp.isSuccessful) {
                val flags = resp.body()?.results ?: emptyList()
                val count = flags.count {
                    it.flag_type.equals("GREEN", ignoreCase = true) && it.date_of_inspection == date
                }
                emit(count)
            } else emit(0)
        } catch (e: Exception) {
            emit(0)
        }
    }.flowOn(Dispatchers.IO)

    /** Clears local auth state, effectively logging out. */
    fun logout() {
        TokenManager.token = null
        _authToken.value = null
        _userRole.value = null
    }
}
